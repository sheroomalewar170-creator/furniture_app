import json
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget


DATA_FILE = "projects.json"


class CabinetPreview(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width_mm = 1800
        self.height_mm = 2100
        self.shelves = 5

        self.bind(pos=self.draw_cabinet, size=self.draw_cabinet)

    def update(self, width_mm, height_mm, shelves):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.shelves = shelves
        self.draw_cabinet()

    def draw_cabinet(self, *args):
        self.canvas.clear()

        with self.canvas:
            Color(1, 1, 1, 1)

            x = self.x + 30
            y = self.y + 20
            w = self.width - 60
            h = self.height - 40

            if h <= 0 or w <= 0:
                return

            Line(
                rectangle=(x, y, w, h),
                width=2
            )

            if self.shelves > 0:
                shelf_gap = h / (self.shelves + 1)

                for i in range(1, self.shelves + 1):
                    sy = y + shelf_gap * i

                    Line(
                        points=[x, sy, x + w, sy],
                        width=1
                    )


class FurnitureApp(App):

    def build(self):

        self.projects = []
        self.edit_index = None

        self.load_projects()

        root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        title = Label(
            text="MODERN FURNITURE SOFTWARE",
            font_size=22,
            size_hint_y=None,
            height=45
        )

        root.add_widget(title)

        scroll = ScrollView()

        form = GridLayout(
            cols=2,
            spacing=6,
            size_hint_y=None
        )

        form.bind(
            minimum_height=form.setter("height")
        )

        # Customer
        form.add_widget(Label(text="Customer Name"))

        self.customer = TextInput(
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.customer)

        # Mobile
        form.add_widget(Label(text="Mobile"))

        self.mobile = TextInput(
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.mobile)

        # Project
        form.add_widget(Label(text="Project Name"))

        self.project = TextInput(
            text="Wardrobe",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.project)

        # Width
        form.add_widget(Label(text="Width (mm)"))

        self.width = TextInput(
            text="1800",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.width)

        # Height
        form.add_widget(Label(text="Height (mm)"))

        self.height = TextInput(
            text="2100",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.height)

        # Depth
        form.add_widget(Label(text="Depth (mm)"))

        self.depth = TextInput(
            text="600",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.depth)

        # Thickness
        form.add_widget(Label(text="Material Thickness"))

        self.thickness = Spinner(
            text="18 mm",
            values=("18 mm", "12 mm"),
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.thickness)

        # Shelves
        form.add_widget(Label(text="Number of Shelves"))

        self.shelves = TextInput(
            text="5",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.shelves)

        # Doors
        form.add_widget(Label(text="Number of Doors"))

        self.doors = TextInput(
            text="2",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.doors)

        # DRAWERS - STEP 32
        form.add_widget(Label(text="Number of Drawers"))

        self.drawers = TextInput(
            text="0",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.drawers)

        # Material Cost
        form.add_widget(Label(text="Material Cost"))

        self.material_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.material_cost)

        # Labour
        form.add_widget(Label(text="Labour Cost"))

        self.labour_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.labour_cost)

        # Hardware
        form.add_widget(Label(text="Hardware Cost"))

        self.hardware_cost = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.hardware_cost)

        # Advance
        form.add_widget(Label(text="Advance"))

        self.advance = TextInput(
            text="0",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
        )

        form.add_widget(self.advance)

        scroll.add_widget(form)
        root.add_widget(scroll)

        # Buttons
        button_box = BoxLayout(
            size_hint_y=None,
            height=45,
            spacing=5
        )

        save_btn = Button(
            text="SAVE / UPDATE"
        )

        save_btn.bind(
            on_press=self.save_or_update
        )

        clear_btn = Button(
            text="CLEAR"
        )

        clear_btn.bind(
            on_press=self.clear_fields
        )

        list_btn = Button(
            text="PROJECT LIST"
        )

        list_btn.bind(
            on_press=self.show_projects
        )

        button_box.add_widget(save_btn)
        button_box.add_widget(clear_btn)
        button_box.add_widget(list_btn)

        root.add_widget(button_box)

        # Cutting List
        cut_btn = Button(
            text="GENERATE CUTTING LIST",
            size_hint_y=None,
            height=45
        )

        cut_btn.bind(
            on_press=self.generate_cutting_list
        )

        root.add_widget(cut_btn)

        self.output = Label(
            text="",
            size_hint_y=None,
            height=180,
            halign="left",
            valign="top"
        )

        self.output.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                max(180, value[1] + 20)
            )
        )

        root.add_widget(self.output)

        # Preview
        self.preview = CabinetPreview(
            size_hint_y=None,
            height=220
        )

        root.add_widget(self.preview)

        self.update_preview()

        return root

    # -------------------------
    # LOAD PROJECTS
    # -------------------------

    def load_projects(self):

        if os.path.exists(DATA_FILE):

            try:

                with open(DATA_FILE, "r") as f:
                    self.projects = json.load(f)

            except:

                self.projects = []

    # -------------------------
    # SAVE PROJECTS
    # -------------------------

    def save_projects(self):

        with open(DATA_FILE, "w") as f:

            json.dump(
                self.projects,
                f,
                indent=4
            )

    # -------------------------
    # THICKNESS
    # -------------------------

    def get_thickness(self):

        return int(
            self.thickness.text.replace(
                " mm",
                ""
            )
        )

    # -------------------------
    # ESTIMATE NUMBER
    # -------------------------

    def get_estimate_number(self):

        numbers = []

        for p in self.projects:

            estimate = p.get(
                "estimate_no",
                ""
            )

            if estimate.startswith("EST-"):

                try:

                    numbers.append(
                        int(
                            estimate.replace(
                                "EST-",
                                ""
                            )
                        )
                    )

                except:
                    pass

        next_number = (
            max(numbers) + 1
            if numbers
            else 1
        )

        return f"EST-{next_number:03d}"

    # -------------------------
    # PREVIEW
    # -------------------------

    def update_preview(self):

        try:

            w = float(self.width.text)
            h = float(self.height.text)
            s = int(self.shelves.text)

            self.preview.update(
                w,
                h,
                s
            )

        except:
            pass

    # -------------------------
    # CUTTING LIST
    # -------------------------

    def generate_cutting_list(self, instance):

        try:

            w = float(self.width.text)
            h = float(self.height.text)
            d = float(self.depth.text)

            t = self.get_thickness()

            shelves = int(
                self.shelves.text or 0
            )

            doors = int(
                self.doors.text or 0
            )

            drawers = int(
                self.drawers.text or 0
            )

            body_width = w - (2 * t)

            shelf_depth = d - t

            text = ""

            text += "CUTTING LIST\n"
            text += "-------------------------\n"

            text += (
                f"Material Thickness: "
                f"{t} mm\n\n"
            )

            text += (
                f"Left Side   : "
                f"{h} x {d} mm\n"
            )

            text += (
                f"Right Side  : "
                f"{h} x {d} mm\n"
            )

            text += (
                f"Top         : "
                f"{body_width} x {d} mm\n"
            )

            text += (
                f"Bottom      : "
                f"{body_width} x {d} mm\n"
            )

            text += (
                f"Shelves     : "
                f"{shelves} pcs\n"
            )

            text += (
                f"Shelf Size  : "
                f"{body_width} x "
                f"{shelf_depth} mm\n"
            )

            text += (
                f"Back        : "
                f"{w} x {h} mm\n"
            )

            text += (
                f"Doors       : "
                f"{doors} pcs\n"
            )

            text += (
                f"Drawers     : "
                f"{drawers} pcs\n"
            )

            self.output.text = text

            self.update_preview()

        except Exception as e:

            self.output.text = (
                "Error: " + str(e)
            )

    # -------------------------
    # SAVE / UPDATE
    # -------------------------

    def save_or_update(self, instance):

        try:

            w = float(self.width.text)
            h = float(self.height.text)
            d = float(self.depth.text)

            material = float(
                self.material_cost.text or 0
            )

            labour = float(
                self.labour_cost.text or 0
            )

            hardware = float(
                self.hardware_cost.text or 0
            )

            advance = float(
                self.advance.text or 0
            )

            total = (
                material
                + labour
                + hardware
            )

            remaining = total - advance

            if advance >= total and total > 0:

                status = "PAID"

            elif advance > 0:

                status = "PARTIAL"

            else:

                status = "PENDING"

            if self.edit_index is None:

                estimate_no = (
                    self.get_estimate_number()
                )

                date = datetime.now().strftime(
                    "%d-%m-%Y"
                )

            else:

                estimate_no = self.projects[
                    self.edit_index
                ].get(
                    "estimate_no",
                    self.get_estimate_number()
                )

                date = self.projects[
                    self.edit_index
                ].get(
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
                    w,

                "height":
                    h,

                "depth":
                    d,

                "thickness":
                    self.get_thickness(),

                "shelves":
                    int(
                        self.shelves.text or 0
                    ),

                "doors":
                    int(
                        self.doors.text or 0
                    ),

                # STEP 32
                "drawers":
                    int(
                        self.drawers.text or 0
                    ),

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

            if self.edit_index is None:

                self.projects.append(data)

            else:

                self.projects[
                    self.edit_index
                ] = data

                self.edit_index = None

            self.save_projects()

            self.output.text = (
                "Saved Successfully\n\n"
                f"Estimate: {estimate_no}\n"
                f"Doors: {data['doors']}\n"
                f"Drawers: {data['drawers']}\n"
                f"Total: ₹{total:.2f}\n"
                f"Remaining: ₹{remaining:.2f}"
            )

            self.clear_fields()

        except Exception as e:

            self.output.text = (
                "Save Error: " + str(e)
            )

    # -------------------------
    # CLEAR
    # -------------------------

    def clear_fields(self, instance=None):

        self.customer.text = ""
        self.mobile.text = ""
        self.project.text = "Wardrobe"

        self.width.text = "1800"
        self.height.text = "2100"
        self.depth.text = "600"

        self.thickness.text = "18 mm"

        self.shelves.text = "5"

        self.doors.text = "2"

        # STEP 32
        self.drawers.text = "0"

        self.material_cost.text = "0"
        self.labour_cost.text = "0"
        self.hardware_cost.text = "0"
        self.advance.text = "0"

        self.edit_index = None

        self.update_preview()

    # -------------------------
    # PROJECT LIST
    # -------------------------

    def show_projects(self, instance):

        if not self.projects:

            self.output.text = (
                "No Projects Found"
            )

            return

        text = "PROJECT LIST\n"
        text += "====================\n\n"

        for i, p in enumerate(
            self.projects
        ):

            text += (
                f"{i + 1}. "
                f"{p.get('estimate_no', '')}\n"
            )

            text += (
                f"Customer: "
                f"{p.get('customer', '')}\n"
            )

            text += (
                f"Project: "
                f"{p.get('project', '')}\n"
            )

            text += (
                f"Doors: "
                f"{p.get('doors', 2)}\n"
            )

            text += (
                f"Drawers: "
                f"{p.get('drawers', 0)}\n"
            )

            text += (
                f"Total: "
                f"₹{p.get('total', 0):.2f}\n"
            )

            text += (
                f"Status: "
                f"{p.get('status', '')}\n"
            )

            text += "--------------------\n"

        self.output.text = text

    # -------------------------
    # EDIT PROJECT
    # -------------------------

    def edit_project(self, index):

        if index < 0 or index >= len(
            self.projects
        ):
            return

        p = self.projects[index]

        self.edit_index = index

        self.customer.text = str(
            p.get("customer", "")
        )

        self.mobile.text = str(
            p.get("mobile", "")
        )

        self.project.text = str(
            p.get("project", "Wardrobe")
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

        self.thickness.text = (
            f"{p.get('thickness', 18)} mm"
        )

        self.shelves.text = str(
            p.get("shelves", 5)
        )

        self.doors.text = str(
            p.get("doors", 2)
        )

        # STEP 32
        self.drawers.text = str(
            p.get("drawers", 0)
        )

        self.material_cost.text = str(
            p.get("material_cost", 0)
        )

        self.labour_cost.text = str(
            p.get("labour_cost", 0)
        )

        self.hardware_cost.text = str(
            p.get("hardware_cost", 0)
        )

        self.advance.text = str(
            p.get("advance", 0)
        )

        self.update_preview()


if __name__ == "__main__":
    FurnitureApp().run()