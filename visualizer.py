import csv
import random
from PIL import Image, ImageDraw


class Visuals:
    symbol_colors = {}
    csv_symbols = {}

    def __init__(self, csv_symbol):
        # Define symbol-color mappings
        self.symbol_colors = {
            csv_symbol['storage']: "#FF6347",  # Orange
            csv_symbol['guard_ring']: "#808080",  # Dark Grey
            csv_symbol['routing_path']: "#FFFF00",  # Yellow
            csv_symbol['row']: "#d9d9d9",  # Light Grey
            csv_symbol['reservoir']: "#2aa16f",  # Moss green
            csv_symbol['waste_reservoir']: "#543b0b"  # brown
        }
        self.csv_symbols = csv_symbol

    def visualize(self, file_path, output_path):

        # Define the size of each square in the grid
        square_size = 20

        # Read the CSV file and store the symbols in a list
        symbols = []
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                symbols.append(row)

        # Calculate the dimensions of the grid based on the number of symbols
        num_rows = len(symbols)
        num_cols = len(symbols[0])
        grid_width = num_cols * square_size
        grid_height = num_rows * square_size

        # Create a new image for the grid
        grid_image = Image.new("RGB", (grid_width, grid_height), "#000000")

        # Create a new drawing object for the grid image
        grid_draw = ImageDraw.Draw(grid_image)

        # Draw squares for each symbol in the grid
        for row in range(num_rows):
            for col in range(num_cols):
                symbol = symbols[row][col]

                # Calculate the x and y position of the square based on the row and column indices
                x = col * square_size
                y = row * square_size

                if symbol in self.symbol_colors:
                    # standard symbols
                    color = self.symbol_colors[symbol]
                elif symbol[0] == self.csv_symbols['reservoir'] or symbol[0] == self.csv_symbols['waste_reservoir']:
                    # reservoir and waste_reservoir
                    color = self.symbol_colors[symbol[0]]
                elif symbol[0] == self.csv_symbols['operation']:
                    # normal operation
                    while True:
                        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                        sum = int(color[1:3], 16) + int(color[3:5], 16) + int(color[5:7], 16)
                        avg = sum / 3
                        if color not in self.symbol_colors.values() and (96 < avg < 196):
                            break
                    self.symbol_colors[symbol] = color

                else:
                    # its a storage operation
                    # assume module is already present in a row
                    symbol = tuple(map(str, symbol[1:len(symbol)-1].split(', ')))
                    if symbol[0] == 'G':
                        color = self.symbol_colors[symbol[0]]
                        grid_draw.rectangle((x, y, x + square_size, y + square_size), fill=color, outline="#000000")
                        continue
                    if symbol[1] not in self.symbol_colors.keys():
                        print("Storage module " + str(symbol) + " not present in any row")
                        continue
                    color = self.symbol_colors[symbol[1]]

                    center_x = x + (square_size // 2)
                    center_y = y + (square_size // 2)
                    text_width, text_height = grid_draw.textsize(symbol[0])
                    x_offset = (square_size - text_width) // 2
                    y_offset = (square_size - text_height) // 2
                    text_x = center_x - (text_width // 2) + x_offset
                    text_y = center_y - (text_height // 2) + y_offset
                    grid_draw.rectangle((x, y, x + square_size, y + square_size), fill=color, outline="#000000")
                    grid_draw.text((text_x, text_y), symbol[0], fill="#000000")
                    continue

                if symbol[0] in list(self.csv_symbols[key] for key in ['operation', 'reservoir', 'waste_reservoir']):
                    center_x = x + (square_size // 2)
                    center_y = y + (square_size // 2)
                    text_width, text_height = grid_draw.textsize(symbol)
                    x_offset = (square_size - text_width) // 2
                    y_offset = (square_size - text_height) // 2
                    text_x = center_x - (text_width // 2) + x_offset
                    text_y = center_y - (text_height // 2) + y_offset
                    grid_draw.rectangle((x, y, x + square_size, y + square_size), fill=color, outline="#000000")
                    grid_draw.text((text_x, text_y), symbol, fill="#000000")
                    continue

                grid_draw.rectangle((x, y, x + square_size, y + square_size), fill=color, outline="#000000")

        grid_image.save(output_path)