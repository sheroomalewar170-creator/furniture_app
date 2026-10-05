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

        calculate = Button(
            text="CALCULATE ESTIMATE",
            size_hint_y=None,
            height=55
        )

        calculate.bind(
            on_press=self.calculate
        )

        layout.add_widget(calculate)

        pdf_button = Button(
            text="CREATE PDF ESTIMATE",
            size_hint_y=None,
            height=55
        )

        pdf_button.bind(
            on_press=self.create_pdf
        )

        layout.add_widget(pdf_button)

        self.result = Label(
            text=""
        )

        layout.add_widget(self.result)

        return layout

    def calculate(self, instance):

        try:

            material = float(self.material.text)
            labour = float(self.labour.text)
            hardware = float(self.hardware.text)

            self.total = material + labour + hardware

            self.result.text = (
                f"Material: ₹{material:.2f}\n"
                f"Labour: ₹{labour:.2f}\n"
                f"Hardware: ₹{hardware:.2f}\n\n"
                f"TOTAL: ₹{self.total:.2f}"
            )

        except:

            self.result.text = "Enter valid amounts."

    def create_pdf(self, instance):

        try:

            material = float(self.material.text)
            labour = float(self.labour.text)
            hardware = float(self.hardware.text)

            total = material + labour + hardware

            filename = "Furniture_Estimate.pdf"

            pdf = canvas.Canvas(filename)

            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawString(
                50,
                800,
                "FURNITURE ESTIMATE"
            )

            pdf.setFont("Helvetica", 12)

            pdf.drawString(
                50,
                760,
                "Customer: " + self.customer.text
            )

            pdf.drawString(
                50,
                740,
                "Project: " + self.project.text
            )

            pdf.drawString(
                50,
                700,
                "Date: " +
                datetime.now().strftime("%d-%m-%Y")
            )

            pdf.drawString(
                50,
                650,
                f"Material Cost: Rs. {material:.2f}"
            )

            pdf.drawString(
                50,
                625,
                f"Labour Cost: Rs. {labour:.2f}"
            )

            pdf.drawString(
                50,
                600,
                f"Hardware Cost: Rs. {hardware:.2f}"
            )

            pdf.setFont(
                "Helvetica-Bold",
                15
            )

            pdf.drawString(
                50,
                550,
                f"FINAL TOTAL: Rs. {total:.2f}"
            )

            pdf.save()

            self.result.text = (
                "PDF CREATED!\n"
                "Furniture_Estimate.pdf"
            )

        except Exception as e:

            self.result.text = (
                "PDF Error:\n" + str(e)
            )


FurnitureApp().run()