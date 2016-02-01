from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from notary_client import Notary

notary_obj = None

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<CreateWalletScreen>:
    FloatLayout:
        Label:
            text: "Notary - Create Wallet "
            pos_hint: {'x': .1, 'y': .8}
            size_hint: .5, .1
            font_size: '30sp'
        Label:
            text: "Password : "
            pos_hint: {'x': .1, 'y': .7}
            size_hint: .23, .1
            halign: 'left'
            font_size: '20sp'
        TextInput:
            id: password
            pos_hint: {'x': .3, 'y': .7}
            size_hint: .6, .1
            password: 'true'
            font_size: '20sp'
        Label:
            text: "Verify Password : "
            pos_hint: {'x': .1, 'y': .5}
            size_hint: .16, .1
            halign: 'left'
            font_size: '20sp'
        TextInput:
            id: retype_password
            pos: 400, 500
            pos_hint: {'x': .3, 'y': .5}
            size_hint: .6, .1
            password: 'true'
            font_size: '20sp'
        Button:
            text: 'Create'
            pos_hint: {'x': .3, 'y': .3}
            size_hint: .3, .1
            font_size: '20sp'
            on_press: root.create_wallet_callback();root.manager.current = 'registerwallet'
<RegisterWalletScreen>:
    FloatLayout:
        Label:
            text: "Notary - Register "
            pos_hint: {'x': .1, 'y': .8}
            size_hint: .425, .1
            font_size: '30sp'
        Label:
            text: "Email : "
            pos_hint: {'x': .1, 'y': .7}
            size_hint: .23, .1
            halign: 'left'
            font_size: '20sp'
        TextInput:
            id: email
            pos_hint: {'x': .3, 'y': .7}
            size_hint: .6, .1
            font_size: '20sp'
        Button:
            text: 'Register'
            pos_hint: {'x': .3, 'y': .5}
            size_hint: .3, .1
            font_size: '20sp'
            on_press: root.register_wallet_callback();root.manager.current = 'registerwallet'
""")


# Declare both screens
class CreateWalletScreen(Screen):
    password = ObjectProperty(None)
    retype_password = ObjectProperty(None)

    def create_wallet_callback(self):
        global notary_obj
        print('create wallet callback called')
        password_value =  self.ids.password.text
        retyped_value = self.ids.retype_password.text
        if password_value == retyped_value:
            notary_obj = Notary("notaryconfig.ini", password_value)
        else :
            popup = Popup(title='Password Mismatch', content=Label(text='Passwords does not match'),size_hint=(None, None), size=(400, 200))
            popup.open()


class RegisterWalletScreen(Screen):
    email = ObjectProperty(None)
    def register_wallet_callback(self):
        print('register wallet callback called')
        email_value = self.ids.email.text
        notary_obj.register_user(email_value)


# Create the screen manager
sm = ScreenManager()
smcwallet = CreateWalletScreen(name='createwallet')
smrwallet = RegisterWalletScreen(name='registerwallet')
sm.add_widget(smcwallet)
sm.add_widget(smrwallet)


# layout = FloatLayout()
# lblemail = Label(text='Email: ', size_hint=(.2, .05),  pos_hint={'x': .1, 'y': .9})
# txtemail = TextInput(text='', size_hint=(.6, .05),  pos_hint={'x': .3, 'y': .9})
# layout.add_widget(lblemail)
# layout.add_widget(txtemail)
# smsetting.add_widget(layout)


class TestApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    TestApp().run()
