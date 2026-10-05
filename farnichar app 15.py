from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from reportlab.pdfgen import canvas
from datetime import datetime


class FurnitureApp(App):

    def build(self):

        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=6
        )

        layout.add_widget(
            Label(
                text="FURNITURE ESTIMATE",
                font_size=22
            )
        )

        layout.add_widget(Label(text="Company Name"))
        self.company = TextInput(
            text="My Furniture Company",
            multiline=False
        )
        layout.add_widget(self.company)

        layout.add_widget(Label(text="Customer Name"))
        self.customer = TextInput(
            multiline=False
        )
        layout.add_widget(self.customer)

        layout.add_widget(Label(text="Project Name"))
        self.project = TextInput(
            text="Wardrobe",
            multiline=False
        )
        layout.add_widget(self.project)

        layout.add_widget(Label(text="Estimate Number"))
        self.estimate_no = TextInput(
            text="EST-001",
            multiline=False
        )
        layout.add_widget(self.estimate_no)

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

        layout.add_widget(Label(text="Advance Payment (₹)"))
        self.advance = TextInput(
            text="5000",
            multiline=False,
            input_filter="float"
        )
        layout.add_widget(self.advance)

        button = Button(
            text="CALCULATE PAYMENT",
            size_hint_y=None,
            height=55
        )

        button.bind(
            on_press=self.calculate_payment
        )

        layout.add_widget(button)

        self.result = Label(
            text=""
        )

        layout.add_widget(self.result)

        return layout

    def calculate_payment(self, instance):

        try:

            material = float(self.material.text)
            labour = float(self.labour.text)
            hardware = float(self.hardware.text)
            advance = float(self.advance.text)

            total = material + labour + hardware

            remaining = total - advance

            if advance <= 0:
                status = "PENDING"

            elif advance < total:
                status = "PARTIAL"

            else:
                status = "PAID"
                remaining = 0

            self.result.text = (
                "PAYMENT SUMMARY\n\n"
                f"Final Total: ₹{total:.2f}\n"
                f"Advance: ₹{advance:.2f}\n"
                f"Remaining: ₹{remaining:.2f}\n\n"
                f"Status: {status}"
            )

        except:

            self.result.text = (
                "Please enter valid amounts."
            )


FurnitureApp().run()