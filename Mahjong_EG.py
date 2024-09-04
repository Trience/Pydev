import random
from tool_kit import rank_card, get_combinations, have_same, orphan_count

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


# 一个没什么用的基本类
class collection(object):
    def __init__(self, name):
        self.name = name

    total = []

    # 展示自己的所有内容物


# 抽卡叠
class pile(collection):
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
        print("当前回合宝牌为：", end=" ")
        for dr in self.dora:
            print(dr, end=" ")
        print()


# 手牌
class hand():
    def __init__(self, ):

        self.shown = []
        self.move = []
        self.respond = []
        self.possible = []
        self.pair = []
        self.gang = 0
        self.inter = {}

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

    discard = collection("discard")

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
        temp = []
        j = 0
        while (j < 10):
            sub = []
            for unit in self.move:
                if unit.suit == j:
                    sub.append(unit)
            if len(sub) != 0:
                for thing in rank_card(sub):
                    temp.append(thing)
            j += 1
        self.possible_detect()
        self.move = temp
        self.inter = self.interaction()

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

    def wait(self):

        waiting = []
        # 国士
        if (orphan_count(self.move) == 12 and len(self.pair) == 1):
            ref = [card(1, 0), card(9, 0), card(1, 1), card(9, 1), card(1, 2), card(1, 2), card(0, 3), card(0, 4),
                   card(0, 5), card(0, 6), card(0, 7), card(0, 8), card(0, 9)]
            for kard in self.move:
                if kard in ref:
                    ref.remove(kard)
            waiting.append(ref[0])

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
                        if chosen[0] in temp[i - j]:
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
                                waiting.append(self.move[chosen[0]])
                                if (chosen in self.pair):
                                    self.pair.remove(chosen)
                            # 两连的平和
                            if right[0].suit == right[1].suit and right[0].rank + 1 == right[1].rank:
                                if (right[0].rank != 1):
                                    waiting.append(card(right[0].rank - 1, right[0].suit))
                                if (right[1].rank != 9):
                                    waiting.append(card(right[1].rank + 1, right[1].suit))
                            # 坎张听牌
                            if right[0].suit == right[1].suit and right[0].rank + 2 == right[1].rank:
                                waiting.append(card(right[0].rank + 1, right[1].suit))
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
                                    waiting.append(self.move[i])

                else:
                    print("你也别急")
        else:
            print("别急")
        final_waiting = []

        # 去除重复项目
        for kard in waiting:
            status = 0
            for k in final_waiting:
                if kard == k:
                    status = 1
            if status == 0:
                final_waiting.append(kard)
        final_waiting = rank_card(final_waiting)
        return final_waiting


# 牌河
class river():
    def __init__(self):
        self.rivers = [[], [], [], []]
        self.repeat = [set(), set(), set(), set()]

    def update(self, i, j):
        self.repeat[i].add(j)


