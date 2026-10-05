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

        # ---------------- DASHBOARD ----------------

        main.add_widget(
            Label(
                text="PROJECT DASHBOARD",
                font_size=18,
                size_hint_y=None,
                height=35
            )
        )

        self.dashboard = Label(
            text="",
            halign="left",
            valign="top",
            size_hint_y=None,
            height=120,
            font_size=15
        )

        main.add_widget(self.dashboard)

        # ---------------- DIMENSIONS ----------------

        main.add_widget(
            Label(text="Width (mm)")
        )

        self.width = TextInput(
            text="1800",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.width)

        main.add_widget(
            Label(text="Height (mm)")
        )

        self.height = TextInput(
            text="2100",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.height)

        main.add_widget(
            Label(text="Depth (mm)")
        )

        self.depth = TextInput(
            text="600",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.depth)

        main.add_widget(
            Label(text="Material Thickness")
        )

        self.thickness = Spinner(
            text="18 mm",
            values=("18 mm", "12 mm"),
            size_hint_y=None,
            height=45
        )

        main.add_widget(self.thickness)

        main.add_widget(
            Label(text="Number of Shelves")
        )

        self.shelves = TextInput(
            text="5",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.shelves)

        # ---------------- CUSTOMER ----------------

        main.add_widget(
            Label(text="Customer Name")
        )

        self.customer = TextInput(
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.customer)

        main.add_widget(
            Label(text="Project Name")
        )

        self.project = TextInput(
            text="Wardrobe",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.project)

        # ---------------- PRICE ----------------

        main.add_widget(
            Label(
                text="PRICE DETAILS",
                font_size=17,
                size_hint_y=None,
                height=35
            )
        )

        main.add_widget(
            Label(text="Material Cost (₹)")
        )

        self.material_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.material_cost)

        main.add_widget(
            Label(text="Labour Cost (₹)")
        )

        self.labour_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.labour_cost)

        main.add_widget(
            Label(text="Hardware Cost (₹)")
        )

        self.hardware_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.hardware_cost)

        main.add_widget(
            Label(text="Advance Payment (₹)")
        )

        self.advance = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(self.advance)

        # ---------------- BUTTONS ----------------

        calculate_button = Button(
            text="CALCULATE & SAVE PROJECT",
            size_hint_y=None,
            height=50
        )

        calculate_button.bind(
            on_press=self.save_project
        )

        main.add_widget(calculate_button)

        # ---------------- PROJECT LIST ----------------

        main.add_widget(
            Label(
                text="ALL PROJECTS",
                font_size=17,
                size_hint_y=None,
                height=35
            )
        )

        scroll = ScrollView()

        self.project_list = BoxLayout(
            orientation="vertical",
            spacing=5,
            size_hint_y=None
        )

        self.project_list.bind(
            minimum_height=
            self.project_list.setter("height")
        )

        scroll.add_widget(
            self.project_list
        )

        main.add_widget(scroll)

        self.refresh_dashboard()
        self.refresh_list()

        return main

    # ---------------- DASHBOARD ----------------

    def refresh_dashboard(self):

        total_projects = len(self.projects)

        total_billing = 0
        total_advance = 0
        total_remaining = 0

        paid = 0
        partial = 0
        pending = 0

        for p in self.projects:

            total_billing += float(
                p.get("total", 0)
            )

            total_advance += float(
                p.get("advance", 0)
            )

            total_remaining += float(
                p.get("remaining", 0)
            )

            status = p.get(
                "status",
                "PENDING"
            )

            if status == "PAID":
                paid += 1

            elif status == "PARTIAL":
                partial += 1

            else:
                pending += 1

        text = (
            f"Total Projects : {total_projects}\n"
            f"Total Billing  : ₹{total_billing:.2f}\n"
            f"Total Advance  : ₹{total_advance:.2f}\n"
            f"Remaining      : ₹{total_remaining:.2f}\n\n"
            f"PAID: {paid}   "
            f"PARTIAL: {partial}   "
            f"PENDING: {pending}"
        )

        self.dashboard.text = text

    # ---------------- SAVE PROJECT ----------------

    def save_project(self, instance):

        try:

            material = float(
                self.material_cost.text
            )

            labour = float(
                self.labour_cost.text
            )

            hardware = float(
                self.hardware_cost.text
            )

            advance = float(
                self.advance.text
            )

            total = (
                material +
                labour +
                hardware
            )

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

                "width": float(
                    self.width.text
                ),

                "height": float(
                    self.height.text
                ),

                "depth": float(
                    self.depth.text
                ),

                "thickness":
                    self.get_thickness(),

                "shelves": int(
                    self.shelves.text
                ),

                "material_cost": material,

                "labour_cost": labour,

                "hardware_cost": hardware,

                "total": total,

                "advance": advance,

                "remaining": remaining,

                "status": status,

                "date":
                    datetime.now().strftime(
                        "%d-%m-%Y"
                    )
            }

            self.projects.append(data)

            with open(
                FILE_NAME,
                "w"
            ) as file:

                json.dump(
                    self.projects,
                    file,
                    indent=4
                )

            self.refresh_dashboard()
            self.refresh_list()

        except:

            self.dashboard.text = (
                "Please enter valid data."
            )

    # ---------------- MATERIAL ----------------

    def get_thickness(self):

        if self.thickness.text == "12 mm":

            return 12

        return 18

    # ---------------- PROJECT LIST ----------------

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
                f"{p.get('status', '-')}\n"

                f"Date: "
                f"{p.get('date', '-')}"
            )

            self.project_list.add_widget(
                Label(
                    text=text,
                    halign="left",
                    valign="top",
                    size_hint_y=None,
                    height=130
                )
            )


FurnitureApp().run()