from pprint import pprint
import sys

def get_data_from_file(filepath):
    file_content = None
    index = 1
    data = {
        'contributors': {
            'items': 0,
            'data': []
        },
        'projects': {
            'items': 0,
            'data': []
        }
    }

    with open(filepath, 'r') as f:
        file_content = f.read().split('\n')
    constributors, projects = file_content[0].split()
    data['contributors']['items'], data['projects']['items'] = int(constributors), int(projects)

    for _ in range(data['contributors']['items']):
        contributor, n_skill = file_content[index].split()
        index += 1
        skills = []
        for _ in range(int(n_skill)):
            skill, skill_level = file_content[index].split()
            skills.append({
                'name': skill,
                'level': int(skill_level) 
            })
            index += 1
        data['contributors']['data'].append({
            'name': contributor,
            'skills': skills,
            'delay': 0
        })
    
    for _ in range(data['projects']['items']):
        project, days_takes, score, best_day, roles = file_content[index].split()
        index += 1
        skills = []
        for _ in range(int(roles)):
            skill, skill_level = file_content[index].split()
            skills.append({
                'name': skill,
                'level': int(skill_level) 
            })
            index += 1
        data['projects']['data'].append({
            'name': project,
            'days_takes': int(days_takes),
            'score': int(score),
            'best_day': int(best_day),
            'skills': skills
        })
    return data

file = sys.argv[1]
data = get_data_from_file(file)
finished_project = []

def contributors_get_index_skill(contributor, skill_name):
    for i, skill in enumerate(contributor['skills']):
        if skill['name'] == skill_name:
            return i 
    return -1

def contributors_get_best_by_level_skill(skill_name, level, contributors):
    bests = []
    
    for contributor in contributors:
        if contributor['delay'] != 0:
            continue
        for skill in contributor['skills']:
            if skill['name'] == skill_name and skill['level'] >= level:
                bests.append(contributor)
    if len(bests) == 0:
        return None
    bests.sort(key=lambda x: x['skills'][contributors_get_index_skill(x, skill_name)]['level'])
    return bests[0]

def contributors_level_up_skill(contributors, skill_name, skill_level, coontributor_nam):
    for contributor in contributors:
        for skill in contributor['skills']:
            if skill_name == skill['name'] and skill_level == skill['level']:
                skill['level'] += 1

def contributors_set_delay(contributors, contributor_name, delay):
    for contributor in contributors:
        if contributor['name'] == contributor_name:
            contributor['delay'] = delay

def contributors_decrease_delay(contributors):
    for contributor in contributors:
        if contributor['delay'] > 0:
            contributor['delay'] -= 1

def get_contributor_by_name(contributors, contributor_name):
    for contributor in contributors:
        if contributor['name'] == contributor_name:
            return contributor
    return None

def project_fill_roles(project, contributors):
    todo = []
    contributors_tmp = []
    contributors_name = []

    for skill in project['skills']:
        best_contributors = contributors_get_best_by_level_skill(skill['name'], skill['level'], contributors)
        if not best_contributors:
            todo.append(project)
            break
        else:
            contributors_name.append(best_contributors['name'])
            contributors_tmp.append({'name': best_contributors['name'], 'skill': skill})
    if len(contributors_tmp) != 0 and len(todo) == 0:
        finished_project.append(f"{project['name']}\n{' '.join(contributors_name)}")
        for contributor in contributors_tmp:
            contributors_set_delay(contributors, contributor['name'], project['days_takes'])
            contributors_level_up_skill(contributors, contributor['skill']['name'], contributor['skill']['level'], contributor['name'])
    return todo

def contributors_all_finished(contributors):
    for contributor in contributors:
        if contributor['delay'] != 0:
            return False
    return True

contributors = data['contributors']['data']
projects = data['projects']['data']
projects.sort(key=lambda x: x['best_day'])

todo_projects = projects
old_len = len(todo_projects)

import json


while len(todo_projects) != 0:
    todo_later = []

    for project in todo_projects:
        tmp = []
        for todo in todo_later:
            tmp += project_fill_roles(todo, contributors)
        todo_later = tmp
        tmp = project_fill_roles(project, contributors)
        todo_later += tmp

    if old_len == len(todo_later) and contributors_all_finished(contributors):
        break
    old_len = len(todo_later)
    todo_projects = todo_later
    contributors_decrease_delay(contributors)

print(len(projects) - len(todo_projects))
print("\n".join(finished_project))