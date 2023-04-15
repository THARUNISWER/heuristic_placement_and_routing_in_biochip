from new_row import Row
import csv


def minimum(list1, list2):
    if list2[1][1] < list1[1][1]:
        return list2
    return list1


class NewPlace:
    rows = []
    ROW_SIZE = 10
    STORAGE_SIZE = 10
    N = 0

    def __init__(self, n):
        self.N = n
        self.rows = [Row(i, self.ROW_SIZE) for i in range(0, n)]
        self.store = [Row(0, self.STORAGE_SIZE), Row(1, self.STORAGE_SIZE)]

    def insert(self, oper, V):
        best_fit = None
        min_space = None
        for id in range(self.N):
            ans = self.rows[id].search(V)
            if ans[0] != -1:
                if best_fit is None:
                    best_fit = [id, ans]
                else:
                    best_fit = minimum(best_fit, [id, ans])

            if self.rows[id].tot_space >= V:
                if min_space is None:
                    min_space = [id, self.rows[id].tot_space]
                else:
                    if min_space[1] > self.rows[id].tot_space:
                        min_space = [id, self.rows[id].tot_space]

        if best_fit is None:
            if min_space is None:
                if V > self.ROW_SIZE:
                    print("Module: " + str(oper) + " is too big")
                    return -2
                print(
                    "No space in any row for operation: " + str(oper[0]) + " and module: " + str(oper[1]))
                return -1
            else:
                self.rows[min_space[0]].compact()
                ans = self.rows[min_space[0]].search(V)
                best_fit = [min_space[0], ans]

        st_pos = self.rows[best_fit[0]].insert(oper, V, best_fit[1][0])
        stat = (st_pos, best_fit[0])
        return stat

    def delete(self, oper, row_id):
        st_pos = self.rows[row_id].delete(oper)

        if st_pos == -1:
            print("Invalid module id")
            return 0

        stat = (st_pos, row_id)
        return stat

    def storage(self, mod_pos, V_s, stor_mod_id):
        best_fit = None
        min_space = None
        for id in range(0, 1):
            ans = self.store[id].search(V_s)
            if ans[0] != -1:
                if best_fit is None:
                    best_fit = [id, ans]
                else:
                    best_fit = minimum(best_fit, [id, ans])

            if self.store[id].tot_space >= V_s:
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
                ans = self.store[min_space[0]].search(V_s)
                best_fit = [min_space[0], ans]

        st_pos = self.store[best_fit[0]].insert(stor_mod_id, V_s, best_fit[1][0])
        stat = (st_pos, best_fit[0])
        return stat

    def del_store(self, mod_pos, stor_mod_id, stor_row):
        st_pos = self.store[stor_row].delete(stor_mod_id)

        if st_pos == -1:
            print("Invalid module id")
            return 0

        stat = (st_pos, stor_row)
        return stat

    def waste(self, mod_pos, V_w):
        print(mod_pos)
        return

    def display(self, cur_time):
        for row in self.rows:
            print(str(row.id) + " row_frag: " + str(row.frag))
            print(str(row.id) + " row_place: " + str(row.place))

        for row in self.store:
            print(str(row.id) + " store_frag: " + str(row.frag))
            print(str(row.id) + " store_place: " + str(row.place))

        file_name = "./placement/" + str(cur_time) + "_place.csv"

        place_list = []
        for row in self.rows:
            list_row = ['-' for i in range(0, row.row_size)]
            for x in row.place:
                for i in range(int(x['st_position']), int(x['end_position'])):
                    list_row[i] = x['module_id']

            place_list.append(list_row)

        with open(file_name, "w+", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(place_list)






