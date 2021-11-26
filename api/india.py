import json
import os
from django.conf import settings


exam_data_path = os.path.join(settings.PROJECT_ROOT, "train\\tests.json")

exams_college = json.loads(open(exam_data_path).read())

college_data_path = os.path.join(
    settings.PROJECT_ROOT, "train\\orignal_data.json")

college_data = json.loads(open(college_data_path).read())


def colleges_list_exam_india(exam_name):
    return exams_college[exam_name]


def complete_detail(college_name):
    return [i for i in college_data if i['institute_name'].title() == college_name.title()]
