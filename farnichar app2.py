from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner


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
            hint_text="Example: 36",
            multiline=False
        )
        layout.add_widget(self.width)

        layout.add_widget(Label(text="Height (inch)"))

        self.height = TextInput(
            hint_text="Example: 72",
            multiline=False
        )
        layout.add_widget(self.height)

        layout.add_widget(Label(text="Depth (inch)"))

        self.depth = TextInput(
            hint_text="Example: 18",
            multiline=False
        )
        layout.add_widget(self.depth)

        layout.add_widget(Label(text="Material Thickness"))

        self.material = Spinner(
            text="18 mm",
            values=("18 mm", "12 mm")
        )
        layout.add_widget(self.material)

        button = Button(
            text="CALCULATE",
            font_size=20
        )
        button.bind(on_press=self.calculate)
        layout.add_widget(button)

        self.result = Label(
            text="Result yahan aayega"
        )
        layout.add_widget(self.result)

        return layout

    def calculate(self, instance):

        self.result.text = (
            "Width: " + self.width.text + " inch\n"
            "Height: " + self.height.text + " inch\n"
            "Depth: " + self.depth.text + " inch\n"
            "Material: " + self.material.text
        )


FurnitureApp().run()