from new_row import Row
from visualizer import Visuals
import csv
import copy


def minimum(list1, list2):
    if list2[1][1] < list1[1][1]:
        return list2
    return list1


class NewPlace:
    csv_symbols = {
        'routing_path': 'R',
        'guard_ring': 'G',
        'row': 'M',
        'storage': 'S',
        'reservoir': 'D',
        'waste_reservoir': 'W',
        'operation': 'O'
    }
    V = Visuals(csv_symbols)

    def __init__(self, n, row_size, row_width):
        self.N = n
        self.ROW_SIZE = row_size
        if row_size < 6:
            print("Too small row size to accommodate 6 reservoirs and 2 waste reservoirs")
            return
        self.ROW_WIDTH = row_width
        self.GRID_WIDTH = 4 + (8+row_width)*n
        self.rows = [Row(i, self.ROW_SIZE) for i in range(0, n)]
        self.store = [Row(0, self.GRID_WIDTH), Row(1, self.GRID_WIDTH)]
        self.reservoir = {
            # (i,j)
            "D1": (0, self.ROW_WIDTH + 4),
            "D2": (0, self.ROW_WIDTH + 8),
            "D3": (0, self.ROW_WIDTH + 12),
            "D4": (self.GRID_WIDTH - 1, self.ROW_WIDTH + 4),
            "D5": (self.GRID_WIDTH - 1, self.ROW_WIDTH + 8),
            "D6": (self.GRID_WIDTH - 1, self.ROW_WIDTH + 12)
        }
        self.waste_reservoir = {
            # (i,j)
            "W1": (0, self.ROW_WIDTH + 16),
            "W2": (self.GRID_WIDTH - 1, self.ROW_WIDTH + 16)
        }

    def insert(self, oper, V):
        best_fit = None
        min_space = None
        for id in range(self.N):
            ans = self.rows[id].search(V + 2)
            if ans[0] != -1:
                if best_fit is None:
                    best_fit = [id, ans]
                else:
                    best_fit = minimum(best_fit, [id, ans])

            if self.rows[id].tot_space >= V + 2:
                if min_space is None:
                    min_space = [id, self.rows[id].tot_space]
                else:
                    if min_space[1] > self.rows[id].tot_space:
                        min_space = [id, self.rows[id].tot_space]

        if best_fit is None:
            if min_space is None:
                if V + 2 > self.ROW_SIZE:
                    print("Module: " + str(oper) + " is too big to fit in any row")
                    return -2
                print(
                    "No space in any row for operation: " + str(oper[0]) + " and module: " + str(oper[1]))
                return -1
            else:
                self.rows[min_space[0]].compact()
                ans = self.rows[min_space[0]].search(V + 2)
                best_fit = [min_space[0], ans]

        st_pos = self.rows[best_fit[0]].insert(oper, V, best_fit[1][0])
        stat = (st_pos, best_fit[0])
        return stat

    def delete(self, oper, row_id):
        st_pos = self.rows[row_id].delete(oper)
        pad = (self.csv_symbols['guard_ring'], oper[0])
        self.rows[row_id].delete(pad)
        if st_pos == -1:
            print("Invalid module id")
            return 0

        stat = (st_pos, row_id)
        return stat

    def storage(self, mod_pos, V_s, stor_mod_id):
        best_fit = None
        min_space = None
        for id in range(0, 1):
            ans = self.store[id].search(V_s + 2)
            if ans[0] != -1:
                if best_fit is None:
                    best_fit = [id, ans]
                else:
                    best_fit = minimum(best_fit, [id, ans])

            if self.store[id].tot_space >= V_s + 2:
                if min_space is None:
                    min_space = [id, self.store[id].tot_space]
                else:
                    if min_space[1] > self.store[id].tot_space:
                        min_space = [id, self.store[id].tot_space]

        if best_fit is None:
            if min_space is None:
                print("No space in any row for operation: " + str(stor_mod_id[0]) + " and module: " + str(stor_mod_id[1]))
                return -1
            else:
                self.store[min_space[0]].compact()
                ans = self.store[min_space[0]].search(V_s + 2)
                best_fit = [min_space[0], ans]

        st_pos = self.store[best_fit[0]].insert(stor_mod_id, V_s, best_fit[1][0])
        stat = (st_pos, best_fit[0])

        # routing needed
        print(str(V_s) + ' volumes is sent as storage from module at ' + str(mod_pos) + ' to storage_module at ' + str(stat))
        return stat

    def del_store(self, mod_pos, stor_mod_id, stor_row, V_d):
        st_pos = self.store[stor_row].delete(stor_mod_id)
        pad = (self.csv_symbols['guard_ring'], stor_mod_id[0])
        self.store[stor_row].delete(pad)
        if st_pos == -1:
            print("Invalid module id")
            return 0

        stat = (st_pos, stor_row)

        # routing needed
        print(str(V_d) + ' volumes is sent as storage from storage module at ' + str(stat) + ' to module at ' + str(mod_pos))
        return stat

    def waste(self, mod_pos, V_w):
        # mod_pos = (starting position of module(x), row id of module(y))
        # (j,i) i.e. (x,y)
        # routing needed
        print(str(V_w) + ' volumes is sent as waste from module ' + str(mod_pos))
        return

    def display(self, cur_time, output_csv_dir, output_jpg_dir):
        for row in self.rows:
            row.display()

        for st in self.store:
            st.display()

        csv_file_name = output_csv_dir + "/" + str(cur_time) + "_place.csv"
        jpg_file_name = output_jpg_dir + "/" + str(cur_time) + "_place.jpg"

        place_list = []
        guard_row = [self.csv_symbols['guard_ring'] for i in range(0, self.ROW_SIZE + 2*(8 + self.ROW_WIDTH))]
        routing_path = [self.csv_symbols['routing_path'] for i in range(0, self.ROW_SIZE + 2*(8 + self.ROW_WIDTH))]

        # top 2 routing rows
        place_list.append(copy.deepcopy(routing_path))
        place_list.append(copy.deepcopy(routing_path))

        # keeping modules in rows and creating rows
        for row in self.rows:
            list_row = [self.csv_symbols['row'] for i in range(0, self.ROW_SIZE + 2*(8 + self.ROW_WIDTH))]
            list_row[self.ROW_WIDTH + 6] = self.csv_symbols['guard_ring']
            list_row[self.ROW_WIDTH + 7] = self.csv_symbols['guard_ring']
            for x in row.place:
                for i in range(self.ROW_WIDTH + 8 + int(x['st_position']), self.ROW_WIDTH + 8 + int(x['end_position'])):
                    list_row[i] = x['module_id'][0]
            list_row[self.ROW_WIDTH + self.ROW_SIZE + 8] = self.csv_symbols['guard_ring']
            list_row[self.ROW_WIDTH + self.ROW_SIZE + 9] = self.csv_symbols['guard_ring']

            place_list.append(copy.deepcopy(routing_path))
            place_list.append(copy.deepcopy(routing_path))
            place_list.append(copy.deepcopy(guard_row))
            place_list.append(copy.deepcopy(guard_row))

            for _ in range(self.ROW_WIDTH):
                place_list.append(copy.deepcopy(list_row))

            place_list.append(copy.deepcopy(guard_row))
            place_list.append(copy.deepcopy(guard_row))
            place_list.append(copy.deepcopy(routing_path))
            place_list.append(copy.deepcopy(routing_path))

        # last 2 routing rows
        place_list.append(copy.deepcopy(routing_path))
        place_list.append(copy.deepcopy(routing_path))

        # placing storage rows as columns
        for x in self.store[0].place:
            for i in range(int(x['st_position']), int(x['end_position'])):
                for k in range(self.ROW_WIDTH):
                    s = '(' + ', '.join(x['module_id']) + ')'
                    place_list[i][k] = s
                for k in range(self.ROW_WIDTH, self.ROW_WIDTH + 2):
                    place_list[i][k] = self.csv_symbols['guard_ring']
                for k in range(self.ROW_WIDTH + 2, self.ROW_WIDTH + 6):
                    place_list[i][k] = self.csv_symbols['routing_path']

        for x in self.store[0].frag:
            for i in range(int(x['st_position']), int(x['end_position'])):
                for k in range(0, self.ROW_WIDTH):
                    place_list[i][k] = self.csv_symbols['storage']
                for k in range(self.ROW_WIDTH, self.ROW_WIDTH + 2):
                    place_list[i][k] = self.csv_symbols['guard_ring']
                for k in range(self.ROW_WIDTH + 2, self.ROW_WIDTH + 6):
                    place_list[i][k] = self.csv_symbols['routing_path']

        for x in self.store[1].place:
            offset = self.ROW_WIDTH + 8 + self.ROW_SIZE
            for i in range(int(x['st_position']), int(x['end_position'])):
                for k in range(offset + 8, offset + 8 + self.ROW_WIDTH):
                    s = '(' + ', '.join(x['module_id']) + ')'
                    place_list[i][k] = s
                for k in range(offset + 6, offset + 8):
                    place_list[i][k] = self.csv_symbols['guard_ring']
                for k in range(offset + 2, offset + 6):
                    place_list[i][k] = self.csv_symbols['routing_path']

        for x in self.store[1].frag:
            offset = self.ROW_WIDTH + 8 + self.ROW_SIZE
            for i in range(int(x['st_position']), int(x['end_position'])):
                for k in range(offset + 8, offset + 8 + self.ROW_WIDTH):
                    place_list[i][k] = self.csv_symbols['storage']
                for k in range(offset + 6, offset + 8):
                    place_list[i][k] = self.csv_symbols['guard_ring']
                for k in range(offset + 2, offset + 6):
                    place_list[i][k] = self.csv_symbols['routing_path']

        # placing reservoirs
        for key in self.reservoir:
            (i, j) = self.reservoir[key]
            place_list[i][j] = key
            place_list[i][j+1] = key

        for key in self.waste_reservoir:
            (i, j) = self.waste_reservoir[key]
            place_list[i][j] = key
            place_list[i][j+1] = key

        with open(csv_file_name, "w+", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(place_list)

        self.V.visualize(csv_file_name, jpg_file_name)






