#!/usr/bin/env python
__author__ = "Arana Fireheart"

from statistics import mean

import codegrade
from os import getenv
from dateutil import parser

LOGIN_USERNAME = "DragonFire"
LOGIN_PASSWORD = getenv('CG_PASS')
LOGIN_TENANT = "Southern New Hampshire University"


class Student(object):
    def __init__(self, openingName):
        self.name = openingName
        self._email = ""
        self.assignments = {}
        self.progress = 0

    def add_assignment(self, assignmentName, assignmentGrade, submittedDate):
        self.assignments[assignmentName] = assignmentGrade
        self.progress = mean(list(self.assignments.values()))

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, newEmailAddress):
        from re import fullmatch
        try:
            if fullmatch(r"[^@]+@[^@]+\.[^@]+", newEmailAddress):
                self._email = newEmailAddress
        except TypeError:
            pass


def submissionIsNewer(oldISODateTime, newISODateTime):
    oldDate = parser.parse(oldISODateTime)
    newDate = parser.parse(newISODateTime)
    if newDate > oldDate:
        return True
    return False


def getEmailAddress(searchUser, userObjects):
    for currentUser in userObjects:
        if searchUser.lower() == currentUser.name.lower() and '@' in currentUser.username:
            return currentUser.username.lower()
    return ""   # No matching user was found.


def printCGData(dataObject):
    for student in dataObject:
        print(f"Student: {student.name} Progress: {student.progress * 10:5.1f}%")
        for assignmentName, grade in student.assignments.items():
            print(f"\t Assignment: {assignmentName:16}\t| Grade: {grade}")


def fetchCGCourseList():
    with codegrade.login(
            username=LOGIN_USERNAME,
            password=LOGIN_PASSWORD,
            tenant=LOGIN_TENANT,
            ) as client:

        # Get all courses
        allCourses = client.course.get_all()
        for course in allCourses:
            try:
                courseList.append(course)
            except NameError:
                courseList = [course]
    return courseList


def fetchCGData(requestedCourse):
    with codegrade.login(
            username=LOGIN_USERNAME,
            password=LOGIN_PASSWORD,
            tenant=LOGIN_TENANT,
    ) as client:

        # Get all course's users, map them to user types and select the desired one
        bulkUsers = list(map(
            lambda u: u if isinstance(u, codegrade.models.user.User) else u.user,
            client.course.get_all_users(course_id=requestedCourse.id)))
        # Remove 'duplicate' user accounts named with the user's email address
        allUsers = [user for user in bulkUsers
                    if '@' not in user.username and
                    user.username not in ["TestStudent", f"{client.user.get().username}"]]

        allStudents = []
        for user in allUsers:
            # Fetch all of the assignments for this user
            # print(f"User: {user.name}")
            try:
                allStudents.append(currentStudent)
            except NameError:
                pass    # First student entry
            currentStudent = Student(user.name)
            currentStudent.email = getEmailAddress(user.name, bulkUsers)

            for assignment in requestedCourse.assignments:
                # Get all user's submissions for the given assignment
                submissions = client.assignment.get_submissions_by_user(
                    assignment_id=assignment.id,
                    user_id=user.id)

                latestSubmission = []
                # Loop over user's submissions and print only the latest achieved grade.
                for submission in submissions:
                    try:
                        if submissionIsNewer(latestSubmission[0], submission.created_at.isoformat()):
                            latestSubmission = [submission.created_at.isoformat(), submission.grade]
                    except IndexError:
                        latestSubmission = [submission.created_at.isoformat(), submission.grade]
                if len(latestSubmission) > 0:
                    submissionTime, submissionGrade = latestSubmission[0], latestSubmission[1]
                else:
                    submissionTime, submissionGrade = "Never", 0.0
                # print(f"\t Assignment: {assignment.name:16}| Grade: {submissionGrade} | Uploaded: {submissionTime}")
                currentStudent.add_assignment(assignment.name, submissionGrade, submissionTime)
    return allStudents


if __name__ == "__main__":
    coursesList = fetchCGCourseList()
    for selectionNumber, courseObject in enumerate(coursesList, start=1):
        print(f"[{selectionNumber}] {courseObject.name}")
    courseSelection = int(input("Select a course: "))

    currentCourse = coursesList[courseSelection - 1]

    studentData = fetchCGData(currentCourse)
    printCGData(studentData)
    pass
