from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from lotoSheet import LotoSheet
import os
import random

def HEX_to_RGB(hex: str) -> tuple[int, int, int]:
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

class LotoDrawer:
    def draw(self, result_dir: str, background_dir: str, frame_dir: str, loto_sheet: LotoSheet, font_dir: str, item_dir_list: list[str] = []):
        background = Image.open(background_dir)
        frame = self.create_new_frame(background, thickness=0, margin_top=552, margin_bottom=84, margin_left=120, margin_right=120, third_spacing=152, edge_color=(255, 255, 255, 255))

        font = ImageFont.truetype(font_dir, 75)
        item_list = [
            Image.open(item_dir) for item_dir in item_dir_list
        ]
        numbers = self.create_board_image(frame.size, self.get_cell_rectangles(frame), loto_sheet, font, item_list)

        merged = Image.new('RGBA', frame.size, (0, 0, 0, 0))
        merged.paste(background, (0, 0))
        merged.paste(numbers, (0, 0), numbers)

        if not frame_dir == None:
            _frame = Image.open(frame_dir)
            if not _frame.mode == "RGBA":
                _frame = _frame.convert("RGBA")
            merged.paste(_frame, (0, 0), _frame)

        result_directory = os.path.dirname(result_dir)
        if not os.path.exists(result_directory):
            os.makedirs(result_directory)
        merged.save(result_dir)

    def create_new_frame(self, background: Image, thickness: int, margin_top: int = 0, margin_left: int = 0, margin_right: int = 0, margin_bottom: int = 0, third_spacing: int = 0, edge_color: tuple[int, int, int, int] = (0, 0, 255, 255)) -> Image:
        frame = Image.new('RGBA', background.size, (0, 0, 1, 255))
        draw = ImageDraw.Draw(frame)

        frame.paste(background, (0, 0))

        width, height = background.size
        
        section_width = width - margin_left - margin_right
        section_height = (height - margin_top - margin_bottom - 2 * third_spacing) / 3
        cell_width = section_width / 9
        cell_height = section_height / 3

        for i in range(0, 3):
            top = margin_top + i * (section_height + third_spacing)
            bottom = top + section_height
            left = margin_left
            right = left + section_width
            draw.rectangle((left, top, right, bottom), fill=(0, 0, 0, 0), outline=(0, 0, 0, 255), width=thickness)

            for j in range(0, 4):            
                draw.rectangle((left, top + j * cell_height, right, top + j * cell_height + thickness), fill=edge_color)
            for j in range(0, 10):
                draw.rectangle((left + j * cell_width, top, left + j * cell_width + thickness, bottom), fill=edge_color)

        return frame

    def get_cell_rectangles(self, frame: Image) -> list[list[tuple[int, int, int, int]]]:
        pic = frame.load()
        row, col = frame.size
        cell_rectangles = [[(0, 0, 0, 0) for _ in range(0, 9)] for _ in range(0, 9)]
        _i, _j = 0, 0
        visited = [[False for _ in range(0, col)] for _ in range(0, row)]

        for x in range(0, row):
            for y in range(0, col):
                if pic[x, y] == (0, 0, 0, 0) and not visited[x][y]:
                    _x, _y = x, y
                    while pic[_x, y] == (0, 0, 0, 0):
                        _x += 1
                    while pic[x, _y] == (0, 0, 0, 0):
                        _y += 1
                    for i in range(x, _x):
                        for j in range(y, _y):
                            visited[i][j] = True

                    cell_rectangles[_i][_j] = (x, y, _x, _y)
                    _j += 1
                    if _j == 9:
                        _j = 0
                        _i += 1
        return cell_rectangles
    
    def create_board_image(self, image_size, cells: list, loto_sheet: LotoSheet, font: ImageFont, item_list: list[Image.Image] = []) -> Image:
        image = Image.new('RGBA', image_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        item_cells = [[-1 for _ in range(0, 9)] for _ in range(0, 9)]
        for i in range(0, 9):
            has_number = []
            for x in loto_sheet.sheet_array[i]:
                str_x = str(x)
                j = 0
                if len(str_x) == 2:
                    j = int(str_x[0])
                has_number.append(j)
                cell = cells[j][i]
                x = cell[0] + (cell[2] - cell[0]) // 2
                y = cell[1] + (cell[3] - cell[1]) // 2
                draw.rectangle((cell[0]-1, cell[1]-1, cell[2] - 1, cell[3] - 1), fill=HEX_to_RGB("#DB1962"))
                draw.text((x, y), str_x, (255, 255, 255), font=font, anchor="mm")
            
            has_item = [x for x in range(0, 9) if not x in has_number]

            for j in has_item:
                cell = cells[j][i]
                x = cell[0] + (cell[2] - cell[0]) // 2
                y = cell[1] + (cell[3] - cell[1]) // 2
                draw.rectangle((cell[0]-1, cell[1]-1, cell[2] - 1, cell[3] - 1), fill=HEX_to_RGB("#37438D"))
                id, random_item = random.choice([(a, b) for a, b in enumerate(item_list)])
                while True:
                    if j-1 >= 0:
                        if id == item_cells[j-1][i]:
                            id, random_item = random.choice([(a, b) for a, b in enumerate(item_list)])
                            continue
                    if i-1 >=0:
                        if id == item_cells[j][i-1]:
                            id, random_item = random.choice([(a, b) for a, b in enumerate(item_list)])
                            continue
                    break
                item_cells[j][i] = id
                image.paste(random_item, (cell[0], cell[1]), random_item)
        return image
        