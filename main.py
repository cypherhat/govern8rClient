from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from notary_client import Notary, NotaryError
from client_wallet import ClientWallet
import simplecrypt

notary_obj = None

Builder.load_file("create_wallet.kv")
Builder.load_file("register_wallet.kv")
Builder.load_file("password.kv")
Builder.load_file("confirmation.kv")


# Declare both screens
class CreateWalletScreen(Screen):
    password = ObjectProperty(None)
    retype_password = ObjectProperty(None)

    def create_wallet_callback(self):
        global notary_obj
        print('create wallet callback called')
        password_value = self.ids.password.text
        retyped_value = self.ids.retype_password.text
        if password_value == retyped_value:
            notary_obj = Notary("notaryconfig.ini", password_value)
            sm.current = 'registerwallet'
        else:
            popup = Popup(title='Password Mismatch', content=Label(text='Passwords does not match'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()


class RegisterWalletScreen(Screen):
    email = ObjectProperty(None)

    def register_wallet_callback(self):
        print('register wallet callback called')
        email_value = self.ids.email.text
        notary_obj.register_user(email_value)
        sm.current = 'confirmemail'


class PasswordScreen(Screen):
    password = ObjectProperty(None)

    def open_wallet_callback(self):
        global notary_obj
        print('open wallet callback called')
        password_value = self.ids.password.text
        try:
            notary_obj = Notary("notaryconfig.ini", password_value)
            #print notary_obj.register_user_status()
            if isinstance(notary_obj.register_user_status(), NotaryError):
                sm.current = 'confirmemail'
            else:
                sm.current = 'selectnotaryfile'
        except simplecrypt.DecryptionException as e:
            print e.message
            popup = Popup(title='Wrong Password', content=Label(text='Wrong password'), size_hint=(None, None),
                          size=(400, 200))
            popup.open()


class ConfirmScreen(Screen):
    def confirm_email_callback(self):
        global notary_obj
        print('confirm email callback called')
        #print notary_obj.register_user_status()
        if isinstance(notary_obj.register_user_status(),NotaryError):
            popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'), size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            sm.current = 'confirmemail'
        else:
            sm.current = 'selectnotaryfile'

class SelectNotaryFileScreen(Screen):
    pass



# Create the screen manager
sm = ScreenManager()
smcwallet = CreateWalletScreen(name='createwallet')
smrwallet = RegisterWalletScreen(name='registerwallet')
openwallet = PasswordScreen(name='openwallet')
confirmemail = ConfirmScreen(name='confirmemail')
selectnotaryfile=SelectNotaryFileScreen(name='selectnotaryfile')
sm.add_widget(smcwallet)
sm.add_widget(smrwallet)
sm.add_widget(openwallet)
sm.add_widget(confirmemail)
sm.add_widget(selectnotaryfile)

client_wallet_obj = ClientWallet("somepassword")
print "wallet exists"
print client_wallet_obj.wallet_exists()

if client_wallet_obj.wallet_exists():
    sm.current = "openwallet"
else:
    sm.current = "createwallet"


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
