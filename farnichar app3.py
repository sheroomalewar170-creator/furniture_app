from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class FurnitureApp(App):

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        layout.add_widget(
            Label(
                text="MODERN FURNITURE DESIGNER",
                font_size=24
            )
        )

        layout.add_widget(Label(text="Width (inch)"))
        self.width = TextInput(
            text="36",
            multiline=False
        )
        layout.add_widget(self.width)

        layout.add_widget(Label(text="Height (inch)"))
        self.height = TextInput(
            text="72",
            multiline=False
        )
        layout.add_widget(self.height)

        layout.add_widget(Label(text="Depth (inch)"))
        self.depth = TextInput(
            text="24",
            multiline=False
        )
        layout.add_widget(self.depth)

        button = Button(
            text="CREATE FURNITURE",
            size_hint_y=None,
            height=60
        )
        button.bind(on_press=self.create_furniture)
        layout.add_widget(button)

        self.result = Label(text="")
        layout.add_widget(self.result)

        return layout

    def create_furniture(self, instance):
        w = self.width.text
        h = self.height.text
        d = self.depth.text

        self.result.text = (
            "Furniture Size\n"
            f"Width: {w} inch\n"
            f"Height: {h} inch\n"
            f"Depth: {d} inch"
        )


FurnitureApp().run()