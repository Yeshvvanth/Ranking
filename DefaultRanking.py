import pymysql
import re
from operator import itemgetter

db = pymysql.connect("localhost", "root", "password",
                     "Job_Seekers", cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
cursor.execute(
    "SELECT job_seeker_id,skills,experience,location FROM java_user_profile")
Employee_records = cursor.fetchall()


skills = ["Servlets"]
experience = ["2 years"]
location = ["stockholm", "gothenburg"]
list_requirements = [location, experience, skills]

# To convert Skills in String format to List


def data_transform(Employee_records):
    for d in Employee_records:
        Employee_skills = d.get('skills')
        skills = re.split(',', Employee_skills)
        d['skills'] = skills
        d['rank'] = 0
    return Employee_records


Employee_records = data_transform(Employee_records)


def skill_relevance_score(Employee_records, skills):
    for skill in skills:
        for dict_ in Employee_records:
            if skill in dict_["skills"]:
                dict_["rank"] += 1

    return Employee_records


def experience_relevance_score(Employee_records, experience):

    for exp in experience:
        for dict_ in Employee_records:
            if exp in dict_["experience"]:
                dict_["rank"] += 1

    return Employee_records

# To assign relevance for candidates
# Based on how many requirements candidates satisfy


def location_relevance_score(Employee_records, location):
    for loc in location:
        for dict_ in Employee_records:
            if loc in dict_["location"]:
                dict_["rank"] += 1
    return Employee_records


def relevance_score(Employee_records, list_requirements):

    for elm in list_requirements:
        if elm == skills:
            Employee_records = skill_relevance_score(Employee_records, skills)
        elif elm == experience:
            Employee_records = experience_relevance_score(
                Employee_records, experience)
        elif elm == location:
            Employee_records = location_relevance_score(
                Employee_records, location)
        else:
            print("Please fill the requirements")
    Employee_records = sorted(
        Employee_records, key=lambda x: x['rank'], reverse=True)
    return Employee_records


Employee_records = relevance_score(Employee_records, list_requirements)


print(Employee_records)
