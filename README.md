A gambling game program to guess MVS blockchan hash.
----------------

### trial on MVS blockchain

**Question: Is the last character of block hash which is the next 100 integer multiple height number => numeric?**

then send ETP to one of these two address as below:

addressA for YES: [**MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D**](http://mymvs.info/address/MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D)

addressB for NO: [**MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2**](http://mymvs.info/address/MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2)

You can trial this game right now, but only for testing , DO NOT send too many ETPs.

### Backgroud
This program is written by python script, and no need 7x24 hours servers.
You can run it with your MVS fullnode wallet at same time.

If you wanna run your own instance, notice that THIS IS NOT DAPP.
It means your customers have to trust you firstly.

### Configuation

Configuation：
```
$ wget http://sfo.newmetaverse.org/mvs-download/mvs-linux-x86_64-v0.7.5.tar.gz
$ tar -xzvf mvs-linux-x86_64-v0.7.5.tar.gz
$ cd mvs-linux-x86_64-v0.7.5
$ ./mvsd -d
$ ./mvs-cli getnewaccount chenhao chenhao //backup 24words
$ ./mvs-cli getnewaddress chenhao chenhao
$ ./mvs-cli getnewaddress chenhao chenhao
```

Open mvs-gambling.py, see the as below:
```python
class Command:
    name="chenhao666"  ## put your account name from your fullnode
    passwd="chenhao666" ## put your account password
    #bronze
    address_A="MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D" ##   stake address - A for YES
    address_B="MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2"  ##  stake address - B for NO
    mychange="MB5KLQ8Mg2bToCC4cM5TJJj9KwLU1xUPdD"   ## Fee from customers
```

then run mvs-gambling.py
```bash
$ nohup ./mvs-gambling.py &
```
you can monitor it from mvs-gambling.log file.

waiting for customers tranfer ETP to these two address.
Program will do the judgement, then payment automaticly.

### Game rules

stake ETP to：

address A for YES: [**MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D**](http://mymvs.info/address/MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D)

address B for NO: [**MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2**](http://mymvs.info/address/MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2)

### Question: Is the last character of block hash which is the next 100 integer multiple height number => numeric?

Example:
height 958200, 958300, 958400, block hash is
```
82450071f44e94be72779b3cbb8ff6917de5e8c67df572cafcc8e9ea4359f67d
63fc451a02215318181343770d80e15a04c5d838741b20dc9fc331550a6d066e
2afbb7269f666c50d6e37ff16df3bf37cf4bd64f0d33787d2d854287f2987226
```
Answer is: NO，NO，YES

### winning and payment
Round peroid about 50 minutes (100 MVS blocks), settlement and payment within 6 minutes (11 blocks).
Porgram got commission in 2% of each round ETP pool.
If no players, or only one play, the ETP will goes to next round.

### 中奖概率
区块哈希的组成其实是十六进制，所以押注的概率:
是 62.5% - 否 37.5%

### 赔率计算公式
A胜：  (A+B) * 0.98 / A
B胜：  (A+B) * 0.98 / B
在[元界的区块浏览器](http://mymvs.info)上可查询上述地址的余额，即可计算赔率。


### monitor log file like this:

```
Sun, 18 Mar 2018 08:23:15 ################### 新回合 1036700 - 1036800 开始 ###################
Sun, 18 Mar 2018 08:23:36 1036701: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:24:33 1036702: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:24:48 1036703: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:24:54 1036704: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:24:57 1036705: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:25:55 1036706: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:26:10 1036707: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:26:46 1036708: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:28:26 1036709: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:28:35 1036710: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:29:11 1036711: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:29:11 ========  1036600 - 1036700 轮清算回合开始 =========
Sun, 18 Mar 2018 08:29:11 池子A有充值进来
Sun, 18 Mar 2018 08:29:11 (73716657164996b279d088aecdbc80978a402d1e66b89b45cc3aab5a29296cd6, 1036600:1036701, MUnnjjQJVvT8Yq7jPe9Rd3cGrYc6ND5igj, 230000000, A)
Sun, 18 Mar 2018 08:29:11 池子B有充值进来
Sun, 18 Mar 2018 08:29:11 (73716657164996b279d088aecdbc80978a402d1e66b89b45cc3aab5a29296cd6, 1036600:1036701, MUnnjjQJVvT8Yq7jPe9Rd3cGrYc6ND5igj, 460000000, B)
Sun, 18 Mar 2018 08:29:11 blockhash: e578c135f5f29177041dada525a1ee6ef9ff4b273879225606ade7e7b06b3375
Sun, 18 Mar 2018 08:29:11 本轮实施清算,A: 余额[230000000]-sum_A[230000000], B: 余额[460000000]-Sum_B[460000000]
Sun, 18 Mar 2018 08:29:11 本轮 A 胜, 最终赔率 2.94
Sun, 18 Mar 2018 08:29:11 --- round(1036600:1036701)支付开始 ---
Sun, 18 Mar 2018 08:29:11 支付给 MUnnjjQJVvT8Yq7jPe9Rd3cGrYc6ND5igj:676200000
Sun, 18 Mar 2018 08:29:11 支付结果: e9bf9f2a179517a72c6a75396612f5c53e0b4944a2cdaf7a9868b0f50c683763
Sun, 18 Mar 2018 08:29:11 --- round(1036600:1036701)支付结束 ---
Sun, 18 Mar 2018 08:29:11 ========  1036600 - 1036700 轮清算回合结束 =========
Sun, 18 Mar 2018 08:29:11 round_block 100
Sun, 18 Mar 2018 08:29:35 1036712: 当前回合 1036700 - 1036800 等待用户押注
Sun, 18 Mar 2018 08:29:44 1036713: 当前回合 1036700 - 1036800 等待用户押注
```
