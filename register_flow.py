from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from notary_client import NotaryClient, NotaryException
import simplecrypt


def initFlow(m_app):
    global notary_app
    notary_app = m_app


class CreateWalletScreen(Screen):
    password = ObjectProperty(None)
    retype_password = ObjectProperty(None)

    def create_wallet_callback(self):

        print('create wallet callback called')
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
        email_value = self.ids.email.text
        notary_app.notary_obj.register_user(email_value)
        notary_app.sm.current = 'confirmemail'


class PasswordScreen(Screen):
    password = ObjectProperty(None)
    def open_wallet_callback(self):
        print('open wallet callback called')
        password_value = self.ids.password.text
        try:
            notary_app.notary_obj = NotaryClient("notaryconfig.ini", password_value)
            account = notary_app.notary_obj.get_account()
            notary_app.sm.current = 'selectnotaryfile'
        except NotaryException as e:
            print("Code %s " % e.error_code)
            print(e.message)
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
        # print notary_obj.register_user_status()
        try:
            account = notary_app.notary_obj.get_account()
            notary_app.sm.current = 'selectnotaryfile'
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
