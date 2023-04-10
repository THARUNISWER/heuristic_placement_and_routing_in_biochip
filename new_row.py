import bisect
from PIL import Image, ImageDraw, ImageFont
import random

class Row:
    id = 0
    place = []
    frag = []
    ROW_SIZE = 10
    tot_space = 10

    def __init__(self, id: int):
        self.id = id
        self.place = []
        self.frag = [{"st_position": 0, "end_position": self.ROW_SIZE, "area": self.ROW_SIZE}]
        self.tot_space = self.ROW_SIZE

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
        self.frag = [{"st_position": self.ROW_SIZE - self.tot_space, "end_position": self.ROW_SIZE, "area": self.ROW_SIZE}]

        curr_pos = 0
        for i in range(0, len(self.place)):
            if curr_pos != self.place[i]["st_position"]:
                v = self.place[i]["end_position"] - self.place[i]["st_position"]
                self.place[i]["st_position"] = curr_pos
                self.place[i]["end_position"] = curr_pos + v

            curr_pos = self.place[i]["end_position"]

    def delete(self, module_id):
        module = None
        for index in range(len(self.place)):
            if self.place[index]['module_id'] == module_id:
                module = self.place[index]
                del self.place[index]
                break

        if module is None:
            return 0

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
        return 1

    def insert(self, module_id, V, frag_id):
        if self.frag[frag_id]["st_position"] + V > self.frag[frag_id]["end_position"]:
            print("Invalid insertion")
            return

        self.tot_space -= V
        new_mod = {"module_id": module_id, "st_position": self.frag[frag_id]["st_position"], "end_position": self.frag[frag_id]["st_position"] + V}
        frag_mod = self.frag[frag_id]
        del self.frag[frag_id]
        if frag_mod["end_position"] != new_mod["end_position"]:
            frag_mod["st_position"] = new_mod["end_position"]
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

    def generate_module_image(self):
        print(self.frag)
        print(self.place)
        # Calculate the width and height of the image based on the start and end positions
        width = 100
        height = 2

        # Create a new image object with the calculated size
        im = Image.new('RGB', (width, height), )

        draw = ImageDraw.Draw(im)

        # Define a font for the module ids
        font = ImageFont.truetype("arial.ttf", 18)

        # Loop through each module in the list and assign a unique color to it
        for module in self.place:
            start_pos = module['st_position']
            end_pos = module['end_position']
            color = tuple(random.sample(range(256), 4))  # convert color values from [0,1] range to [0,255]

            # Set the color of the pixels for the current module
            for i in range(start_pos, end_pos):
                print(color)
                im.putpixel((i, 0), color)
                im.putpixel((i, 1), color)

            module_id = str(module['module_id'])
            text_width, text_height = draw.textsize(module_id, font=font)
            text_x = (start_pos + end_pos) // 2 - text_width // 2
            text_y = 1
            draw.text((text_x, text_y), module_id, font=font, fill=(0, 0, 0))

        # Save the image to a file
        im.save('module_image.jpg')

