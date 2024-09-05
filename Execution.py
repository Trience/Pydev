from Card_collection import *
from tool_kit import *
from Mahjong_EG import *


def demo():
    mypile = pile()
    testant = hand(0)
    # 初始化和洗牌
    mypile.ini()
    # print(mypile.dora[0], mypile.doradown[0])

    return 0

    # testant.print_all()


# demo()


def test_wait():
    test_hand = hand(0)

    test_hand.move = [card(1, 0), card(2, 0), card(4, 0), card(6, 1), card(7, 1), card(8, 1), card(1, 2), card(2, 2),card(3, 2), card(9, 1), card(3, 0), card(4, 1), card(5, 1)]

    # test_hand.move = [card(1, 1), card(1, 1), card(1, 1), card(3, 1), card(2, 1), card(4, 1), card(5, 1), card(6, 1),
    # card(7, 1), card(8, 1), card(9, 1), card(9, 1), card(9, 1)]
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
    print(orphan_count(test_hand.move))


# start_time = time.time()
test_wait()


# end_time = time.time()
# print(f"运行时间: {end_time - start_time} 秒")

def demo_inter():
    a = player(0, 0, 1, 25000, 1)
    b = player(1, 1, 0, 25000, 2)
    c = player(2, 2, 0, 25000, 3)
    d = player(3, 3, 0, 25000, 4)

    test_hand = hand(0)
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
