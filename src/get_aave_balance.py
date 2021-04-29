import darp
import json
import os
from web3 import Web3
from contracts import CONTRACTS
from abi import ABI

def get_erc_bal(w3, token, child, addr):
    """Retrieves the corrected-for-decimals balance of the token"""

    info = CONTRACTS[token]
    contract = w3.eth.contract(info[child], abi=ABI['ERC_20'])

    precision = info['PRECISION']
    decimals = 10 ** (info['DECIMALS']-precision)
    raw = contract.functions.balanceOf(addr).call()
    return raw // decimals / (10 ** precision)

def balances(address="DEFI_ADDRESS", httpRpc="https://rpc-mainnet.maticvigil.com/", showZero=False):
    provider = Web3.HTTPProvider(httpRpc)
    w3 = Web3(provider)
    if address == "DEFI_ADDRESS":
        wallet = os.environ.get('DEFI_ADDRESS')
        if not wallet:
            raise Error('Need env DEFI_ADDRESS or passed in')
        wallet = os.environ['DEFI_ADDRESS']
    else:
        wallet = address

    print("Wallet: %s" % wallet)
    bal = w3.eth.get_balance(wallet)
    print("Balance: %s MATIC" % Web3.fromWei(bal, "ether"))

    for token in CONTRACTS:
        bal = get_erc_bal(w3, token, "ATOKEN", wallet)
        if showZero or bal > 0.0:
            print("%s: %s" % (token, bal))
    
        bal = get_erc_bal(w3, token, "STABLE_DEBT", wallet)
        if showZero or bal > 0.0:
            print("%s (stable) : (%s)" % (token, bal))

        bal = get_erc_bal(w3, token, "VARIABLE_DEBT", wallet)
        if showZero or bal > 0.0:
            print("%s (variable): (%s)" % (token, bal))

if __name__=='__main__':
    darp.prep(balances).run()
