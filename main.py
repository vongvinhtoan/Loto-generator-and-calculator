from lotoDrawer import LotoDrawer
from lotoGrader import LotoGrader
import lotoSheet
import random

def __main__():
    random.seed(22125108)

    drawer = LotoDrawer()
    for i in range(0, 1):
        print(f"Drawing {i}")
        result_dir = f"results/result{i}.png"
        drawer.draw(
            result_dir=result_dir,
            background_dir="backgrounds/lotov2.png",
            frame_dir="frames/frame.png",
            loto_sheet=lotoSheet.create_random_lotoSheet(),
            font_dir="fonts/Gotham Regular.otf",
            item_dir_list=[
                "items/item 1.png",
                "items/item 2.png",
                "items/item 3.png",
                "items/item 4.png"
            ]
        )

    # grader = LotoGrader([lotoSheet.create_random_lotoSheet() for _ in range(0, 10)])
    # grader.grade(10000)

if __name__ == "__main__":
    __main__()

