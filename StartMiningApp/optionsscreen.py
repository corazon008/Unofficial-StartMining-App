from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from data import Datas


class OptionsScreen(Screen):
    Builder.load_file('optionsscreen.kv')

    def on_enter(self, *args):
        self.update_label()

    def update_label(self):
        try:
            Datas.load_data()
        except:
            pass

        self.ids.btc_wallet.text = Datas.btc_wallet
        self.ids.eth_wallet.text = Datas.eth_wallet

    def submit(self):
        Datas.store_data()