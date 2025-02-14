from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from database import DataBase

# Constants
POPUP_SIZE = (400, 400)


class BaseLabel(Label):
    font_size_ratio = NumericProperty(17)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(width=self.update_font_size, height=self.update_font_size)

    def update_font_size(self, *args):
        self.font_size = (self.width ** 2 + self.height ** 2) / self.font_size_ratio ** 4


class BaseTextInput(TextInput):
          font_size_ratio = NumericProperty(17)

          def __init__(self, **kwargs):
                    super().__init__(**kwargs)
                    self.bind(width=self.update_font_size, height=self.update_font_size)

          def update_font_size(self, *args):
                    self.font_size = (self.width ** 2 + self.height ** 2) / self.font_size_ratio ** 4


class BaseButton(Button):
          font_size_ratio = NumericProperty(17)

          def __init__(self, **kwargs):
                    super().__init__(**kwargs)
                    self.bind(width=self.update_font_size, height=self.update_font_size)

          def update_font_size(self, *args):
                    self.font_size = (self.width ** 2 + self.height ** 2) / self.font_size_ratio ** 4


class CreateAccountWindow(Screen):
          namee = ObjectProperty(None)
          email = ObjectProperty(None)
          password = ObjectProperty(None)

          def submit(self):
                    if self._validate_input():
                              try:
                                        db.add_user(self.email.text, self.password.text, self.namee.text)
                                        self.reset()
                                        sm.current = "login"
                              except Exception as e:
                                        self._show_error(f"An error occurred: {str(e)}")
                    else:
                              self._show_error("Invalid form data")

          def login(self):
                    self.reset()
                    sm.current = "login"

          def reset(self):
                    self.email.text = ""
                    self.password.text = ""
                    self.namee.text = ""

          def _validate_input(self) -> bool:
                    return (self.namee.text and self.email.text
                            and self.email.text.count("@") == 1
                            and self.email.text.count(".") > 0
                            and self.password.text)

          def _show_error(self, message: str):
                    show_popup("Error", message)


def show_popup(title: str, content: str):
          popup = Popup(title=title,
                        content=BaseLabel(text=content),
                        size_hint=(None, None), size=POPUP_SIZE)
          popup.open()


class LoginWindow(Screen):
          email = ObjectProperty(None)
          password = ObjectProperty(None)

          def loginBtn(self):
                    if db.validate(self.email.text, self.password.text):
                              MainWindow.current = self.email.text
                              self.reset()
                              sm.current = "main"
                    else:
                              invalidLogin()

          def createBtn(self):
                    self.reset()
                    sm.current = "create"

          def reset(self):
                    self.email.text = ""
                    self.password.text = ""


class MainWindow(Screen):
          n = ObjectProperty(None)
          created = ObjectProperty(None)
          email = ObjectProperty(None)
          current = ""

          def logOut(self):
                    sm.current = "login"

          def on_enter(self, *args):
                    password, name, created = db.get_user(self.current)
                    self.n.text = "Account Name: " + name
                    self.email.text = "Email: " + self.current
                    self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
          pass


def invalidLogin():
          pop = Popup(title='Invalid Login',
                      content=Label(text='Invalid username or password.'),
                      size_hint=(None, None), size=(400, 400))
          pop.open()


def invalidForm():
          pop = Popup(title='Invalid Form',
                      content=Label(text='Please fill in all inputs with valid information.'),
                      size_hint=(None, None), size=(400, 400))

          pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main")]
for screen in screens:
          sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
          def build(self):
                    return sm


if __name__ == "__main__":
          MyMainApp().run()
