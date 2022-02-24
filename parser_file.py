import json

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
            skills.append({skill: int(skill_level)})
            index += 1
        data['contributors']['data'].append({contributor: skills})
    
    for _ in range(data['projects']['items']):
        project, days_takes, score, best_day, roles = file_content[index].split()
        index += 1
        skills = []
        for _ in range(int(roles)):
            skill, skill_level = file_content[index].split()
            skills.append({skill: int(skill_level)})
            index += 1
        data['projects']['data'].append({ project: {
            'days_takes': int(days_takes),
            'score': int(score),
            'best_day': int(best_day),
            'skills': skills
        }})
    return data

# Example to use and print print(json.dumps(get_data_from_file (<file>), sort_keys=False, indent=2))