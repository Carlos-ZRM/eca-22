from random import random
from PIL import Image, ImageDraw
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')


class FractalCountTriangle:
    def __init__(
        self,
        start_size=3,
        image_path="",
        one_pixel_color=(255, 255, 255),
        zero_pixel_color=(0, 0, 0),
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.histogram_lines = {}
        self.image_path = image_path
        self.one_pixel_color = one_pixel_color
        self.zero_pixel_color = zero_pixel_color
        self.binary_image = None
        self.line_value_search = False
        self.histogram_triangles = []
        self.histogram_colors = {}

    def read_image(self):
        """Reads the image from the specified path and converts it to a binary format."""
        try:
            with Image.open(self.image_path) as img:
                self.binary_image = np.array(img)
                # Create a binary image based on the specified colors
                return self.binary_image
        except Exception as e:
            self.logger.error(f"Error reading image: {e}")
            return None

    def count_lines_for(self):
        # Get the dimensions of the binary image
        rows, cols = self.binary_image.shape
        self.logger.debug(f"Image shape: {rows}x{cols}")
        list_lines = []
        for x in range(rows):
        #for x in range(9,14):
            # Set the starting column index for the current row
            y = 0
            # Set the list of lines for the current row to an empty list
            list_lines = []
            self.logger.debug(f"Processing row {x}")
            line_start = None
            line_end = None
            while y < cols:
                # Get the value of the current pixel in the binary image
                value = self.binary_image[x, y]
                self.logger.debug(f" |Processing pixel at ({x}, {y}): {value}")
                # Check if the current pixel value is different from the line value we are searching for

                if value == self.line_value_search:

                    line_start = y
                    line_end = y
                    self.logger.debug(f"     || y value {y} {value}")
                    # Increment y to continue searching for the end of the line
                    y += 1
                    while y < cols and (line_end is not None) :
                        next_value = self.binary_image[x, y]
                        self.logger.debug(f"     || yy value {y} {next_value}")
                        if next_value == self.line_value_search:
                            # If next pixel is the same as the line value, update the end of the line
                            line_end = y
                        else:
                            # 1. Check if is a single point
                            # If next pixel is different, we have found the end of the line or a single point
                            if line_start == line_end:
                                self.logger.debug(f"     ||Found a single point at ({x}, {y}, {next_value})")
                            else:
                            # 2, Check end of line on right side right pixel is different) 
                                self.logger.debug(f"     ||Found a line from ({x}, {line_start}) to ({x}, {line_end})")
                                self.logger.debug(f"     ||End line at {y} ")
                                list_lines.append((line_start, line_end))
                            line_start = None
                            line_end = None
                        y += 1
                    if line_start is not None and line_end is cols - 1:
                        self.logger.debug(f"     ||Found a line from ({x}, {line_start}) to ({x}, {line_end})")
                        self.logger.debug(f"     ||End line at {y} ")
                        list_lines.append((line_start, line_end))
                        
                    y += 1
                y += 1

                    
                    # Found a pixel that matches the line value we are searching for, so we need to find the start and end of the line

            # Check end line conditions.
            if len(list_lines) > 0:
                self.logger.debug(f"            ||| Checking for wrap-around lines in row {x}: {list_lines}")
                first_line = list_lines[0] if list_lines else None
                last_line = list_lines[-1] if list_lines else None
                if first_line[0] == 0 and last_line[1] == cols - 1:
                    self.logger.debug(f"     ||Found a line that wraps around the row {x}: {first_line} to {last_line}")
                    # Merge the first and last lines into a single line
                    merged_line = (last_line[0], first_line[1])
                    list_lines = [merged_line] + list_lines[1:-1]
                    self.logger.debug(f"     ||Merged line: {merged_line}")
                elif  last_line[1] == cols - 1 and  self.binary_image[x, 0] == self.line_value_search:
                    self.logger.debug(f"     ||Found a line that wraps around the row {x}: 0 to {last_line}")
                    merged_line = (last_line[0], 0)
                    list_lines = [merged_line] + list_lines[1:-1]
                    self.logger.debug(f"     ||Merged line: {merged_line}")
                #elif first_line[0] == 0 and  self.binary_image[x,  cols - 1] == self.line_value_search:
                #    self.logger.debug(f"     ||Found a line that wraps around the row {x}: 0 to {last_line}")
                #    merged_line = ( cols - 1 ,first_line[0])
                #    list_lines = [merged_line] + list_lines[1:-1]
                #    self.logger.debug(f"     ||Merged line: {merged_line}")
                

                    
            self.histogram_lines[x] = list_lines
            self.logger.debug(f"List of lines found {x}: {list_lines}, value search {self.line_value_search}")
        self.logger.info(f"Final histogram of lines by row: {self.histogram_lines}")

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
            self.histogram_lines[x] = list_lines
            # print(f"List of lines found {x}:", list_lines, "value search ", self.line_value_search)
            x += 1
        print("Final histogram of lines by row:", self.histogram_lines)

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
        for x in self.histogram_lines:
            for line in self.histogram_lines[x]:
                start_col, end_col = line

                # if start_col < 0:
                #     print("Error in start_col", start_col, ":", 49 + start_col)
                #     start_col = 49 + start_col

                #     draw.line([(0, x), (end_col, x)], fill="red", width=1)
                #     draw.line([(start_col, x), (49, x)], fill="blue", width=1)
                if start_col > end_col:
                    #print("Line with border lines ", start_col, end_col)
                    draw.line([(start_col, x), (cols-1, x)], fill="red", width=1)
                    draw.line([(0, x), (end_col, x)], fill="red", width=1)
                else:
                    draw.line([(start_col, x), (end_col, x)], fill="red", width=1)
                # Draw the line at the appropriate position
        img_result.save("result_" + self.image_path)

    def count_triangles_for(self):
        # Implement the logic to count lines based on the histogram of lines
        # Get the histogram of lines
        lines = self.histogram_lines.copy()
        # Get the dimensions of the binary image
        rows, cols = self.binary_image.shape
        self.logger.debug(f"SHAPE")
        # Iterate through each row in the histogram of lines
        for x in lines:
            self.logger.debug(f"Processing line {x} ")
            triangle_lines = []
            list_lines = lines[x]
            
            for line in list_lines:
                is_triangle = True
                triangle_lines.append(line)
                # Determine the start and end columns of the line
                start_line_y = line[0]
                end_line_y = line[1]
                if end_line_y > start_line_y:
                    base = end_line_y - start_line_y
                else:
                    base = (cols - start_line_y) + end_line_y
                
                self.logger.info(f"Line found at row {x}, from column {start_line_y} to {end_line_y} with base {base}")


                is_pair = True if base % 2 == 0 else False
                # Calculate the height and area of the triangle based on whether the base is even or odd
                if is_pair:
                    # 
                    height = base // 2
                    area = height * (height + 1)
                else:
                    height = (base + 1) // 2
                    area = height * height
                xx = 1
                # For to check if the next lines in the subsequent rows form a triangle with the current line
                self.logger.debug("+++++++++++++++++++++++++++")
                for h in range(x , x+ height - 1):
                    self.logger.info(f" h {h}")
                    # Check follow up lines in the next rows to see if they form a triangle with the current line
                    if start_line_y < end_line_y:
                        next_start = (start_line_y + xx )  % cols
                        next_end = (end_line_y - xx  )  % cols
                    else:
                        next_start = (start_line_y + xx )  % cols 
                        next_end = (end_line_y - xx  )  % cols 
                    self.logger.debug(f"    {h} , {xx} | current lines {start_line_y} {end_line_y} | {next_start} {next_end} ")

                    
                    next__line = (next_start, next_end)
                    self.logger.info(f"Checking for triangle at row {h+1}, expected line: {next__line}")
                    if h + 1 >= rows:
                        self.logger.info(f"Reached the end of the image at row {h+1}, stopping triangle check.")
                        if h - x >= 2 :
                            is_triangle = True
                        else:
                            is_triangle = False
                        break
                    if next__line not in lines[h+1]  :
                        is_triangle = False
                        break
                    else:
                        triangle_lines.append(next__line)
                        lines[h+1].remove(next__line)
                    xx += 1
                if is_triangle:
                    self.logger.info(f"Triangle found with base {base} and height {height} at row {x} and first line {triangle_lines[0]}")
                    triangle = { "base": base, "height": height, "lines": triangle_lines , "area": area, "row": x}
                    self.histogram_triangles.append(triangle)
                
        self.logger.info(f"Total triangles found: {len(self.histogram_triangles)}")

    def draw_triangles(self):
        img_result = Image.open(self.image_path).convert("RGBA")
        draw = ImageDraw.Draw(img_result)
        rows, cols = self.binary_image.shape
        for triangle in self.histogram_triangles:
            self.logger.info(f"Triangle details: {triangle}")
            area = str(triangle["area"])
            if area in self.histogram_colors:
                color = self.histogram_colors[area]
            else:
                r = int(random() * 256)
                g = int(random() * 256)
                b = int(random() * 256)
                color = (r,g,b)
                self.histogram_colors[area]= color

            x = triangle["row"]
            lines = triangle["lines"]
            
            for line in lines:
                start_col, end_col = line

                # if start_col < 0:
                #     print("Error in start_col", start_col, ":", 49 + start_col)
                #     start_col = 49 + start_col

                #     draw.line([(0, x), (end_col, x)], fill="red", width=1)
                #     draw.line([(start_col, x), (49, x)], fill="blue", width=1)
                if start_col > end_col:
                    #print("Line with border lines ", start_col, end_col)
                    draw.line([(start_col, x), (cols-1, x)], fill=color, width=1)
                    draw.line([(0, x), (end_col, x)], fill=color, width=1)
                else:
                    draw.line([(start_col, x), (end_col, x)], fill=color, width=1)
                # Draw the line at the appropriate position
                x = x + 1
        img_result.save("result_triangle_" + self.image_path)
    

