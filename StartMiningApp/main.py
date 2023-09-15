import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

kivy.require("2.2.1")

#Window.size = (540, 540) # (540, 900)

from startminingscreen import StartMiningScreen
from optionsscreen import OptionsScreen
from data import Datas

__version__ = "1.1"


class NavBar(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        Datas.my_stake_per_pool()
        self.screen_manager = ScreenManager()

        # Ajoutez les écrans à votre gestionnaire d'écrans
        self.screen_manager.add_widget(StartMiningScreen(name='start_mining'))
        self.screen_manager.add_widget(OptionsScreen(name='options'))

        return self.screen_manager

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name

    def color(self, r, g, b, a):
        return (r / 255, g / 255, b / 255, a)


if __name__ == '__main__':
    MyApp().run()
