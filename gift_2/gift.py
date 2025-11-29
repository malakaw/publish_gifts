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
    assert sig_present, "gift5 Required signature 99 missing"