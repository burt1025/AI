import random
file_number = 0
line_split = '\n'
for grid_number in range(6, 8, 1):
    for trap_number in range(grid_number / 2, grid_number+1, 1):
        animal_number = random.randint(1, min(100, grid_number*2)+1)
        file = open('input' + str(file_number) + '.txt', 'w+')
        file.write(str(grid_number) + line_split)
        file.write(str(trap_number) + line_split)
        file.write(str(animal_number) + line_split)
        file.write('dfs' + line_split)
        for loop in range(animal_number):
            r = random.randint(0, grid_number-1)
            c = random.randint(0, grid_number-1)
            file.write(str(r)+','+str(c)+line_split)
        file_number += 1