# 游戏进行！
class player(object):
    winds = ['東', '南', '西', '北']

    def __init__(self, name, wind, button, score, ranking):
        self.name = name
        self.wind = wind
        self.button = button  # Is button or not, boolean
        self.score = score
        self.ranking = ranking
        self.hand = hand()
        self.pure = True  # 被别人碰过吗

    def copy(self):
        return player(self.name, self.wind, self.button, self.score, self.ranking)

    def __str__(self):
        des = '玩家:' + str(self.name) + '\t风向:' + self.winds[self.wind] + '\t得分:' + str(
            self.score) + '\t 顺位:' + str(self.ranking)
        return (des)

    def __repr__(self):
        des = '玩家:' + str(self.name) + '\t风向:' + self.winds[self.wind] + '\t得分:' + str(
            self.score) + '\t 顺位:' + str(self.ranking) + '\n'
        return (des)

    def play(self, round):
        print('现在余{}, {}号玩家出牌'.format(round, self.name))
        self.hand.print_all()

        while True:
            ans = input('出牌: ')
            try:
                if len(ans) == 2:
                    cardans = card(int(ans[0]), names_reversed[ans[1]])
                else:
                    cardans = card(0, names_reversed[ans[0]])
                for i in range(len(self.hand.move)):
                    if self.hand.move[i] == cardans:
                        self.hand.move.pop(i)
                        self.hand.clean()
                        return (cardans)
                print("你目前未持有{}".format(cardans))
            except:
                print('这不是一个有效输入')

    def chi(self, new, round):
        self.hand.print_all()
        ans = input("{}号玩家,你是否要吃{}?(Y/N)\n".format(self.name, new))
        if ans in ['Y', 'y']:
            target = self.hand.inter['c'][new]
            choice = 0
            # Markpoint 需要防报错
            if len(target) > 1:
                print('输入希望用来吃的牌组的编号')
                i = 1
                for comb in target:
                    print('{}：{}, {}'.format(i, self.hand.move[comb[0]], self.hand.move[comb[1]]))
                    i += 1
                choice = int(input()) - 1

            temp = []
            i = target[choice][0]
            j = target[choice][1]
            temp.append(self.hand.move[i])
            temp.append(self.hand.move[j])
            temp.append(new)
            temp.append('straight')
            # temp.append((self.name + 3) % 4)
            self.hand.shown.append(temp)
            self.hand.move.pop(i)
            self.hand.move.pop(j - 1)
            self.play(round)

        else:
            print("不吃")
        return None

    def pon(self, new, round):
        self.hand.print_all()
        ans = input('{}号玩家，你是否要碰{}?Y/N'.format(self.name, new))
        if ans in ['Y', 'y']:
            temp = []
            i = self.hand.inter['p'][new][0]
            j = self.hand.inter['p'][new][1]
            temp.append(self.hand.move[i])
            temp.append(self.hand.move[j])
            temp.append(new)
            temp.append('triple')
            self.hand.shown.append(temp)
            self.hand.move.pop(i)
            self.hand.move.pop(j - 1)
            self.play(round)
        else:
            print("不碰")
        return None

    def gang(self, new, round, add):
        self.hand.print_all()
        # add是可能存在的杠牌
        ans = input('{}号玩家，你是否要杠{}?Y/N'.format(self.name, new))
        if ans in ['Y', 'y']:
            temp = []
            i = self.hand.inter['g'][new][0]
            j = self.hand.inter['g'][new][1]
            k = self.hand.inter['g'][new][2]
            temp.append(self.hand.move[i])
            temp.append(self.hand.move[j])
            temp.append(self.hand.move[k])
            temp.append(new)
            temp.append('gang')
            self.hand.shown.append(temp)
            self.hand.move.pop(i)
            self.hand.move.pop(i)
            self.hand.move.pop(i)
            self.hand.move.append(add)
            self.play(round)
        else:
            print("不碰")
        return None


