with open('data.dat', 'r') as file:
    block_num = -1
    block_lines = []
    for line in file:
        flag = True if line.startswith('---') or line.startswith('\t---') else False
        if not flag:
            block_lines.append(line)
        if flag:
            with open(f'trajs\\block_{block_num}.txt', 'w') as block_file:
                block_file.writelines(block_lines)
            block_num += 1
            block_lines = []
