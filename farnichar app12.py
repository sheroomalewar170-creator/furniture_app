import json

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
            spacing=8
        )

        layout.add_widget(
            Label(
                text="FURNITURE ESTIMATE",
                font_size=22
            )
        )

        layout.add_widget(Label(text="Customer Name"))
        self.customer = TextInput(multiline=False)
        layout.add_widget(self.customer)

        layout.add_widget(Label(text="Project Name"))
        self.project = TextInput(
            text="Wardrobe",
            multiline=False
        )
        layout.add_widget(self.project)

        layout.add_widget(Label(text="Material Cost (₹)"))
        self.material = TextInput(
            text="10000",
            multiline=False,
            input_filter="float"
        )
        layout.add_widget(self.material)

        layout.add_widget(Label(text="Labour Cost (₹)"))
        self.labour = TextInput(
            text="5000",
            multiline=False,
            input_filter="float"
        )
        layout.add_widget(self.labour)

        layout.add_widget(Label(text="Hardware Cost (₹)"))
        self.hardware = TextInput(
            text="3000",
            multiline=False,
            input_filter="float"
        )
        layout.add_widget(self.hardware)

        button = Button(
            text="CALCULATE ESTIMATE",
            size_hint_y=None,
            height=60
        )

        button.bind(
            on_press=self.calculate
        )

        layout.add_widget(button)

        self.result = Label(
            text="",
            font_size=18
        )

        layout.add_widget(self.result)

        save_button = Button(
            text="SAVE ESTIMATE",
            size_hint_y=None,
            height=55
        )

        save_button.bind(
            on_press=self.save_estimate
        )

        layout.add_widget(save_button)

        return layout

    def calculate(self, instance):

        try:

            material = float(self.material.text)
            labour = float(self.labour.text)
            hardware = float(self.hardware.text)

            total = material + labour + hardware

            self.total = total

            self.result.text = (
                "ESTIMATE\n\n"
                f"Material: ₹{material:.2f}\n"
                f"Labour: ₹{labour:.2f}\n"
                f"Hardware: ₹{hardware:.2f}\n\n"
                f"TOTAL: ₹{total:.2f}"
            )

        except:

            self.result.text = "Please enter valid amounts."

    def save_estimate(self, instance):

        try:

            data = {
                "customer": self.customer.text,
                "project": self.project.text,
                "material": self.material.text,
                "labour": self.labour.text,
                "hardware": self.hardware.text,
                "total": self.total
            }

            with open(
                "estimate.json",
                "w"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

            self.result.text += "\n\nEstimate Saved!"

        except:

            self.result.text = (
                "First calculate the estimate."
            )


FurnitureApp().run()