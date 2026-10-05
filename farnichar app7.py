from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Line


class FurniturePreview(Widget):

    def draw_furniture(self, width, height, shelves):
        self.canvas.clear()

        with self.canvas:
            # Furniture box
            Rectangle(
                pos=(self.x + 40, self.y + 30),
                size=(width, height)
            )

            Line(
                rectangle=(
                    self.x + 40,
                    self.y + 30,
                    width,
                    height
                ),
                width=2
            )

            # Shelves
            if shelves > 0:
                shelf_gap = height / (shelves + 1)

                for i in range(1, shelves + 1):
                    y = self.y + 30 + shelf_gap * i

                    Line(
                        points=[
                            self.x + 40,
                            y,
                            self.x + 40 + width,
                            y
                        ],
                        width=2
                    )


class FurnitureApp(App):

    def build(self):

        main = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=8
        )

        main.add_widget(
            Label(
                text="MODERN FURNITURE DESIGNER",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        main.add_widget(Label(text="Width (inch)"))

        self.width = TextInput(
            text="200",
            multiline=False
        )
        main.add_widget(self.width)

        main.add_widget(Label(text="Height (inch)"))

        self.height = TextInput(
            text="300",
            multiline=False
        )
        main.add_widget(self.height)

        main.add_widget(Label(text="Number of Shelves"))

        self.shelves = TextInput(
            text="5",
            multiline=False,
            input_filter="int"
        )
        main.add_widget(self.shelves)

        button = Button(
            text="SHOW FURNITURE",
            size_hint_y=None,
            height=55
        )

        button.bind(
            on_press=self.show_furniture
        )

        main.add_widget(button)

        self.preview = FurniturePreview()

        main.add_widget(self.preview)

        return main

    def show_furniture(self, instance):

        try:
            w = float(self.width.text)
            h = float(self.height.text)
            shelves = int(self.shelves.text)

            # Screen ke according size
            preview_width = 220
            preview_height = 300

            self.preview.draw_furniture(
                preview_width,
                preview_height,
                shelves
            )

        except:
            pass


FurnitureApp().run()