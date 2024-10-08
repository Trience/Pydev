from Card_collection import *
from tool_kit import *
from Mahjong_EG import *

start_time = time.time()

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

    #test_hand.move = [card(2, 0), card(2, 0), card(3, 0), card(3, 0), card(4, 0), card(4, 0), card(2, 2), card(2, 2),card(2, 0), card(3, 0), card(4, 0), card(4, 1), card(2, 2)]
    #test_hand.move = [card(2, 0), card(2, 0), card(3, 0), card(3, 0), card(4, 0), card(4, 0), card(2, 2), card(2, 2),
                      #card(0, 3), card(0, 3), card(0, 3), card(4, 1), card(5, 1)]
    #test_hand.move = [card(1, 1), card(1, 1), card(1, 1), card(3, 1), card(2, 1), card(4, 1), card(5, 1), card(6, 1), card(7, 1), card(8, 1), card(9, 1), card(9, 1), card(9, 1)]
    # test_hand.total = [card(1, 1), card(1, 1), card(6, 1), card(6, 1), card(8, 1), card(8, 1), card(2, 2), card(2, 2),
    # card(3, 2), card(3, 0), card(3, 0), card(5, 1), card(5, 1)]
    test_hand.print_all()
    test_hand.initiate()

    print(len(test_hand.move))
    print(test_hand.possible)

    test_hand.clean()
    a = player(0,0,1,25000,0)
    a.hand = test_hand
    b = player(1,1,0,25000,0)
    c = player(1, 1, 0, 25000, 0)
    d = player(1, 1, 0, 25000, 0)
    print(a.hand.waiting)
#test_wait()

def test_game():
    a = player(0, 0, 0, 35000, 0)
    b = player(1, 1, 0, 30000, 1)
    c = player(2, 1, 0, 25000, 2)
    d = player(3, 1, 0, 20000, 3)
    game = round(0,0,[a,b,c,d])

    game.agame()#测试整个游戏
    def test_ron():
        game.initialize()
        c.hand.move = [card(2, 0), card(2, 0), card(3, 0), card(3, 0), card(4, 0), card(4, 0), card(2, 2), card(2, 2),card(0, 3), card(0, 3), card(0, 3), card(4, 1), card(5, 1)]
        c.hand.clean()
        print(game.around(2,card(3,1)))
    #test_ron() #这个是单元测试
test_game()





end_time = time.time()

print(f"运行时间: {end_time - start_time} 秒")

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

