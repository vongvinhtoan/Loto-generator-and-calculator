from lotoSheet import LotoSheet
from lotoStatistics import LotoStatisticsItem
from lotoStatistics import LotoStatistics
import random

class LotoGrader:
    def __init__(self, loto_sheets: list[LotoSheet]) -> None:
        self.loto_sheets = loto_sheets
        self.loto_statistics = LotoStatistics([])

    def grade(self, num_call: int, called_seq: list[int], is_show_figure: bool = True) -> None:
        for loto_sheet in self.loto_sheets:
            loto_sheet.reset()
        winners = []
        for loto_number in called_seq:
            for loto_sheet in self.loto_sheets:
                loto_sheet.mark(loto_number)
            winners = [loto_sheet for loto_sheet in self.loto_sheets if loto_sheet.isComplete()]
            
            if len(winners) > 0:
                print(f"Found winner(s) at {called_seq.index(loto_number) + 1}th call, with number {loto_number}")
                print(f"No. of winners: {len(winners)}")
                print("Winners:")
                for winner in winners:
                    print(winner.id())
                return

        if len(winners) > 0:
            print("Winners:")
            for winner in winners:
                print(winner.id())
            return

        for i in range(0, num_call):
            if (i+1) % (num_call//10) == 0:
                print(f"Processing {i + 1}/{num_call}")
            self.call(called_seq)

        self.loto_statistics.draw_all(is_show_figure)

    def get_next_called_number(self, called_numbers: list[int]) -> int:
        while True:
            called_number = random.randint(1, 90)
            if called_number not in called_numbers:
                return called_number

    def call(self, called_seq: list[int]) -> None:
        for loto_sheet in self.loto_sheets:
            loto_sheet.reset()
            for loto_number in called_seq:
                loto_sheet.mark(loto_number)
            if loto_sheet.isComplete():
                loto_statistic_item = LotoStatisticsItem()
                loto_statistic_item.called_sequence = []
                loto_statistic_item.winners.append(self.loto_sheets.index(loto_sheet))
                self.loto_statistics.add_item(loto_statistic_item)
                return

        called_numbers = called_seq.copy()
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
        loto_statistic_item.called_sequence = [x for x in called_numbers if not x in called_seq]
        for i, loto_sheet in enumerate(self.loto_sheets):
            if loto_sheet.isComplete():
                loto_statistic_item.winners.append(i)

        self.loto_statistics.add_item(loto_statistic_item)