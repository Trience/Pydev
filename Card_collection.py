import random
from tool_kit import *
from itertools import combinations
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

    def __lt__(self, other):
        if self.suit < other.suit:
            return True
        elif self.suit > other.suit:
            return False
        elif self.rank < other.rank:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.suit > other.suit:
            return True
        elif self.suit < other.suit:
            return False
        elif self.rank > other.rank:
            return True
        else:
            return False


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
        self.close = True # 门清
        self.waiting = None  # 听牌
        self.reach = False  # 立直

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
            k = 0
            while self.move[i] + 2 > self.move[i + 1 + k]:
                if self.move[i] == self.move[i + 1 + k]:
                    if i + 1 + k < len(self.move) - 1:
                        k += 1
                        continue
                    else:
                        break
                j = 0
                if i + k + j + 2 >= len(self.move):
                    break
                while self.move[i] + 3 > self.move[i+k+j+2]:

                    if (self.move[i].rank == self.move[i + k + 1].rank - 1 == self.move[i + k + j + 2].rank - 2 and
                            self.move[i].suit ==
                            self.move[i + k + 1].suit == self.move[i + k + j + 2].suit):
                        self.possible.append([i, i + k + 1, i + k + j + 2, "straight"])
                    if i+k+j+2 < len(self.move) - 1:
                        j += 1
                    else:
                        break
                k += 1

            if (self.move[i].rank == self.move[i + 1].rank == self.move[i + 2].rank and self.move[i].suit == self.move[
                i + 1].suit == self.move[i + 2].suit):
                self.possible.append([i, i + 1, i + 2, "triple"])
            if (self.move[i].rank == self.move[i + 1].rank and self.move[i].suit == self.move[i + 1].suit):
                self.pair.append([i, i + 1, "pair"])
            i += 1
        if (self.move[i].rank == self.move[i + 1].rank and self.move[i].suit == self.move[i + 1].suit):
            self.pair.append([i, i + 1, "pair"])


    def kind(self, total, stat):
        # 根据total来算番
        result = []
        fu = 20
        sort = {'straight': [], 'triple': [], 'pair': []}
        for k in total:
            if k[-1] == 'straight':
                sort['straight'].append(k)
            elif k[-1] in ['triple','gang','angang']:
                sort['triple'].append(k)
            else:
                sort['pair'].append(k)
        shatter = [] #打散的牌

        for i in total:
            shatter += i[:-1]
        orphan = orphan_count(shatter)
        #先放一下七对子也能有的牌型
        color = set()
        for i in shatter:
            color.add(i.suit)
        if (0 in color) + (1 in color) + (2 in color) <= 1:
            #字一色
            if (0 in color) + (1 in color) + (2 in color) == 0:
                result.append(-3)
            #清一色
            elif len(color) ==1:
                if self.close:
                    result.append(32)
                else:
                    result.append(33)
            #混一色
            else:
                if self.close:
                    result.append(27)
                else:
                    result.append(28)
        #老头相关
        if orphan >= 5:
            temp = 2
            if stat ==2 or not sort['straight']:
                for unit in total:
                    if unit[0].rank not in [1, 9]:
                        temp = 1
                    if unit[0].rank != 0:
                        temp =0
                        break
                if temp == 2:
                    result.append(-4) # 清老头
                elif temp == 1:
                    result.append(17) # 混老头
        if orphan and (17 not in result):
            temp = 0
            for unit in total:
                if unit[0].rank in [1,9] or unit[-2].rank in [1,9]:
                    temp += 2
                    continue
                elif unit[0].rank != 0:
                    temp = 0
                    break
            if temp == 10:
                result.append(30 - self.close) # 纯全
            elif temp != 0:
                result.append(24 - self.close) # 混全

        #立直
        if self.reach:
            if 26 not in result:
                result.append(0)
        #断幺九
        if orphan == 0:
            result.append(1)

        #以下都是七对不可能有的牌型
        if stat == 2:
            return [result, 25] #固定25符
        #自风 场风 三元
        for i in sort['triple']:
            if i[0].suit == 3 + self.wind:
                result.append(2)
            if i[0].suit == 3:
                result.append(3)
            if i[0].suit in [7, 8, 9]:
                result.append(4)
        #平和
        if self.close:
            if not (sort['triple']) and stat == 1:
                result.append(7)
            #一杯口
            if len(sort['straight']) > 1:
                for k in range(len(sort['straight']) - 1):
                    if sort['straight'][k][0] == sort['straight'][k + 1][0]:
                        result.append(8)
            #二杯口
            if len(sort['straight']) > 3:
                if sort['straight'][0][0] == sort['straight'][1][0] and sort['straight'][2][0] == sort['straight'][3][0]:
                    result.append(31)
        #四暗刻
            if len(sort['triple'])>=3:
                result.append(14)
                if len(sort['triple'])>=4:
                    if stat == 6:
                        result.append(-5)
                    else:
                        result.append(-6)
        if not sort['straight']:
            result.append(13)
        if self.gang >=3:
            result.append(15)#三杠
            if self.gang>=4:
                result.append(-7)#四杠
        #三色同顺
        if len(sort['straight'])>=3:
            temp_list = list(combinations(sort['straight'], 3))
            for i in temp_list:
                if i[0][0].rank == i[1][0].rank == i[2][0].rank:
                    if i[0][0].suit != i[1][0].suit and i[0][0].suit != i[2][0].suit and i[1][0].suit != i[2][0].suit:
                        result.append(20 - self.close)
        #三色同刻

        if stat != 1 and stat != 6:
            fu += 2 #除了双碰和两面，只有边坎单调了
        if sort['pair'][0][0].suit in [7, 8, 9, 3, 3 + self.wind]:
            fu += 2 #自风场风三元将头
        for unit in total:
            if unit[-1] == 'triple':
                if unit not in self.shown:
                    print('debug msg: 一个暗刻')
                    if unit[0].rank in [0,1,9]:
                        fu += 8
                    else:
                        fu += 4
                else:
                    print('debug msg: 一个明刻')
                    if unit[0].rank in [0,1,9]:
                        fu += 4
                    else:
                        fu += 2
            elif unit[-1] == 'gang':
                if unit[0].rank in [0, 1, 9]:
                    fu += 16
                else:
                    fu += 8
            elif unit[-1] == 'angang':
                if unit[0].rank in [0, 1, 9]:
                    fu += 32
                else:
                    fu += 16
        fu = (fu // 10 + 1) * 10
        if not self.close:
            if not sort['triple']:
                if stat == 1:
                    fu = 30 #副露平和固定30符
        result = list(set(result))
        return [result, fu]

    def calc(self, new, stat):
        fu = 20
        # stat是表示特殊和牌的一个整数
        temp_hand = hand(self.wind)
        temp_hand.move = self.move.copy()
        temp_hand.move.append(new)
        temp_hand.move = clean_handlike(temp_hand.move)  # 生成一个14张牌的可能和牌结构
        temp_hand.shown = self.shown.copy()
        temp_hand.possible_detect()
        kinded = []
        if stat == 2:
            temp_pair = []
            for i in temp_hand.pair:
                empty_pair = []
                empty_pair.append(temp_hand.move[i[0]])
                empty_pair.append(temp_hand.move[i[1]])
                empty_pair.append('pair')
                temp_pair.append(empty_pair)

            result = self.kind(temp_pair, 2)
            return [result, temp_hand.move]
        #国士这些不用管
        if stat == 3:
            self.move.append(new)
            return [[-1], self.move]
        if stat == 4:
            self.move.append(new)
            return [[-2], self.move]

        for chosen in temp_hand.pair:
            temp = temp_hand.possible.copy()
            j = 0
            for i in range(len(temp)):
                if chosen[0] in temp[i - j] or chosen[1] in temp[i - j]:
                    temp.pop(i - j)
                    j += 1
            if len(temp_hand.shown) == 4:
                formed = temp_hand.shown + temp_hand.pair
                kinded = [self.kind(formed, stat)]
            else:
                temp_comb = get_combinations(temp, 4 - len(temp_hand.shown))
                for choice in temp_comb:
                    if have_same(choice) == False:
                        formed = temp_hand.shown.copy()
                        for unit in choice:
                            temp = unit.copy()
                            for k in range(len(temp) - 1):
                                temp[k] = temp_hand.move[unit[k]].copy()
                            formed.append(temp)
                        temp = [None, None, 'pair'] #把选中的雀头对子提炼出来
                        temp[0] = temp_hand.move[chosen[0]]
                        temp[1] = temp_hand.move[chosen[1]]
                        formed.append (temp)
                        kinded_temp = self.kind(formed, stat)
                        kinded.append(kinded_temp)
                        # 算上手牌和副露
        best = 0
        result = None
        for p in kinded:
            if kind_into_score(p[0]) >= best:
                result = p[0]
                fu = p[1]
        # 把牌理好准备结算
        final_list = self.move.copy()
        for unit in temp_hand.shown:
            final_list += unit[:-1]
        final_list += [new]
        return [result, fu, final_list]

    def wait(self):

        waiting = []
        # 国士
        if (orphan_count(self.move) == 12 and len(self.pair) == 1):
            ref = [card(1, 0), card(9, 0), card(1, 1), card(9, 1), card(1, 2), card(1, 2), card(0, 3), card(0, 4),
                   card(0, 5), card(0, 6), card(0, 7), card(0, 8), card(0, 9)]
            for kard in self.move:
                if kard in ref:
                    ref.remove(kard)
            # Markpoint: 需要修改
            waiting.append((ref[0], 3))
        if (orphan_count(self.move) == 13 and len(self.pair) == 0):
            for kard in self.move:
                waiting.append((kard, 4))


        # 七对子
        if (len(self.shown) == 0 and len(self.pair) == 6):
            temp = 0
            for i in self.possible:
                if i[-1] == 'triple':
                    temp += 1
            if temp < 1:
                print("七对")
                for e in range(len(self.move)):
                    g = 0
                    for f in self.pair:

                        if e in f:
                            g = 1
                    if g == 0:
                        waiting.append((self.move[e], 2))
        # 基本的和牌形状
        if len(self.possible) + len(self.shown) >= 3:
            status = 1
            for not_pair in self.pair:
                for v in self.possible:
                    if not_pair[0] in v == False and v[3] == 'triple' == False:
                        status = 0
            if len(self.pair) > 0:
                for chosen in self.pair:
                    temp = self.possible.copy()
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
                                #waiting.append((right[0]))
                                waiting.append((self.move[chosen[0]], 6))
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
                                if item == 'straight' or item == 'triple' or item == 'pair':
                                    lala.remove(item)
                            # print(lala)
                            for i in range(len(self.move)):
                                if i not in lala:
                                    waiting.append((self.move[i], 0))

                else:
                    print("你也别急")
        else:
            print("别急")
        #九莲
        final_waiting = list(set(waiting))
        if len(final_waiting) == 9:
            for i in range(9):
                final_waiting.append((final_waiting[0][0], 5))
                final_waiting.pop(0)

        # 去除重复项目
        # final_waiting = rank_card(final_waiting)
        dict_waiting = {}
        for i in range(len(final_waiting)):
            temp_comb = self.calc(final_waiting[i][0], final_waiting[i][1])
            dict_waiting[final_waiting[i][0]] = temp_comb

        return dict_waiting


# 牌河
class river():
    def __init__(self):
        self.rivers = [[], [], [], []]
        self.repeat = [set(), set(), set(), set()]
        self.all_count = {}
    def update(self, i, j):
        #i是玩家编号，j是牌
        self.repeat[i].add(j)
        if j in list(self.all_count.keys()):
            self.all_count[j] += 1
        else:
            self.all_count[j] = 1

