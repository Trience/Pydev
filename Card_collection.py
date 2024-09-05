import random
from tool_kit import *
names = {
    0: 'm',
    1: 'p',
    2: 's',
    3: '東',
    4: '南',
    5: '西',
    6: '北',
    7: '白',
    8: '發',
    9: '中',
}
names_reversed = {value: key for key, value in names.items()}
class card(object):
    def __init__(self, rank, suit, aka=False):
        self.suit = suit
        self.rank = rank
        self.aka = aka  # 布尔值，是否是赤宝牌

    def copy(self):
        return card(self.rank, self.suit)

    # 方便内部统计的小编号
    private = 0

    # names = ['m', 'p', 's', '東', '南', '西', '北', '白', '發', '中']

    # 基础地反馈一个标准编号
    def display(self):
        return str(self.rank) + self.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __eq__(self, other):
        if (self.rank == other.rank and self.suit == other.suit):
            return True
        else:
            return False

    def __str__(self):
        out = ''
        if self.aka:
            out += '赤'
        if self.rank != 0:
            out += str(self.rank)
        out += names[self.suit]
        return out

    def __repr__(self):
        out = ''
        if self.aka:
            out += '赤'
        if self.rank != 0:
            out += str(self.rank)
        out += names[self.suit]
        return out

    def __add__(self, other):
        return card(self.rank + other, self.suit)


# 抽卡叠
class pile():
    dora = []
    doradown = []
    gang = 0

    def ini(self):  # 初始化，给牌堆136张牌
        # 我知道这里是屎山但是我修改编码系统之后懒得改了，就这样吧
        i = 0
        self.dora = []
        while i < 4:
            self.total.append(card(0, 3))
            self.total.append(card(0, 4))
            self.total.append(card(0, 5))
            self.total.append(card(0, 6))
            self.total.append(card(0, 7))
            self.total.append(card(0, 8))
            self.total.append(card(0, 9))
            j = 1
            while j <= 9:
                if i == 0 and j == 5:
                    self.total.append(card(j, 0, True))
                    self.total.append(card(j, 1, True))
                    self.total.append(card(j, 2, True))
                else:
                    self.total.append(card(j, 0))
                    self.total.append(card(j, 1))
                    self.total.append(card(j, 2))
                j += 1
            i += 1
        self.shuffle()
        self.show_dora(1)

    # 把牌洗一遍
    def shuffle(self):
        temp = []
        i = 0
        fix = len(self.total)
        while i < fix:
            temp.append(self.total.pop(random.randint(0, len(self.total)) - 1))
            i += 1
        self.total = temp

    # 宝牌指示牌
    def dora_indicator(self, n):
        # n从零开始算起，n=0为第一张表 ，n=1为第一张里
        temp = self.total[-5 - n]
        dora = card(0, 0)
        if temp.rank != 0:
            dora.suit = temp.suit
            if temp.rank != 9:
                dora.rank = temp.rank + 1
            else:
                dora.rank = 1
        elif temp.suit in [3, 4, 5, 6]:
            dora.suit = (temp.suit + 2) % 4 + 3
        elif temp.suit in [7, 8, 9]:
            dora.suit = temp.suit % 3 + 7

        return dora

    # 每回合展示宝牌，如果addnew为1，则增加一张新宝牌
    def show_dora(self, add_new):
        if add_new == 1:
            print("翻开了一张新宝牌！")
            self.dora.append(self.dora_indicator(2 * self.gang))
            self.doradown.append(self.dora_indicator(2 * self.gang + 1))
            self.gang += 1
        print("当前回合宝牌为：", end=" ")
        for dr in self.dora:
            print(dr, end=" ")
        print()


