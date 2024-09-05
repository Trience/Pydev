from Card_collection import card, hand, river, pile
import time

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


# 游戏进行！
class player(object):
    winds = ['東', '南', '西', '北']

    def __init__(self, name, wind, button, score, ranking):
        self.name = name
        self.wind = wind
        self.button = button  # Is button or not, boolean
        self.score = score
        self.ranking = ranking
        self.hand = hand(wind)
        self.gangnum = 0 #杠过几次
        self.pure = True  # 被别人碰过吗
        self.zhen = [] #振听
        self.reach = False #是否立直

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
        self.hand.clean()

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

    def ron(self, new):
        #返回的是一整个player
        self.hand.print_all()
        ans = input('{}号玩家，你是否要胡{}?(Y/N)'.format(self.name, new))
        if ans in ['Y', 'y']:
            self.hand.move.append(new)
            self.hand.clean()
            return self
        else:
            return None



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
            return self.play(round)

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
            return self.play(round)
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
            self.gangnum += 1
            return self.play(round)
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

        self.draw = pile()
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
        win = [] #一个包含所有胡牌的组
        # 询问碰，杠
        for one in self.players:
            if one.name == (num + 3) % 4:
                continue
            if last in one.wait:
                if last not in one.zhen:
                    win.append(one.ron())
                    #查看是否有一炮多响
            if win:
                return [-1, card(0,0)]

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
                    if self.gang >= 4:
                        #是否是一个人杠了四次，否则四杠散
                        temp = 0
                        for one in self.players:
                            if one.gangnum != 0:
                                temp += 1
                        if temp > 1:
                            return [-2, card(0,0)] #四杠散了
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
        self.players[(num + 3) % 4].zhen = list(self.river.repeat[(num + 3) % 4])
        print("東{}局".format(self.but_pos + 1), end=', ')
        self.players[num].hand.move.append(self.draw.total.pop(0))
        return ([num, self.players[num].play(self.history)])

    def agame(self):
        self.initialize()
        self.players[self.but_pos].play(self.history)

        return 0





