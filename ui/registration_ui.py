import kivy
import notary

kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class TestApp(App):

    def build(self):
        layout = FloatLayout()
        lblemail = Label(text='Email: ', size_hint=(.2, .05),  pos_hint={'x': .1, 'y': .9})
        txtemail = TextInput(text='', size_hint=(.6, .05),  pos_hint={'x': .3, 'y': .9})
        layout.add_widget(lblemail)
        layout.add_widget(txtemail)

        lblpassword1 = Label(text='Password: ', size_hint=(.2, .05),  pos_hint={'x': .1, 'y': .8})
        txtpassword1 = TextInput(text='', size_hint=(.6, .05), password='true',  pos_hint={'x': .3, 'y': .8})
        layout.add_widget(lblpassword1)
        layout.add_widget(txtpassword1)

        lblpassword2 = Label(text='Confirm Password: ', size_hint=(.2, .05),  pos_hint={'x': .1, 'y': .7})
        txtpassword2 = TextInput(text='', size_hint=(.6, .05), password='true',  pos_hint={'x': .3, 'y': .7})
        layout.add_widget(lblpassword2)
        layout.add_widget(txtpassword2)

        btnSubmit = Button(text='Submit', size_hint=(.2, .05),  pos_hint={'x': .3, 'y': .6})
        layout.add_widget(btnSubmit)

        def callback(instance):
            print ("register started")
            print('The button <%s> is being pressed' % instance.text)
            lbltester.text= txtemail.text + '|' + txtpassword1.text + '|' + txtpassword2.text
            notary_obj=notary.Notary(txtpassword1.text)
            result = notary_obj.register_user(txtemail.text)
            print result

        lbltester = Label(text='Testing: ', size_hint=(.2, .2),  pos_hint={'x': .1, 'y': .2})
        layout.add_widget(lbltester)
        lbltester.bind(on_press=callback)

        btnSubmit.bind(on_press=callback)
        # return a Button() as a root widget
        #return Button(text='hello world')


        return layout

TestApp().run()
