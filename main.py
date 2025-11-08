from kivy.config import Config

# CONFIG BASE 
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
import os, time

Window.clearcolor = (1, 1, 1, 1)  # Sfondo bianco

# Pulsante con stile arrotondato coerente
class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Schermata di login
class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        self.add_widget(Widget())  # Spacer

        self.label = Label(
            text="Master Password",
            font_size=30,
            font_name="utils/Jaro.ttf",
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=50
        )
        self.add_widget(self.label)

        self.input_pw = TextInput(
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.input_pw)

        self.button = RoundedButton(
            text="Login",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1)
        )
        self.button.bind(on_press=self.check_password)
        self.add_widget(self.button)

        self.feedback = Label(
            text="",
            font_size=18,
            color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=30
        )
        self.add_widget(self.feedback)

        self.add_widget(Widget())  # Spacer

        try:
            with open("utils/psw.txt", "r") as file:
                self.correct_password = file.read().strip()
        except FileNotFoundError:
            self.correct_password = None
            self.feedback.text = "Password file non trovato."

    def check_password(self, instance):
        if self.correct_password is None:
            return

        if self.input_pw.text == self.correct_password:
            self.feedback.text = "Accesso riuscito!"
            from ui import ui
            self.clear_widgets()
            ui.MyApp().run()
        else:
            self.feedback.text = "Password errata."


# Schermata per nuova password
class NewPasswordScreen(BoxLayout):
    def __init__(self, switch_to_login_callback, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        self.switch_to_login = switch_to_login_callback

        self.add_widget(Widget())  # Spacer

        self.label = Label(
            text="Crea una nuova password",
            font_size=30,
            font_name="utils/Jaro.ttf",
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=50
        )
        self.add_widget(self.label)

        self.input_new_pw = TextInput(
            password=True,
            multiline=False,
            hint_text="Nuova password",
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.input_new_pw)

        self.button = RoundedButton(
            text="Salva password",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1)
        )
        self.button.bind(on_press=self.save_password)
        self.add_widget(self.button)

        self.feedback = Label(
            text="",
            font_size=18,
            color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=30
        )
        self.add_widget(self.feedback)

        self.add_widget(Widget())  # Spacer

    def save_password(self, instance):
        new_pw = self.input_new_pw.text.strip()

        if not new_pw:
            self.feedback.text = "La password non può essere vuota."
            return

        try:
            with open("utils/psw.txt", "w") as f:
                f.write(new_pw)

            with open("utils/temp.txt", "w") as f:
                f.write("Accesso")

            self.feedback.color = (0, 0.6, 0, 1)
            self.feedback.text = "Password salvata!"
            self.switch_to_login()

        except Exception as e:
            self.feedback.text = f"Errore: {e}"

        Clock.schedule_once(lambda dt: self.__init__, 2)
        self.clear_widgets()
        MyApp().run()


# App principale
class MyApp(App):
    def build(self):
        self.root_layout = BoxLayout()
        return self.check_state()

    def check_state(self):
        if os.path.exists("utils/temp.txt"):
            with open("utils/temp.txt", "r") as file:
                content = file.read()
                if "Accesso" in content:
                    return LoginScreen()
                elif "" in content:
                    return NewPasswordScreen(self.restart_with_login)
        return Label(text="File temp.txt non valido o mancante")

    def restart_with_login(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(LoginScreen())
        return self.root_layout


if __name__ == "__main__":
    MyApp().run()