class round(object):

    # but_pos is the button player's number
    # players是整句游戏中的编码，不是一轮中的风向

    def __init__(self, but_pos, pool, players):
        self.but_pos = but_pos
        self.pool = pool  # 场供
        self.players = players  # 传入的玩家信息
        self.river = river()  # 牌河
        self.turn = but_pos  # 到谁出牌 (每回合更新)

        self.draw = pile('')
        self.draw.ini()
        self.history = len(self.draw.total) - 14  # 还剩多少牌
        self.dora = self.draw.dora
        self.doradown = self.draw.doradown

    def __str__(self):
        return ('東{}局，当前玩家:\n{}'.format(self.but_pos + 1, self.players))

    def initialize(self):

        for i in range(4):
            for j in range(13):
                self.players[i].hand.move.append(self.draw.total.pop(0))
        self.players[self.but_pos].hand.move.append(self.draw.total.pop(0))
        for i in range(4):
            self.players[i].wind = (i + 4 - self.but_pos) % 4
            self.players[i].hand.initiate()

    def around(self, num, last):
        # 返回的格式是(出了牌的玩家，出的牌)
        self.history = len(self.draw.total) - 14
        # num是现在几号玩家出票,last是上一张牌

        respond = None  # 是否有玩家应答
        who = num  # 谁出了牌
        # 询问碰，杠
        for one in self.players:
            if one.name == (num + 3) % 4:
                continue
            pon = list(one.hand.inter['p'].keys())
            gang = list(one.hand.inter['g'].keys())
            if last in pon:
                ans = one.pon(last, self.history)  # 碰
                if ans:
                    self.players[(num + 3) % 4].pure = False
                    respond = ans
                    who = one.name
                    break
            if last in gang:
                ans = one.gang(last, self.history, self.draw.total[-1])  # 碰
                if ans:
                    self.draw.total.pop(-1)
                    self.players[(num + 3) % 4].pure = False
                    self.draw.show_dora(1)
                    self.dora = self.draw.dora
                    self.doradown = self.draw.doradown
                    respond = ans
                    who = one.name
                    break
        if respond:
            # 谁出了牌，出了什么牌
            return ([who, respond])
        # 到num号玩家行动！
        if last in list(self.players[num].hand.inter['c'].keys()):
            respond = self.players[num].chi(last, self.history)  # 吃
            if respond:
                self.players[(num + 3) % 4].pure = False
                return ([num, respond])
        # 牌进入牌河
        self.river.rivers[(num + 3) % 4].append(last)  # 放进牌河
        self.river.update((num + 3) % 4, last)
        print("東{}局".format(self.but_pos + 1), end=', ')
        self.players[num].hand.move.append(self.draw.total.pop(0))
        return ([num, self.players[num].play(self.history)])

    def agame(self):
        self.initialize()
        self.players[self.but_pos].play(self.history)

        return 0


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


def demo():
    mypile = pile("mypile")
    testant = hand()
    # 初始化和洗牌
    mypile.ini()
    # print(mypile.dora[0], mypile.doradown[0])

    return 0

    # testant.print_all()


# demo()


def test_wait():
    test_hand = hand()

    # test_hand.move = [card(1, 1), card(1, 1), card(1, 1), card(6, 1), card(7, 1), card(8, 1), card(1, 2), card(2, 2),card(3, 2), card(3, 0), card(3, 0), card(4, 1), card(5, 1)]

    test_hand.move = [card(1, 1), card(1, 1), card(1, 1), card(3, 1), card(2, 1), card(4, 1), card(5, 1), card(6, 1),
                      card(7, 1), card(8, 1), card(9, 1), card(9, 1), card(9, 1)]
    # test_hand.total = [card(1, 1), card(1, 1), card(6, 1), card(6, 1), card(8, 1), card(8, 1), card(2, 2), card(2, 2),
    # card(3, 2), card(3, 0), card(3, 0), card(5, 1), card(5, 1)]
    test_hand.initiate()

    print(len(test_hand.move))
    test_hand.print_all()
    test_hand.possible_detect()
    print(test_hand.possible)
    print(test_hand.pair)
    print("WAITING:", end=' ')
    wl = test_hand.wait()
    print(wl)


test_wait()


def demo_inter():
    a = player(0, 0, 1, 25000, 1)
    b = player(1, 1, 0, 25000, 2)
    c = player(2, 2, 0, 25000, 3)
    d = player(3, 3, 0, 25000, 4)

    test_hand = hand()
    # test_hand.total = [card(1, 1), card(1, 1), card(6, 1), card(6, 1), card(8, 1), card(8, 1), card(2, 2), card(2, 2),
    # card(3, 2), card(3, 0), card(3, 0), card(5, 1), card(5, 1)]
    # test_hand.move = [card(1, 1), card(1, 1), card(1, 1), card(6, 1), card(7, 1), card(8, 1), card(1, 2), card(2, 2),card(3, 2), card(3, 0), card(3, 0), card(4, 1), card(5, 1)]
    test_hand.initiate()

    easy_player = player(0, 0, 1, 25000, 1)
    easy_player.hand = test_hand
    test_game = round(0, 0, [a, b, c, d])
    easy_game = round(0, 0, [easy_player, easy_player, easy_player, easy_player])
    # easy_game.around(0,card(6,1))
    # test_game.initialize()
    # test_game.around(0,card(1,1))
    test_hand.print_all()
    print(test_hand.wait())
# demo_inter()
