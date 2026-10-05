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
from kivy.graphics import Rectangle, Line
from kivy.uix.widget import Widget


FILE_NAME = "projects.json"


class CabinetPreview(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.width_mm = 1800
        self.height_mm = 2100
        self.shelves = 5

        self.bind(
            size=self.draw_cabinet,
            pos=self.draw_cabinet
        )

    def update_data(self, width, height, shelves):

        self.width_mm = width
        self.height_mm = height
        self.shelves = shelves

        self.draw_cabinet()

    def draw_cabinet(self, *args):

        self.canvas.clear()

        if self.width_mm <= 0 or self.height_mm <= 0:
            return

        # Available drawing area
        margin = 20

        available_width = self.width - (margin * 2)
        available_height = self.height - (margin * 2)

        if available_width <= 0 or available_height <= 0:
            return

        # Keep cabinet proportional
        ratio = min(
            available_width / self.width_mm,
            available_height / self.height_mm
        )

        cabinet_width = self.width_mm * ratio
        cabinet_height = self.height_mm * ratio

        x = self.x + (
            self.width - cabinet_width
        ) / 2

        y = self.y + (
            self.height - cabinet_height
        ) / 2

        with self.canvas:

            # Cabinet outer box
            Line(
                rectangle=(
                    x,
                    y,
                    cabinet_width,
                    cabinet_height
                ),
                width=2
            )

            # Shelves
            if self.shelves > 0:

                shelf_gap = (
                    cabinet_height /
                    (self.shelves + 1)
                )

                for i in range(1, self.shelves + 1):

                    shelf_y = (
                        y +
                        shelf_gap * i
                    )

                    Line(
                        points=[
                            x,
                            shelf_y,
                            x + cabinet_width,
                            shelf_y
                        ],
                        width=1.5
                    )


class FurnitureApp(App):

    def build(self):

        self.projects = []

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

        preview_button = Button(
            text="SHOW 2D PREVIEW",
            size_hint_y=None,
            height=50
        )

        preview_button.bind(
            on_press=self.show_preview
        )

        main.add_widget(preview_button)

        # 2D Preview
        self.preview = CabinetPreview(
            size_hint_y=None,
            height=260
        )

        main.add_widget(self.preview)

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
            texture_size=
            self.cutting_result.setter("size")
        )

        cutting_scroll = ScrollView(
            size_hint_y=None,
            height=200
        )

        cutting_scroll.add_widget(
            self.cutting_result
        )

        main.add_widget(cutting_scroll)

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
            minimum_height=
            self.project_list.setter("height")
        )

        scroll.add_widget(
            self.project_list
        )

        main.add_widget(scroll)

        self.refresh_list()

        return main

    def get_thickness(self):

        if self.thickness.text == "12 mm":
            return 12

        return 18

    def show_preview(self, instance):

        try:

            w = float(self.width.text)
            h = float(self.height.text)
            shelves = int(self.shelves.text)

            self.preview.update_data(
                w,
                h,
                shelves
            )

        except:

            self.cutting_result.text = (
                "Please enter valid dimensions."
            )

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

                f"Material Thickness: {t} mm\n\n"

                "1. SIDE LEFT\n"
                "Qty: 1\n"
                f"Size: {h:.0f} x "
                f"{d:.0f} mm\n\n"

                "2. SIDE RIGHT\n"
                "Qty: 1\n"
                f"Size: {h:.0f} x "
                f"{d:.0f} mm\n\n"

                "3. TOP\n"
                "Qty: 1\n"
                f"Size: {top_width:.0f} x "
                f"{d:.0f} mm\n\n"

                "4. BOTTOM\n"
                "Qty: 1\n"
                f"Size: {top_width:.0f} x "
                f"{d:.0f} mm\n\n"

                "5. BACK\n"
                "Qty: 1\n"
                f"Size: {w:.0f} x "
                f"{h:.0f} mm\n\n"

                "6. SHELVES\n"
                f"Qty: {shelves}\n"
                f"Size: {shelf_width:.0f} x "
                f"{shelf_depth:.0f} mm"
            )

            self.cutting_result.text = text

            self.preview.update_data(
                w,
                h,
                shelves
            )

        except:

            self.cutting_result.text = (
                "Please enter valid dimensions."
            )

    def save_project(self, instance):

        try:

            data = {
                "customer": self.customer.text,
                "project": self.project.text,
                "width": float(self.width.text),
                "height": float(self.height.text),
                "depth": float(self.depth.text),
                "thickness": self.get_thickness(),
                "shelves": int(self.shelves.text),
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

            self.cutting_result.text = (
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
                f"Size: "
                f"{p.get('width', 0):.0f} x "
                f"{p.get('height', 0):.0f} x "
                f"{p.get('depth', 0):.0f} mm\n"
                f"Material: "
                f"{p.get('thickness', 0)} mm\n"
                f"Shelves: "
                f"{p.get('shelves', 0)}\n"
                f"Date: "
                f"{p.get('date', '-')}"
            )

            self.project_list.add_widget(
                Button(
                    text=text,
                    size_hint_y=None,
                    height=135
                )
            )


FurnitureApp().run()