
class Box:
    id = 0
    WIDTH = 5
    module_id = -1

    def __init__(self, id):
        self.id = id
        self.module_id = -1

    def insert(self, module_id, V):
        if self.module_id != -1:
            return 0
        if self.WIDTH < V:
            print("Oversize module")
            return 1

        self.module_id = module_id
        return 2

    def delete(self, module_id):
        if self.module_id == -1:
            print("Empty before")
            return 0

        if self.module_id != module_id:
            return 1

        self.module_id = -1
        return 2


class OldPlace:
    boxes = []
    N = 0

    def __init__(self, n):
        self.N = n
        self.boxes = [Box(i) for i in range(0, n)]

    def insert(self, module_id, V):
        for box in self.boxes:
            if box.insert(module_id, V) == 2:
                return 1

        return 0

    def delete(self, module_id):
        for box in self.boxes:
            if box.delete(module_id) == 2:
                return 1
        return 0

    def display(self):
        for box in self.boxes:
            print("id: " + str(box.id) + " module: " + str(box.module_id))




