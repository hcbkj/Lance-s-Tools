# https://blog.csdn.net/u012328476/article/details/51149363?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1-51149363-blog-81911548.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1-51149363-blog-81911548.pc_relevant_default&utm_relevant_index=1
# 理解@classmethod及@staticmethod
D = 1
M = 2
Y = 333


class Date(object):
    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    def tellDate(self):
        print('Today is %s-%s-%s' % (self.day, self.month, self.year))

    @classmethod
    def from_string(cls, date_as_string):
        D, M, Y = map(int, date_as_string.split('-'))
        date = cls(D, M, Y)
        return date

    @staticmethod
    def is_date_valid(date_as_string):
        D, M, Y = map(int, date_as_string.split('-'))
        return D <= 31 and M <= 12 and Y <= 3999


if __name__ == '__main__':
    date1 = Date()
    # date1.tellDate()
    date2 = Date.from_string("30-06-2022")
    # date2.tellDate()
    # print(Date.is_date_valid("30-06-2022"))
    Date(30, 6, 2022).tellDate()

# https://blog.csdn.net/GeekLeee/article/details/52624742?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1-52624742-blog-51149363.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1-52624742-blog-51149363.pc_relevant_default&utm_relevant_index=2