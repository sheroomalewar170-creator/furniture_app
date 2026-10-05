import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class FurnitureApp(App):

    def build(self):

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        layout.add_widget(
            Label(
                text="MODERN FURNITURE DESIGNER",
                font_size=22
            )
        )

        layout.add_widget(Label(text="Project Name"))

        self.project = TextInput(
            text="My Furniture",
            multiline=False
        )
        layout.add_widget(self.project)

        layout.add_widget(Label(text="Width (inch)"))

        self.width = TextInput(
            text="36",
            multiline=False
        )
        layout.add_widget(self.width)

        layout.add_widget(Label(text="Height (inch)"))

        self.height = TextInput(
            text="72",
            multiline=False
        )
        layout.add_widget(self.height)

        layout.add_widget(Label(text="Depth (inch)"))

        self.depth = TextInput(
            text="24",
            multiline=False
        )
        layout.add_widget(self.depth)

        layout.add_widget(Label(text="Shelves"))

        self.shelves = TextInput(
            text="5",
            multiline=False,
            input_filter="int"
        )
        layout.add_widget(self.shelves)

        save_button = Button(
            text="SAVE PROJECT",
            size_hint_y=None,
            height=60
        )

        save_button.bind(
            on_press=self.save_project
        )

        layout.add_widget(save_button)

        return layout

    def save_project(self, instance):

        data = {
            "project_name": self.project.text,
            "width": self.width.text,
            "height": self.height.text,
            "depth": self.depth.text,
            "shelves": self.shelves.text
        }

        with open(
            "furniture_project.json",
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        popup = Popup(
            title="Project Saved",
            content=Label(
                text="Project successfully saved!"
            ),
            size_hint=(0.8, 0.3)
        )

        popup.open()


FurnitureApp().run()