from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os.path, time
import ntpath
from os import stat
from pwd import getpwuid

from kivy.properties import ObjectProperty, StringProperty


def initFlow(m_app, ui_test):
    global notary_app
    global ui_test_mode
    ui_test_mode = ui_test
    notary_app = m_app


class SelectNotaryFileScreen(Screen):
    filechooser = ObjectProperty(None)
    filelabel = ObjectProperty(None)
    notary_file = StringProperty()

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def my_callback(self, filename):
        if len(filename) > 0:
            print('The button <%s> is being pressed' + filename[0])
            print('The parsed title is ' + self.path_leaf(str(filename[0])))
            print('Time is ' + time.ctime(os.path.getctime(filename[0])))
            print('Owner is ' + getpwuid(stat(filename[0]).st_uid).pw_name)

            selected_file_name = filename[0]
            selected_file_name_no_path = self.path_leaf(str(filename[0]))
            selected_file_created_dt = '' + time.ctime(os.path.getctime(filename[0]))
            selected_file_mod_dt = '' + time.ctime(os.path.getmtime(filename[0]))
            selected_file_owner = getpwuid(stat(selected_file_name).st_uid).pw_name

            notary_app.meta_data.notary_file = selected_file_name
            notary_app.meta_data.notary_file_no_path = selected_file_name_no_path
            notary_app.meta_data.file_created_dt = selected_file_created_dt
            notary_app.meta_data.file_mod_dt = selected_file_mod_dt
            notary_app.meta_data.file_created_by = selected_file_owner

            self.notary_file = selected_file_name
            notary_app.sm.current = 'selectnotaryfile'
        else:
            print "Nothing selected"

    def next_callback(self):
        if len(self.notary_file) > 0:
            notary_app.sm.current = 'metadata'
        else:
            message_value = 'No File Selected. Choose one first.'
            popup = Popup(title='File Selection', content=Label(text=message_value),
                      size_hint=(None, None),
                      size=(400, 200))
            popup.open()




def getMetaData(notary_file, file_owner, file_created_dt, file_created_by):
    print('Meta: ' + notary_file)
    print('Meta: ' + file_created_dt)
    print('Meta: ' + file_created_by)

    meta_data = {
        'title': notary_file,
        'creator': file_created_by,
        'subject': 'TV show',
        'description': 'A show about a monkey... that you like the best...',
        'publisher': 'J.J. Ploughman',
        'contributor': 'J.J. Ploughman',
        'date': file_created_dt,
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
    file_owner = StringProperty()
    file_created_dt = StringProperty()
    file_mod_dt = StringProperty()
    file_created_by = StringProperty()
    selected_file = ObjectProperty(None)

    def yes_callback(self):
        print('The button Yes is being pressed')
        if ui_test_mode:
            notary_app.sm.current = "landingpage"
            return
        result = notary_app.notary_obj.notarize_file(str(self.notary_file), getMetaData())
        message_value = 'Your document notarization is done !!!'
        popup = Popup(title='Confirmation of Notary', content=Label(text=message_value),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()

        notary_app.notary_obj.upload_file_encrypted(str(self.notary_file))
        popup = Popup(title='Confirmation of Upload', content=Label(text='Your document upload is done !!!'),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()

        notary_app.sm.current = 'viewclaims'

    def no_callback(self):
        print('The button No is being pressed')
        if ui_test_mode:
            notary_app.sm.current = "landing page"
            return
        result = notary_app.notary_obj.notarize_file(self.notary_file, getMetaData())
        popup = Popup(title='Confirmation of Notary', content=Label(
                text='Your document notarization is done !!!' + 'https://live.blockcypher.com/btc-testnet/tx/' + result[
                    'hash']),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()
        notary_app.sm.current = 'landingpage'  # Create the screen manager

class MetadataScreen(Screen):
    notary_file = StringProperty()
    notary_file_no_path = StringProperty()
    file_owner = StringProperty()
    file_created_dt = StringProperty()
    file_mod_dt = StringProperty()
    file_created_by = StringProperty()

    def yes_callback(self):
        print('The button Yes is being pressed' + self.notary_file)

        json = getMetaData(self.notary_file_no_path,self.file_owner,self.file_created_dt,self.file_created_by)

        print('Meta Json Test: ' + str(json))
        import notary_client
        try :
            result = notary_app.notary_obj.notarize_file(str(self.notary_file), json)
        except notary_client.NotaryException as e:
           print("Code %s " % e.error_code)
           print(e.message)

        try :
            notary_app.notary_obj.upload_file_encrypted(str(self.notary_file))
        except notary_client.NotaryException as e:
           print("Code %s " % e.error_code)
           print(e.message)

        popup = Popup(title='Confirmation of Upload',
                      content=Label(text='Congrats. Your document notariztion and upload are successfully.'),
                      size_hint=(None, None),
                      size=(400, 200))
        popup.open()

        notary_app.sm.current = 'viewclaims'