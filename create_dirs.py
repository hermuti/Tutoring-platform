import os

dirs = [
    "onlineschool/students/templates/students",
    "onlineschool/teachers/templates/teachers",
    "onlineschool/courses/templates/courses",
]

for dir in dirs:
    os.makedirs(dir, exist_ok=True)