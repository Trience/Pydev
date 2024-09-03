from itertools import combinations
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


# 返回二维数组，包含所有组合
def get_combinations(input_list, x):
    if x > len(input_list):
        return []

    result = list(combinations(input_list, x))
    return result


def have_same(two):
    temp = []
    for one in two:
        #for j in one:
            #temp.append(j)
        temp += one[:3]
    i = 0
    while (i < len(temp) - 1):
        if sorted(temp)[i] == sorted(temp)[i + 1]:
            return True
        i += 1
    return False
