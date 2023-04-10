from new_row import Row
import csv


def minimum(list1, list2):
    if list2[1][1] < list1[1][1]:
        return list2
    return list1


class NewPlace:
    rows = []
    N = 0

    def __init__(self, n):
        self.N = n
        self.rows = [Row(i) for i in range(0, n)]

    def insert(self, module_id, V):
        best_fit = None
        min_space = None
        for id in range(len(self.rows)):
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
                print("No space in any row")
                return -1
            else:
                self.rows[min_space[0]].compact()
                ans = self.rows[min_space[0]].search(V)
                best_fit = [min_space[0], ans]

        self.rows[best_fit[0]].insert(module_id, V, best_fit[1][0])
        return best_fit[0]

    def delete(self, module_id, row_id):
        stat = self.rows[row_id].delete(module_id)

        if stat == 0:
            print("Invalid module id")
            return 0

        return 1

    def display(self, cur_time):
        for row in self.rows:
            print(str(row.id) + " row_frag: " + str(row.frag))
            print(str(row.id) + " row_place: " + str(row.place))

        file_name = "./placement/" + str(cur_time) + "_place.csv"

        place_list = []
        for row in self.rows:
            list_row = ['-' for i in range(0, row.ROW_SIZE)]
            for x in row.place:
                for i in range(int(x['st_position']), int(x['end_position'])):
                    list_row[i] = x['module_id']

            place_list.append(list_row)

        with open(file_name, "w+", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(place_list)






