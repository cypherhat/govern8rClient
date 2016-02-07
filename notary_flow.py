from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty


def initFlow(m_app , ui_test):
    global notary_app
    global ui_test_mode
    ui_test_mode = ui_test
    notary_app = m_app


class SelectNotaryFileScreen(Screen):
    filechooser = ObjectProperty(None)
    filelabel = ObjectProperty(None)
    notary_file = StringProperty()

    def my_callback(self, filename):
        if ui_test_mode:
            notary_app.sm.current = "selectnotaryfile"
            return
        if len(filename) >0:
            print('The button <%s> is being pressed' + filename[0])
            selected_file_name = filename[0]
            notary_app.uploadoption.notary_file = selected_file_name
            self.notary_file = selected_file_name
            notary_app.sm.current='selectnotaryfile'
        else:
            print "Nothing selected"



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
        if ui_test_mode:
            notary_app.sm.current = "openwallet"
            return
        result = notary_app.notary_obj.notarize_file(str(self.notary_file), getMetaData())
        message_value = 'Your document notarization is done !!!' + 'https://live.blockcypher.com/btc-testnet/tx/' + str(
                result)
        popup = Popup(title='Confirmation of Notary', content=Label(text=message_value),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()

        notary_app.notary_obj.upload_file(str(self.notary_file))
        popup = Popup(title='Confirmation of Upload', content=Label(text='Your document upload is done !!!'),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()
        popup = Popup(title='Confirmation of Notary', content=Label(text=str(result)),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()

        notary_app.sm.current = 'uploadoption'

    def no_callback(self):
        print('The button Nois being pressed')
        if ui_test_mode:
            notary_app.sm.current = "uploadoption"
            return
        result = notary_app.notary_obj.notarize_file(self.notary_file, getMetaData())
        popup = Popup(title='Confirmation of Notary', content=Label(
                text='Your document notarization is done !!!' + 'https://live.blockcypher.com/btc-testnet/tx/' + result[
                    'hash']),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()
        notary_app.sm.current = 'uploadoption'  # Create the screen manager
class MetadataScreen(Screen):
    pass
