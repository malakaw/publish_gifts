from pycardano import *
network = Network.TESTNET

import os
from pycardano import BlockFrostChainContext


blockfrost_key = os.getenv("BET_BLOCKFROST_PROJECT_ID", None)
context = BlockFrostChainContext(  project_id=blockfrost_key, network=network)

payment_1_skey            = f"./payment_1.skey"
payment_2_skey            = f"./payment_2.skey"

payment_1_skey = PaymentSigningKey.load("./payment_1.skey")
payment_1_vkey = PaymentVerificationKey.from_signing_key(payment_1_skey)
payment_1_address = Address(payment_1_vkey.hash(), network=network)

payment_2_skey = PaymentSigningKey.load("./payment_2.skey")
payment_2_vkey = PaymentVerificationKey.from_signing_key(payment_2_skey)
payment_2_address = Address(payment_2_vkey.hash(), network=network)

 
builder = TransactionBuilder(context)
builder.add_input_address(payment_1_address)
builder.add_output(
    TransactionOutput.from_primitive([payment_2_address.encode(), 500_000_000])
)
 
signed_tx = builder.build_and_sign([payment_1_skey], change_address=payment_1_address)
context.submit_tx(signed_tx.to_cbor())

