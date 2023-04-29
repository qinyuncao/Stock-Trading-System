import shutil


def syncronization():
    # When order server starts, we synchronize their own database file with the latest one
    # The latest database file contains the most data
    file_list = ['order1.txt', 'order2.txt', 'order3.txt']
    lines_len = []
    for file in file_list:
        with open(file, 'r') as f:
            lines = f.readlines()
        lines_len.append(len(lines))
    # Get the index of the latest file
    i = lines_len.index(max(lines_len))
    for j in range(len(file_list)):
        if j != i:
            open(file_list[j], 'w').close()
            shutil.copy(file_list[i], file_list[j])

syncronization()