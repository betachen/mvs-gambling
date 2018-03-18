A gambling game program to guess MVS blockchan hash.
----------------

### trial on MVS blockchain

**Question: Is the last character of block hash which is the next 100 integer multiple height number => numeric?**
then send ETP to these two address as below:
addressA for YES: [**MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D**](http://mymvs.info/address/MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D)
addressB for NO: [**MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2**](http://mymvs.info/address/MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2)


### Backgroud
This program is written by python script, and no need 7x24 hours servers.
You can run it with your MVS fullnode wallet at same time.

You can try this game right now, but only for testing , DO NOT try too many ETP.
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

### 游戏玩法

先投注：
addressA for YES: [**MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D**](http://mymvs.info/address/MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D)
addressB for NO: [**MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2**](http://mymvs.info/address/MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2)

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
