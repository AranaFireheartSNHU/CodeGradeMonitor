#!/usr/bin/env python3
__author__ = "Arana Fireheart"

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy. uix.screenmanager import ScreenManager, Screen
from fetchCGData import fetchCGCourseList, fetchCGData


# Define our different screens
class WindowManager(ScreenManager):
    pass


class CourseGridLayout(Screen):
    pass


class CourseProgressWindow(Screen):
    pass


# Designate our .kv design file
CGMonitorUI = Builder.load_file("CGMonitor.kv")


class CourseGridLayout(GridLayout):
    pass

    def buttonHandler(self, instance, buttonNumber):
        print(f"Hello {buttonNumber}")


class CodeGradeMonitorApp(App):
    def build(self):
        # Build button widgets
        coursesList = fetchCGCourseList()
        for course in coursesList:
            pushButton = Button(
                text=course.name[:30],
            )
            callbackMethod= lambda instance, who=course.id: self.buttonHandler(instance, who)
            pushButton.bind(on_press=callbackMethod)
            self.bottomGrid.add_widget(pushButton)

        # Add the new bottomGrid to our app
        self.add_widget(self.bottomGrid)
        return CGMonitorUI


if __name__ == "__main__":
    CodeGradeMonitorApp().run()
