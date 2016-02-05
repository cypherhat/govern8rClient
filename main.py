from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty
from notary_client import NotaryClient, NotaryException
from client_wallet import ClientWallet
import simplecrypt

notary_obj = None
selected_file_name = None

Builder.load_file("create_wallet.kv")
Builder.load_file("register_wallet.kv")
Builder.load_file("password.kv")
Builder.load_file("confirmation.kv")
Builder.load_file("select_notary_file.kv")
Builder.load_file("upload_option.kv")


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
            notary_obj = NotaryClient("notaryconfig.ini", password_value)
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
            notary_obj = NotaryClient("notaryconfig.ini", password_value)
            account = notary_obj.get_account()
            sm.current = 'selectnotaryfile'
        except NotaryException as e:
            print("Code %s " % e.error_code)
            print(e.message)
            sm.current = 'confirmemail'
        except ValueError as e:
            print("ValueError ")
            print(e.message)
            popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'),
                          size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            sm.current = 'confirmemail'
        except simplecrypt.DecryptionException as e:
            print e.message
            popup = Popup(title='Wrong Password', content=Label(text='Wrong password'), size_hint=(None, None),
                          size=(400, 200))
            popup.open()


class ConfirmScreen(Screen):
    def confirm_email_callback(self):
        global notary_obj
        print('confirm email callback called')
        # print notary_obj.register_user_status()
        try:
            account = notary_obj.get_account()
            sm.current = 'selectnotaryfile'
        except ValueError as e:
            print("ValueError ")
            print(e.message)
            popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'),
                          size_hint=(None, None),
                          size=(400, 200))
            popup.open()
            sm.current = "confirmemail"
        except NotaryException as e:
            if e.error_code == 404 or e.error_code == 403:
                popup = Popup(title='Confirmation', content=Label(text='Not yet confirmed. Try again.'),
                              size_hint=(None, None),
                              size=(400, 200))
                popup.open()
                sm.current = 'confirmemail'


class SelectNotaryFileScreen(Screen):
    filechooser = ObjectProperty(None)

    def my_callback(self, filename):
        print('The button <%s> is being pressed' + filename[0])
        selected_file_name = filename[0]
        uploadoption.notary_file = selected_file_name
        sm.current = 'uploadoption'


def getMetaData():
    meta_data = {
        'title': 'My favorite monkey',
        'creator': 'Ploughman, J.J.',
        'subject': 'TV show',
        'description': 'A show about a monkey... that you like the best...',
        'publisher': 'J.J. Ploughman',
        'contributor': 'J.J. Ploughman',
        'date': '2001-08-03T03:00:00.000000',
        'type': 'Video',
        'format': 'mpeg',
        'source': 'CBS',
        'language': 'en',
        'relation': 'Unknown',
        'coverage': 'Unknown',
        'rights': 'Unknown'
    }
    return meta_data


class UploadFileScreen(Screen):
    notary_file = StringProperty()
    selected_file = ObjectProperty(None)

    def yes_callback(self):
        print('The button Yes is being pressed')
        result = notary_obj.notarize_file(str(self.notary_file), getMetaData())
        message_value = 'Your document notarization is done !!!' + 'https://live.blockcypher.com/btc-testnet/tx/' + str(
            result)
        popup = Popup(title='Confirmation of Notary', content=Label(text=message_value),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()

        notary_obj.upload_file(str(self.notary_file))
        popup = Popup(title='Confirmation of Upload', content=Label(text='Your document upload is done !!!'),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()
        popup = Popup(title='Confirmation of Notary', content=Label(text=str(result)),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()

        sm.current = 'uploadoption'

    def no_callback(self):
        print('The button Nois being pressed')
        result = notary_obj.notarize_file(self.notary_file, getMetaData())
        popup = Popup(title='Confirmation of Notary', content=Label(
                text='Your document notarization is done !!!' + 'https://live.blockcypher.com/btc-testnet/tx/' + result[
                    'hash']),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()
        sm.current = 'uploadoption'  # Create the screen manager


sm = ScreenManager()
smcwallet = CreateWalletScreen(name='createwallet')
smrwallet = RegisterWalletScreen(name='registerwallet')
openwallet = PasswordScreen(name='openwallet')
confirmemail = ConfirmScreen(name='confirmemail')
selectnotaryfile = SelectNotaryFileScreen(name='selectnotaryfile')
uploadoption = UploadFileScreen(name='uploadoption')
sm.add_widget(smcwallet)
sm.add_widget(smrwallet)
sm.add_widget(openwallet)
sm.add_widget(confirmemail)
sm.add_widget(selectnotaryfile)
sm.add_widget(uploadoption)

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


class NotaryApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    NotaryApp().run()
