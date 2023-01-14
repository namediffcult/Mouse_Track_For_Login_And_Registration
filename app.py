from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
import json
import csv
import os
import numpy as np
from SQL.SQL_command import data_search, data_insert
from base_funtion.change_str import change_str

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = "BY pipe_dream"


@app.route('/', methods=['GET', 'POST'])
def welcome():
    user = session.get('username')
    if not user:
        return render_template("welcome.html")

    return redirect('/login_in/' + str(user))



@app.route('/login_in/<username>/')
def login_in(username):
    return "Already logged in to account: " + str(username) + ", but there's nothing here ;-)"


@app.route('/getData_for_info1', methods=['GET', 'POST'])
def getData_for_info1():
    _data_str = request.form['idx']
    data = change_str(_data_str)
    if len(data) == 0:
        return jsonify([])

    flag_left = 0
    flag_right = 0
    flag_hight = 0
    for i in range(2, len(data)):
        if i % 2 == 0:
            if data[i] > data[i - 2]:
                flag_right = 1
            else:
                flag_left = 1
        else:
            if abs(data[i] - data[i - 2]) > 6:
                return jsonify([])
    if flag_right and flag_left:
        return jsonify([])
    elif flag_left:
        return jsonify([1])
    else:
        return jsonify([2])

@app.route('/getData_for_info3', methods=['GET', 'POST'])
def getData_for_info3():
    _data_str1 = request.form['idx1']
    _data_str2 = request.form['idx2']
    account = change_str(_data_str1)
    password = change_str(_data_str2)
    find_account = data_search("user", account, int(150))
    find_password = data_search("password", password, int(150))

    # --------debug-----------
    # 为了测试关闭注册
    # return jsonify([])

    # 测试成功匹配
    # session['username'] = 1
    # return jsonify([1])
    # --------debug-----------

    for acc in find_account:
        for pas in find_password:
            if acc == pas:
                return jsonify([])

    # create id
    if os.path.exists('.//data//account_number.npy') == False:
        np.save('.//data//account_number.npy', 0)

    tot = np.load('.//data//account_number.npy')
    tot = tot + 1
    data_insert("user", account, tot)
    data_insert("password", password, tot)
    np.save('.//data//account_number.npy', tot)
    print("append new account, id: ", tot)
    return jsonify([1])

@app.route('/getData_for_info5', methods=['GET', 'POST'])
def getData_for_info5():
    _data_str1 = request.form['idx1']
    _data_str2 = request.form['idx2']
    account = change_str(_data_str1)
    password = change_str(_data_str2)

    Maximum_fuzzy_search_range = int(150)
    decline_range = int(50)


    # --------debug-----------
    # 测试没匹配情况
    # return jsonify([])

    # 测试成功匹配
    # session['username'] = 1
    # return jsonify([1])
    # --------debug-----------

    while Maximum_fuzzy_search_range > 0 :
        find_account = data_search("user", account, Maximum_fuzzy_search_range)
        find_password = data_search("password", password, Maximum_fuzzy_search_range)
        cnt = 0
        tar_acc = -1
        for acc in find_account:
            for pas in find_password:
                if acc == pas:
                    cnt = cnt + 1
                    tar_acc = acc

        if cnt == 1:
            return jsonify([tar_acc])
        Maximum_fuzzy_search_range = Maximum_fuzzy_search_range - decline_range
        # print("Maximum_fuzzy_search_range :", Maximum_fuzzy_search_range)

    return jsonify([])


# -------------------test-------------------------
@app.route('/getData_for_test', methods=['GET', 'POST'])
def form_data():
    _data_str = request.form['idx']
    data = change_str(_data_str)
    if len(data) == 0:
        return jsonify([])
    return jsonify([])
    # print(_data_str)
    # print(data)
    test_mode = 1
    # if test_mode == 0:
    #     data_insert("user", data, 2)
    #     return jsonify([])
    # else:
    #     tar = data_search("user", data)
    #     print("tar", tar)
    #     return jsonify(tar)

    # data_insert("user", data, 2)

    # 查询操作


if __name__ == '__main__':
    app.run()
