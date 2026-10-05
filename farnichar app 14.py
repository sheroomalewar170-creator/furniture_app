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

        layout.add_widget(Label(text="Address"))

        self.address = TextInput(
            text="Maharashtra, India",
            multiline=False
        )
        layout.add_widget(self.address)

        layout.add_widget(Label(text="Company Mobile"))

        self.company_mobile = TextInput(
            text="",
            multiline=False,
            input_filter="int"
        )
        layout.add_widget(self.company_mobile)

        layout.add_widget(Label(text="Estimate Number"))

        self.estimate_no = TextInput(
            text="EST-001",
            multiline=False
        )
        layout.add_widget(self.estimate_no)

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

        pdf_button = Button(
            text="CREATE PDF ESTIMATE",
            size_hint_y=None,
            height=60
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

    def create_pdf(self, instance):

        try:

            material = float(self.material.text)
            labour = float(self.labour.text)
            hardware = float(self.hardware.text)

            total = material + labour + hardware

            filename = (
                self.estimate_no.text +
                "_Estimate.pdf"
            )

            pdf = canvas.Canvas(filename)

            # Company
            pdf.setFont(
                "Helvetica-Bold",
                20
            )

            pdf.drawString(
                50,
                800,
                self.company.text
            )

            pdf.setFont(
                "Helvetica",
                11
            )

            pdf.drawString(
                50,
                780,
                self.address.text
            )

            pdf.drawString(
                50,
                762,
                "Mobile: " +
                self.company_mobile.text
            )

            # Estimate
            pdf.setFont(
                "Helvetica-Bold",
                16
            )

            pdf.drawString(
                50,
                720,
                "FURNITURE ESTIMATE"
            )

            pdf.setFont(
                "Helvetica",
                11
            )

            pdf.drawString(
                50,
                695,
                "Estimate No: " +
                self.estimate_no.text
            )

            pdf.drawString(
                50,
                675,
                "Date: " +
                datetime.now().strftime(
                    "%d-%m-%Y"
                )
            )

            # Customer
            pdf.drawString(
                50,
                640,
                "Customer: " +
                self.customer.text
            )

            pdf.drawString(
                50,
                620,
                "Project: " +
                self.project.text
            )

            # Costs
            pdf.drawString(
                50,
                570,
                f"Material Cost: Rs. {material:.2f}"
            )

            pdf.drawString(
                50,
                545,
                f"Labour Cost: Rs. {labour:.2f}"
            )

            pdf.drawString(
                50,
                520,
                f"Hardware Cost: Rs. {hardware:.2f}"
            )

            pdf.setFont(
                "Helvetica-Bold",
                15
            )

            pdf.drawString(
                50,
                470,
                f"FINAL TOTAL: Rs. {total:.2f}"
            )

            pdf.save()

            self.result.text = (
                "PDF CREATED!\n\n" +
                filename
            )

        except Exception as e:

            self.result.text = (
                "PDF Error:\n" +
                str(e)
            )


FurnitureApp().run()