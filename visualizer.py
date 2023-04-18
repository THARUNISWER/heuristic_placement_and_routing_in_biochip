import csv
import random
from PIL import Image, ImageDraw


class Visuals:
    symbol_colors = {}

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
        self.const_symbols = csv_symbol.values()

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

                # Check if the symbol has a fixed color
                if symbol in self.symbol_colors:
                    color = self.symbol_colors[symbol]
                elif symbol[0] == 'R' or symbol[0] == 'D':
                    color = self.symbol_colors[symbol[0]]
                else:
                    # Assign a random color to the symbol
                    while True:
                        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                        if color not in self.symbol_colors.values():
                            break
                    self.symbol_colors[symbol] = color

                # Draw the square with the assigned color
                grid_draw.rectangle((x, y, x + square_size, y + square_size), fill=color, outline="#000000")

                if symbol not in self.const_symbols:
                    # Calculate the center position of the square
                    center_x = x + (square_size // 2)
                    center_y = y + (square_size // 2)

                    # Calculate the x and y offsets for the text
                    text_width, text_height = grid_draw.textsize(symbol)
                    x_offset = (square_size - text_width) // 2
                    y_offset = (square_size - text_height) // 2

                    # Draw the symbol character within the square
                    text_x = center_x - (text_width // 2) + x_offset
                    text_y = center_y - (text_height // 2) + y_offset
                    grid_draw.text((text_x, text_y), symbol, fill="#000000")

        # Save the grid image as a JPEG file
        grid_image.save(output_path)