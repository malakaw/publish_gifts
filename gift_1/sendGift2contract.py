from blockfrost import ApiUrls
from pycardano import BlockFrostChainContext
import os
blockfrost_key = os.getenv("BLOCKFROST_PROJECT_ID", None)

context = BlockFrostChainContext(blockfrost_key, base_url=ApiUrls.preprod.value)


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

# This artifact was generated in step 2. By default, opshin will generate Plutus V3 scripts, so we need to load the script as a `PlutusV3Script`.
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




builder = TransactionBuilder(context)
builder.add_input_address(giver_address)

from gift import WithdrawDatum
datum = WithdrawDatum(payment_vkey_2.hash().to_primitive())
builder.add_output(
    TransactionOutput(script_address, 50000000, datum_hash=datum_hash(datum))
)

signed_tx = builder.build_and_sign([payment_skey], giver_address)
context.submit_tx(signed_tx.to_cbor_hex())
print("Tx ID:", signed_tx.id)