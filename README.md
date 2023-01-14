## 基于鼠标轨迹的注册/登录系统：前端+后端+数据库 (Flask框架)

---



- 1. 它能做啥?

一只手用鼠标即可登录/注册网页（是的， 图一乐  :）



---



- 2. 它长啥样？

  -  主页

  ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href2_1.gif )

  - 登录

  ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href2_2.gif )

  - 登录失败

  ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href2_3.gif )

  - 注册并登录

  ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href2_4.gif )

  - 注册失败

  ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href2_5.gif )

  - 停滞：5s内无操作则无缝衔接主页动画

  ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href2_6.gif )



---



- 3. **鼠标轨迹**的信息收集，处理，存储？

  - 收集

    在前端将用户从**按下鼠标--移动鼠标--松开鼠标**捕获一系列屏幕坐标，打包成 *Json* 文件用 *Ajax* 发送给后端

  - 处理

    对于不同长短的数据统一拉伸至50帧长度， 中间空缺部分采用线性插帧

    ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href3_1.png )

  - 存储

    因为信息呈链状，搓了个类似 *Trie* 树提高匹配效率和存储效率，更新每个节点信息并存储到多个 *.npy* 文件中（见 *data* 文件夹）

    

----



- 4. **信息匹配**概览与原理

  - 概览：

    - 形状匹配

    ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href4_1.png )

    - 位置匹配

    ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href4_2.png )

    - 大小匹配

    ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href4_3.png )

    - 方向匹配

    ![image](https://github.com/namediffcult/Mouse_Track_For_Login_And_Registration/blob/master/For_README_PIC/href4_4.png )

    

    - 注：信息匹配过程**不受书写时间**，即相同轨迹但速度不同仍视为匹配

    

  - 原理：

    

    显然让用户精确绘出两次一模一样的轨迹是不可能的，遂只能在 *Trie* 树上进行**模糊搜索**，设置每个节点可模糊范围为 *150px（可调节）* 以内，从第一个头节点 *DFS* 下去， 在 *Trie* 树节点上可能存在较多后继节点，为了寻找下一个在模糊区间内的节点，采用折半搜索确定边界，再放入 *DFS* 栈中

    注册过程中：存在在模糊搜索范围 150*px* 内有相似账号，则不允许通过
    
    登录过程中：存在两个以上相似账号，则会缩小搜索范围进一步匹配直到仅有一个账号才允许登录成功
    
    

  ---

  

- 5. 关于写前端的碎碎念

  - 关于实现 *div* 触发从透明到实体，再触发从实体到透明的循环？

    第一版是将动画 {0% -> 透明度: 0 , 50% -> 透明度: 1 , 100% -> 透明度: 0 }，再配合 *setTimeout()* 与 *querySelector()* 强行修改 *animationPlayState* 来控制动画走一半停止，但逆天的是 *JavaScript* 执行方式是单线程，异步执行，说人话就是你设置走 1*s* 但实际上不一定精准走1s。详情见：*\templates\demo1.html*

    

    第二版思路，你无非就是出现与消失，已知消失过程控制不当，那在消失操作最后直接手动设置透明度为0，结果是不行的，猜测是动画和 *JavaScript* 控制相同属性会出问题

    

    第三版思路（目前），如同第二版，*JavaScript* 控制 *display* 属性直接在需要消失的阶段将 *div* 隐藏。详情见：*\templates\demo2.html*

    

  - 这前端+CSS代码怎么又臭又长？

    ​	我也这么觉得

     

  ---

  

- 6. 登陆后用户接口

     *\templates\welcome.html* 内在 *type_info == 5* 分支内 *window.location.href = '/login_in/' + user_info[0].toString();* 

     为跳后端转用户界面

     

----



- 7. 想起啥补充啥

  - *data* 文件夹内数据没清空，可以直接删掉文件夹内的数据，但需要保留 *user* 和 *password* 两个文件夹，（说白了就是 *.npy* 都能删掉）
  - 





