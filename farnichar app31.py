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
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.widget import Widget


FILE_NAME = "projects.json"


# ==============================
# 2D CABINET PREVIEW
# ==============================

class CabinetPreview(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.width_mm = 1800
        self.height_mm = 2100
        self.shelves = 5

        self.bind(
            pos=self.draw_cabinet,
            size=self.draw_cabinet
        )

    def update_preview(self, width, height, shelves):

        self.width_mm = width
        self.height_mm = height
        self.shelves = shelves

        self.draw_cabinet()

    def draw_cabinet(self, *args):

        self.canvas.clear()

        if self.width_mm <= 0 or self.height_mm <= 0:
            return

        with self.canvas:

            # Cabinet border

            Color(0.2, 0.2, 0.2)

            x = self.x + 20
            y = self.y + 20

            available_w = self.width - 40
            available_h = self.height - 40

            scale_x = available_w / self.width_mm
            scale_y = available_h / self.height_mm

            scale = min(
                scale_x,
                scale_y
            )

            cabinet_w = self.width_mm * scale
            cabinet_h = self.height_mm * scale

            x = self.center_x - cabinet_w / 2
            y = self.center_y - cabinet_h / 2

            # Outer rectangle

            Line(
                rectangle=(
                    x,
                    y,
                    cabinet_w,
                    cabinet_h
                ),
                width=2
            )

            # Shelves

            if self.shelves > 0:

                shelf_gap = (
                    cabinet_h /
                    (self.shelves + 1)
                )

                for i in range(
                    1,
                    self.shelves + 1
                ):

                    shelf_y = (
                        y +
                        shelf_gap * i
                    )

                    Line(
                        points=[
                            x,
                            shelf_y,
                            x + cabinet_w,
                            shelf_y
                        ],
                        width=1.5
                    )


# ==============================
# MAIN APP
# ==============================

class FurnitureApp(App):

    def build(self):

        self.projects = []
        self.edit_index = None

        if os.path.exists(FILE_NAME):

            try:

                with open(
                    FILE_NAME,
                    "r"
                ) as file:

                    self.projects = json.load(
                        file
                    )

            except:

                self.projects = []

        main = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=5
        )

        # ==========================
        # TITLE
        # ==========================

        main.add_widget(
            Label(
                text="MODERN FURNITURE SOFTWARE",
                font_size=21,
                size_hint_y=None,
                height=45
            )
        )

        # ==========================
        # DASHBOARD
        # ==========================

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

        main.add_widget(
            self.dashboard
        )

        # ==========================
        # CUSTOMER
        # ==========================

        main.add_widget(
            Label(
                text="Customer Name"
            )
        )

        self.customer = TextInput(
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.customer
        )

        main.add_widget(
            Label(
                text="Customer Mobile"
            )
        )

        self.mobile = TextInput(
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.mobile
        )

        main.add_widget(
            Label(
                text="Project Name"
            )
        )

        self.project = TextInput(
            text="Wardrobe",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.project
        )

        # ==========================
        # DIMENSIONS
        # ==========================

        main.add_widget(
            Label(
                text="Width (mm)"
            )
        )

        self.width = TextInput(
            text="1800",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.width
        )

        main.add_widget(
            Label(
                text="Height (mm)"
            )
        )

        self.height = TextInput(
            text="2100",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.height
        )

        main.add_widget(
            Label(
                text="Depth (mm)"
            )
        )

        self.depth = TextInput(
            text="600",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.depth
        )

        # ==========================
        # MATERIAL
        # ==========================

        main.add_widget(
            Label(
                text="Material Thickness"
            )
        )

        self.thickness = Spinner(
            text="18 mm",
            values=(
                "18 mm",
                "12 mm"
            ),
            size_hint_y=None,
            height=45
        )

        main.add_widget(
            self.thickness
        )

        # ==========================
        # SHELVES
        # ==========================

        main.add_widget(
            Label(
                text="Number of Shelves"
            )
        )

        self.shelves = TextInput(
            text="5",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.shelves
        )

        # ==========================
        # CUTTING LIST BUTTON
        # ==========================

        cutting_button = Button(
            text="GENERATE CUTTING LIST",
            size_hint_y=None,
            height=50
        )

        cutting_button.bind(
            on_press=self.generate_cutting_list
        )

        main.add_widget(
            cutting_button
        )

        # ==========================
        # CUTTING LIST OUTPUT
        # ==========================

        self.cutting_output = Label(
            text="CUTTING LIST WILL APPEAR HERE",
            halign="left",
            valign="top",
            size_hint_y=None,
            height=220,
            font_size=14
        )

        main.add_widget(
            self.cutting_output
        )

        # ==========================
        # 2D PREVIEW
        # ==========================

        main.add_widget(
            Label(
                text="2D CABINET PREVIEW",
                font_size=17,
                size_hint_y=None,
                height=35
            )
        )

        self.preview = CabinetPreview(
            size_hint_y=None,
            height=250
        )

        main.add_widget(
            self.preview
        )

        # ==========================
        # PRICE DETAILS
        # ==========================

        main.add_widget(
            Label(
                text="PRICE DETAILS",
                font_size=17,
                size_hint_y=None,
                height=35
            )
        )

        main.add_widget(
            Label(
                text="Material Cost (₹)"
            )
        )

        self.material_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.material_cost
        )

        main.add_widget(
            Label(
                text="Labour Cost (₹)"
            )
        )

        self.labour_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.labour_cost
        )

        main.add_widget(
            Label(
                text="Hardware Cost (₹)"
            )
        )

        self.hardware_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.hardware_cost
        )

        main.add_widget(
            Label(
                text="Advance Payment (₹)"
            )
        )

        self.advance = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        main.add_widget(
            self.advance
        )

        # ==========================
        # SAVE
        # ==========================

        self.save_button = Button(
            text="SAVE PROJECT",
            size_hint_y=None,
            height=50
        )

        self.save_button.bind(
            on_press=self.save_or_update
        )

        main.add_widget(
            self.save_button
        )

        # ==========================
        # CANCEL
        # ==========================

        self.cancel_button = Button(
            text="CANCEL EDIT",
            size_hint_y=None,
            height=45
        )

        self.cancel_button.bind(
            on_press=self.cancel_edit
        )

        self.cancel_button.disabled = True

        main.add_widget(
            self.cancel_button
        )

        # ==========================
        # PROJECT LIST
        # ==========================

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
            spacing=8,
            size_hint_y=None
        )

        self.project_list.bind(
            minimum_height=
            self.project_list.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.project_list
        )

        main.add_widget(
            scroll
        )

        self.refresh_dashboard()
        self.refresh_list()

        return main

    # ==============================
    # THICKNESS
    # ==============================

    def get_thickness(self):

        if self.thickness.text == "12 mm":
            return 12

        return 18

    # ==============================
    # CUTTING LIST
    # ==============================

    def generate_cutting_list(
        self,
        instance
    ):

        try:

            w = float(
                self.width.text
            )

            h = float(
                self.height.text
            )

            d = float(
                self.depth.text
            )

            t = self.get_thickness()

            shelves = int(
                self.shelves.text
            )

            top_width = w - (
                2 * t
            )

            shelf_width = w - (
                2 * t
            )

            shelf_depth = d - t

            text = (
                "===== CUTTING LIST =====\n\n"

                f"Material Thickness: "
                f"{t} mm\n\n"

                f"1. LEFT SIDE\n"
                f"   {h:.0f} x {d:.0f} mm\n\n"

                f"2. RIGHT SIDE\n"
                f"   {h:.0f} x {d:.0f} mm\n\n"

                f"3. TOP\n"
                f"   {top_width:.0f} x "
                f"{d:.0f} mm\n\n"

                f"4. BOTTOM\n"
                f"   {top_width:.0f} x "
                f"{d:.0f} mm\n\n"

                f"5. BACK\n"
                f"   {w:.0f} x "
                f"{h:.0f} mm\n\n"

                f"6. SHELVES\n"
                f"   QTY: {shelves}\n"
                f"   {shelf_width:.0f} x "
                f"{shelf_depth:.0f} mm"
            )

            self.cutting_output.text = text

            self.preview.update_preview(
                w,
                h,
                shelves
            )

        except:

            self.cutting_output.text = (
                "Please enter valid dimensions."
            )

    # ==============================
    # ESTIMATE NUMBER
    # ==============================

    def get_estimate_number(self):

        numbers = []

        for p in self.projects:

            estimate = p.get(
                "estimate_no",
                ""
            )

            if estimate.startswith(
                "EST-"
            ):

                try:

                    number = int(
                        estimate.replace(
                            "EST-",
                            ""
                        )
                    )

                    numbers.append(
                        number
                    )

                except:

                    pass

        if numbers:

            next_number = max(
                numbers
            ) + 1

        else:

            next_number = 1

        return f"EST-{next_number:03d}"

    # ==============================
    # SAVE / UPDATE
    # ==============================

    def save_or_update(
        self,
        instance
    ):

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

            remaining = (
                total - advance
            )

            if advance <= 0:

                status = "PENDING"

            elif advance < total:

                status = "PARTIAL"

            else:

                status = "PAID"
                remaining = 0

            if self.edit_index is None:

                estimate_no = (
                    self.get_estimate_number()
                )

                date = datetime.now().strftime(
                    "%d-%m-%Y"
                )

            else:

                old = self.projects[
                    self.edit_index
                ]

                estimate_no = old.get(
                    "estimate_no",
                    self.get_estimate_number()
                )

                date = old.get(
                    "date",
                    datetime.now().strftime(
                        "%d-%m-%Y"
                    )
                )

            data = {

                "estimate_no":
                    estimate_no,

                "customer":
                    self.customer.text,

                "mobile":
                    self.mobile.text,

                "project":
                    self.project.text,

                "width":
                    float(self.width.text),

                "height":
                    float(self.height.text),

                "depth":
                    float(self.depth.text),

                "thickness":
                    self.get_thickness(),

                "shelves":
                    int(self.shelves.text),

                "material_cost":
                    material,

                "labour_cost":
                    labour,

                "hardware_cost":
                    hardware,

                "total":
                    total,

                "advance":
                    advance,

                "remaining":
                    remaining,

                "status":
                    status,

                "date":
                    date
            }

            if self.edit_index is not None:

                self.projects[
                    self.edit_index
                ] = data

                self.edit_index = None

                self.save_button.text = (
                    "SAVE PROJECT"
                )

                self.cancel_button.disabled = True

            else:

                self.projects.append(
                    data
                )

            self.save_data()

            self.clear_fields()

            self.refresh_dashboard()
            self.refresh_list()

        except:

            self.dashboard.text = (
                "Please enter valid data."
            )

    # ==============================
    # EDIT
    # ==============================

    def edit_project(
        self,
        index
    ):

        try:

            p = self.projects[index]

            self.edit_index = index

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
                "Wardrobe"
            )

            self.width.text = str(
                p.get("width", 1800)
            )

            self.height.text = str(
                p.get("height", 2100)
            )

            self.depth.text = str(
                p.get("depth", 600)
            )

            thickness = p.get(
                "thickness",
                18
            )

            if thickness == 12:

                self.thickness.text = (
                    "12 mm"
                )

            else:

                self.thickness.text = (
                    "18 mm"
                )

            self.shelves.text = str(
                p.get("shelves", 5)
            )

            self.material_cost.text = str(
                p.get(
                    "material_cost",
                    0
                )
            )

            self.labour_cost.text = str(
                p.get(
                    "labour_cost",
                    0
                )
            )

            self.hardware_cost.text = str(
                p.get(
                    "hardware_cost",
                    0
                )
            )

            self.advance.text = str(
                p.get(
                    "advance",
                    0
                )
            )

            self.save_button.text = (
                "UPDATE PROJECT"
            )

            self.cancel_button.disable= False

            # Update preview

            self.generate_cutting_list(
                None
            )

        except:

            pass

    # ==============================
    # DELETE
    # ==============================

    def delete_project(
        self,
        index
    ):

        if 0 <= index < len(
            self.projects
        ):

            del self.projects[index]

            self.save_data()

            self.refresh_dashboard()
            self.refresh_list()

    # ==============================
    # CANCEL
    # ==============================

    def cancel_edit(
        self,
        instance
    ):

        self.edit_index = None

        self.save_button.text = (
            "SAVE PROJECT"
        )

        self.cancel_button.disabled = True

        self.clear_fields()

    # ==============================
    # CLEAR
    # ==============================

    def clear_fields(self):

        self.customer.text = ""
        self.mobile.text = ""
        self.project.text = "Wardrobe"

        self.width.text = "1800"
        self.height.text = "2100"
        self.depth.text = "600"

        self.thickness.text = "18 mm"

        self.shelves.text = "5"

        self.material_cost.text = "0"
        self.labour_cost.text = "0"
        self.hardware_cost.text = "0"
        self.advance.text = "0"

        self.cutting_output.text = (
            "CUTTING LIST WILL APPEAR HERE"
        )

        self.preview.update_preview(
            1800,
            2100,
            5
        )

    # ==============================
    # FILE SAVE
    # ==============================

    def save_data(self):

        with open(
            FILE_NAME,
            "w"
        ) as file:

            json.dump(
                self.projects,
                file,
                indent=4
            )

    # ==============================
    # DASHBOARD
    # ==============================

    def refresh_dashboard(self):

        total_projects = len(
            self.projects
        )

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

        self.dashboard.text = (

            f"Total Projects : "
            f"{total_projects}\n"

            f"Total Billing  : "
            f"₹{total_billing:.2f}\n"

            f"Total Advance  : "
            f"₹{total_advance:.2f}\n"

            f"Remaining      : "
            f"₹{total_remaining:.2f}\n\n"

            f"PAID: {paid}   "
            f"PARTIAL: {partial}   "
            f"PENDING: {pending}"
        )

    # ==============================
    # PROJECT LIST
    # ==============================

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

            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=190,
                spacing=3
            )

            info = Label(
                text=(

                    f"{p.get('estimate_no', '-')}"
                    f" | "
                    f"{p.get('project', '-')}\n"

                    f"Customer: "
                    f"{p.get('customer', '-')}\n"

                    f"Mobile: "
                    f"{p.get('mobile', '-')}\n"

                    f"Total: ₹"
                    f"{p.get('total', 0):.2f}\n"

                    f"Remaining: ₹"
                    f"{p.get('remaining', 0):.2f}\n"

                    f"Status: "
                    f"{p.get('status', '-')}\n"

                    f"Date: "
                    f"{p.get('date', '-')}"
                ),

                halign="left",
                valign="middle"
            )

            buttons = BoxLayout(
                size_hint_y=None,
                height=45,
                spacing=5
            )

            edit_button = Button(
                text="EDIT"
            )

            edit_button.bind(
                on_press=lambda btn,
                i=index:
                self.edit_project(i)
            )

            delete_button = Button(
                text="DELETE"
            )

            delete_button.bind(
                on_press=lambda btn,
                i=index:
                self.delete_project(i)
            )

            buttons.add_widget(
                edit_button
            )

            buttons.add_widget(
                delete_button
            )

            card.add_widget(
                info
            )

            card.add_widget(
                buttons
            )

            self.project_list.add_widget(
                card
            )


FurnitureApp().run()