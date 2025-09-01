from PIL import Image
import numpy as np

class FractalCountTriangle:
    def __init__(self, start_size=3, image_path="", one_pixel_color=(255, 255, 255), zero_pixel_color=(0, 0, 0)):
        self.histogram = {}
        self.image_path = image_path
        self.one_pixel_color = one_pixel_color
        self.zero_pixel_color = zero_pixel_color
        self.binary_image = None
        self.line_value_search = True

    def read_image(self):
        """Reads the image from the specified path and converts it to a binary format."""
        try:
            with Image.open(self.image_path) as img:
                #img = img.convert("L")
                #binary_image = np.array(img)
                #self.binary_image = 1 - binary_image
                self.binary_image = np.array(img)
                # Create a binary image based on the specified colors
                return self.binary_image
        except Exception as e:
            print(f"Error reading image: {e}")
            return None

    def count_triangles(self):
        rows, cols = self.binary_image.shape
        print(f"Image shape: {rows}x{cols}")
        x = 5
        visited_j = [0]*cols
        print(self.binary_image[x])
        list_lines = []
        for j in range(cols):
            flag_visited = visited_j[j]
            if flag_visited == 0:
                #print(f"Processing cell at row {x}, column {j}, flag_visited: {flag_visited}" )
                line_start, line_end = self.find_line(x, j)
                if line_start != None and line_end != None:
                    self.mark_visited(visited_j, line_start, line_end)
                    #print("Range of columns:", visited_j)
                    #print(f"Line found at: {line_start}, {line_end}")
                    list_lines.append((line_start, line_end))
                else:
                    visited_j[j] = 1
        print("List of lines found:", list_lines, "value search ", self.line_value_search)

        # for j in range(cols):
        #     cell = self.binary_image[x, j]
        #     line_start, line_end = self.find_line(x, j)
        #     if line_start != None and line_end != None:
        #         print(self.binary_image[x])
        #         print(f"Line found at: {line_start}, {line_end}")
        #     # Process each cell as needed
        #     # For example, you might want to count certain patterns
        #     # This is a placeholder for actual triangle counting logic
        #     pass
        # #while x  < rows:
        #    x += 1
        #return self.histogram

    def find_line(self, row, col):
        if self.binary_image[row, col] != self.line_value_search:
            # Is a background pixel
            return None, None
        left_col = self.find_start_line(row, col-1)
        right_col = self.find_end_line(row, col+1)

        
        if col == left_col and col == right_col:
            # Is a point
            return None, None
        else:
            return (left_col, right_col)

    def find_start_line(self, row, col):
        value = self.binary_image[row, col]
        if value == self.line_value_search:
            return self.find_start_line(row, col-1)
        else:
            return col+1
    def find_end_line(self, row, col):
        end_col = None
        if col >= 50:
            #print("At the end of the row",col)
            end_col = col
            col = 0
        value = self.binary_image[row, col]
        if value == self.line_value_search:
            return self.find_end_line(row, col+1)
        else:
            if end_col!=None:
                return end_col - 1
            return col-1
    def mark_visited(self, row_list, j_start, j_end):
        x = j_start
        while x <= j_end:
            row_list[x]=1
            # Process the cell at row_list, x
            x += 1