# 手牌
class hand():
    def __init__(self, wind):

        self.wind = wind
        self.shown = []
        self.move = []
        self.respond = []
        self.possible = []
        self.pair = []
        self.gang = 0
        self.inter = {}
        self.yi = []
        self.waiting = None #听牌
        self.reach = False #立直

    def interaction(self):

        # 可以鸣牌的情况
        inter = {
            'c': {},
            'p': {},
            'g': {}
        }
        # 注意c的储存格式不一样！！！
        for i in range(len(self.move) - 1):
            j = 0
            while True:
                j += 1
                if i + j == len(self.move):
                    break
                if self.move[i] == self.move[i + j]:

                    inter['p'][self.move[i].copy()] = [i, i + j]
                    continue
                elif self.move[i] + 1 == self.move[i + j]:
                    try:
                        inter['c'][self.move[i] + (-1)].append([i, i + j])
                    except KeyError:
                        inter['c'][self.move[i] + (-1)] = []
                        inter['c'][self.move[i] + (-1)].append([i, i + j])
                    try:
                        inter['c'][self.move[i] + 2].append([i, i + j])
                    except KeyError:
                        inter['c'][self.move[i] + 2] = []
                        inter['c'][self.move[i] + 2].append([i, i + j])
                    continue
                elif self.move[i] + 2 == self.move[i + j]:
                    try:
                        inter['c'][self.move[i] + 1].append([i, i + j])
                    except KeyError:
                        inter['c'][self.move[i] + 1] = []
                        inter['c'][self.move[i] + 1].append([i, i + j])
                    continue
                else:
                    break

        for pairs in self.possible:
            if pairs[3] == 'triple':
                inter['g'][self.move[pairs[0]].copy()] = pairs[:3]
        return inter

    def print_all(self):
        # 打印所有牌
        print("可动手牌:", end=' ')
        for units in self.move:
            print(units, end=" ")
        print("副露:", end=' ')
        for units in self.shown:
            for i in range(3):
                print(units[i], end=' ')
            print(' | ')
        print('')

    def print_all_slash(self):
        # 打印所有牌，用|列出新获得的牌
        print("可动手牌:", end=' ')
        for units in self.move[:-1]:
            print(units, end=" ")
        print('| ', self.move[-1])
        print('')
        print("副露:", end=' ')
        for units in self.shown:
            for i in range(3):
                print(units[i], end=' ')
            print(' | ')
        print('')

    # 理牌

    def clean(self):
        self.move = clean_handlike(self.move)
        self.possible_detect()

        self.inter = self.interaction()
        self.waiting = self.wait()

    def initiate(self):
        self.possible = []
        self.pair = []
        self.shown = []
        self.gang = 0
        self.clean()
        self.inter = self.interaction()

    # 以[索引，索引，索引，类型]的格式显示可以成一组牌的牌

    def possible_detect(self):
        i = 0
        self.possible = []
        self.respond = []
        self.pair = []

        # 已经成形的所有组合
        while i < len(self.move) - 2:
            # print(type(self.move[i]))
            if (self.move[i].rank == self.move[i + 1].rank - 1 == self.move[i + 2].rank - 2 and self.move[i].suit ==
                    self.move[i + 1].suit == self.move[i + 2].suit):
                self.possible.append([i, i + 1, i + 2, "straight"])
            if (self.move[i].rank == self.move[i + 1].rank == self.move[i + 2].rank and self.move[i].suit == self.move[
                i + 1].suit == self.move[i + 2].suit):
                self.possible.append([i, i + 1, i + 2, "triple"])
            if (self.move[i].rank == self.move[i + 1].rank and self.move[i].suit == self.move[i + 1].suit):
                self.pair.append([i, i + 1, "double"])

            i += 1
        if (self.move[i].rank == self.move[i + 1].rank and self.move[i].suit == self.move[i + 1].suit):
            self.pair.append([i, i + 1, "double"])
    def kind(self, total, stat):
        #根据total来算番
        return

    def calc(self, new, stat):
        #stat是表示特殊和牌的一个整数
        temp_hand = hand(self.wind)
        temp_hand.move = clean_handlike(temp_hand.move.append(new)) #生成一个14张牌的可能和牌结构
        temp_hand.shown = self.shown
        temp_hand.possible_detect()
        for chosen in temp_hand.pair:
            temp = temp_hand.possible.copy()
            j = 0
            for i in range(len(temp)):
                if chosen[0] in temp[i] or chosen[1] in temp[i]:
                    temp.pop(i - j)
                    j += 1
            if len(temp_hand.shown) == 4:
                formed = temp_hand.shown + temp_hand.pair
                kinded = temp_hand.kind(formed, stat)
            else:
                temp_comb = get_combinations(temp, 4 - len(temp_hand.shown))
                for choice in temp_comb:
                    if have_same(choice) == False:
                        formed = temp_hand.shown
                        for unit in temp_hand.possible:
                            temp = unit.copy()
                            for k in range(len(temp)):
                                temp[k] = temp_hand.move[unit[k]].copy()
                            formed.append(temp)
                        kinded = temp_hand.kind(formed, stat)
                        #算上手牌和副露

        #把牌理好准备结算
        final_list = self.move.copy()
        for unit in temp_hand.shown:
            final_list.append(unit[:-1])
        return [kinded, final_list]
    def wait(self):

        waiting = []
        # 国士
        if (orphan_count(self.move) == 12 and len(self.pair) == 1):
            ref = [card(1, 0), card(9, 0), card(1, 1), card(9, 1), card(1, 2), card(1, 2), card(0, 3), card(0, 4),
                   card(0, 5), card(0, 6), card(0, 7), card(0, 8), card(0, 9)]
            for kard in self.move:
                if kard in ref:
                    ref.remove(kard)
            #Markpoint: 需要修改
            waiting[ref[0]] = []

        # 七对子
        if (len(self.shown) == 0 and len(self.pair) == 6):
            print("七对")
            for e in range(len(self.move)):
                g = 0
                for f in self.pair:

                    if e in f:
                        g = 1
                if g == 0:
                    waiting.append(self.move[e])
        # 基本的和牌形状
        if len(self.possible) + len(self.shown) >= 3:
            status = 1
            for not_pair in self.pair:
                for v in self.possible:
                    if not_pair[0] in v == False and v[3] == 'triple' == False:
                        status = 0
            if len(self.pair) > 0:
                for chosen in self.pair:
                    temp = []
                    for pu in self.possible:
                        temp.append(pu)
                    j = 0
                    for i in range(len(temp)):
                        if chosen[0] in temp[i - j] or chosen[1] in temp[i - j]:
                            temp.pop(i - j)
                            j += 1
                    # print(temp)
                    # print("COMBINATION:",get_combinations(temp, 3 - len(self.shown)))
                    total_comb = get_combinations(temp, 3 - len(self.shown))
                    for choice in total_comb:

                        # print("choice:", choice)
                        if have_same(choice) == False:
                            # print(choice)
                            lala = []
                            for one in choice:
                                lala += one[:3]
                            # print(lala)
                            left = self.move
                            right = []  # 正在听牌中的两张牌
                            # print("LEFT:", left)
                            n = len(left)
                            for i in range(0, n):
                                if i not in lala and i != chosen[0] and i != chosen[1]:
                                    right.append(left[i])
                            # print("LEFT:", right, len(right))
                            # 双碰听牌
                            if right[0] == right[1]:
                                waiting.append(right[0])
                                waiting.append((self.move[chosen[0]], 0))
                                if (chosen in self.pair):
                                    self.pair.remove(chosen)
                            # 两连的平和
                            if right[0].suit == right[1].suit and right[0].rank + 1 == right[1].rank:
                                if (right[0].rank != 1) and (right[1].rank != 9):
                                    waiting.append((card(right[0].rank - 1, right[0].suit), 1))
                                    waiting.append((card(right[1].rank + 1, right[1].suit), 1))
                                elif (right[0].rank != 1):
                                    waiting.append((card(right[0].rank - 1, right[0].suit), 0))
                                elif (right[1].rank != 9):
                                    waiting.append((card(right[1].rank + 1, right[1].suit), 0))
                            # 坎张听牌
                            if right[0].suit == right[1].suit and right[0].rank + 2 == right[1].rank:
                                waiting.append((card(right[0].rank + 1, right[1].suit), 0))
                # print("AHHH:",waiting)
            # 单调，或1234等牌型
            if (len(self.pair) == 0 or status == 1):
                # print("哇奥奥")
                if ((len(self.possible) + len(self.shown) >= 4)):
                    temp = []
                    for pu in self.possible:
                        temp.append(pu)
                    # print(len(temp))
                    # print(get_combinations(temp, 4 - len(self.shown)))
                    for choice in get_combinations(temp, 4 - len(self.shown)):
                        if have_same(choice) == False:
                            lala = []
                            for one in choice:
                                for j in one:
                                    lala.append(j)
                            for item in lala:
                                if item == 'straight' or item == 'triple' or item == 'double':
                                    lala.remove(item)
                            # print(lala)
                            for i in range(len(self.move)):
                                if i not in lala:
                                    waiting.append((self.move[i], 0))

                else:
                    print("你也别急")
        else:
            print("别急")
        final_waiting = list(set(waiting))
        # 去除重复项目
        #final_waiting = rank_card(final_waiting)
        '''
        dict_waiting = {}
        for i in range(len(final_waiting)):
            temp_comb = self.calc(final_waiting[i][0], final_waiting[i][1])
            if temp_comb[0]:
                dict_waiting[final_waiting[i]] = temp_comb
            else:
                print("{}无役".format(final_waiting[i]))
        '''
        return final_waiting




# 牌河
class river():
    def __init__(self):
        self.rivers = [[], [], [], []]
        self.repeat = [set(), set(), set(), set()]

    def update(self, i, j):
        self.repeat[i].add(j)
