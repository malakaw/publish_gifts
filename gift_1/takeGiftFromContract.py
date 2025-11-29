import cbor2
from pycardano import (
    Address,
    PaymentVerificationKey,
    PaymentSigningKey,
    plutus_script_hash,
    Transaction,
    TransactionBuilder,
    TransactionOutput,
    Unit,
    Redeemer,
    PlutusV3Script,
    Network,
    datum_hash,
)
import os
from blockfrost import ApiUrls
from pycardano import BlockFrostChainContext

blockfrost_key = os.getenv("BLOCKFROST_PROJECT_ID", None)

context = BlockFrostChainContext(blockfrost_key, base_url=ApiUrls.preprod.value)

gift_script = PlutusV3Script.load("build/gift/script.plutus")
script_hash = plutus_script_hash(gift_script)
network = Network.TESTNET
script_address = Address(script_hash, network=network)

 
payment_vkey = PaymentVerificationKey.load("../wallet/payment_1.vkey")
payment_skey = PaymentSigningKey.load("../wallet/payment_1.skey")
giver_address = Address(payment_vkey.hash(), network=network)

payment_vkey_2 = PaymentVerificationKey.load("../wallet/payment_2.vkey")
payment_skey_2 = PaymentSigningKey.load("../wallet/payment_2.skey")
taker_address = Address(payment_vkey_2.hash(), network=network)



from gift import WithdrawDatum
datum = WithdrawDatum(payment_vkey_2.hash().to_primitive())

#-----

redeemer = Redeemer(Unit())  # The plutus equivalent of None

utxo_to_spend = context.utxos(str(script_address))[0]

builder = TransactionBuilder(context)

builder.add_script_input(utxo_to_spend, gift_script, datum, redeemer)
take_output = TransactionOutput(taker_address, 25123456)
builder.add_output(take_output)

 
builder.required_signers = [payment_vkey_2.hash()]

signed_tx = builder.build_and_sign([payment_skey_2], taker_address)

context.submit_tx(signed_tx.to_cbor_hex())

print("Tx ID:", signed_tx.id)

