import requests
for i in range(5):
    new_body = requests.get('http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com' + '/game?token=' + requests.post('http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com' + '/session', data = {'uid': '205125796'}).json()['token']).json()
    maze, move_list, maze_stack = [[1 if i == new_body['cur_loc'][1] and j == new_body['cur_loc'][0] else 0 for i in range(new_body['size'][1])] for j in range(new_body['size'][0])], [], []
    while True:
        if new_body['cur_loc'][0] + 1 < new_body['size'][0] and maze[new_body['cur_loc'][0] + 1][new_body['cur_loc'][1]] == 0 and (new_body['cur_loc'][0] + 1, new_body['cur_loc'][1]) not in maze_stack:   maze_stack.append((new_body['cur_loc'][0] + 1, new_body['cur_loc'][1]))
        if new_body['cur_loc'][0] - 1 >= 0 and maze[new_body['cur_loc'][0] - 1][new_body['cur_loc'][1]] == 0 and (new_body['cur_loc'][0] - 1, new_body['cur_loc'][1]) not in maze_stack:                    maze_stack.append((new_body['cur_loc'][0] - 1, new_body['cur_loc'][1]))
        if new_body['cur_loc'][1] + 1 < new_body['size'][1] and maze[new_body['cur_loc'][0]][new_body['cur_loc'][1] + 1] == 0 and (new_body['cur_loc'][0], new_body['cur_loc'][1] + 1) not in maze_stack:   maze_stack.append((new_body['cur_loc'][0], new_body['cur_loc'][1] + 1))
        if new_body['cur_loc'][1] - 1 >= 0 and maze[new_body['cur_loc'][0]][new_body['cur_loc'][1] - 1] == 0 and (new_body['cur_loc'][0], new_body['cur_loc'][1] - 1) not in maze_stack:                    maze_stack.append((new_body['cur_loc'][0], new_body['cur_loc'][1] - 1))
        next_spot = maze_stack.pop()
        while abs(next_spot[0] - new_body['cur_loc'][0]) + abs(next_spot[1] - new_body['cur_loc'][1]) > 1:
            last_move = move_list.pop()
            new_body['cur_loc'][{'up': (1, -1, 'down'), 'down': (1, +1, 'up'), 'right': (0, +1, 'left'), 'left': (0, -1, 'right')}[last_move][0]], body = new_body['cur_loc'][{'up': (1, -1, 'down'), 'down': (1, +1, 'up'), 'right': (0, +1, 'left'), 'left': (0, -1, 'right')}[last_move][0]] - {'up': (1, -1, 'down'), 'down': (1, +1, 'up'), 'right': (0, +1, 'left'), 'left': (0, -1, 'right')}[last_move][1], requests.post('http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com' + '/game?token=' + requests.post('http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com' + '/session', data = {'uid': '205125796'}).json()['token'], data = {'action': {'up': (1, -1, 'down'), 'down': (1, +1, 'up'), 'right': (0, +1, 'left'), 'left': (0, -1, 'right')}[last_move][2]}).json()
        action = (('up', 'down')[next_spot[1] > new_body['cur_loc'][1]], ('left', 'right')[next_spot[0] > new_body['cur_loc'][0]])[next_spot[0] != new_body['cur_loc'][0]]
        body, maze[next_spot[0]][next_spot[1]] = requests.post('http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com' + '/game?token=' + requests.post('http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com' + '/session', data = {'uid': '205125796'}).json()['token'], data = {'action': action}).json(), 1
        if body['result'] == 0:     
            new_body['cur_loc'][{'up': (1, -1, 'down'), 'down': (1, +1, 'up'), 'right': (0, +1, 'left'), 'left': (0, -1, 'right')}[action][0]] += {'up': (1, -1, 'down'), 'down': (1, +1, 'up'), 'right': (0, +1, 'left'), 'left': (0, -1, 'right')}[action][1]
            move_list.append(action)
        elif body['result'] == 1: break
