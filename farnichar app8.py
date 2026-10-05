from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color


class Cabinet3D(Widget):

    def draw_cabinet(self, shelves):

        self.canvas.clear()

        with self.canvas:

            Color(1, 1, 1)

            # Front
            x = self.x + 60
            y = self.y + 40
            w = 220
            h = 300

            Line(
                rectangle=(x, y, w, h),
                width=2
            )

            # 3D depth
            depth = 70

            Line(
                points=[
                    x, y + h,
                    x + depth, y + h + 40,
                    x + w + depth, y + h + 40,
                    x + w, y + h
                ],
                width=2
            )

            Line(
                points=[
                    x + w, y,
                    x + w + depth, y + 40,
                    x + w + depth, y + h + 40
                ],
                width=2
            )

            Line(
                points=[
                    x + w, y,
                    x + w + depth, y + 40
                ],
                width=2
            )

            # Shelves
            gap = h / (shelves + 1)

            for i in range(1, shelves + 1):

                sy = y + gap * i

                Line(
                    points=[
                        x,
                        sy,
                        x + w,
                        sy
                    ],
                    width=2
                )

                Line(
                    points=[
                        x + w,
                        sy,
                        x + w + depth,
                        sy + 40
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
                text="3D FURNITURE DESIGNER",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        main.add_widget(
            Label(text="Number of Shelves")
        )

        self.shelves = TextInput(
            text="5",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=50
        )

        main.add_widget(self.shelves)

        button = Button(
            text="SHOW 3D CABINET",
            size_hint_y=None,
            height=55
        )

        button.bind(
            on_press=self.show_3d
        )

        main.add_widget(button)

        self.preview = Cabinet3D()

        main.add_widget(self.preview)

        return main

    def show_3d(self, instance):

        try:
            shelves = int(self.shelves.text)

            self.preview.draw_cabinet(
                shelves
            )

        except:
            pass


FurnitureApp().run()