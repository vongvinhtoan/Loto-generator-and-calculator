import matplotlib.pyplot as plt
import math

class LotoStatisticsItem:
    def __init__(self) -> None:
        self.called_sequence = []
        self.winners = []
        
class LotoStatistics:
    def __init__(self, items: list[LotoStatisticsItem]) -> None:
        self.items = items

    def add_item(self, item: LotoStatisticsItem) -> None:
        self.items.append(item)

    def draw_calling_numbers(self) -> None:
        calling_numbers = [len(item.called_sequence) for item in self.items]
        plt.hist(calling_numbers, bins=range(0, 100, 5))
        plt.title("Calling Numbers")
        plt.xlabel("Number of Calling Numbers")
        plt.ylabel("Frequency")
        plt.show()

    def draw_winning_numbers(self) -> None:
        # plt.hist(self.winning_numbers, bins=range(0, 100, 5))
        winning_numbers = [len(item.winners) for item in self.items]
        plt.hist(winning_numbers, bins=range(0, 100, 5))
        plt.title("Winning Numbers")
        plt.xlabel("Number of Winning Numbers")
        plt.ylabel("Frequency")
        plt.show()

    def draw_all(self) -> None:
        calling_numbers = [len(item.called_sequence) for item in self.items]
        winning_numbers = [len(item.winners) for item in self.items]
        winning_times = [0] * (max([max(item.winners) for item in self.items]) + 1)

        calling_numbers_freq = [0] * 100
        for calling_number in calling_numbers:
            calling_numbers_freq[calling_number] += 1
        calling_numbers_left = 0
        while calling_numbers_freq[calling_numbers_left] == 0:
            calling_numbers_left += 1
        calling_numbers_right = 99
        while calling_numbers_freq[calling_numbers_right] == 0:
            calling_numbers_right -= 1

        winning_numbers_freq = [0] * 100
        for winning_number in winning_numbers:
            winning_numbers_freq[winning_number] += 1
        winning_numbers_left = 0
        while winning_numbers_freq[winning_numbers_left] == 0:
            winning_numbers_left += 1
        winning_numbers_right = 99
        while winning_numbers_freq[winning_numbers_right] == 0:
            winning_numbers_right -= 1

        for item in self.items:
            for winner in item.winners:
                winning_times[winner] += 1
        winning_times_x_axis = [i for i in range(0, len(winning_times))]

        sub_plt_calling_numbers = plt.subplot(3, 1, 1)
        sub_plt_calling_numbers.bar(
            range(calling_numbers_left, calling_numbers_right + 1),
            calling_numbers_freq[calling_numbers_left:calling_numbers_right + 1],
            width=0.8
        )
        avg = sum(calling_numbers) / len(calling_numbers)
        sub_plt_calling_numbers.axvline(avg, color='r', linestyle='dashed', linewidth=1)
        x_ticks = [i for i in range(calling_numbers_left, calling_numbers_right + 1, 3)] + [round(avg)]
        sub_plt_calling_numbers.set_xticks(x_ticks)
        sub_plt_calling_numbers.get_xticklabels()[len(x_ticks) - 1].set_color('r')
        sub_plt_calling_numbers.get_xticklabels()[len(x_ticks) - 1].set_fontweight('bold')
        sub_plt_calling_numbers.set_title("Thời gian chơi còn lại")
        sub_plt_calling_numbers.set_xlabel("Số lần gọi")
        sub_plt_calling_numbers.set_ylabel("Tần suất")

        sub_plt_winning_numbers = plt.subplot(3, 1, 2)
        sub_plt_winning_numbers.bar(
            range(winning_numbers_left, winning_numbers_right + 1),
            winning_numbers_freq[winning_numbers_left:winning_numbers_right + 1],
            width=0.8
        )
        avg = sum(winning_numbers) / len(winning_numbers)
        sub_plt_winning_numbers.axvline(avg, color='r', linestyle='dashed', linewidth=1)
        x_ticks = [i for i in range(winning_numbers_left, winning_numbers_right + 1, 1)] + [int(avg)]
        sub_plt_winning_numbers.set_xticks(x_ticks)
        sub_plt_winning_numbers.get_xticklabels()[len(x_ticks) - 1].set_color('r')
        sub_plt_winning_numbers.get_xticklabels()[len(x_ticks) - 1].set_fontweight('bold')

        sub_plt_winning_numbers.set_title("Kinh trùng")
        sub_plt_winning_numbers.set_xlabel("Số lượng người trúng")
        sub_plt_winning_numbers.set_ylabel("Tần suất")

        sub_plt_winning_times = plt.subplot(3, 1, 3)
        sub_plt_winning_times.bar(winning_times_x_axis, winning_times, width=0.8)
        sub_plt_winning_times.set_xticks(range(0, len(winning_times), 1))
        sub_plt_winning_times.xaxis.set_tick_params(rotation=-45)
        # make xaxis labels smaller so that they fit in the figure
        sub_plt_winning_times.tick_params(axis='x', which='major', labelsize=6)
        sub_plt_winning_times.set_title("Người thắng")
        sub_plt_winning_times.set_xlabel("Số thứ tự người thắng")
        sub_plt_winning_times.set_ylabel("Số lần thắng")
        
        # add more space between subplots
        plt.subplots_adjust(hspace=1.0)
        # make the plot wider
        plt.gcf().set_size_inches(30, 10)
        plt.show()

        