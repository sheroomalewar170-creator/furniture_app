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
                text="MODERN FURNITURE SOFTWARE",
                font_size=21,
                size_hint_y=None,
                height=45
            )
        )

        # FURNITURE SIZE

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
            Label(text="Material Thickness (mm)")
        )

        self.thickness = TextInput(
            text="18",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=38
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
            self.cutting_result.setter(
                "size"
            )
        )

        cutting_scroll = ScrollView(
            size_hint_y=None,
            height=230
        )

        cutting_scroll.add_widget(
            self.cutting_result
        )

        main.add_widget(
            cutting_scroll
        )

        # CUSTOMER

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

        # SAVE

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
            self.project_list.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.project_list
        )

        main.add_widget(scroll)

        self.refresh_list()

        return main

    def load_projects(self):

        if os.path.exists(FILE_NAME):

            try:

                with open(
                    FILE_NAME,
                    "r"
                ) as file:

                    return json.load(file)

            except:

                return []

        return []

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

    def create_cutting_list(
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

            t = float(
                self.thickness.text
            )

            shelves = int(
                self.shelves.text
            )

            side_height = h
            side_depth = d

            top_width = w - (
                2 * t
            )

            top_depth = d

            back_width = w
            back_height = h

            shelf_width = w - (
                2 * t
            )

            shelf_depth = d - t

            text = (
                "CUTTING LIST\n\n"

                "1. SIDE LEFT\n"
                f"   Qty: 1\n"
                f"   Size: {side_height:.0f} x "
                f"{side_depth:.0f} mm\n\n"

                "2. SIDE RIGHT\n"
                f"   Qty: 1\n"
                f"   Size: {side_height:.0f} x "
                f"{side_depth:.0f} mm\n\n"

                "3. TOP\n"
                f"   Qty: 1\n"
                f"   Size: {top_width:.0f} x "
                f"{top_depth:.0f} mm\n\n"

                "4. BOTTOM\n"
                f"   Qty: 1\n"
                f"   Size: {top_width:.0f} x "
                f"{top_depth:.0f} mm\n\n"

                "5. BACK\n"
                f"   Qty: 1\n"
                f"   Size: {back_width:.0f} x "
                f"{back_height:.0f} mm\n\n"

                f"6. SHELVES\n"
                f"   Qty: {shelves}\n"
                f"   Size: {shelf_width:.0f} x "
                f"{shelf_depth:.0f} mm\n\n"

                f"Material Thickness: "
                f"{t:.0f} mm"
            )

            self.cutting_result.text = text

        except:

            self.cutting_result.text = (
                "Please enter valid dimensions."
            )

    def save_project(self, instance):

        try:

            data = {

                "customer":
                    self.customer.text,

                "project":
                    self.project.text,

                "width":
                    float(self.width.text),

                "height":
                    float(self.height.text),

                "depth":
                    float(self.depth.text),

                "thickness":
                    float(self.thickness.text),

                "shelves":
                    int(self.shelves.text),

                "date":
                    datetime.now().strftime(
                        "%d-%m-%Y"
                    )
            }

            self.projects.append(data)

            self.save_data()

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
                f"{p.get('thickness', 0):.0f} mm\n"
                f"Shelves: "
                f"{p.get('shelves', 0)}\n"
                f"Date: "
                f"{p.get('date', '-')}"
            )

            button = Button(
                text=text,
                size_hint_y=None,
                height=135
            )

            self.project_list.add_widget(
                button
            )


FurnitureApp().run()