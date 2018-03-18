#!/usr/bin/env python
# coding:utf-8

import requests
import json
import time
import datetime
import logging

ROUND_BLOCK_UNIT = 50
SETTLEMENT_BLOCK = 11

################################################################
class Command:
    name="chenhao666"
    passwd="chenhao666"
    #bronze
    address_A="MLuy4exuzMcoZvtkmFHeBqwBzczmwagC3D"
    address_B="MBt5aoaJwngvDz4BqMfWpxG62PyN8Y5VJ2"
    mychange="MB5KLQ8Mg2bToCC4cM5TJJj9KwLU1xUPdD"

    def __init__(self, url):
        self.url = url

    def getinfo(self):
        cmd = {"jsonrpc":"2.0","method":"getinfo","params":[],"id":25}
        ret = requests.post(self.url, json.dumps(cmd))
        return json.loads(ret.content)

    def getblockheaderhash(self, round_height):
        cmd = {"jsonrpc":"2.0","method":"getblockheader","params":[{"height":round_height}],"id":25}
        ret = requests.post(self.url, json.dumps(cmd))
        return json.loads(ret.content)["result"]["hash"]

    def getbalance(self):
        cmd = {"jsonrpc":"2.0","method":"getbalance","params":[self.name, self.passwd],"id":25}
        ret = requests.post(self.url, json.dumps(cmd))
        return json.loads(ret.content)

    def listtxs_A(self, height_range):
        """获取A押注方-数字 充值队列- 地址指定作为参数貌似无效"""
        cmd = {"jsonrpc":"2.0","method":"listtxs","params":[self.name,self.passwd,{"height":height_range,"address":self.address_A}],"id":25}
        ret = requests.post(self.url, json.dumps(cmd))
        return json.loads(ret.content)

    def listtxs_B(self, height_range):
        """获取B押注方-字母 充值队列- 地址指定作为参数貌似无效"""
        cmd = {"jsonrpc":"2.0","method":"listtxs","params":[self.name,self.passwd,{"height":height_range,"address":self.address_B}],"id":25}
        ret = requests.post(self.url, json.dumps(cmd))
        return json.loads(ret.content)

    def sendmore(self, receipt):
        cmd = {"jsonrpc":"2.0","method":"sendmore","params":[self.name,self.passwd,{"receivers":receipt,"mychange":self.mychange}],"id":25}
        ret = requests.post(self.url, json.dumps(cmd))
        return json.loads(ret.content)

    def collcetion(self, amount):
        receipt = self.mychange + ":" + str(amount)
        self.sendmore(receipt)

    def get_address_etp(self):
        cmd = {"jsonrpc":"2.0","method":"getaddressetp","params":[self.address_A],"id":25}
        ret = requests.post(self.url, json.dumps(cmd))
        a = json.loads(ret.content)["result"]["balance"]["unspent"]

        cmd = {"jsonrpc":"2.0","method":"getaddressetp","params":[self.address_B],"id":25}
        ret = requests.post(self.url, json.dumps(cmd))
        b = json.loads(ret.content)["result"]["balance"]["unspent"]
        return (a,b)

################################################################
def get_send_queue(cmd, height_range, queue_type):
    """获取两个队列的充值总额，用于计算赔率"""
    json_txs = None
    if queue_type == 'A':
        json_txs = cmd.listtxs_A(height_range);
        address = cmd.address_A
    if queue_type == 'B':
        json_txs = cmd.listtxs_B(height_range);
        address = cmd.address_B

    try:
        if json_txs["error"]["code"] ==  2003:
            #logging.critical( "池子%s在本轮没有任何充值进来,本轮放弃" % queue_type)
            return 0
    except:
        logging.critical( "池子%s有充值进来" % queue_type)

    txs = json_txs["result"]["transactions"]
    recevie_sum = 0
    for tx in txs:
        if tx["direction"] == "receive":
            for output in tx["outputs"]:
                if output["own"] == True and output["locked_height_range"] == 0 and output["address"] == address:
                    recevie_sum += output["etp-value"]
                    logging.critical( "(%s, %s, %s, %s, %s)" % (tx["hash"], height_range, str(tx["inputs"][0]["address"]), output["etp-value"], queue_type))
    return recevie_sum

