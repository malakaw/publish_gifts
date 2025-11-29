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
from pycardano import (
        KupoOgmiosV6ChainContext,
        OgmiosV6ChainContext,
    )


ogmios_host = os.getenv("OGMIOS_API_HOST", "localhost")
ogmios_port = os.getenv("OGMIOS_API_PORT", "443")
ogmios_protocol = os.getenv("OGMIOS_API_PROTOCOL", "wss")
ogmios_url = f"{ogmios_protocol}://{ogmios_host}:{ogmios_port}"

network = Network.TESTNET

def get_OGMIOS_chain_context():
    print(ogmios_host)
    print(ogmios_port)
    print(ogmios_url)
    return OgmiosV6ChainContext(
            host=ogmios_host,
            port=int(ogmios_port),
            secure=True,
            network=network,
        )

context =  get_OGMIOS_chain_context()



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

redeemer = Redeemer(Unit())  # The plutus equivalent of None

refernce_script_utxo = context.utxo_by_tx_id("91174d6582ac48ce045ed228ef03a743c37d60a56097f6cd1d4dceb4b8920608",0)

builder = TransactionBuilder(context)
builder.add_script_input(utxo=refernce_script_utxo, redeemer=redeemer)

take_output = TransactionOutput(taker_address, 25123456)
builder.add_output(take_output)

builder.required_signers = [payment_vkey_2.hash()]

signed_tx = builder.build_and_sign([payment_skey_2], taker_address)

context.submit_tx(signed_tx.to_cbor_hex())

print("Tx ID:", signed_tx.id)

