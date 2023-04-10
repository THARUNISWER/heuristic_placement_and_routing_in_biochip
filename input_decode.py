import csv
from new_place import NewPlace

datafile = "input_dag.csv"
data = list(csv.reader(open(datafile)))
sorted(data, key=lambda x: x[10])


N = NewPlace(1)
curr_data = {}
max_start_time = int(data[len(data)-1][10])
max_end_time = int(data[len(data)-1][11])
curr_pos = 1
cur_time = 0


def time_compact():
    for t in range(cur_time, max_end_time):
        if str(t) in curr_data.keys():
            dev = t - cur_time
            for i in range(curr_pos, len(data)):
                temp = int(data[i][10])
                temp += dev
                data[i][10] = str(temp)
                temp = int(data[i][11])
                temp += dev
                data[i][11] = str(temp)
            return t


while True:

    if str(cur_time) in curr_data.keys():
        for x in curr_data[str(cur_time)]:
            N.delete(x[9], int(x[12]))

    print(str(cur_time))
    while curr_pos < len(data) and str(data[curr_pos][10]) == str(cur_time):
        stat = N.insert(data[curr_pos][9], int(data[curr_pos][8]))  # take care on module size
        if stat == -1:
            t = time_compact()
            max_start_time = int(data[len(data) - 1][10])
            max_end_time = int(data[len(data) - 1][11])
            break

        data[curr_pos][12] = str(stat)

        if str(data[curr_pos][11]) not in curr_data.keys():
            curr_data[str(data[curr_pos][11])] = []
        curr_data[str(data[curr_pos][11])].append(data[curr_pos])
        curr_pos += 1

    N.display(cur_time)
    cur_time += 1
    if cur_time > max_start_time + 1:
        break

with open("mod_input_dag.csv", "w+", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)


