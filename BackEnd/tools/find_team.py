def find_team(data):
    leader_list = list()
    student_dict = dict()  # {'leader-1': [{'name': 'lili'}]}
    for d in data:
        if d['belong_to']:
            # 队员
            student_dict.setdefault(d['belong_to'], [])
            student_dict[d['belong_to']].append({'name': d['name']})
        else:
            # 队长
            leader_list.append({'name': d['name'], 'team': []})
    for l in leader_list:
        if l['name'] in student_dict:
            l['team'] = student_dict[l['name']]

    return leader_list


# 测试数据
s = [{'name': 'leader-1', 'belong_to': None}, {'name': 'jack', 'belong_to': 'leader-2'}, {'name': 'lili', 'belong_to': 'leader-1'}, {'name': 'leader-2', 'belong_to': None}, {'name': 'Tom', 'belong_to': 'leader-1'}]
print(find_team(s))