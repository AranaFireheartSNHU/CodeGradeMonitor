#!/usr/bin/env python3
__author__ = "Arana Fireheart"

from math import ceil

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from fetchCGData import fetchCGCourseList, fetchCGData
from kivy.uix.screenmanager import ScreenManager, Screen
from fetchCGData import fetchCGCourseList, fetchCGData


# Define our different screens
class CourseGridLayout(Screen):
    def buttonAdd(self, buttonName):
        pushButton = Button(
            text=buttonName,
        )
        pushButton.bind(on_press=lambda instance, who=buttonName: self.buttonHandler(instance, who))
        self.ids["buttonGrid"].add_widget(pushButton)

    def buttonHandler(self, instance, buttonName):
        app = CodeGradeMonitorApp.get_running_app()
        app.root.current = "courseprogress"
        self.parent.children[0].ids["progressoutput"].text = f"{buttonName}"
        app.root.transition.direction = "left"


class CourseProgressWindow(Screen):
    # def __init__(self):
    #     super().__init__()
    pass


class WindowManager(ScreenManager):
    pass


class CodeGradeMonitorApp(App):
    def build(self):
        # Designate Our .kv design file
        CGMonitorUI = Builder.load_file("CGMonitor.kv")

        coursesList = fetchCGCourseList()
        numberOfRows = ceil(len(coursesList) / 2)
        for course in coursesList:
            CGMonitorUI.screens[0].buttonAdd(course.name[:20])
        return CGMonitorUI


if __name__ == "__main__":
    CodeGradeMonitorApp().run()
