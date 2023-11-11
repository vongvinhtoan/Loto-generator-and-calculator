from lotoSheet import LotoSheet
from lotoStatistics import LotoStatisticsItem
from lotoStatistics import LotoStatistics
import random

class LotoGrader:
    def __init__(self, loto_sheets: list[LotoSheet]) -> None:
        self.loto_sheets = loto_sheets
        print(f"len(self.loto_sheets) = {len(self.loto_sheets)}")
        self.loto_statistics = LotoStatistics([])

    def grade(self, num_call: int) -> None:
        for i in range(0, num_call):
            if (i+1) % (num_call//100 + 1) == 0:
                print(f"Calling {i + 1}/{num_call}")
            self.call()

        self.loto_statistics.draw_all()

    def get_next_called_number(self, called_numbers: list[int]) -> int:
        while True:
            called_number = random.randint(1, 90)
            if called_number not in called_numbers:
                return called_number

    def call(self) -> None:
        for loto_sheet in self.loto_sheets:
            loto_sheet.reset()

        called_numbers = []
        while True:
            called_number = self.get_next_called_number(called_numbers)
            called_numbers.append(called_number)
            is_someone_won = False
            for loto_sheet in self.loto_sheets:
                loto_sheet.mark(called_number)
                if loto_sheet.isComplete():
                    is_someone_won = True

            if is_someone_won:
                break

        loto_statistic_item = LotoStatisticsItem()
        loto_statistic_item.called_sequence = called_numbers
        for i, loto_sheet in enumerate(self.loto_sheets):
            if loto_sheet.isComplete():
                loto_statistic_item.winners.append(i)

        self.loto_statistics.add_item(loto_statistic_item)

            
                
    