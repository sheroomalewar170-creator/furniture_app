import json
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from reportlab.pdfgen import canvas


FILE_NAME = "projects.json"


class FurnitureApp(App):

    def build(self):

        self.projects = self.load_projects()
        self.selected_index = None

        main = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=5
        )

        main.add_widget(
            Label(
                text="FURNITURE ESTIMATE",
                font_size=22,
                size_hint_y=None,
                height=45
            )
        )

        main.add_widget(Label(text="Company Name"))

        self.company = TextInput(
            text="My Furniture Company",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.company)

        main.add_widget(Label(text="Estimate Number"))

        self.estimate = TextInput(
            text="EST-001",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.estimate)

        main.add_widget(Label(text="Customer Name"))

        self.customer = TextInput(
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.customer)

        main.add_widget(Label(text="Mobile Number"))

        self.mobile = TextInput(
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.mobile)

        main.add_widget(Label(text="Project Name"))

        self.project = TextInput(
            text="Wardrobe",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.project)

        main.add_widget(Label(text="Final Total"))

        self.total = TextInput(
            text="18000",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.total)

        main.add_widget(Label(text="Advance Payment"))

        self.advance = TextInput(
            text="0",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.advance)

        self.payment_result = Label(
            text="Remaining: Rs. 18000\nStatus: PENDING",
            size_hint_y=None,
            height=50
        )

        main.add_widget(self.payment_result)

        calculate = Button(
            text="CALCULATE PAYMENT",
            size_hint_y=None,
            height=45
        )

        calculate.bind(
            on_press=self.calculate_payment
        )

        main.add_widget(calculate)

        pdf_button = Button(
            text="CREATE ESTIMATE PDF",
            size_hint_y=None,
            height=50
        )

        pdf_button.bind(
            on_press=self.create_pdf
        )

        main.add_widget(pdf_button)

        buttons = BoxLayout(
            size_hint_y=None,
            height=48,
            spacing=5
        )

        save = Button(text="SAVE")
        save.bind(on_press=self.save_project)

        update = Button(text="UPDATE")
        update.bind(on_press=self.update_project)

        delete = Button(text="DELETE")
        delete.bind(on_press=self.delete_project)

        buttons.add_widget(save)
        buttons.add_widget(update)
        buttons.add_widget(delete)

        main.add_widget(buttons)

        scroll = ScrollView()

        self.project_list = BoxLayout(
            orientation="vertical",
            spacing=5,
            size_hint_y=None
        )

        self.project_list.bind(
            minimum_height=self.project_list.setter("height")
        )

        scroll.add_widget(self.project_list)

        main.add_widget(scroll)

        self.refresh_list()

        return main

    def load_projects(self):

        if os.path.exists(FILE_NAME):

            try:

                with open(FILE_NAME, "r") as file:
                    return json.load(file)

            except:

                return []

        return []

    def save_data(self):

        with open(FILE_NAME, "w") as file:

            json.dump(
                self.projects,
                file,
                indent=4
            )

    def get_payment(self):

        total = float(self.total.text)
        advance = float(self.advance.text)

        if advance < 0:
            advance = 0

        if advance >= total:

            remaining = 0
            status = "PAID"

        elif advance > 0:

            remaining = total - advance
            status = "PARTIAL"

        else:

            remaining = total
            status = "PENDING"

        return total, advance, remaining, status

    def calculate_payment(self, instance):

        try:

            total, advance, remaining, status = \
                self.get_payment()

            self.payment_result.text = (
                f"Remaining: Rs. {remaining:.2f}\n"
                f"Status: {status}"
            )

        except:

            self.payment_result.text = \
                "INVALID PAYMENT DATA"

    def get_data(self):

        total, advance, remaining, status = \
            self.get_payment()

        return {
            "company": self.company.text,
            "estimate": self.estimate.text,
            "customer": self.customer.text,
            "mobile": self.mobile.text,
            "project": self.project.text,
            "total": total,
            "advance": advance,
            "remaining": remaining,
            "status": status,
            "date": datetime.now().strftime("%d-%m-%Y")
        }

    def save_project(self, instance):

        try:

            data = self.get_data()

            self.projects.append(data)

            self.save_data()

            self.clear_fields()
            self.refresh_list()

        except:

            self.payment_result.text = \
                "INVALID DATA"

    def create_pdf(self, instance):

        try:

            total, advance, remaining, status = \
                self.get_payment()

            estimate_no = self.estimate.text.strip()

            if estimate_no == "":
                estimate_no = "ESTIMATE"

            filename = estimate_no + "_Estimate.pdf"

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
                765,
                "FURNITURE ESTIMATE"
            )

            pdf.setFont(
                "Helvetica",
                11
            )

            pdf.drawString(
                50,
                735,
                "Estimate No: "
                + estimate_no
            )

            pdf.drawString(
                50,
                715,
                "Date: "
                + datetime.now().strftime(
                    "%d-%m-%Y"
                )
            )

            pdf.drawString(
                50,
                680,
                "Customer: "
                + self.customer.text
            )

            pdf.drawString(
                50,
                660,
                "Mobile: "
                + self.mobile.text
            )

            pdf.drawString(
                50,
                640,
                "Project: "
                + self.project.text
            )

            pdf.line(
                50,
                620,
                550,
                620
            )

            pdf.setFont(
                "Helvetica-Bold",
                13
            )

            pdf.drawString(
                50,
                580,
                "PAYMENT DETAILS"
            )

            pdf.setFont(
                "Helvetica",
                12
            )

            pdf.drawString(
                50,
                550,
                f"Final Total: Rs. {total:.2f}"
            )

            pdf.drawString(
                50,
                520,
                f"Advance: Rs. {advance:.2f}"
            )

            pdf.drawString(
                50,
                490,
                f"Remaining: Rs. {remaining:.2f}"
            )

            pdf.setFont(
                "Helvetica-Bold",
                13
            )

            pdf.drawString(
                50,
                450,
                "STATUS: " + status
            )

            pdf.line(
                50,
                420,
                550,
                420
            )

            pdf.setFont(
                "Helvetica",
                10
            )

            pdf.drawString(
                50,
                390,
                "Thank you for your business."
            )

            pdf.save()

            self.payment_result.text = (
                "PDF CREATED!\n"
                + filename
            )

        except Exception as e:

            self.payment_result.text = (
                "PDF ERROR:\n"
                + str(e)
            )

    def refresh_list(self):

        self.project_list.clear_widgets()

        if not self.projects:

            self.project_list.add_widget(
                Label(
                    text="No projects found.",
                    size_hint_y=None,
                    height=50
                )
            )

            return

        for index, p in enumerate(
            self.projects
        ):

            text = (
                f"{index + 1}. "
                f"{p.get('estimate', '-')}\n"
                f"Customer: "
                f"{p.get('customer', '-')}\n"
                f"Project: "
                f"{p.get('project', '-')}\n"
                f"Total: Rs. "
                f"{p.get('total', 0):.2f}\n"
                f"Advance: Rs. "
                f"{p.get('advance', 0):.2f}\n"
                f"Remaining: Rs. "
                f"{p.get('remaining', 0):.2f}\n"
                f"Status: "
                f"{p.get('status', '-')}"
            )

            button = Button(
                text=text,
                size_hint_y=None,
                height=165
            )

            button.bind(
                on_press=lambda btn, i=index:
                self.select_project(i)
            )

            self.project_list.add_widget(
                button
            )

    def select_project(self, index):

        self.selected_index = index

        p = self.projects[index]

        self.company.text = p.get(
            "company",
            "My Furniture Company"
        )

        self.estimate.text = p.get(
            "estimate",
            ""
        )

        self.customer.text = p.get(
            "customer",
            ""
        )

        self.mobile.text = p.get(
            "mobile",
            ""
        )

        self.project.text = p.get(
            "project",
            ""
        )

        self.total.text = str(
            p.get("total", 0)
        )

        self.advance.text = str(
            p.get("advance", 0)
        )

        self.payment_result.text = (
            f"Remaining: Rs. "
            f"{p.get('remaining', 0):.2f}\n"
            f"Status: "
            f"{p.get('status', 'PENDING')}"
        )

    def update_project(self, instance):

        if self.selected_index is None:

            self.payment_result.text = \
                "SELECT PROJECT FIRST"

            return

        try:

            self.projects[
                self.selected_index
            ] = self.get_data()

            self.save_data()
            self.refresh_list()

        except:

            self.payment_result.text = \
                "INVALID DATA"

    def delete_project(self, instance):

        if self.selected_index is None:

            self.payment_result.text = \
                "SELECT PROJECT FIRST"

            return

        del self.projects[
            self.selected_index
        ]

        self.save_data()

        self.selected_index = None

        self.clear_fields()
        self.refresh_list()

    def clear_fields(self):

        self.company.text = \
            "My Furniture Company"

        self.estimate.text = "EST-001"
        self.customer.text = ""
        self.mobile.text = ""
        self.project.text = "Wardrobe"
        self.total.text = "18000"
        self.advance.text = "0"

        self.payment_result.text = (
            "Remaining: Rs. 18000\n"
            "Status: PENDING"
        )


FurnitureApp().run()