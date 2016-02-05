from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from client_wallet import ClientWallet
import register_flow
import notary_flow

class NotaryApp(App):

    def __init__(self):
        super(NotaryApp, self).__init__()

        Builder.load_file("create_wallet.kv")
        Builder.load_file("register_wallet.kv")
        Builder.load_file("password.kv")
        Builder.load_file("confirmation.kv")
        Builder.load_file("select_notary_file.kv")
        Builder.load_file("upload_option.kv")
        self.notary_obj = None
        self.selected_file_name = None
        self.sm = ScreenManager()
        self.smcwallet =  register_flow.CreateWalletScreen(name='createwallet')
        self.smrwallet =  register_flow.RegisterWalletScreen(name='registerwallet')
        self.openwallet = register_flow.PasswordScreen(name='openwallet')
        self.confirmemail=register_flow.ConfirmScreen(name='confirmemail')
        self.selectnotaryfile = notary_flow.SelectNotaryFileScreen(name='selectnotaryfile')
        self.uploadoption = notary_flow.UploadFileScreen(name='uploadoption')
        self.sm.add_widget(self.smcwallet)
        self.sm.add_widget(self.smrwallet)
        self.sm.add_widget(self.openwallet)
        self.sm.add_widget(self.confirmemail)
        self.sm.add_widget(self.selectnotaryfile)
        self.sm.add_widget(self.uploadoption)

    def find_state(self):
        client_wallet_obj = ClientWallet("somepassword")
        print "wallet exists"
        print client_wallet_obj.wallet_exists()

        if client_wallet_obj.wallet_exists():
             self.sm.current = "openwallet"
        else:
             self.sm.current = "createwallet"
    def build(self):
        return self.sm

if __name__ == '__main__':
    global notary_app
    notary_app = NotaryApp()
    register_flow.initFlow(notary_app)
    notary_flow.initFlow(notary_app)
    notary_app.find_state()
    notary_app.run()
