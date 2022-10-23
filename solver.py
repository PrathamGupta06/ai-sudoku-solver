import os
import time
import cv2
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.models import load_model  # noqa


class Sudoku:
    def __init__(self, board):
        self.board = board
        self.original_board = board.copy()
        self.is_solved = False
        self.possibilities_tried = 0
        self.empty_cells = None
        self.set_empty_cells()

    def display(self):
        """Display the sudoku board"""
        print()
        for row_number, row in enumerate(self.board):
            for column_number, cell  in enumerate(row):
                print(cell, end=" ")
                if column_number == 2 or column_number == 5:
                    print("|", end=" ")
            print()
            if row_number == 2 or row_number == 5:
                print("------|-------|------")
        print()

        # print("\n".join([" ".join(str(item) for item in row) for row in self.board]))

    def solve(self, current_cell=0):
        """Solves the sudoku board"""
        if current_cell >= len(self.empty_cells):
            self.check_if_solved()
            return

        row, col = self.empty_cells[current_cell][0], self.empty_cells[current_cell][1]

        if self.board[row][col] == 0:  # cell is empty
            for possibility in range(1, 10):  # try all the numbers from 1 to 9
                if not self.is_valid(row, col,
                                     possibility):  # if the number is not valid as per rules, try the next one
                    continue
                self.possibilities_tried += 1
                self.board[row][col] = possibility
                self.solve(current_cell + 1)  # recursively call the solve function to solve the rest of the board
                if self.is_solved:  # if the board is solved by this possibility, return
                    return
                # print("Backtracked, resetting row {} and column {} to *, for possibility {}".format(row,
                # col, possibility))
                self.board[row][col] = 0  # Reset the cell to 0 if the board is not solved by this possibility
            # print("Unsolvable", row, col, "Backtracking")
            return  # if no number is valid in this cell, backtrack
        # print("Solved")

    def is_valid(self, row, column, value):
        """Check if the number "value" is valid in the sudoku board"""

        # print("Checking if {} is valid in row {} and column {}".format(k, row, column))
        if value in self.board[row]:
            return False
        for i in range(9):
            if self.board[i][column] == value:
                return False
        for i in range(3):
            for j in range(3):
                if self.board[(row // 3) * 3 + i][(column // 3) * 3 + j] == value:
                    return False
        # print("{} is valid in row {} and column {}".format(value, row, column))
        # self.display()
        return True

    def check_if_solved(self):
        """ Check if the sudoku board is solved. Sets is_solved to True if it is solved """
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return
        self.is_solved = True

    def set_empty_cells(self):
        """ Sets the empty cells in the board """
        self.empty_cells = [[row, col] for row in range(9) for col in range(9) if self.board[row][col] == 0]

    def reset(self):
        """Clears the board"""
        self.board = self.original_board.copy()
        self.is_solved = False
        self.possibilities_tried = 0

    def clear(self):
        """Resets the board"""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = self.board.copy()
        self.is_solved = False
        self.possibilities_tried = 0
        self.set_empty_cells()

    def modify_value(self, row, column, value):
        """Modifies the value of a cell"""
        self.board[row-1][column-1] = value  # -1 because the board is 0-indexed and the user input is 1-indexed
        self.set_empty_cells()


class SudokuExtractor:
    def __init__(self, image_path):
        self.path = image_path
        self.img = cv2.imread(image_path)
        self.board = None

    def display(self):
        """Display the sudoku board"""
        if self.board is None:
            print("Board is not extracted yet. Please call extract_board() first")
            return

        print()
        for row_number, row in enumerate(self.board):
            for column_number, cell  in enumerate(row):
                print(cell, end=" ")
                if column_number == 2 or column_number == 5:
                    print("|", end=" ")
            print()
            if row_number == 2 or row_number == 5:
                print("------|-------|------")
        print()

        # print("\n".join([" ".join(str(item) for item in row) for row in self.board]))

    def preprocess_image(self, cell_image):  # noqa: 88
        rows, cols = np.shape(cell_image)
        for i in range(rows):
            # Floodfilling with the outer and second outer points as seed values
            cv2.floodFill(cell_image, None, (0, i), 0)
            cv2.floodFill(cell_image, None, (i, 0), 0)
            cv2.floodFill(cell_image, None, (rows - 1, i), 0)
            cv2.floodFill(cell_image, None, (i, rows - 1), 0)
            cv2.floodFill(cell_image, None, (2, i), 0)
            cv2.floodFill(cell_image, None, (i, 2), 0)
            cv2.floodFill(cell_image, None, (rows - 2, i), 0)
            cv2.floodFill(cell_image, None, (i, rows - 2), 0)

        # Finding the bounding cell of the number in the cell
        top_row = None
        bottom_row = None
        left_col = None
        right_col = None
        threshold_bottom = 50
        threshold_top = 50
        threshold_left = 50
        threshold_right = 50
        center = rows // 2
        for i in range(center, rows):  # Looping from the center to the bottom of the image
            if bottom_row is None:
                temp = cell_image[i]
                if sum(temp) < threshold_bottom or i == rows - 1:
                    bottom_row = i

            if top_row is None:
                temp = cell_image[rows - i - 1]
                if sum(temp) < threshold_top or i == rows - 1:
                    top_row = rows - i - 1

        for i in range(center, cols):  # Looping from the center to the right of the image
            if right_col is None:
                temp = cell_image[:, i]
                if sum(temp) < threshold_right or i == cols - 1:
                    right_col = i

            if left_col is None:
                temp = cell_image[:, cols - i - 1]
                if sum(temp) < threshold_left or i == cols - 1:
                    left_col = cols - i - 1

        # Centering the bounding cell's contents
        newimg = np.zeros(np.shape(cell_image))
        startat_x = (rows + left_col - right_col) // 2
        startat_y = (rows - bottom_row + top_row) // 2
        for y in range(startat_y, (rows + bottom_row - top_row) // 2):
            for x in range(startat_x, (rows - left_col + right_col) // 2):
                newimg[y, x] = cell_image[top_row + y - startat_y, left_col + x - startat_x]
        return newimg

    def extract_sudoku(self):
        original_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        # Convert image to gray
        gray_img = cv2.cvtColor(original_img.copy(), cv2.COLOR_BGR2GRAY)

        # Adaptive threshold using 11 nearest neighbour pixels
        gray_img = cv2.GaussianBlur(gray_img, (7, 7), 0)
        gray_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        # cv2.imshow(gray_img)

        # Find Contours
        contours, hierarchy = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        location = None
        for contour in contours:
            polygon = cv2.approxPolyDP(contour, 15, True)
            if len(polygon) == 4:
                location = polygon
                break

        # Display the detected sudoku with contours
        # contourimg = cv2.drawContours(original_img.copy(), contours, -1, (0, 255, 0), 1)
        # cv2.imshow("Image with contours", contourimg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Transform the board
        height, width = 900, 900
        locations = sorted(location, key=lambda coord: np.sum(coord[0]))
        top_left = locations[0]
        bottom_right = locations[3]
        if locations[1][0][0] < locations[2][0][0]:
            bottom_left = locations[1]
            top_right = locations[2]
        else:
            bottom_left = locations[2]
            top_right = locations[1]

        pts1 = np.float32([top_left, top_right, bottom_left, bottom_right])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        board = cv2.warpPerspective(gray_img, matrix, (width, height))

        # Splitting the board into 9 x 9 images.
        cells = []
        rows = np.vsplit(board, 9)
        for row in rows:
            cols = np.hsplit(row, 9)
            for cell in cols:
                cell = cv2.resize(cell, (28, 28))  # Resizing each cell to 28x28 for the model
                cells.append(cell)

        # Preprocessing the images to floodfill the outermost layer and center the number in the cell
        for index, cell in enumerate(cells):
            cells[index] = self.preprocess_image(cell)

        blank_cells = []
        for i, cell in enumerate(cells):
            # cv2.imshow(cell)
            if np.mean(cell) < 1:  # If the mean of the cell is less than 1, it is a blank cell
                blank_cells.append(i)
            cells[i] /= 255.0  # Normalizing the cell

        cells = np.array(cells).reshape((-1, 28, 28, 1))  # Reshaping the cells list to a 4D array

        # Loading the model
        classes = np.arange(0, 10)
        model = load_model('model.h5')

        # Predicting the digits in the cells
        prediction = model.predict(cells)
        predicted_numbers = []
        for i in prediction:
            index = (np.argmax(i))
            predicted_number = classes[index]
            predicted_numbers.append(predicted_number)

        # Changing the value of blank cells to 0
        for i in blank_cells:
            predicted_numbers[i] = 0

        # Reshaping the predicted numbers to a 9x9 grid
        predicted_numbers = np.array(predicted_numbers).reshape(9, 9)
        self.board = predicted_numbers


if __name__ == "__main__":
    test_boards = [
        [[3, 1, 6, 5, 7, 8, 4, 9, 2],
         [5, 2, 9, 1, 3, 4, 7, 6, 8],
         [4, 8, 7, 6, 2, 9, 5, 3, 1],
         [2, 6, 3, 0, 1, 5, 9, 8, 7],
         [9, 7, 4, 8, 6, 0, 1, 2, 5],
         [8, 5, 1, 7, 9, 2, 6, 4, 3],
         [1, 3, 8, 0, 4, 7, 2, 0, 6],
         [6, 9, 2, 3, 5, 1, 8, 7, 4],
         [7, 4, 5, 0, 8, 6, 3, 1, 0]],  # Easiest

        [[3, 0, 6, 5, 0, 8, 4, 0, 0],
         [5, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 8, 7, 0, 0, 0, 0, 3, 1],
         [0, 0, 3, 0, 1, 0, 0, 8, 0],
         [9, 0, 0, 8, 6, 3, 0, 0, 5],
         [0, 5, 0, 0, 9, 0, 6, 0, 0],
         [1, 3, 0, 0, 0, 0, 2, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 7, 4],
         [0, 0, 5, 2, 0, 6, 3, 0, 0]],  # Medium

        [[6, 5, 0, 8, 0, 9, 0, 0, 0],
         [0, 0, 0, 5, 0, 0, 8, 0, 7],
         [0, 0, 1, 0, 4, 0, 0, 9, 0],
         [0, 0, 9, 1, 0, 0, 0, 0, 0],
         [2, 0, 0, 0, 0, 0, 0, 0, 8],
         [0, 0, 0, 0, 0, 2, 6, 0, 0],
         [0, 3, 0, 0, 2, 0, 7, 0, 0],
         [1, 0, 2, 0, 0, 8, 0, 0, 0],
         [0, 0, 0, 3, 0, 1, 0, 4, 5]]  # Hardest

    ]

    board1 = test_boards[2]  # Change this to test different boards
    sudoku1 = Sudoku(board1)

    start = time.time()

    print("Empty Board")
    print(sudoku1.display())

    sudoku1.solve()
    end = time.time()
    print("There are {} empty cells".format(len(sudoku1.empty_cells)))

    if sudoku1.is_solved:
        sudoku1.display()
        print("Solved in {} seconds, and {} different possibilities were tried.".format(end - start,
                                                                                        sudoku1.possibilities_tried))
    else:
        print("Unsolvable. Took {} seconds, and {} different possibilities were tried.".format(end - start,
                                                                                               sudoku1.possibilities_tried))  # noqa: E501
    # 9^55 miliseconds = 9 × 10^41 years

    sudoku2 = SudokuExtractor(r'sample/sudoku3.png')
    print("We will extract the board from the image {}".format(sudoku2.path))
    print("Starting the extraction")
    start = time.time()
    sudoku2.extract_sudoku()
    end = time.time()
    sudoku2.display()
    print("Extracted in {} seconds".format(end - start))
    print("Please correct the wrong cell values")
