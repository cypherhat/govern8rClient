from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from notary_client import NotaryException
from kivy.uix.label import Label
from kivy.uix.button import Button
import json


def initFlow(m_app , ui_test):
    global notary_app
    global ui_test_mode
    ui_test_mode = ui_test
    notary_app = m_app


class CreateWalletScreen(Screen):
    password = ObjectProperty(None)
    retype_password = ObjectProperty(None)

    def create_wallet_callback(self):
        print('create wallet callback called')
        if ui_test_mode:
            notary_app.sm.current = "registerwallet"
            return
        from notary_client import NotaryClient
        password_value = self.ids.password.text
        retyped_value = self.ids.retype_password.text
        if password_value == retyped_value:
            notary_app.notary_obj = NotaryClient("notaryconfig.ini", password_value)
            notary_app.sm.current = 'registerwallet'
        else:
            popup = Popup(title='Password Mismatch', content=Label(text='Passwords does not match'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()


class RegisterWalletScreen(Screen):
    email = ObjectProperty(None)

    def register_wallet_callback(self):
        print('register wallet callback called')
        if ui_test_mode:
            notary_app.sm.current = "confirmemail"
            return
        email_value = self.ids.email.text
        notary_app.notary_obj.register_user(email_value)
        notary_app.sm.current = 'confirmemail'


class PasswordScreen(Screen):
    password = ObjectProperty(None)
    def open_wallet_callback(self):
        print('open wallet callback called')
        if ui_test_mode:
            notary_app.sm.current = "landingpage"
            return
        from notary_client import NotaryClient, NotaryException
        import simplecrypt
        password_value = self.ids.password.text
        if password_value is None:
            popup = Popup(title='Wrong Password', content=Label(text='Wrong password'), size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            return
        if len(password_value) is 0:
            popup = Popup(title='Wrong Password', content=Label(text='Wrong password'), size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            return

        try:
            notary_app.notary_obj = NotaryClient("notaryconfig.ini", password_value)
            account = notary_app.notary_obj.get_account()
            notary_app.sm.add_widget(ViewClaimsScreen(name='viewclaims'))
            notary_app.sm.current = 'landingpage'
        except NotaryException as e:
            print("Code %s " % e.error_code)
            print(e.message)
            if e.error_code == 404:
                notary_app.sm.current = 'registerwallet'
            elif e.error_code == 403:
                notary_app.sm.current = 'confirmemail'
        except ValueError as e:
            print("ValueError ")
            print(e.message)
            popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'),
                          size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            notary_app.sm.current = 'confirmemail'
        except simplecrypt.DecryptionException as e:
            print e.message
            popup = Popup(title='Wrong Password', content=Label(text='Wrong password'), size_hint=(None, None),
                          size=(400, 200))
            popup.open()


class ConfirmScreen(Screen):
    def confirm_email_callback(self):
        print('confirm email callback called')
        if ui_test_mode:
            notary_app.sm.current = "landingpage"
            return
        from notary_client import  NotaryException
        # print notary_obj.register_user_status()
        try:
            account = notary_app.notary_obj.get_account()
            notary_app.sm.current = 'landingpage'
        except ValueError as e:
            print("ValueError ")
            print(e.message)
            popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'),
                          size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            notary_app.sm.current = "confirmemail"
        except NotaryException as e:
            if e.error_code == 404 or e.error_code == 403:
                popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'),
                              size_hint=(None, None),
                              size=(400, 200))
                popup.open()
                notary_app.sm.current = 'confirmemail'


class ViewClaimsScreen(Screen):

    def callback1(instance):
            print ("register started")
            print('The 1 button <%s> is being pressed' )
    def callback2(instance):
            print ("register started")
            print('The 2 button <%s> is being pressed' )
    def callback3(instance):
            print ("register started")
            print('The 3 button <%s> is being pressed')


    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.current = 'start'
        try:
            message = notary_app.notary_obj.get_notarizations()
            if len(message) > 0:
                print(message)
                for notarization in message:
                    print(notarization)
                    print(notarization['title'])
                    print(notarization['document_hash'][:4])
                    print(notarization['transaction_hash'][:4])
                    btn1 = Button(text=notarization['title'][:4], size=(200, 50), size_hint=(None, None))
                    lbl2 = Label(text=notarization['document_hash'][:4], size_hint=(.2, .05), pos_hint={'x': .1, 'y': .9})
                    lbl3 = Label(text=notarization['transaction_hash'][:4], size_hint=(.2, .05), pos_hint={'x': .1, 'y': .9})
                    self.ids.claimsgrid.add_widget(btn1)
                    self.ids.claimsgrid.add_widget(lbl2)
                    self.ids.claimsgrid.add_widget(lbl3)
                    btn1.bind(on_press=self.callback1)
                    lbl2.bind(on_press=self.callback2)
                    lbl3.bind(on_press=self.callback3)


        except NotaryException as e:
            print("Code %s " % e.error_code)
            print(e.message)







