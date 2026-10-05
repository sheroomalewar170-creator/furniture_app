import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


FILE_NAME = "projects.json"


class FurnitureApp(App):

    def build(self):

        self.projects = self.load_projects()

        main = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=8
        )

        main.add_widget(
            Label(
                text="FURNITURE PROJECT DASHBOARD",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        main.add_widget(Label(text="Customer Name"))

        self.customer = TextInput(
            multiline=False,
            size_hint_y=None,
            height=45
        )

        main.add_widget(self.customer)

        main.add_widget(Label(text="Project Name"))

        self.project = TextInput(
            text="Wardrobe",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        main.add_widget(self.project)

        main.add_widget(Label(text="Final Total (₹)"))

        self.total = TextInput(
            text="18000",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=45
        )

        main.add_widget(self.total)

        main.add_widget(Label(text="Status"))

        self.status = TextInput(
            text="PENDING",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        main.add_widget(self.status)

        save_button = Button(
            text="SAVE PROJECT",
            size_hint_y=None,
            height=55
        )

        save_button.bind(
            on_press=self.save_project
        )

        main.add_widget(save_button)

        refresh_button = Button(
            text="REFRESH PROJECT LIST",
            size_hint_y=None,
            height=55
        )

        refresh_button.bind(
            on_press=self.refresh_list
        )

        main.add_widget(refresh_button)

        scroll = ScrollView()

        self.project_list = Label(
            text="",
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.project_list.bind(
            texture_size=self.project_list.setter(
                "size"
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

    def save_project(self, instance):

        try:

            data = {
                "customer": self.customer.text,
                "project": self.project.text,
                "total": float(self.total.text),
                "status": self.status.text
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

            self.refresh_list()

            self.customer.text = ""

        except:

            self.project_list.text = (
                "Please enter a valid total."
            )

    def refresh_list(self, instance=None):

        if not self.projects:

            self.project_list.text = (
                "No projects saved yet."
            )

            return

        text = "PROJECT LIST\n\n"

        for i, p in enumerate(
            self.projects,
            start=1
        ):

            text += (
                f"{i}. "
                f"{p['customer']} | "
                f"{p['project']}\n"
                f"   Total: ₹{p['total']:.2f}\n"
                f"   Status: {p['status']}\n\n"
            )

        self.project_list.text = text


FurnitureApp().run()