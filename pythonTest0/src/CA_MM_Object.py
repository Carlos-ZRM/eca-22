
import numpy as np

from CA_Object import ECA
import cv2 as cv

class ECA_MM(ECA):
    def __init__(self, rule_number=22, kernel=np.array([[0,1,0], [1,1,1]], np.uint8), iterations=1):
        """
        Initialize the ECA_MM class.
        Args:
            rule_number (int): The rule number for the elementary cellular automaton.
            kernel (np.ndarray): The structuring element used for morphological operations.
            iterations (int): The number of iterations for morphological operations.
        """
        super().__init__(rule_number=rule_number)
        self.kernel = kernel
        self.image_file = ""
        self.iterations = iterations

    def set_kernel(self, kernel):
        """
        Set the structuring element for morphological operations.
        Args:
            kernel (np.ndarray): The structuring element used for morphological operations.
        """
        self.kernel = kernel

    def set_iterations(self, iterations):
        """
        Set the number of iterations for morphological operations.
        Args:
            iterations (int): The number of iterations for morphological operations.
        """
        self.iterations = iterations

    def dilation(self):
        """
        Apply morphological dilation to the image.
        """
        dilated_filename = "dilated_image.png"
        if self.image_file == "":
            self.image_file = super()._print_img()
        img = cv.imread(self.image_file, 0)
        dilation = cv.dilate(img, self.kernel, iterations=self.iterations)
        cv.imwrite(dilated_filename, dilation, [cv.IMWRITE_PNG_BILEVEL, 1])
        return dilated_filename
    
    def erosion(self):
        """
        Apply morphological erosion to the image.
        """
        eroded_filename = "eroded_image.png"
        if self.image_file == "":
            self.image_file = super()._print_img()
        img = cv.imread(self.image_file, 0)
        erosion = cv.morphologyEx(img, cv.MORPH_OPEN, self.kernel, iterations=self.iterations)
        cv.imwrite(eroded_filename, erosion, [cv.IMWRITE_PNG_BILEVEL, 1])
        return eroded_filename

    def gradation(self):
        """
        Apply morphological gradient to the image.
        """
        gradient_filename = "gradient_image.png"
        if self.image_file == "":
            self.image_file = super()._print_img()
        img = cv.imread(self.image_file, 0)
        gradient = cv.morphologyEx(img, cv.MORPH_GRADIENT, self.kernel, iterations=self.iterations)
        cv.imwrite(gradient_filename, gradient, [cv.IMWRITE_PNG_BILEVEL, 1])
        return gradient_filename
    
    def black_hat(self):
        """
        Apply morphological black hat to the image.
        """
        black_hat_filename = "black_hat_image.png"
        if self.image_file == "":
            self.image_file = super()._print_img()
        img = cv.imread(self.image_file, 0)
        black_hat = cv.morphologyEx(img, cv.MORPH_BLACKHAT, self.kernel, iterations=self.iterations)
        cv.imwrite(black_hat_filename, black_hat, [cv.IMWRITE_PNG_BILEVEL, 1])
        return black_hat_filename

