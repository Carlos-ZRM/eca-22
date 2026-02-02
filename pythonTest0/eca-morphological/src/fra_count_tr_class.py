from PIL import Image, ImageDraw
import numpy as np
import os


class FractalCountTriangle:
    def __init__(
        self,
        start_size=3,
        image_path="",
        one_pixel_color=(255, 255, 255),
        zero_pixel_color=(0, 0, 0),
    ):
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
                # img = img.convert("L")
                # binary_image = np.array(img)
                # self.binary_image = 1 - binary_image
                self.binary_image = np.array(img)
                # Create a binary image based on the specified colors
                return self.binary_image
        except Exception as e:
            print(f"Error reading image: {e}")
            return None

    def count_triangles_for(self):
        rows, cols = self.binary_image.shape
        print(f"Image shape: {rows}x{cols}")
        list_lines = []
        for x in range(rows):
        #for x in range(4,5):
            y = 0
            list_lines = []
            while y < cols:
                value = self.binary_image[x, y]
                if value != self.line_value_search:
                    ## its not a point of line
                    y += 1
                else:
                    line_start = y
                    right_col = y + 1
                    
                    if right_col >= cols:
                        line_end = y
                        y += 1
                    else:
                        right_value = self.binary_image[x, right_col]
                    
                        ## right border condition
                    while right_value == self.line_value_search and right_col < cols:
                        y += 1
                        print("y incremented to ", y)
                        line_end = right_col
                        right_col += 1
                        if right_col < cols:
                            right_value = self.binary_image[x, right_col]      
                    if line_start != line_end:
                        print(f"Line found at row {x}, from column {line_start} to {line_end}")
                        if line_start == 0 and line_end == cols -1:
                            print("Line spans the entire row")
                            list_lines = [(line_start, line_end)]
                        elif len(list_lines) > 0 and line_end == cols - 1:
                            print("Line reaches the end of the row")
                            
                            #element = list_lines[0]
                            element = list_lines[0]
                            print("Previous line element:", element)
                            if element[0] == 0:
                                print("Merging with previous line")
                                line_end= element[1]
                                list_lines[0] = ( line_start, line_end)
                            else:
                                list_lines.append((line_start, line_end))
                        else:
                            list_lines.append((line_start, line_end))
                        line_start = None
                        y += 1



            self.histogram[x] = list_lines
            print(f"List of lines found {x}:", list_lines, "value search ", self.line_value_search)
        print("Final histogram of lines by row:", self.histogram)



    def count_triangles(self):
        rows, cols = self.binary_image.shape
        print(f"Image shape: {rows}x{cols}")
        
        x = 1
        while x < rows:
            # 0 Generate visited_j list for each row and Initialize all to 0 (not visited)
            # 0.1 Create empty list of lines for the current row
            visited_j = [0] * cols
            list_lines = []
            for j in range(cols):
                # 1 Check if the cell has been visited
                flag_visited = visited_j[j]
                # 2 If not visited, process the cell
                if flag_visited == 0:
                    # 3 Find line and get start and end columns line_start, line_end
                    # print(f"Processing cell at row {x}, column {j}, flag_visited: {flag_visited}" )
                    line_start, line_end = self.find_line(x, j)

                    if line_start is not None and line_end is not None:
                        self.mark_visited(visited_j, line_start, line_end)
                        # print("Range of columns:", visited_j)
                        # print(f"Line found at: {line_start}, {line_end}")
                        list_lines.append((line_start, line_end))
                    else:
                        visited_j[j] = 1
            self.histogram[x] = list_lines
            # print(f"List of lines found {x}:", list_lines, "value search ", self.line_value_search)
            x += 1
        print("Final histogram of lines by row:", self.histogram)

    def find_line(self, row, col):
        """
        Args:
            row (int): The row index in the binary image.
            col (int): The column index in the binary image.
        Returns:
            tuple: A tuple containing the start and end columns of the line, or (None, None) if not found.

        Description:
            Finds the start and end columns of a line in the binary image.
            1. IF the pixel is different from the line value (line_value_search), it's a background pixel.
                1.1 Return None for a background pixel.
            2. Find the start line recursively (left_col-1) (lines continuous in the left pixel)
            and end line (right_col) recursively (right_col+1) (lines continuous in the right pixel)
            3. If the start and end columns are the same, it's a point.
                3.1 Return None, None for a point.
                3.2 Else, return the start and end columns.
        """
        if self.binary_image[row, col] != self.line_value_search:
            # Is a background pixel
            return None, None
        # Find the start and end columns recursively
        left_col = self.find_start_line(row, col, col - 1)
        right_col = self.find_end_line(row, col, col + 1)

        if col == left_col and col == right_col:
            # Is a point
            return None, None
        else:
            return (left_col, right_col)

    def find_start_line(self, row, col, left_col ):
        """
        Finds the start column of a line in the binary image.

        Args:
            row (int): The row index in the binary image.
            col (int): The column index in the binary image.

        Returns:
            int: The start column of the line, or None if not found.

        Description:
            Finds value of the selected pixel in the binary image.
            1. IF the pixel is  equals to desired line_value_search is a line point continue searching left recursiverly.
               1.2 Call function recursively to find the start line.
            2. IF the pixel is different from the line value (line_value_search), it's a background pixel ( end recursion)
               2.1 Return col + 1.
        """
        value = self.binary_image[row, left_col]
        if value == self.line_value_search:
            return self.find_start_line(row, col, left_col - 1)
        else:
            return left_col + 1

    def find_end_line(self, row, col, right_col ):
        """
        Finds the end column of a line in the binary image.

        Args:
            row (int): The row index in the binary image.
            col (int): The column index in the binary image.

        Returns:
            int: The end column of the line, or None if not found.
        """
        end_col = None
        if right_col >= 50:
            # print("At the end of the row",col)
            end_col = col
            col = 0
        value = self.binary_image[row, right_col]
        if value == self.line_value_search:
            return self.find_end_line(row, col, right_col + 1)
        else:
            if end_col is not None:
                return end_col - 1
            return col - 1

    def mark_visited(self, row_list, j_start, j_end):
        """
        Marks the visited cells in the row_list between the start and end columns.
        """
        x = j_start
        while x <= j_end:
            row_list[x] = 1
            # Process the cell at row_list, x
            x += 1

    def draw_lines(self):
        img_result = Image.open(self.image_path).convert("RGBA")
        draw = ImageDraw.Draw(img_result)
        rows, cols = self.binary_image.shape
        for x in self.histogram:
            for line in self.histogram[x]:
                start_col, end_col = line

                # if start_col < 0:
                #     print("Error in start_col", start_col, ":", 49 + start_col)
                #     start_col = 49 + start_col

                #     draw.line([(0, x), (end_col, x)], fill="red", width=1)
                #     draw.line([(start_col, x), (49, x)], fill="blue", width=1)
                if start_col > end_col:
                    print("Line with border lines ", start_col, end_col)
                    draw.line([(start_col, x), (cols-1, x)], fill="red", width=1)
                    draw.line([(0, x), (end_col, x)], fill="red", width=1)
                else:
                    draw.line([(start_col, x), (end_col, x)], fill="red", width=1)
                # Draw the line at the appropriate position
        img_result.save("result_" + self.image_path)
