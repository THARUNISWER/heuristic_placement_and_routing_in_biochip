import csv
from new_place import NewPlace
import os
import shutil
import sys

# path names
datafile_path = "./inputs/t1/scheduled_csv_files/t1_asap.csv"
storage_file_path = "./inputs/t1/storage_csv_files/t1_ASAP_storage.csv"
modified_datafile_path = "mod_input_dag.csv"
modified_storage_path = "mod_input_store.csv"
output_csv_dir = "./placement"
output_jpg_dir = "./placement_jpg"

# input parameters
no_of_rows = 2
row_width = 4
row_size = 22  # min row size must be 6 to accommodate 6 reservoirs and 2 waste reservoirs

# making directories and files ready for processing
if os.path.isdir(output_csv_dir):
    shutil.rmtree(output_csv_dir)
if os.path.isdir(output_jpg_dir):
    shutil.rmtree(output_jpg_dir)

os.mkdir(output_csv_dir)
os.mkdir(output_jpg_dir)

ini_data = list(csv.reader(open(datafile_path)))

# processing of files to remove unwanted data and to sort it
data = []
for d in ini_data:
    if d[0][0] != 'R' and d[0][0] != '-':
        data.append(d)
no_of_op = len(data) + 1
if storage_file_path == "":
    s_data = []
    stor_data = []
else:
    s_data = list(csv.reader(open(storage_file_path)))
    s_data[0].append('R_id')
    s_data[0].append('pos')
    s_data[0].append('M_id')
    for i in range(1, len(s_data)):
        s_data[i].append('-')
        s_data[i].append('-')
        s_data[i].append('-')
    stor_data = s_data[1:]

data = sorted(data, key=lambda x: int(x[no_of_op + 2]))
stor_data = sorted(stor_data, key=lambda x: int(x[4]))

# Heuristic Placement processing begins
# Variable declarations
N = NewPlace(no_of_rows, row_size, row_width)
curr_data = {}
curr_store_data = {}
max_start_time = int(data[len(data)-1][no_of_op + 2])
max_end_time = int(data[len(data)-1][no_of_op + 3])
curr_pos = 0
stor_pos = 1
cur_time = 0


# function to perform time shift in the absence of space in chip
def time_shift(cat):
    dev = 0
    new_time = cur_time
    for t in range(cur_time, max_end_time):
        if cat == 1 and str(t) in curr_data.keys():
            dev = t - cur_time
            break
        if cat == 2 and str(t) in curr_store_data.keys():
            dev = t - cur_time
            break
    for i in range(curr_pos, len(data)):
        temp = int(data[i][no_of_op + 2])
        temp += dev
        data[i][no_of_op + 2] = str(temp)
        temp = int(data[i][no_of_op + 3])
        temp += dev
        data[i][no_of_op + 3] = str(temp)
    for i in range(stor_pos, len(stor_data)):
        temp = int(stor_data[i][4])
        temp += dev
        stor_data[i][4] = str(temp)
        temp = int(stor_data[i][5])
        temp += dev
        stor_data[i][5] = str(temp)


# loop to initiate placement in each timestamp
while True:

    print(str(cur_time))

    # removal in rows and insertion in storage
    if str(cur_time) in curr_data.keys():
        temp_st = {}
        for x in curr_data[str(cur_time)]:
            stat = N.delete((x[0], x[0]), int(x[no_of_op + 4]))
            temp_st[str(x[0])] = (stat, x[no_of_op], x[no_of_op + 1])

        del curr_data[str(cur_time)]
        while stor_pos < len(stor_data) and str(stor_data[stor_pos][1]) in temp_st.keys():
            store_row_id = N.storage(temp_st[str(stor_data[stor_pos][1])][0], 2*int(stor_data[stor_pos][3]), (stor_data[stor_pos][0], stor_data[stor_pos][1]))
            if store_row_id == -1:
                print("Shifting time due to lack of storage..")
                time_shift(2)
                max_start_time = int(data[len(data) - 1][no_of_op + 2])
                max_end_time = int(data[len(data) - 1][no_of_op + 3])
                break
            waste_fluid = 2*int(temp_st[str(stor_data[stor_pos][1])][1]) - 2*int(stor_data[stor_pos][3])
            N.waste(temp_st[str(stor_data[stor_pos][1])][0], waste_fluid)
            stor_data[stor_pos][6] = str(store_row_id[1])
            stor_data[stor_pos][7] = str(store_row_id[0])
            stor_data[stor_pos][8] = str(temp_st[str(stor_data[stor_pos][1])][2])

            if str(stor_data[stor_pos][2]) not in curr_store_data.keys():
                curr_store_data[str(stor_data[stor_pos][2])] = []
            curr_store_data[str(stor_data[stor_pos][2])].append(stor_data[stor_pos])
            stor_pos += 1

    # insertion in rows and removal of storage
    while curr_pos < len(data) and str(data[curr_pos][no_of_op + 2]) == str(cur_time):
        stat = N.insert((data[curr_pos][0], data[curr_pos][0]), 2*int(data[curr_pos][no_of_op]))  # take care on module size
        if stat == -2:
            print("Stopping placement..")
            sys.exit(0)

        if stat == -1:
            print("Shifting time due to lack of space in rows..")
            time_shift(1)
            max_start_time = int(data[len(data) - 1][no_of_op + 2])
            max_end_time = int(data[len(data) - 1][no_of_op + 3])
            break

        data[curr_pos][no_of_op + 4] = str(stat[1])
        data[curr_pos][no_of_op + 5] = str(stat[0])

        if str(data[curr_pos][no_of_op + 3]) not in curr_data.keys():
            curr_data[str(data[curr_pos][no_of_op + 3])] = []
        curr_data[str(data[curr_pos][no_of_op + 3])].append(data[curr_pos])

        if str(data[curr_pos][0]) in curr_store_data.keys():
            for x in curr_store_data[str(data[curr_pos][0])]:
                st = N.del_store(stat, (x[0], x[1]), int(x[6]), x[3])
                if st == 0:
                    print("Invalid module id: " + str((x[0], x[7])) + " storage number: " + str(x[6]))
                    sys.exit()
            del curr_store_data[str(data[curr_pos][0])]

        curr_pos += 1

    N.display(cur_time, output_csv_dir, output_jpg_dir)
    cur_time += 1
    if cur_time > max_end_time:
        break


# storing modified data (time shift could have happened)
with open(modified_datafile_path, "w+", newline="") as f:
    writer = csv.writer(f)
    data.insert(0, ini_data[0])
    for d in ini_data:
        if d[0][0] == 'R':
            data.append(d)
    writer.writerows(data)

with open(modified_storage_path, "w+", newline="") as f:
    writer = csv.writer(f)
    if storage_file_path != "":
        stor_data.insert(0, s_data[0])
    writer.writerows(stor_data)