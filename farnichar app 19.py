import json
import os
from datetime import datetime

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
        self.selected_index = None

        main = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=5
        )

        main.add_widget(
            Label(
                text="PROJECT MANAGEMENT",
                font_size=22,
                size_hint_y=None,
                height=45
            )
        )

        main.add_widget(Label(text="Estimate Number"))

        self.estimate = TextInput(
            text="EST-001",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        main.add_widget(self.estimate)

        main.add_widget(Label(text="Customer Name"))

        self.customer = TextInput(
            multiline=False,
            size_hint_y=None,
            height=40
        )
        main.add_widget(self.customer)

        main.add_widget(Label(text="Mobile Number"))

        self.mobile = TextInput(
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=40
        )
        main.add_widget(self.mobile)

        main.add_widget(Label(text="Project Name"))

        self.project = TextInput(
            text="Wardrobe",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        main.add_widget(self.project)

        main.add_widget(Label(text="Final Total"))

        self.total = TextInput(
            text="18000",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=40
        )
        main.add_widget(self.total)

        main.add_widget(Label(text="Status"))

        self.status = TextInput(
            text="PENDING",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        main.add_widget(self.status)

        buttons = BoxLayout(
            size_hint_y=None,
            height=50,
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

    def get_data(self):

        return {
            "estimate": self.estimate.text,
            "customer": self.customer.text,
            "mobile": self.mobile.text,
            "project": self.project.text,
            "total": float(self.total.text),
            "status": self.status.text,
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

            self.status.text = "INVALID DATA"

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

        for index, p in enumerate(self.projects):

            text = (
                f"{index + 1}. {p.get('estimate', '-')}\n"
                f"Customer: {p.get('customer', '-')}\n"
                f"Mobile: {p.get('mobile', '-')}\n"
                f"Project: {p.get('project', '-')}\n"
                f"Total: Rs. {p.get('total', 0):.2f}\n"
                f"Status: {p.get('status', '-')}\n"
                f"Date: {p.get('date', '-')}"
            )

            button = Button(
                text=text,
                size_hint_y=None,
                height=150
            )

            button.bind(
                on_press=lambda btn, i=index:
                self.select_project(i)
            )

            self.project_list.add_widget(button)

    def select_project(self, index):

        self.selected_index = index

        p = self.projects[index]

        self.estimate.text = p.get("estimate", "")
        self.customer.text = p.get("customer", "")
        self.mobile.text = p.get("mobile", "")
        self.project.text = p.get("project", "")
        self.total.text = str(p.get("total", 0))
        self.status.text = p.get("status", "PENDING")

    def update_project(self, instance):

        if self.selected_index is None:

            self.status.text = "SELECT PROJECT FIRST"
            return

        try:

            self.projects[self.selected_index] = self.get_data()

            self.save_data()
            self.refresh_list()

        except:

            self.status.text = "INVALID DATA"

    def delete_project(self, instance):

        if self.selected_index is None:

            self.status.text = "SELECT PROJECT FIRST"
            return

        del self.projects[self.selected_index]

        self.save_data()

        self.selected_index = None

        self.clear_fields()
        self.refresh_list()

    def clear_fields(self):

        self.estimate.text = "EST-001"
        self.customer.text = ""
        self.mobile.text = ""
        self.project.text = "Wardrobe"
        self.total.text = "18000"
        self.status.text = "PENDING"


FurnitureApp().run()