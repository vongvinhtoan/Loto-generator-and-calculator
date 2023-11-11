from lotoDrawer import LotoDrawer
from lotoGrader import LotoGrader
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import lotoSheet
import random

def __main__():
    random.seed(22125108)

    font = ImageFont.truetype("fonts/Gotham Regular.otf", 75)
    item_list = [
        Image.open(item_dir) for item_dir in [
            "items/item 1.png",
            "items/item 2.png",
            "items/item 3.png",
            "items/item 4.png"
        ]
    ]
    frame = Image.open("frames/frame.png")
    background = Image.open("backgrounds/lotov2.png")
    loto_sheet = lotoSheet.create_distinct_random_sheet(1)[0]

    drawer = LotoDrawer()
    for i in range(0, 1):
        print(f"Drawing {i}")
        result_dir = f"results/result{i}.png"
        drawer.draw(
            result_dir=result_dir,
            background=background,
            frame=frame,
            loto_sheet=lotoSheet.create_random_lotoSheet(),
            font=font,
            item_list=item_list
        )

    # grader = LotoGrader([lotoSheet.create_random_lotoSheet() for _ in range(0, 10)])
    # grader.grade(10000)

if __name__ == "__main__":
    __main__()

