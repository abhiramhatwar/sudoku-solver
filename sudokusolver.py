import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_sudoku_from_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    text = pytesseract.image_to_string(thresh, config='--psm 6')
    lines = text.splitlines()
    grid = [[int(num) if num.isdigit() else 0 for num in line.split()] for line in lines]
    return grid

def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def draw_sudoku(board, output_image_path):
    img = Image.new('RGB', (450, 450), 'white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    cell_size = 50

    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        draw.line([(0, i * cell_size), (450, i * cell_size)], fill='black', width=line_width)
        draw.line([(i * cell_size, 0), (i * cell_size, 450)], fill='black', width=line_width)

    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num != 0:
                x = c * cell_size + cell_size // 2
                y = r * cell_size + cell_size // 2
                draw.text((x, y), str(num), fill='black', font=font, anchor='mm')

    img.save(output_image_path)
    print(f"Sudoku image saved to {output_image_path}")

def main():
    input_image_path = 'sudoku_input.jpg'
    output_image_path = 'sudoku_solved.png'
    
    grid = extract_sudoku_from_image(input_image_path)
    print("Extracted Sudoku Grid:")
    print_board(grid)
    
    if solve_sudoku(grid):
        print("Solved Sudoku Grid:")
        print_board(grid)
        draw_sudoku(grid, output_image_path)
    else:
        print("No solution exists.")

if __name__ == "__main__":
    main()
