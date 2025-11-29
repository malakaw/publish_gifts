
# 概述
这里有两个小小cardano智能合约的全流程例子，包含所有的准备工作和上链操作，并测试。是完整的，可以运行的。合约语言是opshin,交互脚本是pycardano。

两个例子，目录gift_1是使用传统的每次上传合约脚本来执行。gift_2则是使用reference的合约来执行智能合约。当然reference的方式对于频繁执行合约或是多次执行肯定是更加划算便宜的方式。毕竟每次上传合约脚本都是要花费更多手续费的。



# 环境准备 
## 安装准备1

+ cardano-cli 
+ python3.11以上


## 安装准备2
安装python相关依赖包

```
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```


## 安装准备3

```
python3 -m venv venv
source venv/bin/activate
pip install opshin
opshin build gift.py
```

## 安装准备4
+ 在https://blockfrost.io/ 注册并创建preprod的project 
+ 在https://demeter.run/ 注册并创建ogmios服务

然后准备环境变量，下面是.bashrc的配置，适合mac/linux系统。
```
export BLOCKFROST_PROJECT_ID="XXXX"
export OGMIOS_API_HOST="xxxxx.cardano-preprod-v6.ogmios-m1.dmtr.host"
export OGMIOS_API_PORT="443"

```
然后source .bashrc 文件。


# 准备钱包

进入wallet目录，执行文件payment-addresses.sh，生成钱包，执行完可以看到payment_1和payment_2两个钱包。

```
└── wallet
    ├── payment_1.addr
    ├── payment_1.skey
    ├── payment_1.vkey
    ├── payment_2.addr
    ├── payment_2.skey
    ├── payment_2.vkey

chmod 755 payment-addresses.sh
./payment-addresses.sh
```

## 添加测试环境的preprod的ada
[测试ada获取](https://docs.cardano.org/cardano-testnets/tools/faucet)
每天有获取限制。注意环境使用的是 preprod。
我们有两个钱包，上面的链接每天只能一个钱包获取测试ada,先用上面链接获取tADA到payment_1,再用下面的命令转发一个的tADA到另外一个钱包payment_2。

```
python3 send_tada
```

好了，两个钱包都有测试ada了。我们可以开始智能合约测试了。

## 合约内容
```
from opshin.prelude import *

@dataclass()
class WithdrawDatum(PlutusData):
    pubkeyhash: bytes

def validator(context: ScriptContext) -> None:
    datum: WithdrawDatum = own_datum_unsafe(context)
    sig_present = False
    for s in context.transaction.signatories:
        if datum.pubkeyhash == s:
            sig_present = True
    assert sig_present, "Required signature missing"
```
合约很简单的，整个例子使用这个合约的过程是 payment_1发送一定数量ada到合约，并指定谁可以来提取，指定的方式是传入提取者的vkey公钥。然后payment_2来从合约提取ada。


## gift_1 (使用传统的script来执行智能合约)
### 编译
进入 gift_1目录
```
opshin build gift.py
```
生成build目录。合约脚本相关信息都在这个目录中。


### 发送ada
```
python sendGift2contract.py 
```
执行完后有Tx ID，在https://preprod.cardanoscan.io/ 上查询这个tx,直到有查询结果后再执行下面的操作。 有了后，你会发现payment_1 的ada减少了，已经发送给智能合约了。再看智能合约地址上的ada验证下。

 ### take ada
 ```
python takeGiftFromContract.py
 ```
同样的，也会返回tx id, 最后你会发现合约上的ada已经转到 payment_2的地址了。好了，一个完整的合约调用过程就完成了。
当中有几个点我指出下。

#### 发布合约代码
```
builder.add_script_input(utxo_to_spend, gift_script, datum, redeemer)
t
```
#### 执行合约代码
```
context.submit_tx(signed_tx.to_cbor_hex())

```
都是在文件takeGiftFromContract.py中，是不是没有什么仪式感，是的。这个就是cardano。

## gift_2 (使用reference的script来执行智能合约)
这个比较第一个gift_1稍微有点复杂，但也不是很复杂。

### 编译
进入 gift_2目录
```
opshin build gift.py
```
生成build目录。合约脚本相关信息都在这个目录中。


### 发送ada
```
python sendGift2contract.py 
```
相同的，执行完后有Tx ID，在https://preprod.cardanoscan.io/ 上查询这个tx,直到有查询结果后再执行下面的操作。 有了后， 修改文件takeGiftFromContract.py中的
```
refernce_script_utxo = context.utxo_by_tx_id("XXXXX",0)
```
把tx id填入。一定是在https://preprod.cardanoscan.io/ 上查询到了再执行下面的命令。

 ### take ada
 ```
python takeGiftFromContract.py
 ```
好了，这里就完成reference的方式执行合约了。

很简单的，就是add_script_input是一个合约的utxo就可以了。
```
builder.add_script_input(utxo=refernce_script_utxo, redeemer=redeemer)
```



# 参考
[pycardano Smart Contracts](https://pycardano.readthedocs.io/en/latest/guides/plutus.html)