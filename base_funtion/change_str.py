def change_str(now):
    ti = 0
    res = 0
    si = len(now)

    data = []
    sub_data = []
    for i in range(1, si):
        if now[i] >= '0' and now[i] <= '9':
            res = res * 10 + int(now[i])
        else:
            sub_data.append(res)
            res = 0
            ti = ti + 1
            if ti == 3:
                data.append(sub_data)
                sub_data = []
                ti = 0

    Data = []
    si = data[len(data) - 1][2]
    Len = len(data)

    if Len < 2 or si == 0:
        return []

    # * 1000 // third
    # define MAX_arr = 1000
    MAX_arr = 50
    for i in range(1, Len):

        l = data[i - 1]
        r = data[i]
        l_time = l[2] * MAX_arr // si
        r_time = r[2] * MAX_arr // si

        # head
        Data.append([int(l[0]), int(l[1]), l_time])

        ti = (r_time - l_time - 1)
        if ti + 1 == 0:
            print("error", l, r, si, l_time, r_time)
            continue

        dx = (r[0] - l[0]) / (ti + 1)
        dy = (r[1] - l[1]) / (ti + 1)

        for j in range(1, ti + 1):
            Data.append([
                int(l[0] + dx * j),
                int(l[1] + dy * j),
                l_time + j
            ])
    if Len > 1:
        Data.append([int(r[0]), int(r[1]), r_time])

    data = []
    for info in Data:
        data.append(info[0])
        data.append(info[1])

    return data
