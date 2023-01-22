# importing libraries
import openai
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy_garden.admob import AdMobBanner

# Create the screen manager
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_balance = 100
        self.chats_per_ad = 20

    def watch_ad(self):
        self.chat_balance += self.chats_per_ad
        self.balance_label.text = f'Chat Balance: {self.chat_balance}'

    def start_chat(self):
        if self.chat_balance > 0:
            self.chat_balance -= 1
            self.balance_label.text = f'Chat Balance: {self.chat_balance}'
            # start chat logic here
        else:
            self.show_watch_ad_popup()

    def show_watch_ad_popup(self):
        watch_ad_popup = WatchAdPopup()
        watch_ad_popup.open()
    
    def start_chat(self):
        if self.chat_balance > 0:
            self.chat_balance -= 1
            self.balance_label.text = f'Chat Balance: {self.chat_balance}'
            user_input = self.text_input.text
            self.text_input.text = ''
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=(f"User: {user_input}\nBot:"),
                max_tokens=2048,
                n=1,
                stop=None,
                temperature=0.5
            )
            bot_response = response.choices[0].text
            self.history.text += f'\nUser: {user_input}\nBot: {bot_response}'
        else:
            self.history.text += '\nYou have run out of chat balance, watch an ad to get more chats!'


class WatchAdPopup(Popup):
    def watch_ad(self):
        self.dismiss()
        main_screen = App.get_running_app().root.get_screen('main')
        main_screen.watch_ad()



class RootWidget(ScreenManager):
    pass

kv = Builder.load_string('''
RootWidget:
    MainScreen:
    ChatScreen:

<MainScreen>:
    name: 'main'
    GridLayout:
        cols: 1
        Button:
            text: 'Start Chat'
            on_press:
                root.current = 'chat'
                root.transition.direction = 'left'

<ChatScreen>:
    name: 'chat'
    GridLayout:
        cols: 1
        Button:
            text: 'Go back'
            on_press:
                root.current = 'main'
                root.transition.direction = 'right'
''')

class MainApp(App):
    def build(self):
        ad = AdMobBanner(size_banner='BANNER', test_device=True)
        self.add_widget(ad)
        return kv

if __name__ == '__main__':
    MainApp().run()
