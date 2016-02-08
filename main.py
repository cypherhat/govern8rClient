from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
import register_flow
import notary_flow
from kivy.uix.screenmanager import Screen

ui_test_mode = True

class LandingScreen(Screen):
     pass

class ViewClaimsScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen,self).__init__(**kwargs)
        self.current = 'start'
        #for child in self.children:
        #    print(child.id)
        print(str(self.ids.claimsgrid))
        print(str(self.ids.title_1.text))

        def callback(instance):
            print ("register started")
            print('The button <%s> is being pressed' % instance.text)

        btn1 =Button(text='Button 1' , size=(200,50), size_hint=(None, None))
        lbl2 =Label(text='Email2: ', size_hint=(.2, .05),  pos_hint={'x': .1, 'y': .9})
        lbl3 =Label(text='Email3: ', size_hint=(.2, .05),  pos_hint={'x': .1, 'y': .9})

        self.ids.claimsgrid.add_widget(btn1)
        self.ids.claimsgrid.add_widget(lbl2)
        self.ids.claimsgrid.add_widget(lbl3)

        btn1.bind(on_press=callback)
        lbl2.bind(on_press=callback)
        lbl3.bind(on_press=callback)


class NotaryApp(App):

    def __init__(self):
        super(NotaryApp, self).__init__()

        Builder.load_file("create_wallet.kv")
        Builder.load_file("register_wallet.kv")
        Builder.load_file("password.kv")
        Builder.load_file("confirmation.kv")
        Builder.load_file("select_notary_file.kv")
        Builder.load_file("upload_option.kv")
        Builder.load_file("meta_data.kv")
        Builder.load_file("landing_page.kv")
        Builder.load_file("view_claims.kv")
        self.title = "1styoos"
        self.icon='img/logo.png'
        self.notary_obj = None
        self.selected_file_name = None
        self.sm = ScreenManager()
        self.smcwallet =  register_flow.CreateWalletScreen(name='createwallet')
        self.smrwallet =  register_flow.RegisterWalletScreen(name='registerwallet')
        self.openwallet = register_flow.PasswordScreen(name='openwallet')
        self.confirmemail=register_flow.ConfirmScreen(name='confirmemail')
        self.selectnotaryfile = notary_flow.SelectNotaryFileScreen(name='selectnotaryfile')
        self.meta_data = notary_flow.MetadataScreen(name='metadata')
        self.uploadoption = notary_flow.UploadFileScreen(name='uploadoption')
        self.landingscreen = LandingScreen(name='landingpage')
        self.viewclaims = ViewClaimsScreen(name='viewclaims')
        self.sm.add_widget(self.smcwallet)
        self.sm.add_widget(self.smrwallet)
        self.sm.add_widget(self.openwallet)
        self.sm.add_widget(self.confirmemail)
        self.sm.add_widget(self.selectnotaryfile)
        self.sm.add_widget(self.uploadoption)
        self.sm.add_widget(self.meta_data)
        self.sm.add_widget(self.landingscreen)
        self.sm.add_widget(self.viewclaims)

    def find_state(self):
        import client_wallet
        client_wallet_obj = client_wallet.ClientWallet("somepassword")
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
    register_flow.initFlow(notary_app,ui_test_mode)
    notary_flow.initFlow(notary_app,ui_test_mode)
    if ui_test_mode is False:
        notary_app.find_state()
    notary_app.run()
