import requests

# Get Token
url, id = 'http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com', '205125796'
init_resp = requests.post(url + '/session', data = {'uid': id})
init_body = init_resp.json()
access_token = init_body['token']
print(f'access token: {access_token}')

# Get new game
new_resp = requests.get(url + '/game?token=' + access_token)
new_body = new_resp.json()
body = {'result': 0}    # Tell the inner while loop that not finished checking

while new_body['total_levels'] != None:
    # Initialize some variables
    maze_size = new_body['size'][0], new_body['size'][1]
    cur_loc = [new_body['cur_loc'][0], new_body['cur_loc'][1]]
    print(f'Initial location: {cur_loc[0]} {cur_loc[1]}')
    print(f'Maze Size: {maze_size[0]} {maze_size[1]}')

    maze = [[0 for i in range(maze_size[1])] for j in range(maze_size[0])]
    maze[cur_loc[0]][cur_loc[1]] = 1
    move_list = []      # Holds the moves performed to go from the original spot to the new spot
    maze_stack = []     # Holds locations to visit

    # Add locations to check to maze_stack
    while body['result'] != 1:
        if cur_loc[0] + 1 < maze_size[0] and maze[cur_loc[0] + 1][cur_loc[1]] == 0 and (cur_loc[0] + 1, cur_loc[1]) not in maze_stack:
            maze_stack.append((cur_loc[0] + 1, cur_loc[1]))
        if cur_loc[0] - 1 >= 0 and maze[cur_loc[0] - 1][cur_loc[1]] == 0 and (cur_loc[0] - 1, cur_loc[1]) not in maze_stack:
            maze_stack.append((cur_loc[0] - 1, cur_loc[1]))
        if cur_loc[1] + 1 < maze_size[1] and maze[cur_loc[0]][cur_loc[1] + 1] == 0 and (cur_loc[0], cur_loc[1] + 1) not in maze_stack:
            maze_stack.append((cur_loc[0], cur_loc[1] + 1))
        if cur_loc[1] - 1 >= 0 and maze[cur_loc[0]][cur_loc[1] - 1] == 0 and (cur_loc[0], cur_loc[1] - 1) not in maze_stack:
            maze_stack.append((cur_loc[0], cur_loc[1] - 1))

        # Get the next thing to check
        next_spot = maze_stack.pop()

        # Go back through past moves until at necessary position to check
        while abs(next_spot[0] - cur_loc[0]) + abs(next_spot[1] - cur_loc[1]) > 1:
            last_move = move_list.pop()
            if last_move == 'up':
                action = 'down'
                cur_loc[1] += 1
            elif last_move == 'down':
                action = 'up'
                cur_loc[1] -= 1
            elif last_move == 'right':
                action = 'left'
                cur_loc[0] -= 1
            elif last_move == 'left':
                action = 'right'
                cur_loc[0] += 1

            # Move back, tracing back the path already travelled
            resp = requests.post(url + '/game?token=' + access_token, data = {'action': action})
            body = resp.json()

        # Now, one move away from the place to check. Attempt a move in that direction
        if next_spot[0] != cur_loc[0]:
            action = 'right' if next_spot[0] > cur_loc[0] else 'left'
            cur_loc[0] += 1 if next_spot[0] > cur_loc[0] else -1
        else:
            action = 'down' if next_spot[1] > cur_loc[1] else 'up'
            cur_loc[1] += 1 if next_spot[1] > cur_loc[1] else -1
        move_list.append(action)
            
        resp = requests.post(url + '/game?token=' + access_token, data = {'action': action})
        body = resp.json()

        maze[next_spot[0]][next_spot[1]] = 1    # Mark current spot as visited

        if body['result'] < 0:
            if action == 'right':
                cur_loc[0] -= 1
            elif action == 'left':
                cur_loc[0] += 1
            elif action == 'up':
                cur_loc[1] += 1
            elif action == 'down':
                cur_loc[1] -= 1
            move_list.pop()

    # Maze Solved, Get New Maze
    print(f"\nMAZE SOLVED, MOVING ON TO NEW MAZE\nPrevious Maze Solution\n{move_list}\n")
    new_resp = requests.get(url + '/game?token=' + access_token)
    new_body = new_resp.json()
    body['result'] = 0

print(f"\nFinished All Mazes, Here is status: {new_body['status']}\n")