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
        self.pure = True  # 被别人碰过吗
        self.zhen = set()  # 振听
        self.reach = False  # 是否立直
        self.cangang = [] #有可能加杠或者暗杠吗

    def copy(self):
        return player(self.name, self.wind, self.button, self.score, self.ranking)

    def __str__(self):
        des = '玩家:' + str(self.name) + '\t风向:' + self.winds[self.wind] + '\t得分:' + str(
            self.score) + '\t 顺位:' + str(self.ranking)
        return (des)

    def __repr__(self):
        des = '当前玩家:' + str(self.name) + '\t风向:' + self.winds[self.wind] + '\t得分:' + str(
            self.score) + '\t 顺位:' + str(self.ranking) + '\n'
        return (des)
    def isclose(self):
        for unit in self.hand.shown:
            if unit[-1] != 'angang':
                return False
        else:
            return True


    def play(self, round):
        print('现在余{}, {}'.format(round, self))
        new = self.hand.move[-1] #进张
        print(f'进张为{new}')
        #暗杠
        if new in list(self.hand.inter['g'].keys()):
            self.cangang.append(new)
        for kngang in self.cangang:
            ans = input('是否暗杠{}(Y/N)?'.format(self.hand.move[-1]))
            if ans in ['Y', 'y']:
                self.cangang.remove(kngang)
                temp = []
                for i in range(4):
                    temp.append(kngang)
                temp.append('angang')
                self.hand.gang += 1
                while kngang in self.hand.move:
                    self.hand.move.remove(kngang)


        #加杠
        for i in self.hand.shown:
            if i[-1] == 'triple' and i[0] == self.hand.move[-1]:
                ans = input('是否加杠{}(Y/N)?'.format(self.hand.move[-1]))
                if ans in ['Y', 'y']:
                    i.insert(0, self.hand.move.pop(-1))
                    i[-1] = 'gang'
                    self.hand.gang += 1
                    return [1, self.name, i[0], 0] #加杠反馈
        if self.reach:
            self.hand.print_all()
            print('立直中')
            ans = self.hand.move.pop(-1)
            return ans
        else:
            self.hand.print_all()


            self.hand.clean()
            stat = 0 #是否能立直
            if self.hand.waiting and self.hand.close:
                print("现在可以立直：")
                stat = 1
            while True:
                ans = input('出牌: ')
                try:
                    if len(ans) == 2:
                        cardans = card(int(ans[0]), names_reversed[ans[1]])
                    else:
                        cardans = card(0, names_reversed[ans[0]])
                    for i in range(len(self.hand.move)):
                        if self.hand.move[i] == cardans:
                            if cardans in self.cangang:
                                self.cangang.remove(cardans)
                            self.hand.move.pop(i)
                            self.hand.clean()
                            if stat == 1:
                                r = input('立直？(Y/N)')
                                if r == 'Y' or r == 'y':
                                    self.reach = True
                            if self.hand.waiting:
                                print("waiting:", self.hand.waiting)
                            return (cardans)
                    print("你目前未持有{}".format(cardans))
                except:
                    print('这不是一个有效输入')

    #吃碰杠之后的play
    def dplay(self, round):
        print('现在余{}, {}'.format(round, self))
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
                        if self.hand.waiting:
                            print("waiting:", self.hand.waiting)
                        return (cardans)
                print("你目前未持有{}".format(cardans))
            except:
                print('这不是一个有效输入')


    def ron(self, new):
        # 返回的是一整个player
        self.hand.print_all()
        ans = input('{}号玩家，你是否要胡{}?(Y/N)'.format(self.name, new))
        if ans in ['Y', 'y']:
            if self.hand.close:
                self.hand.waiting[new][1] += 10 #门清荣和+10
                if -5 in self.hand.waiting[new][0]:
                    self.hand.waiting[new][0].remove(-5)#荣和四暗刻降级
                elif 14 in self.hand.waiting[new][0]:
                    self.hand.waiting[new][0].remove(14)#荣和三暗刻消失
            temp = self.hand.waiting[new]
            return temp
        else:
            return None

    def zimo(self, new):
        self.hand.print_all()
        ans = input('{}号玩家，你是否要自摸{}?(Y/N)'.format(self.name, new))
        if ans in ['Y', 'y']:
            self.hand.waiting[new][1] += 2
            if 7 in self.hand.waiting[new][0]:
                self.hand.waiting[new][1] = 20
            temp = self.hand.waiting[new]
            return temp
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
            if new.rank<self.hand.move[i]:
                temp.insert(0, new)
            elif new.rank<self.hand.move[j]:
                temp.insert(1, new)
            else:
                temp.append(new)
            temp.append('straight')
            # temp.append((self.name + 3) % 4)
            self.hand.shown.append(temp)
            self.hand.move.pop(i)
            self.hand.move.pop(j - 1)
            return self.dplay(round)

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
            return self.dplay(round)
        else:
            print("不碰")
        return None

    def gang(self, new, add):
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
            self.hand.gang += 1
            return [2]
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
        self.players[but_pos].button = 1
        self.river = river()  # 牌河
        self.turn = but_pos  # 到谁出牌 (每回合更新)

        self.draw = pile()
        self.draw.ini()
        print(f'庄家为{but_pos}号玩家')
        self.history = len(self.draw.total) - 14  # 还剩多少牌
        self.reach = [False, False, False, False] #谁立直了
        self.ipa = [False, False, False, False] #一发计算
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
        #四家立直
        if self.reach == [True, True, True, True]:
            return [-3, card[0, 0]]

        temp = 0
        temp_cnt = 0
        for one in self.players:
            if one.hand.gang != 0:
                temp_cnt += 1
                temp += one.hand.gang
        if temp_cnt > 1 and temp >= 4:
            return [-2, card(0, 0)]  # 四杠散了
        # 返回的格式是(出了牌的玩家，出的牌)
        self.history = len(self.draw.total) - 14
        # num是现在几号玩家出票,last是上一张牌
        #海底和河底
        if self.history == 1:
            for one in self.players:
                if one.name == num:
                    if one.hand.waiting:
                        for line in one.hand.waiting:
                            line[0].append(9) #河底
                else:
                    if one.hand.waiting:
                        for line in one.hand.waiting:
                            line[0].append(10) #海底

        respond = None  # 是否有玩家应答
        who = num  # 谁出了牌
        win = []  # 一个包含所有胡牌的组
        # 询问碰，杠
        for one in self.players:
            if one.name == (num + 3) % 4:
                continue
            if last in one.wait:
                if last not in one.zhen:
                    temp = one.ron(last)
                    win.append([one.name, temp[0], temp[1]])
                    # 查看是否有一炮多响
            if win:
                return [-1, win]
        for one in self.players:
            if one.name == (num + 3) % 4:
                continue


            pon = list(one.hand.inter['p'].keys())
            gang = list(one.hand.inter['g'].keys())
            if last in pon:

                ans = one.pon(last, self.history)  # 碰
                if ans:
                    self.ipa = [False, False, False, False]
                    self.players[(num + 3) % 4].pure = False
                    respond = ans
                    who = one.name
                    break
            if last in gang:
                ans = one.gang(last, self.history, self.draw.total[-1])  # 杠
                if ans:
                    self.ipa = [False, False, False, False] #鸣牌破一发
                    one.hand.move.append(self.draw.total.pop(-1)) #补牌
                    self.players[(num + 3) % 4].pure = False
                    self.draw.show_dora(1)
                    respond = one.dplay(self.history)
                    who = one.name
                    break
        if respond:
            # 谁出了牌，出了什么牌
            return ([who, respond])
        # 到num号玩家行动！
        if last in list(self.players[num].hand.inter['c'].keys()):
            respond = self.players[num].chi(last, self.history)  # 吃
            if respond:
                self.ipa = [False, False, False, False]
                self.players[(num + 3) % 4].pure = False
                return ([num, respond])
        self.players[(num + 3) % 4].zhen.add(last)
        # 牌进入牌河
        self.river.rivers[(num + 3) % 4].append(last)  # 放进牌河
        #self.river.update((num + 3) % 4, last)
        self.players[(num + 3) % 4].zhen.add(last)
        print("東{}局".format(self.but_pos + 1), end=', ')
        #自摸

        if self.players[num].hand.waiting:
            if self.players[num].hand.close:
                for line in self.players[num].hand.waiting:
                    if 6 not in line[0]:
                        line[0].append(6)
            else:
                for line in self.players[num].hand.waiting:
                    if 6 in line[0]:
                        line[0].remove(6)
            if self.draw.total[0] in list(self.players[num].hand.waiting.keys()):
                if self.players[num].hand.waiting[self.draw.total[0]][0]:
                    ans = self.players[num].zimo(self.draw.total[0])
                    if ans:
                        return [-1, [num] + ans]
                else:
                    print('自摸无役')
        #出牌
        self.players[num].hand.move.append(self.draw.total.pop(0))
        ans = self.players[num].play(self.history)
        while ans[0] == 1: #只要反馈是暗杠或者加杠就能一直接着加
            self.draw.show_dora(1)
            #抢杠
            for one in self.players:
                if one.hand.waiting:
                    for line in list(one.hand.waiting.keys()):
                        if line == ans[2]:
                            if ans[-1] == 1: #暗杠
                                if -1 in one.hand.waiting[line][0]:
                                    one.ron(ans[2])#国士无双抢暗杠
                            else:
                                for wait in one.hand.waiting:
                                    wait[0].append(12)
                                qianggang = one.ron(ans)
                                if qianggang:#抢杠
                                    return [-1, [one.name] + qianggang]
                                for wait in one.hand.waiting:
                                    wait[0].remove(12)
            self.players[num].hand.move.append(self.draw.total.pop())
            ans = self.players[num].play(self.history) #加牌之后继续出



        if self.players[num].reach:
            if self.reach[num] == False:
                if self.history in [69, 68, 67, 66]:
                    temp = 1
                    for i in self.players:
                        if not i.pure:
                            temp = 0
                            break
                    if temp ==1:
                        for i in list(self.players[num].hand.waiting.keys()):
                            self.players[num].hand.waiting[i][0].append(26)
                self.ipa[num] = True #一发
                self.reach[num] = True
            else:
                self.ipa[num] = False #一巡到了
        return ([num, ans])

    def agame(self):
        self.initialize()
        self.players[self.but_pos].play(self.history)

        return 0
