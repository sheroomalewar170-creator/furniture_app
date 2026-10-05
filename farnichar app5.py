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
            spacing=8
        )

        layout.add_widget(
            Label(
                text="MODERN FURNITURE DESIGNER",
                font_size=22
            )
        )

        layout.add_widget(Label(text="Width (inch)"))
        self.width = TextInput(text="36", multiline=False)
        layout.add_widget(self.width)

        layout.add_widget(Label(text="Height (inch)"))
        self.height = TextInput(text="72", multiline=False)
        layout.add_widget(self.height)

        layout.add_widget(Label(text="Depth (inch)"))
        self.depth = TextInput(text="24", multiline=False)
        layout.add_widget(self.depth)

        layout.add_widget(Label(text="Material Thickness"))

        self.material = Spinner(
            text="18 mm",
            values=("18 mm", "12 mm"),
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.material)

        button = Button(
            text="MAKE CUTTING LIST",
            size_hint_y=None,
            height=55
        )
        button.bind(on_press=self.make_cutting_list)
        layout.add_widget(button)

        self.result = Label(
            text="",
            halign="left"
        )
        layout.add_widget(self.result)

        return layout

    def make_cutting_list(self, instance):

        try:
            w = float(self.width.text)
            h = float(self.height.text)
            d = float(self.depth.text)

            material = self.material.text

            result = (
                "CUTTING LIST\n\n"
                f"Material: {material}\n\n"
                f"1. Side Left   = {h} x {d} inch\n"
                f"2. Side Right  = {h} x {d} inch\n"
                f"3. Top         = {w} x {d} inch\n"
                f"4. Bottom      = {w} x {d} inch\n"
                f"5. Back        = {w} x {h} inch\n"
            )

            self.result.text = result

        except:
            self.result.text = "Please enter numbers only."


FurnitureApp().run()