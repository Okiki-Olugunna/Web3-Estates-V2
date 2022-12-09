"""
This script is a simulation of the full process of 
the inspection, approval & lending process, 
in addition to the buyer buying the 
property and receiving ownership of the NFT and the property
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


def main():
    nft_id = int(input("Please input the NFT ID for the simulation: \n"))
    nft_escrow_price = nft_id * 2
    nft_property_price = nft_id * 4

    print(f"\nUsing NFT ID {nft_id} for the simultion.\n")

    # initialising the accounts
    print("Initialising the accounts...\n")

    seller = config["wallets"]["from_key"]["seller"]
    seller_address = config["addresses"]["seller_address"]

    inspector = config["wallets"]["from_key"]["inspector"]
    inspector_address = config["addresses"]["inspector_address"]

    lender = config["wallets"]["from_key"]["lender"]
    lender_address = config["addresses"]["lender_address"]

    buyer = config["wallets"]["from_key"]["buyer"]
    buyer_address = config["addresses"]["buyer_address"]

    print("Accounts initialised.\n")

    # buyer deposits earnest
    print(f"\nBuyer is now depositing the earnest for property {nft_id}...\n")

    earnest = nft_escrow_price
    print("Getting the buyer's nonce...")
    nonce = w3.eth.get_transaction_count(buyer_address)
    print("Building the trasaction...")
    tx = escrow_contract_instance.functions.depositEarnest(nft_id).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": mumbai_chain_id,
            "from": buyer_address,
            "value": earnest,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    print("Signing the trasanction...")
    signed_tx = w3.eth.account.sign_transaction(tx, buyer)
    print("Sending the trasaction...")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print("Buyer has successfully depsoited the earnest.\n")

    # inspector updates status
    print("The inspector is now inspecting the property...\n")

    print(
        "The property has been successfully inspected, and the status will now be updated.\n"
    )

    print("Getting the inspector's nonce...")
    nonce = w3.eth.get_transaction_count(inspector_address)
    print("Building the transaction...")
    tx = escrow_contract_instance.functions.updateInspectionStatus(
        nft_id, True
    ).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": mumbai_chain_id,
            "from": inspector_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    print("Signing the trasanction...")
    signed_tx = w3.eth.account.sign_transaction(tx, inspector)
    print("Sending the trasaction...")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print("\nThe inspector has successfully updated the inspection status.\n")

    # buyer approves after inspection
    print("The buyer is now approving the sale...\n")

    print("Getting the buyer's nonce...")
    nonce = w3.eth.get_transaction_count(buyer_address)
    print("Building the transaction...")
    tx = escrow_contract_instance.functions.approveSale(nft_id).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": mumbai_chain_id,
            "from": buyer_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    print("Signing the trasanction...")
    signed_tx = w3.eth.account.sign_transaction(tx, buyer)
    print("Sending the trasaction...")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print("\nThe buyer has approved the sale.\n")

    # seller approves
    print("The seller is now approving the sale...\n")

    print("Getting the seller's nonce...")
    nonce = w3.eth.get_transaction_count(seller_address)
    print("Building the transaction...")
    tx = escrow_contract_instance.functions.approveSale(nft_id).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": mumbai_chain_id,
            "from": seller_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    print("Signing the trasanction...")
    signed_tx = w3.eth.account.sign_transaction(tx, seller)
    print("Sending the trasaction...")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print("\nThe seller has approved the sale.\n")

    # lender approves
    print("The lender is now approving the sale...\n")

    print("Getting the lender's nonce...")
    nonce = w3.eth.get_transaction_count(lender_address)
    print("Building the transaction...")
    tx = escrow_contract_instance.functions.approveSale(nft_id).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": mumbai_chain_id,
            "from": lender_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    print("Signing the trasanction...")
    signed_tx = w3.eth.account.sign_transaction(tx, lender)
    print("Sending the trasaction...")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print("\nThe lender has approved the sale.\n")

    # lender sends the remaining funds
    print("The lender is now sending the remaining funds...\n")

    print("Getting the nonce of the lender...")
    nonce = w3.eth.get_transaction_count(lender_address)

    print("Setting the amount to send...")
    lend_amount = nft_property_price - nft_escrow_price

    print("Signing the transaction...\n")
    signed_tx = w3.eth.account.sign_transaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": mumbai_chain_id,
            "gas": 80000,
            "to": escrow_address,
            "from": lender_address,
            "value": lend_amount,
            "nonce": nonce,
        },
        lender,
    )

    # sending the transaction
    print("Sending the transaction...\n")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print("\nThe lender has sent the remaining funds.\n")

    # sale is finalised
    print("The seller is now finalising the sale...\n")

    print("Getting the seller's nonce...")
    nonce = w3.eth.get_transaction_count(seller_address)
    print("Building the transaction...")
    tx = escrow_contract_instance.functions.finaliseSale(nft_id).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": mumbai_chain_id,
            "from": seller_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    print("Signing the trasanction...")
    signed_tx = w3.eth.account.sign_transaction(tx, seller)
    print("Sending the trasaction...")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print("\nThe seller has now finalised the sale.\n")

    print("--------------------------------------------\n")
    print("--------------------------------------------\n")
    print("Some final checks:\n")

    # checking that the ownership has been transferred
    print(
        "Checking that the ownership of the property has been transferred to the buyer...\n"
    )

    owner_of_nft = real_estate_contract_instance.functions.ownerOf(nft_id).call()
    print(
        f"The owner of the real estate property of NFT ID {nft_id} is: {owner_of_nft}\n"
    )

    if owner_of_nft == buyer_address:
        print(
            f"Ownership of NFT ID {nft_id} was transferred to the buyer successfully.\n"
        )
    else:
        print(
            f"Something went wrong. The buyer is not the owner of NFT ID {nft_id}...\n"
        )

    # checking that the escrow balance is updated
    print("Checking that the escrow balance of the contract has been updated...\n")

    escrow_balance = escrow_contract_instance.functions.getBalance().call()
    print(f"The escrow balance is: {escrow_balance}")

    if escrow_balance == 0:
        print(
            "The escrow balance has been successfully updated to 0. Meaning the funds have been sent to the seller.\n"
        )
    else:
        print(
            f"The escrow balance is {escrow_balance}. Extra funds are still in the contract.\n"
        )
        print("Did something go wrong?\n")
