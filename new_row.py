
class Row:

    def __init__(self, id: int, size: int):
        self.id = id
        self.place = []
        self.row_size = size
        self.frag = [{"st_position": 0, "end_position": self.row_size, "area": self.row_size}]
        self.tot_space = self.row_size

    # runs binary search to find best fit space in each row
    def search(self, V):
        first = 0
        last = len(self.frag) - 1
        ans = -1

        while first <= last:
            mid = int((first + last)/2)
            if self.frag[mid]["area"] < V:
                first = mid + 1
            else:
                last = mid - 1
                ans = mid

        if ans == -1:
            return [ans, -1]

        return [ans, self.frag[ans]["area"]]

    def compact(self):
        self.frag = [{"st_position": self.row_size - self.tot_space, "end_position": self.row_size, "area": self.row_size}]

        curr_pos = 0
        for i in range(0, len(self.place)):
            if curr_pos != self.place[i]["st_position"]:
                v = self.place[i]["end_position"] - self.place[i]["st_position"]
                self.place[i]["st_position"] = curr_pos
                self.place[i]["end_position"] = curr_pos + v

            curr_pos = self.place[i]["end_position"]

    def delete(self, oper):
        module = None
        st_pos = None
        for index in range(len(self.place)):
            if self.place[index]['module_id'] == oper:
                module = self.place[index]
                st_pos = self.place[index]["st_position"]
                del self.place[index]
                break

        if module is None:
            return -1

        self.tot_space += module["end_position"] - module["st_position"]
        for ind in range(len(self.frag)):
            if self.frag[ind]["end_position"] == module["st_position"]:
                module["st_position"] = self.frag[ind]["st_position"]
                del self.frag[ind]
                break

        for ind in range(len(self.frag)):
            if self.frag[ind]["st_position"] == module["end_position"]:
                module["end_position"] = self.frag[ind]["end_position"]
                del self.frag[ind]
                break

        del module["module_id"]
        module["area"] = module["end_position"] - module["st_position"]

        ind = len(self.frag)
        for i in range(0, len(self.frag)):
            if self.frag[i]["area"] >= module["area"]:
                ind = i
                break
        self.frag.insert(ind, module)
        return st_pos

    def insert(self, oper, V, frag_id):
        # padding
        if self.frag[frag_id]["st_position"] + V + 2 > self.frag[frag_id]["end_position"]:
            print("Invalid insertion")
            return -1

        self.tot_space -= (V + 2)
        new_mod = {"module_id": oper, "st_position": self.frag[frag_id]["st_position"], "end_position": self.frag[frag_id]["st_position"] + V}
        pad_mod = {"module_id": ('G', oper[0]), "st_position": self.frag[frag_id]["st_position"] + V, "end_position": self.frag[frag_id]["st_position"] + V + 2}
        frag_mod = self.frag[frag_id]
        del self.frag[frag_id]
        if frag_mod["end_position"] != pad_mod["end_position"]:
            frag_mod["st_position"] = pad_mod["end_position"]
            frag_mod["area"] = frag_mod["end_position"] - frag_mod["st_position"]
            ind = len(self.frag)
            for i in range(0, len(self.frag)):
                if self.frag[i]["area"] >= frag_mod["area"]:
                    ind = i
                    break
            self.frag.insert(ind, frag_mod)

        ind = len(self.place)
        for i in range(0, len(self.place)):
            if self.place[i]["st_position"] > new_mod["st_position"]:
                ind = i
                break
        self.place.insert(ind, new_mod)
        self.place.insert(ind + V, pad_mod)
        return new_mod["st_position"]

    def display(self):
        print(str(self.id) + " row_frag: " + str(self.frag))
        print(str(self.id) + " row_place: " + str(self.place))

