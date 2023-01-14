import numpy as np
import os


# data[] -> [, [pos, id]]
# tot

# ------
# -|data
# ----|user  (for user)
# -------|tot
# -------|data
# ----|password
# -------|tot
# -------|data
# init()
# path -> str


def init(path):
    #不要动这下面语句顺序!!!

    tot = 0
    print(".//data//" + path + "//tot.npy")
    save_data(path, tot, [])
    print(tot)
    tot = tot + 1
    np.save(".//data//" + path + "//tot.npy", tot)

    return tot


def load_data(path, id):
    _data = np.load(".//data//" + path + "//data" + str(id) + ".npy")
    data = []
    for sub in _data:
        sub_data = []
        for sub_sub in sub:
            sub_data.append(int(sub_sub))
        data.append(sub_data)
    return data


def save_data(path, id, data):
    np.save(".//data//" + path + "//data" + str(id) + ".npy", data)


def binary_search(sub_data, tar):
    if len(sub_data) == 0:
        return -1

    l = 0
    r = len(sub_data) - 1
    ans = -1
    while l <= r:
        mid = (l + r) // 2
        if sub_data[mid][0] >= tar:
            ans = mid
            r = mid - 1
        else:
            l = mid + 1
    return ans


def data_insert(path, wait_insert, username):
    if os.path.exists('.//data//' + path + '//tot.npy') == False:
        init(path)

    now = 0
    tot = np.load(".//data//" + path + "//tot.npy")
    for i in range(len(wait_insert)):
        # find
        # sub_data = data[now]
        sub_data = load_data(path, now)
        tar = wait_insert[i]
        idx = -1
        ans = binary_search(sub_data, tar)
        if ans != -1 and sub_data[ans][0] == tar:
            idx = ans

        # find -> idx
        if idx == -1:
            save_data(path, tot, [])
            sub_data.append([tar, tot])
            sub_data.sort()
            save_data(path, now, sub_data)
            now = tot
            tot = tot + 1
        else:
            now = sub_data[idx][1]

    # user information save
    sub_data = load_data(path, now)
    sub_data.append([username])
    save_data(path, now, sub_data)

    print('-----------')
    print("Add successfully")
    print('-----------')
    np.save(".//data//" + path + "//tot.npy", tot)


def data_search(path, wait_search, arrange):
    if os.path.exists('.//data//' + path + '//tot.npy') == False:
        init(path)
    # print(type(arrange), arrange)
    # arrange = 150

    # idx & pos
    que = [[0, 0]]
    ans = []
    Len = len(wait_search)
    while len(que):
        now, pos = que[-1][0], que[-1][1]
        que.pop()
        if pos == Len:
            for info in load_data(path, now):
                ans.append(info)
        else:
            sub_data = load_data(path, now)
            idx = binary_search(sub_data, wait_search[pos] - arrange)
            if idx != -1:
                for i in range(idx, len(sub_data)):
                    if sub_data[i][0] > wait_search[pos] + arrange:
                        break

                    que.append([sub_data[i][1], pos + 1])

    return ans


# --------------run for test------------------#
wait_insert1 = [123, 256, 243, 143, 278, 918]
wait_insert2 = [243, 145, 276, 388, 249, 111]
wait_insert3 = [123, 256, 243, 143, 278, 918]


def test1():
    data_insert("user", wait_insert1, 1)


def test2():
    data_insert("user", wait_insert2, 2)


def test3():
    print(data_search("user", wait_insert3))


# test1()
# test2()
# test3()
# print(load_data("user", 0))
# print(load_data("user", 1))
# print(load_data("user", 2))
# print(load_data("user", 3))
# print(load_data("user", 4))
# print(load_data("user", 5))
# print(load_data("user", 6))
# print(load_data("user", 12))
# print(data_search("user", wait_insert3))
