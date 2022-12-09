"""
Run this test after the simulate.py script

"""

from brownie import config
from web3 import Web3

# web3 provider
w3 = Web3(Web3.WebsocketProvider(config["provider"]["websockets"]))
mumbai_chain_id = 80001

# escrow contract instance on mumbai
with open("./contract_data/escrowAddress") as file_a:
    escrow_address = file_a.read()
with open("./contract_data/escrowABI.json") as file_b:
    escrow_abi = file_b.read()
escrow_contract_instance = w3.eth.contract(address=escrow_address, abi=escrow_abi)

# real estate contract instance on mumbai
with open("./contract_data/realEstateAddress") as file_c:
    real_estate_address = file_c.read()
with open("./contract_data/realEstateABI.json") as file_d:
    real_estate_abi = file_d.read()
real_estate_contract_instance = w3.eth.contract(
    address=real_estate_address, abi=real_estate_abi
)


def test_escrow_balance_updated():
    # checking that the escrow balance is updated after the transfer

    escrow_balance = escrow_contract_instance.functions.getBalance().call()

    assert escrow_balance == 0
