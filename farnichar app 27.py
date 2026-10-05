import json
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView

from reportlab.pdfgen import canvas


FILE_NAME = "projects.json"


class FurnitureApp(App):

    def build(self):

        self.projects = []
        self.last_cutting_list = ""

        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r") as file:
                    self.projects = json.load(file)
            except:
                self.projects = []

        main = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=5
        )

        main.add_widget(
            Label(
                text="MODERN FURNITURE SOFTWARE",
                font_size=21,
                size_hint_y=None,
                height=45
            )
        )

        main.add_widget(Label(text="Width (mm)"))

        self.width = TextInput(
            text="1800",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.width)

        main.add_widget(Label(text="Height (mm)"))

        self.height = TextInput(
            text="2100",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.height)

        main.add_widget(Label(text="Depth (mm)"))

        self.depth = TextInput(
            text="600",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.depth)

        main.add_widget(Label(text="Material Thickness"))

        self.thickness = Spinner(
            text="18 mm",
            values=("18 mm", "12 mm"),
            size_hint_y=None,
            height=45
        )
        main.add_widget(self.thickness)

        main.add_widget(Label(text="Number of Shelves"))

        self.shelves = TextInput(
            text="5",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.shelves)

        main.add_widget(Label(text="Customer Name"))

        self.customer = TextInput(
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.customer)

        main.add_widget(Label(text="Project Name"))

        self.project = TextInput(
            text="Wardrobe",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.project)

        cutting_button = Button(
            text="CREATE CUTTING LIST",
            size_hint_y=None,
            height=50
        )

        cutting_button.bind(
            on_press=self.create_cutting_list
        )

        main.add_widget(cutting_button)

        self.cutting_result = Label(
            text="",
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.cutting_result.bind(
            texture_size=self.cutting_result.setter("size")
        )

        cutting_scroll = ScrollView(
            size_hint_y=None,
            height=180
        )

        cutting_scroll.add_widget(
            self.cutting_result
        )

        main.add_widget(cutting_scroll)

        main.add_widget(
            Label(
                text="ESTIMATE / PRICE",
                font_size=18,
                size_hint_y=None,
                height=35
            )
        )

        main.add_widget(Label(text="Material Cost (₹)"))

        self.material_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.material_cost)

        main.add_widget(Label(text="Labour Cost (₹)"))

        self.labour_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.labour_cost)

        main.add_widget(Label(text="Hardware Cost (₹)"))

        self.hardware_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.hardware_cost)

        main.add_widget(Label(text="Advance Payment (₹)"))

        self.advance = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        main.add_widget(self.advance)

        estimate_button = Button(
            text="CALCULATE ESTIMATE",
            size_hint_y=None,
            height=50
        )

        estimate_button.bind(
            on_press=self.calculate_estimate
        )

        main.add_widget(estimate_button)

        self.estimate_result = Label(
            text="",
            halign="left",
            valign="top",
            size_hint_y=None,
            font_size=16
        )

        self.estimate_result.bind(
            texture_size=self.estimate_result.setter("size")
        )

        estimate_scroll = ScrollView(
            size_hint_y=None,
            height=150
        )

        estimate_scroll.add_widget(
            self.estimate_result
        )

        main.add_widget(estimate_scroll)

        pdf_button = Button(
            text="SAVE ESTIMATE PDF",
            size_hint_y=None,
            height=50
        )

        pdf_button.bind(
            on_press=self.save_estimate_pdf
        )

        main.add_widget(pdf_button)

        save_button = Button(
            text="SAVE PROJECT",
            size_hint_y=None,
            height=50
        )

        save_button.bind(
            on_press=self.save_project
        )

        main.add_widget(save_button)

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

    def get_thickness(self):

        if self.thickness.text == "12 mm":
            return 12

        return 18

    def create_cutting_list(self, instance):

        try:

            w = float(self.width.text)
            h = float(self.height.text)
            d = float(self.depth.text)

            t = self.get_thickness()
            shelves = int(self.shelves.text)

            top_width = w - (2 * t)
            shelf_width = w - (2 * t)
            shelf_depth = d - t

            text = (
                "CUTTING LIST\n\n"
                f"Customer: {self.customer.text}\n"
                f"Project: {self.project.text}\n\n"
                f"Material: {t} mm\n\n"

                "1. SIDE LEFT\n"
                "Qty: 1\n"
                f"Size: {h:.0f} x {d:.0f} mm\n\n"

                "2. SIDE RIGHT\n"
                "Qty: 1\n"
                f"Size: {h:.0f} x {d:.0f} mm\n\n"

                "3. TOP\n"
                "Qty: 1\n"
                f"Size: {top_width:.0f} x {d:.0f} mm\n\n"

                "4. BOTTOM\n"
                "Qty: 1\n"
                f"Size: {top_width:.0f} x {d:.0f} mm\n\n"

                "5. BACK\n"
                "Qty: 1\n"
                f"Size: {w:.0f} x {h:.0f} mm\n\n"

                "6. SHELVES\n"
                f"Qty: {shelves}\n"
                f"Size: {shelf_width:.0f} x "
                f"{shelf_depth:.0f} mm"
            )

            self.last_cutting_list = text
            self.cutting_result.text = text

        except:

            self.cutting_result.text = (
                "Please enter valid dimensions."
            )

    def calculate_estimate(self, instance):

        try:

            material = float(self.material_cost.text)
            labour = float(self.labour_cost.text)
            hardware = float(self.hardware_cost.text)
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

            result = (
                "ESTIMATE\n\n"
                f"Material Cost: ₹{material:.2f}\n"
                f"Labour Cost: ₹{labour:.2f}\n"
                f"Hardware Cost: ₹{hardware:.2f}\n"
                "----------------------\n"
                f"TOTAL: ₹{total:.2f}\n\n"
                f"Advance: ₹{advance:.2f}\n"
                f"Remaining: ₹{remaining:.2f}\n"
                f"STATUS: {status}"
            )

            self.estimate_result.text = result

        except:

            self.estimate_result.text = (
                "Please enter valid price values."
            )

    def save_estimate_pdf(self, instance):

        try:

            material = float(self.material_cost.text)
            labour = float(self.labour_cost.text)
            hardware = float(self.hardware_cost.text)
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

            folder = "Estimate_PDF"

            if not os.path.exists(folder):
                os.makedirs(folder)

            project_name = self.project.text.strip()

            if not project_name:
                project_name = "Furniture_Project"

            project_name = (
                project_name
                .replace("/", "_")
                .replace("\\", "_")
                .replace(" ", "_")
            )

            filename = os.path.join(
                folder,
                project_name + "_Estimate.pdf"
            )

            pdf = canvas.Canvas(filename)

            pdf.setFont(
                "Helvetica-Bold",
                18
            )

            pdf.drawString(
                50,
                800,
                "FURNITURE ESTIMATE"
            )

            pdf.setFont(
                "Helvetica",
                11
            )

            y = 770

            lines = [
                f"Customer: {self.customer.text}",
                f"Project: {self.project.text}",
                f"Date: {datetime.now().strftime('%d-%m-%Y')}",
                "",
                f"Material Cost: Rs. {material:.2f}",
                f"Labour Cost: Rs. {labour:.2f}",
                f"Hardware Cost: Rs. {hardware:.2f}",
                "",
                f"TOTAL: Rs. {total:.2f}",
                f"Advance: Rs. {advance:.2f}",
                f"Remaining: Rs. {remaining:.2f}",
                f"STATUS: {status}"
            ]

            for line in lines:

                pdf.drawString(
                    50,
                    y,
                    line
                )

                y -= 22

            pdf.save()

            self.estimate_result.text = (
                "ESTIMATE PDF SAVED!\n\n"
                + filename
            )

        except Exception as e:

            self.estimate_result.text = (
                "PDF ERROR:\n"
                + str(e)
            )

    def save_project(self, instance):

        try:

            material = float(self.material_cost.text)
            labour = float(self.labour_cost.text)
            hardware = float(self.hardware_cost.text)
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

            data = {
                "customer": self.customer.text,
                "project": self.project.text,
                "width": float(self.width.text),
                "height": float(self.height.text),
                "depth": float(self.depth.text),
                "thickness": self.get_thickness(),
                "shelves": int(self.shelves.text),

                "material_cost": material,
                "labour_cost": labour,
                "hardware_cost": hardware,
                "total": total,
                "advance": advance,
                "remaining": remaining,
                "status": status,

                "date": datetime.now().strftime(
                    "%d-%m-%Y"
                )
            }

            self.projects.append(data)

            with open(FILE_NAME, "w") as file:

                json.dump(
                    self.projects,
                    file,
                    indent=4
                )

            self.refresh_list()

        except:

            self.estimate_result.text = (
                "Please enter valid data."
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
                f"{p.get('project', '-')}\n"
                f"Customer: "
                f"{p.get('customer', '-')}\n"
                f"Total: ₹"
                f"{p.get('total', 0):.2f}\n"
                f"Advance: ₹"
                f"{p.get('advance', 0):.2f}\n"
                f"Remaining: ₹"
                f"{p.get('remaining', 0):.2f}\n"
                f"Status: "
                f"{p.get('status', '-')}"
            )

            self.project_list.add_widget(
                Button(
                    text=text,
                    size_hint_y=None,
                    height=145
                )
            )


FurnitureApp().run()