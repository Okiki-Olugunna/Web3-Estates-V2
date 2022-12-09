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


def test_ownership_transferred():
    nft_id = 1

    # initialising the buyer account
    buyer_address = config["addresses"]["buyer_address"]

    # checking that the ownership has been transferred
    owner_of_nft = real_estate_contract_instance.functions.ownerOf(nft_id).call()

    assert owner_of_nft == buyer_address
