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

        calculate = Button(
            text="CALCULATE PAYMENT",
            size_hint_y=None,
            height=55
        )

        calculate.bind(
            on_press=self.calculate_payment
        )

        layout.add_widget(calculate)

        pdf_button = Button(
            text="CREATE PAYMENT PDF",
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

    def get_payment(self):

        material = float(self.material.text)
        labour = float(self.labour.text)
        hardware = float(self.hardware.text)
        advance = float(self.advance.text)

        total = material + labour + hardware

        if advance <= 0:
            status = "PENDING"
            remaining = total

        elif advance < total:
            status = "PARTIAL"
            remaining = total - advance

        else:
            status = "PAID"
            remaining = 0

        return (
            material,
            labour,
            hardware,
            total,
            advance,
            remaining,
            status
        )

    def calculate_payment(self, instance):

        try:

            (
                material,
                labour,
                hardware,
                total,
                advance,
                remaining,
                status
            ) = self.get_payment()

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

    def create_pdf(self, instance):

        try:

            (
                material,
                labour,
                hardware,
                total,
                advance,
                remaining,
                status
            ) = self.get_payment()

            filename = (
                self.estimate_no.text +
                "_Payment.pdf"
            )

            pdf = canvas.Canvas(filename)

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
                "Helvetica-Bold",
                16
            )

            pdf.drawString(
                50,
                760,
                "FURNITURE ESTIMATE"
            )

            pdf.setFont(
                "Helvetica",
                11
            )

            pdf.drawString(
                50,
                730,
                "Estimate No: " +
                self.estimate_no.text
            )

            pdf.drawString(
                50,
                710,
                "Date: " +
                datetime.now().strftime(
                    "%d-%m-%Y"
                )
            )

            pdf.drawString(
                50,
                680,
                "Customer: " +
                self.customer.text
            )

            pdf.drawString(
                50,
                660,
                "Project: " +
                self.project.text
            )

            pdf.drawString(
                50,
                610,
                f"Material: Rs. {material:.2f}"
            )

            pdf.drawString(
                50,
                585,
                f"Labour: Rs. {labour:.2f}"
            )

            pdf.drawString(
                50,
                560,
                f"Hardware: Rs. {hardware:.2f}"
            )

            pdf.setFont(
                "Helvetica-Bold",
                14
            )

            pdf.drawString(
                50,
                510,
                f"FINAL TOTAL: Rs. {total:.2f}"
            )

            pdf.drawString(
                50,
                480,
                f"ADVANCE: Rs. {advance:.2f}"
            )

            pdf.drawString(
                50,
                450,
                f"REMAINING: Rs. {remaining:.2f}"
            )

            pdf.drawString(
                50,
                420,
                "STATUS: " + status
            )

            pdf.save()

            self.result.text = (
                "PAYMENT PDF CREATED!\n\n" +
                filename
            )

        except Exception as e:

            self.result.text = (
                "PDF Error:\n" +
                str(e)
            )


FurnitureApp().run()