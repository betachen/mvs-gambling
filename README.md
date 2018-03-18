
基于区块链的竞猜程序Demo-元界
----------------

### 背景
实际上基于区块链的竞猜类游戏早就诞生了，最早有在比特币上竞猜区块HASH的游戏。
参考了类似思路，我也做了一个。
不过不同的是，我在设计MVS(元界)的接口试弄了很多顺手用的接口，正好在这里用上了。
所以这个程序最大的特色是不需要任何服务器。
你所要做的就是打开mvs-gambling.py 前面几行，填写好账户名密码，以及地址即可。
让钱包和mvs-gambling.py同时运行即可。

从逻辑上来看，这更像是一个自助结算的中心化小程序，而不是DAPP。
这里可以扩展到有庄模式的gambling游戏。

运行：
```
$ wget http://sfo.newmetaverse.org/mvs-download/mvs-linux-x86_64-v0.7.5.tar.gz
$ tar -xzvf mvs-linux-x86_64-v0.7.5.tar.gz
$ cd mvs-linux-x86_64-v0.7.5
$ ./mvsd -d
$ ./mvs-cli getnewaccount chenhao chenhao
$ ./mvs-cli getnewaddress chenhao chenhao
$ #配置mvs-gambling.py
$ ./mvs-gambling.py
```
最后往里面的地址打币即可，开出的区块会按照押注进行判断，自动结算，包含赔率计算。

### 游戏玩法

先投注：
是-请押注到地址A: [**MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D**](http://mymvs.info/address/MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D)
否-请押注到地址B: [**MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2**](http://mymvs.info/address/MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2)

<!-- more -->

### 竞猜下一个100的整数倍高度的区块哈希的最后一位是否是数字?

例如:
区块高度958200, 958300, 958400, 区块哈希分别是
```
82450071f44e94be72779b3cbb8ff6917de5e8c67df572cafcc8e9ea4359f67d
63fc451a02215318181343770d80e15a04c5d838741b20dc9fc331550a6d066e
2afbb7269f666c50d6e37ff16df3bf37cf4bd64f0d33787d2d854287f2987226
```
那么开奖结果分别是: 否，否，是

## 中奖概率
区块哈希的组成其实是十六进制，所以押注的概率:
是 62.5% - 否 37.5%

## 赔率计算公式
A胜：  (A+B) * 0.98 / A
B胜：  (A+B) * 0.98 / B
在[元界的区块浏览器](http://mymvs.info)上可查询上述地址的余额，即可计算赔率。

## 开奖与结算
每次开奖后11个区块开始发起上一轮结算, MVS上的区块时间约30秒，所以一轮大约50分钟，奖金结算控制在6分钟以内。
系统抽取佣金2%。

如果本轮有任意一方押注资金为0，则无法开奖，所有奖金注入下一轮进行开奖。
