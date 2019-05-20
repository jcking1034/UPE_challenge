import requests

# Get Access Token
url, id = 'http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com', '205125796'
access_token = requests.post(url + '/session', data = {'uid': id}).json()['token']
print(f'access token: {access_token}')

move_dict = {   # Direction: (X(0) or Y(1), Positive or Negative, Opposite Direction)
    'up': (1, -1, 'down'),
    'down': (1, +1, 'up'),
    'right': (0, +1, 'left'),
    'left': (0, -1, 'right')
}

for i in range(5):  # Need to solve 5 Mazes
    new_body = requests.get(url + '/game?token=' + access_token).json()    # Get new game

    # Initialize Maze Size, Current Location, Visited Maze array, Move List (solution), Move Stack (locations to visit)
    maze_size = new_body['size'][0], new_body['size'][1]
    cur_loc = [new_body['cur_loc'][0], new_body['cur_loc'][1]]
    maze, move_list, maze_stack = [[1 if i == cur_loc[1] and j == cur_loc[0] else 0 for i in range(maze_size[1])] for j in range(maze_size[0])], [], []
    print(f'Initial location: {cur_loc[0]} {cur_loc[1]}\nMaze Size: {maze_size[0]} {maze_size[1]}')

    # Add locations to check to maze_stack
    while True:
        if cur_loc[0] + 1 < maze_size[0] and maze[cur_loc[0] + 1][cur_loc[1]] == 0 and (cur_loc[0] + 1, cur_loc[1]) not in maze_stack:
            maze_stack.append((cur_loc[0] + 1, cur_loc[1]))
        if cur_loc[0] - 1 >= 0 and maze[cur_loc[0] - 1][cur_loc[1]] == 0 and (cur_loc[0] - 1, cur_loc[1]) not in maze_stack:
            maze_stack.append((cur_loc[0] - 1, cur_loc[1]))
        if cur_loc[1] + 1 < maze_size[1] and maze[cur_loc[0]][cur_loc[1] + 1] == 0 and (cur_loc[0], cur_loc[1] + 1) not in maze_stack:
            maze_stack.append((cur_loc[0], cur_loc[1] + 1))
        if cur_loc[1] - 1 >= 0 and maze[cur_loc[0]][cur_loc[1] - 1] == 0 and (cur_loc[0], cur_loc[1] - 1) not in maze_stack:
            maze_stack.append((cur_loc[0], cur_loc[1] - 1))

        # Get the next thing to check, go back through past moves until at necessary position to check
        next_spot = maze_stack.pop()
        while abs(next_spot[0] - cur_loc[0]) + abs(next_spot[1] - cur_loc[1]) > 1:
            last_move = move_list.pop()
            action = move_dict[last_move][2]
            cur_loc[move_dict[last_move][0]] -= move_dict[last_move][1]
            body = requests.post(url + '/game?token=' + access_token, data = {'action': action}).json()

        # Now, one move away from the place to check. Attempt a move in that direction
        if next_spot[0] != cur_loc[0]:  action = 'right' if next_spot[0] > cur_loc[0] else 'left'
        else:                           action = 'down' if next_spot[1] > cur_loc[1] else 'up'
        body = requests.post(url + '/game?token=' + access_token, data = {'action': action}).json()
        maze[next_spot[0]][next_spot[1]] = 1    # Mark current spot as visited

        # If move good, update current location and add move to list
        if body['result'] == 0:     
            cur_loc[move_dict[action][0]] += move_dict[action][1]
            move_list.append(action)
        elif body['result'] == 1: break

    print(f"\nMAZE SOLVED\nPrevious Maze Solution\n{move_list}\n")

print(f"\nFinished All Mazes")