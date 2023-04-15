import csv
from new_place import NewPlace

datafile = "input_dag_2.csv"
storage_file_path = "storage.csv"
data = list(csv.reader(open(datafile)))
stor_data = list(csv.reader(open(storage_file_path)))
sorted(data, key=lambda x: x[10])


N = NewPlace(2)
curr_data = {}
curr_store_data = {}
max_start_time = int(data[len(data)-1][10])
max_end_time = int(data[len(data)-1][11])
curr_pos = 1
stor_pos = 1
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
            for i in range(stor_pos, len(stor_data)):
                temp = int(stor_data[i][4])
                temp += dev
                stor_data[i][4] = str(temp)
                temp = int(stor_data[i][5])
                temp += dev
                stor_data[i][5] = str(temp)
            return t


while True:

    print(str(cur_time))
    # deletion and storage
    if str(cur_time) in curr_data.keys():
        temp_st = {}
        for x in curr_data[str(cur_time)]:
            stat = N.delete((x[0], x[9]), int(x[12]))
            temp_st[str(x[0])] = (stat, x[8], x[9])
        while stor_pos < len(stor_data) and str(stor_data[stor_pos][1]) in temp_st.keys():
            # print(str([temp_st[str(stor_data[stor_pos][1])][2], stor_data[stor_pos][0]]))
            store_row_id = N.storage(temp_st[str(stor_data[stor_pos][1])][0], 2*int(stor_data[stor_pos][3]), (stor_data[stor_pos][0], temp_st[str(stor_data[stor_pos][1])][2]))
            waste_fluid = 2*int(temp_st[str(stor_data[stor_pos][1])][1]) - 2*int(stor_data[stor_pos][3])
            N.waste(temp_st[str(stor_data[stor_pos][1])][0], waste_fluid)
            stor_data[stor_pos][6] = str(store_row_id[1])
            stor_data[stor_pos][7] = str(temp_st[str(stor_data[stor_pos][1])][2])

            if str(stor_data[stor_pos][2]) not in curr_store_data.keys():
                curr_store_data[str(stor_data[stor_pos][2])] = []
            curr_store_data[str(stor_data[stor_pos][2])].append(stor_data[stor_pos])
            stor_pos += 1

    # insertion and removal of storage
    while curr_pos < len(data) and str(data[curr_pos][10]) == str(cur_time):
        stat = N.insert((data[curr_pos][0], data[curr_pos][9]), 2*int(data[curr_pos][8]))  # take care on module size
        if stat == -2:
            data[curr_pos][12] = "null"
            curr_pos += 1
            break
        if stat == -1:
            print("Shifting time..")
            t = time_compact()
            max_start_time = int(data[len(data) - 1][10])
            max_end_time = int(data[len(data) - 1][11])
            break

        data[curr_pos][12] = str(stat[1])

        if str(data[curr_pos][11]) not in curr_data.keys():
            curr_data[str(data[curr_pos][11])] = []
        curr_data[str(data[curr_pos][11])].append(data[curr_pos])

        if str(data[curr_pos][0]) in curr_store_data.keys():
            for x in curr_store_data[str(data[curr_pos][0])]:
                N.del_store(stat, (x[0], x[7]), int(x[6]))

        curr_pos += 1

    N.display(cur_time)
    cur_time += 1
    if cur_time > max_start_time:
        break

with open("mod_input_dag.csv", "w+", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)


# 1. time compact is only available for rows and not for storage
# 2. for insertion of same modules in adjacent timestamps, direct routing must be performed
