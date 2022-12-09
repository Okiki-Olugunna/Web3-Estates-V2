from brownie import Escrow, RealEstateNFTs, config, accounts
import json
from web3 import Web3

w3 = Web3(Web3.WebsocketProvider(config["provider"]["websockets"]))


def main():
    # initialising the accounts
    print("Initialising the accounts...\n")

    seller = accounts.add(config["wallets"]["from_key"]["seller"])
    seller_address = config["addresses"]["seller_address"]

    inspector = accounts.add(config["wallets"]["from_key"]["inspector"])
    inspector_address = config["addresses"]["inspector_address"]

    lender = accounts.add(config["wallets"]["from_key"]["lender"])
    lender_address = config["addresses"]["lender_address"]

    buyer = accounts.add(config["wallets"]["from_key"]["buyer"])
    buyer_address = config["addresses"]["buyer_address"]

    print("Accounts initialised.\n")

    ########################################################################
    # REAL ESTATE NFT CONTRACT DEPLOYMENT
    ########################################################################
    print("Deploying the Real Estate NFT contract...\n ")

    deployer = seller
    real_estate_contract = RealEstateNFTs.deploy({"from": deployer})

    print("The contract has been successfully deployed.")
    print(f"The contract address is {real_estate_contract.address} \n")

    print(f"Adding and updating the abi in the relevant development folders... ")

    abi = real_estate_contract.abi
    json_object = json.dumps(abi)
    with open("./contract_data/realEstateABI.json", "w") as file:
        file.write(json_object)
    with open("./frontend/utils/realEstateABI.json", "w") as file:
        file.write('{ "realEstateABI": ')
        file.write(json_object)
        file.write(" }")

    print("Successfully updated the ABI. \n")

    print("Updating the contract address file in the frontend...")

    address = real_estate_contract.address
    with open("./contract_data/realEstateAddress", "w") as file:
        file.write(address)
    with open("./frontend/utils/realEstateAddress", "w") as file:
        file.write(address)

    print("Successfully updated the contract address.\n")

    # minting the NFTs
    print("Minting the 3 properties in the Real Estate NFT contract... \n")

    for i in range(1, 4):
        print(f"Minting property {i}...\n")
        nonce = w3.eth.get_transaction_count(seller_address)
        print("Building the transaction...")
        tx = real_estate_contract.mint(
            f"https://ipfs.io/ipfs/QmQVcpsjrA6cr1iJjZAodYwmPekYgbnXGo4DFubJiLc2EB/{i}.json"
        )  # .buildTransaction(
        #     {
        #         "gasPrice": w3.eth.gas_price,
        #         "chainId": 80001,
        #         "from": seller_address,
        #         "nonce": nonce,
        #     }
        # )
        # print("Signing the transaction..")
        # signed_tx = w3.eth.account.sign_transaction(tx, seller)
        # print("Sending the transaction...")
        # send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # print("Waiting for the transaction to go through...")
        # tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
        # print("--------------------------------------------")
        # print(f"Transaction receipt: \n{tx_receipt}\n")
        # print("--------------------------------------------")

        print(f"Successfully minted property {i}.\n")
    print("___________________________________________")
    print("\nAll properties have now been minted.\n")
    print("___________________________________________")

    ########################################################################
    # ESCROW CONTRACT DEPLOYMENT
    ########################################################################
    print("\nDeploying the Escrow contract... \n")

    escrow_contract = Escrow.deploy(
        seller_address,
        real_estate_contract.address,
        inspector_address,
        lender_address,
        {"from": seller},
    )

    print("The Escrow contract has been successfully deployed.")
    print(f"The contract address is {escrow_contract.address} \n")

    print(f"Adding and updating the abi in the relevant development folders...")

    abi = escrow_contract.abi
    json_object = json.dumps(abi)
    with open("./contract_data/escrowABI.json", "w") as file:
        file.write(json_object)
    with open("./frontend/src/utils/escrowABI.json", "w") as file:
        file.write('{ "escrowABI": ')
        file.write(json_object)
        file.write(" }")

    print("Successfully updated the ABI. \n")

    print("Updating the contract address file in the frontend...")

    address = escrow_contract.address
    with open("./contract_data/escrowAddress", "w") as file:
        file.write(address)
    with open("./frontend/src/utils/escrowAddress", "w") as file:
        file.write(address)

    print("Successfully updated the contract address.\n")

    ########################################################################
    # Seller is approving the Escrow contract to transfer each of the properties
    ########################################################################

    print("The seller is approving the Escrow contract to tranfer the NFTs...\n")

    for i in range(1, 4):
        print(f"Approving property {i}...")
        tx = real_estate_contract.approve(escrow_contract.address, i, {"from": seller})
        print(f"Property {i} approved.\n")
    print("All properties have now been approved\n")

    ########################################################################
    # Seller is now listing each of the properties
    ########################################################################

    print("The seller is now listing each of the properties on Web3-Estates...\n")

    for i in range(1, 4):
        print(f"Listing property {i}...")
        property_price = i * 4
        escrow_price = i * 2
        tx = escrow_contract.list(
            i, buyer_address, property_price, escrow_price, {"from": seller}
        )
        print(f"Property {i} has been listed.\n")
    print("All properties have now been listed.\n")

    ########################################################################
    ########################################################################

    print("\n______________________________\n")
    print("Deploy script is complete, and the contracts are ready to be used.")
    print("______________________________\n")
