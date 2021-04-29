import json
import os
from web3 import Web3

contracts = {
    "AAVE": {
        "ATOKEN": "0x1d2a0E5EC8E5bBDCA5CB219e649B565d8e5c3360",
        "STABLE_DEBT": "0x17912140e780B29Ba01381F088f21E8d75F954F9",
        "VARIABLE_DEBT": "0x1c313e9d0d826662F5CE692134D938656F681350",
        "DECIMALS": 18,
        "PRECISION": 8
    },        
    "DAI": {
        "ATOKEN": "0x27F8D03b3a2196956ED754baDc28D73be8830A6e",
        "STABLE_DEBT": "0x2238101B7014C279aaF6b408A284E49cDBd5DB55",
        "VARIABLE_DEBT": "0x75c4d1Fb84429023170086f06E682DcbBF537b7d",
        "DECIMALS": 18,
        "PRECISION": 8
    },
    "USDC": {
        "ATOKEN": "0x1a13F4Ca1d028320A707D99520AbFefca3998b7F",
        "STABLE_DEBT": "0xdeb05676dB0DB85cecafE8933c903466Bf20C572",
        "VARIABLE_DEBT": "0x248960A9d75EdFa3de94F7193eae3161Eb349a12",
        "DECIMALS": 6,
        "PRECISION": 4
    },
    "USDT": {
        "ATOKEN": "0x60D55F02A771d515e077c9C2403a1ef324885CeC",
        "STABLE_DEBT": "0xe590cfca10e81FeD9B0e4496381f02256f5d2f61",
        "VARIABLE_DEBT": "0x8038857FD47108A07d1f6Bf652ef1cBeC279A2f3",
        "DECIMALS": 6,
        "PRECISION": 4
    },
    "WBTC": {
        "ATOKEN": "0x5c2ed810328349100A66B82b78a1791B101C9D61",
        "STABLE_DEBT": "0x2551B15dB740dB8348bFaDFe06830210eC2c2F13",
        "VARIABLE_DEBT": "0xF664F50631A6f0D72ecdaa0e49b0c019Fa72a8dC",
        "DECIMALS": 8,
        "PRECISION": 6
    },
    "WETH": {
        "ATOKEN": "0x28424507fefb6f7f8E9D3860F56504E4e5f5f390",
        "STABLE_DEBT": "0xc478cBbeB590C76b01ce658f8C4dda04f30e2C6f",
        "VARIABLE_DEBT": "0xeDe17e9d79fc6f9fF9250D9EEfbdB88Cc18038b5",
        "DECIMALS": 18,
        "PRECISION": 8
    },
    "WMATIC": {
        "ATOKEN": "0x8dF3aad3a84da6b69A4DA8aeC3eA40d9091B2Ac4",
        "STABLE_DEBT": "0xb9A6E29fB540C5F1243ef643EB39b0AcbC2e68E3",
        "VARIABLE_DEBT": "0x59e8E9100cbfCBCBAdf86b9279fa61526bBB8765",
        "DECIMALS": 18,
        "PRECISION": 8
    }
}

ERC20_ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501

def get_erc_bal(token, child, addr):
    """Retrieves the corrected-for-decimals balance of the token"""

    info = contracts[token]
    contract = w3.eth.contract(info[child], abi=ERC20_ABI)

    precision = info['PRECISION']
    decimals = 10 ** (info['DECIMALS']-precision)
    raw = contract.functions.balanceOf(addr).call()
    return raw // decimals / (10 ** precision)

provider = Web3.HTTPProvider('https://rpc-mainnet.maticvigil.com/')
w3 = Web3(provider)
address = os.environ['DEFI_ADDRESS']
if not address:
    raise Error('need DEFI_ADDRESS')

bal = w3.eth.get_balance(address)
print("Balance: %s MATIC" % Web3.fromWei(bal, "ether"))

for token in contracts:
    bal = get_erc_bal(token, "ATOKEN", address)
    if bal > 0.0:
        print("%s: %s" % (token, bal))
        
    bal = get_erc_bal(token, "STABLE_DEBT", address)
    if bal > 0.0:
        print("%s (stable) : (%s)" % (token, bal))

    bal = get_erc_bal(token, "VARIABLE_DEBT", address)
    if bal > 0.0:
        print("%s (variable): (%s)" % (token, bal))

      