#!/usr/bin/env python3
__author__ = "Arana Fireheart"

import codegrade

# Login to CodeGrade
client = codegrade.login_from_cli()

# Get all courses and select the desired one
all_courses = client.course.get_all()
course = codegrade.utils.value_or_exit(
    codegrade.utils.select_from_list(
        'Select a course',
        all_courses,
        lambda c: c.name))

# Get all course's users, map them to user types and select the desired one
all_users = list(map(
    lambda u: u if isinstance(u, codegrade.models.user.User) else u.user,
    client.course.get_all_users(course_id=course.id)))
user = codegrade.utils.value_or_exit(
    codegrade.utils.select_from_list(
        'Select a user',
        all_users,
        lambda u: f'u.name ({u.username})'))

# Select desired assignment from course
assignment = codegrade.utils.value_or_exit(
    codegrade.utils.select_from_list(
        'Select an assignment',
        course.assignments,
        lambda a: a.name))

# Get all user's submissions for the given assignment
submissions = client.assignment.get_submissions_by_user(
    assignment_id=assignment.id,
    user_id=user.id)

# Loop over user's submissions and print the acheived grade
for submission in submissions:
    print(f'Submission uploaded: {submission.created_at.isoformat()}'
          f' | Grade: {submission.grade}')
