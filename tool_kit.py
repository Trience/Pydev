from itertools import combinations

ref_table = {}


def ranking(unrank):
    if len(unrank) == 1 or len(unrank) == 0:
        return unrank
    i = 1
    while (i < len(unrank)):
        j = 0
        while (j < i):
            if (unrank[i - j] < unrank[i - j - 1]):
                a = unrank[i - j]
                unrank[i - j] = unrank[i - j - 1]
                unrank[i - j - 1] = a
                j += 1
            else:
                break
        i += 1
    return unrank


'''
class IA_reserve():
    # 分析给定的14张牌中有多少幺九牌


    # IA分析
    def ia(self, num):
        drawer = pile("temp")
        drawer.ini()
        i = 0
        result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while i < num:
            if i % (num / 50) == 0:
                print("|", end="")
            drawer.shuffle()
            result[orphan_count()] += 1
            if orphan_count() == 13:
                print("在第%d次模拟时玩家天听/天胡国士无双十三面" % (i + 1))
                for item in drawer.total[0:14]:
                    print(item, end=" ")
            i += 1
        print()
        return result

    def second(self, num):
        drawer = pile("temp")
        drawer.ini()
        i = 0
        result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while i < num:
            if i % (num / 50) == 0:
                print("|", end="")
            drawer.shuffle()
            j = 0
            while (j < 14):
                if self.orphan_count() >= j:
                    result[j] += 1
                j += 1
            i += 1
        print()
        return result
'''


def orphan_count(given):
    cnt = 0
    overlap = []
    for item in given:
        if [item.rank, item.suit] not in overlap:
            if item.rank == 1 or item.rank == 0 or item.rank == 9:
                overlap.append([item.rank, item.suit])
                cnt += 1
    return cnt


def rank_card(unrank):
    if len(unrank) == 1 or len(unrank) == 0:
        return unrank
    i = 1
    while (i < len(unrank)):
        j = 0
        while (j < i):
            if (unrank[i - j].rank < unrank[i - j - 1].rank):
                a = unrank[i - j]
                unrank[i - j] = unrank[i - j - 1]
                unrank[i - j - 1] = a
                j += 1
            else:
                break
        i += 1
    return unrank


def clean_handlike(handlike):
    temp = []
    j = 0
    while (j < 10):
        sub = []
        for unit in handlike:
            if unit.suit == j:
                sub.append(unit)
        if len(sub) != 0:
            for thing in rank_card(sub):
                temp.append(thing)
        j += 1
    return temp


# 返回二维数组，包含所有组合
def get_combinations(input_list, x):
    if x > len(input_list):
        return []
    if not input_list:
        return []
    result = list(combinations(input_list, x))
    return result


def have_same(two):
    temp = []
    for one in two:
        # for j in one:
        # temp.append(j)
        temp += one[:3]
    i = 0
    while (i < len(temp) - 1):
        if sorted(temp)[i] == sorted(temp)[i + 1]:
            return True
        i += 1
    return False


def kind_into_score(kind):
    # kind是一个set，包含了所有番种
    temp = 0
    for i in kind:
        temp += ref_table[i]
    return temp