################################################################
def payment(cmd, queue_type, last_round, odd, mychange):
    logging.critical( "--- round(%s)支付开始 --- " % last_round)
    if queue_type == 'A':
        json_txs = cmd.listtxs_A(last_round);
        address = cmd.address_A
    if queue_type == 'B':
        json_txs = cmd.listtxs_B(last_round);
        address = cmd.address_B

    txs = json_txs["result"]["transactions"]
    for tx in txs:
        if tx["direction"] == "receive":
            for output in tx["outputs"]:
                if output["own"] == True and output["locked_height_range"] == 0 and output["address"] == address:
                    pay = int(output["etp-value"] * odd)
                    receipt = str(tx["inputs"][0]["address"]) + ":" + str(pay)
                    # WARNING - Payment here
                    logging.critical( "支付给 %s" % receipt)
                    tx = cmd.sendmore(receipt)
                    try:
                        logging.critical( "支付结果: %s" % str(tx["result"]["transaction"]["hash"]))
                    except:
                        logging.critical( "支付错误: %s" % str(tx["error"]))
    cmd.sendmore(mychange)
    logging.critical( "--- round(%s)支付结束 --- " % last_round)

################################################################

def settlement(cmd, round_height, round_block):
    logging.critical( "========  %s - %s 轮清算回合开始 =========" % (round_height - round_block, round_height))
    last_round = str(round_height - round_block) + ":" + str(round_height + 1)
    blockhash = cmd.getblockheaderhash(round_height)

    sum_A = get_send_queue(cmd, last_round, 'A')
    sum_B = get_send_queue(cmd, last_round, 'B')

    balances = cmd.get_address_etp()

    if sum_A == 0 and sum_B == 0:
        logging.critical( "双方池子在本轮没有任何充值,本轮放弃清算")
    elif sum_A == 0 or sum_B == 0:
        logging.critical( "有一方池子在本轮没有任何充值,资金直接进入下一轮")
        logging.critical( "========  %s - %s 轮清算回合结束 =========" % (round_height - round_block, round_height))
        round_block += ROUND_BLOCK_UNIT
    else:
        # 实施清算则将round_block重置为1单位的UNIT
        round_block = ROUND_BLOCK_UNIT
        # 计算赔率和支付方向,抽水2%
        payto = 'B'
        odd = (sum_A + sum_B) * 0.98 / float(sum_B)
        logging.critical( "blockhash: %s" % blockhash)
        #if blockhash[-1].isdigit() and blockhash[-1] != '9' and blockhash[-1] != '8':
        if blockhash[-1].isdigit():
            payto = 'A'
            odd = (sum_A + sum_B) * 0.98 / float(sum_A)

        #抽水
        mychange = int((sum_A + sum_B) * 0.02)

        logging.critical( "本轮实施清算,A: 余额[%s]-sum_A[%s], B: 余额[%s]-Sum_B[%s]" % (balances[0], sum_A, balances[1], sum_B))
        logging.critical( "本轮 %s 胜, 最终赔率 %s" % (payto, odd))
        payment(cmd, payto, last_round, odd, mychange)
        logging.critical( "========  %s - %s 轮清算回合结束 =========" % (round_height - round_block, round_height))

    return round_block

################################################################

def main(cmd):
    """
    Get entry
    """
    logging.critical( ">>>>>>>>> MVS 区块大竞猜 启动 <<<<<<<<<")

    # 每轮应该扫描充值队列的长度
    round_block = ROUND_BLOCK_UNIT

    # 当前回合结束的高度
    round_height = 0
    # 产生新块的判断
    is_new_round = False
    tmp_height = cmd.getinfo()["result"]["height"]

    while True:
        """
        每3秒check一次
        """
        time.sleep(3)

        """
        每round_block块开奖一次，即块号后两位是00，开奖后SETTLEMENT_BLOCK个块内结算完毕
        清算的时机不能晚于下一次开奖
        """
        info = cmd.getinfo()
        last_height = info["result"]["height"]
        if last_height == tmp_height:
            continue
        else:
            # 产生了新块
            if last_height - tmp_height > 1:
                logging.critical( ">>> WARNING 3秒扫描%s:%s漏块了" % (tmp_height, last_height))
                last_height = tmp_height + 1
                tmp_height += 1
                logging.critical( ">>> WARNING 扫描高度自动调整为 %s" % last_height)
            else:
                tmp_height = last_height

        if is_new_round == False and last_height % ROUND_BLOCK_UNIT == 0:
            is_new_round = True
            round_height = last_height
            logging.critical( "################### 新回合 %s - %s 开始 ###################" % (round_height, round_height + ROUND_BLOCK_UNIT))
        else:
            logging.critical( "%s: 当前回合 %s - %s 等待用户押注" % (last_height, round_height, round_height + ROUND_BLOCK_UNIT))

        # 发起清算的时机：延迟round_block个区块，校验hash
        if is_new_round and last_height - round_height >= SETTLEMENT_BLOCK:
            # settlement go
            round_block = settlement(cmd, round_height, round_block)
            logging.critical( "round_block %s" % round_block)
            # reset
            is_new_round = False

################################################################

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL,
                format='%(asctime)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='mvs-gambling.log',
                filemode='a')

    cmd = Command("http://127.0.0.1:8820/rpc/v2")
    main(cmd);
