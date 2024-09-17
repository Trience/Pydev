from itertools import combinations

ref_table = {
    -7: ['四杠子',100],
    -6: ['四暗刻单骑', 200],
    -5: ['四暗刻', 100],
    -4: ['清老头',100],
    -3: ['字一色', 100],
    -2: ['国士无双十三面', 200],
    -1: ['国士无双', 100],
    0: ['立直', 1],
    1: ['断幺九', 1],
    2: ['自风', 1],
    3: ['场风', 1],
    4: ['三元', 1],
    5: ['一发', 1],
    6: ['门清自摸', 1],
    7: ['平和', 1],
    8: ['一杯口', 1],
    9: ['河底摸鱼', 1],
    10: ['海底捞月', 1],
    11: ['杠上开花', 1],
    12: ['抢杠', 1],
    13: ['对对和', 2],
    14: ['三暗刻', 2],
    15: ['三杠子', 2],
    16: ['三色同刻', 2],
    17: ['混老头', 2],
    18: ['小三元', 2],
    19: ['三色同刻', 2],
    20: ['三色同刻(副露)', 1],
    21: ['一气通贯', 2],
    22: ['一气通贯(副露)',1],
    23: ['混全带幺九', 2],
    24: ['混全带幺九(副露)', 1],
    25: ['七对子', 2],
    26: ['W立直', 2],
    27: ['混一色', 3],
    28: ['混一色(副露)', 2],
    29: ['纯全带幺九', 3],
    30: ['纯全带幺九(副露)', 2],
    31: ['二杯口', 3],
    32: ['清一色', 6],
    33: ['清一色(副露)', 5]

}


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
        temp += ref_table[i][1]
    return temp
