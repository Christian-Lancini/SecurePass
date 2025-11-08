from kivy.config import Config

# CONFIG BASE 
#Config.set('graphics', 'width', '360')
#Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'fullscreen', '1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
import json, os, string

from lib.crypt import crypt
from lib.decrypt import decrypt
from lib.backup import backup_crypt


Window.clearcolor = (1, 1, 1, 1)


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)  # trasparente per mostrare il canvas personalizzato

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # colore bluastro
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.clear_widgets()

        self.titolo = Label(
            text="SecurePass",
            font_size=40,
            font_name="utils/Jaro.ttf",
            size_hint_y=None,
            height=50,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        )

        self.titolo.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        self.add_widget(self.titolo)

        self.sottotitolo = Label(
            text="Release",
            font_size=20,
            font_name="utils/Jaro.ttf",
            size_hint_y=None,
            height=30,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        )
        self.add_widget(self.sottotitolo)

        self.add_widget(Widget())

        self.aggiungi_password = RoundedButton(
            text="Aggiungi Password",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )

        self.aggiungi_password.bind(on_press=self.aggiungi_gui)
        self.add_widget(self.aggiungi_password)
        
        self.elimina_password = RoundedButton(
            text="Elimina Password",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.elimina_password.bind(on_press=self.elimina_password_gui)
        self.add_widget(self.elimina_password)

        self.mostra_password = RoundedButton(
            text="Mostra password",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.mostra_password.bind(on_press=self.mostra_password_gui)
        self.add_widget(self.mostra_password)

        self.passw_gen = RoundedButton(
            text="Genera Password",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.passw_gen.bind(on_press=self.passw_gen_gui)
        self.add_widget(self.passw_gen)


        self.settigs = RoundedButton(
            text="Impostazioni",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.settigs.bind(on_press=self.settings_gui)
        self.add_widget(self.settigs)

        self.btn_torna = RoundedButton(
            text="Esci",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.btn_torna.bind(on_press=lambda x: exit())
        self.add_widget(self.btn_torna)

        # Spacer per spingere tutto verso l'alto
        self.add_widget(Widget())


    def aggiungi_gui(self, instance):
        self.clear_widgets()

        self.label_pw= Label(
            text="Aggiungi Password",
            font_size=40,
            font_name="utils/Jaro.ttf",
            height=50,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            bold=True
        )
        self.add_widget(self.label_pw)

        self.input_pw = TextInput(
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.input_pw)

        btn_salva = RoundedButton(
            text="Salva",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        btn_salva.bind(on_press=lambda x: self.aggiungi(self.input_pw.text.strip()))
        self.add_widget(btn_salva)

        btn_torna = RoundedButton(
            text="Torna al menu",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        btn_torna.bind(on_press=lambda x: self.__init__())
        self.add_widget(btn_torna)

        self.add_widget(Widget())



    def aggiungi(self, passw):
        decrypt()
        path = 'password/password.json'
        data = []

        if os.path.exists(path):
            with open(path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

        self.clear_widgets()
        
        if passw == '':
            self.empty = Label(
                text="Inserisci una password valida",
                size_hint=(1, None),
                height=50,
                color=(1, 0, 0, 1) 
            )
            self.add_widget(self.empty)
            self.add_widget(Widget())
            crypt()
        elif passw in data:
            self.error = Label(
                text="Password già presente",
                size_hint=(1, None),
                height=50,
                color=(1, 0, 0, 1)
            )
            self.add_widget(self.error)
            self.add_widget(Widget())
            crypt()
        else:
            data.append(passw)
            with open(path, "w") as file:
                json.dump(data, file, indent=4)

            crypt()          

            self.success = Label(
                text="Password salvata!",
                size_hint=(1, None),
                height=50,
                color=(0, 0.6, 0, 1)
            )
            self.add_widget(self.success)
            self.add_widget(Widget())
            # Torna al menu principale dopo 2 secondi
            Clock.schedule_once(lambda dt: self.__init__(), 2)
            return
        

        Clock.schedule_once(lambda dt: self.__init__(), 2)

    def elimina_password_gui(self, instance):
        self.clear_widgets()

        self.label_pw= Label(
            text="Elimina Password",
            font_size=40,
            font_name="utils/Jaro.ttf",
            height=50,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            bold=True
        )

        self.add_widget(self.label_pw)

        self.input_pw = TextInput(
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.input_pw)

        btn_elimina = RoundedButton(
            text="Elimina",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        btn_elimina.bind(on_press=lambda x: self.elimina(self.input_pw.text))
        self.add_widget(btn_elimina)


        btn_torna = RoundedButton(
            text="Torna al menu",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        btn_torna.bind(on_press=lambda x: self.__init__())
        self.add_widget(btn_torna)        

        self.add_widget(Widget())

    def elimina(self, passw):
        decrypt()
        path = 'password/password.json'
        data = []

        if os.path.exists(path):
            with open(path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
                except Exception as e:
                    print(e)

        self.clear_widgets()

        if passw in data:
            data.remove(passw)
            with open(path, "w") as file:
                json.dump(data, file, indent=4)
            crypt()
            self.eliminata = Label(
                text="Password eliminata con successo!",
                size_hint=(1, None),
                height=50,
                color=(0, 0.6, 0, 1)
            )
            self.add_widget(self.eliminata)
            self.add_widget(Widget())
            Clock.schedule_once(lambda dt: self.__init__(), 2)
        else:
            self.non_trovata = Label(
                text="Password non trovata! :(",
                size_hint=(1, None),
                height=50,
                color=(1, 0, 0, 1)
            )
            crypt()
            self.add_widget(self.non_trovata)
            self.add_widget(Widget())
            Clock.schedule_once(lambda dt: self.__init__(), 2)


    def mostra_password_gui(self, instance):
        self.clear_widgets()
        
        # Decripta solo una volta all'inizio
        decrypt()
        
        path = "password/password.json"
        data = []

        self.label_pw= Label(
            text="Mostra Password",
            font_size=40,
            font_name="utils/Jaro.ttf",
            height=50,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            bold=True
        )

        self.add_widget(self.label_pw)

        if os.path.exists(path):
            with open(path, "r") as file:
                try:
                    data = json.load(file)
                    if not data:
                        self.add_widget(Label(text="Nessuna password salvata.", color=(0.5, 0, 0, 1)))
                    for pw in data:
                        lbl_pw = Label(
                            text=pw,
                            size_hint=(1, None),
                            height=40,
                            color=(0, 0, 0, 1)
                        )
                        self.add_widget(lbl_pw)
                except json.JSONDecodeError:
                    self.add_widget(Label(text="Errore nel file JSON.", color=(1, 0, 0, 1)))
                except Exception as e:
                    print(e)
        else:
            self.add_widget(Label(text="File password non trovato.", color=(1, 0, 0, 1)))
        
        self.add_widget(Widget())

        # Quando clicchi il pulsante "Torna al menu", cripta e poi torna
        def torna_menu(instance):
            crypt()
            self.__init__()

        btn_torna = RoundedButton(
            text="Torna al menu",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        btn_torna.bind(on_press=torna_menu)
        self.add_widget(btn_torna)

        self.add_widget(Widget())

    def passw_gen_gui(self, instance):
        self.clear_widgets()

        self.label_pw= Label(
            text="Genera Password",
            font_size=40,
            font_name="utils/Jaro.ttf",
            height=50,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            bold=True
        )

        self.add_widget(self.label_pw)

        self.password_print = Label(
            text="Password",
            font_size=30,
            font_name="utils/Jaro.ttf",
            height=50,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
        )
        self.add_widget(self.password_print)

        self.genera = RoundedButton(
            text="Genera Password",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.genera.bind(on_press=self.generatore)
        self.add_widget(self.genera)


        btn_torna = RoundedButton(
            text="Torna al menu",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        btn_torna.bind(on_press=lambda x: self.__init__())
        self.add_widget(btn_torna)        

        self.add_widget(Widget())

    def generatore(self, instance):
        from lib import generatore
        password = generatore.genera()

        self.clear_widgets()
        self.label_pw = Label(
            text="Genera Password",
            font_size=40,                
            font_name="utils/Jaro.ttf",
            height=50,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            bold=True
        )
        self.add_widget(self.label_pw)

        self.password_label = Label(
            text=password,
            font_size=30,
            font_name="utils/Jaro.ttf",
            height=50,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        )
        self.add_widget(self.password_label)

        self.genera = RoundedButton(                
            text="Genera un'altra",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.genera.bind(on_press=self.generatore)
        self.add_widget(self.genera)

        self.salva = RoundedButton(
            text="Salva",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.salva.bind(on_press=lambda x: self.salva_pass(password))
        self.add_widget(self.salva)

        btn_torna = RoundedButton(            
            text="Torna al menu",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        btn_torna.bind(on_press=lambda x: self.__init__())
        self.add_widget(btn_torna)

        self.add_widget(Widget())

    def salva_pass(self, psw):
        decrypt()
        path = 'password/password.json'
        data = []

        if os.path.exists(path):
            with open(path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

        if psw not in data:
            data.append(psw)
            with open(path, "w") as file:
                json.dump(data, file, indent=4)
            crypt()
            self.clear_widgets()
            self.add_widget(Label(
                text="Password salvata!",
                font_size=24,
                color=(0, 0.6, 0, 1)
            ))
        else:
            self.clear_widgets()
            self.add_widget(Label(
                text="Password già presente.",
                font_size=24,
                color=(1, 0, 0, 1)
            ))

        Clock.schedule_once(lambda dt: self.__init__(), 2)

    
    def settings_gui(self, instance):
        self.clear_widgets()

        self.label_pw= Label(
            text="Impostazioni",
            font_size=40,
            font_name="utils/Jaro.ttf",
            height=50,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            bold=True
        )
        self.add_widget(self.label_pw)

        self.backup = RoundedButton(
            text="Backup Criptato",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        self.backup.bind(on_press=self.backup_s)
        self.add_widget(self.backup)
        
        btn_torna = RoundedButton(
            text="Torna al menu",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        btn_torna.bind(on_press=lambda x: self.__init__())
        self.add_widget(btn_torna)

        self.add_widget(Widget())

    def backup_s(self, instance):
        path = 'password/backup_try.txt'

        try:
            decrypt()
            with open("password/password.json", "r") as file:
                passwords = json.load(file)

            with open(path, 'w') as file:
                for pw in passwords:
                    file.write(pw + '\n')

            backup_crypt()  # Chiamata corretta alla funzione per criptare il file
            crypt()
            self.clear_widgets()
            self.add_widget(Label(
                text="Backup completato con successo!",
                font_size=24,
                color=(0, 0.6, 0, 1)
            ))
            Clock.schedule_once(lambda dt: self.__init__(), 2)

        except FileNotFoundError:
            self.clear_widgets()
            self.add_widget(Label(
                text="Errore: file password.json non trovato.",
                font_size=24,
                color=(1, 0, 0, 1)
            ))
            Clock.schedule_once(lambda dt: self.__init__(), 2)

        except Exception as e:
            self.clear_widgets()
            self.add_widget(Label(
                text="Errore: " + str(e), 
                font_size=20,
                color=(1, 0, 0, 1)
            ))
            Clock.schedule_once(lambda dt: self.__init__(), 2)


class MyApp(App):
    def build(self):
        self.title = "Password Manager"
        return MyLayout()

if __name__ == "__main__":
    MyApp().run()
