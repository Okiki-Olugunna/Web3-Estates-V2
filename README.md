## WEB3 ESTATES V2

### Buy & Sell Real Estate using NFTs

<!-- <b>_Website_</b>: https://web3-estates-v2.okikicodes.repl.co/ -->

#### How it works: 
- A seller mints a represention of their property (tokenisation), using the [RealEstateNFT](https://github.com/Okiki-Olugunna/Web3-Estates-V2/blob/main/contracts/RealEstateNFTs.sol) contract 
- Once the property has been tokenised, the seller lists the property using the [Escrow](https://github.com/Okiki-Olugunna/Web3-Estates-V2/blob/main/contracts/Escrow.sol) contract 
- Fast forward and a buyer would now like to purchase the property, so they deposit the required earnest 
- The physical property is then inspected & an inspector updates the inspection status on the escrow contract 
- After a successful inspection, the buyer and the seller both approve the sale of the property 
- Once the buyer and seller have approved the sale, the lender also approves the sale & transfers the remaining funds required into the escrow contract 
- The seller now finalises the sale & the ownership of the property is now transferred to the buyer

<br> 

<i> To see a full simulation of this process, have a look at the [01_deploy.py](https://github.com/Okiki-Olugunna/Web3-Estates-V2/blob/main/scripts/01_deploy.py) script showing the minitng and listing of the property, as well as the [02_simulate.py script](https://github.com/Okiki-Olugunna/Web3-Estates-V2/blob/main/scripts/02_simulate.py), showing the inspection, approval & lending process. </i>

<br>

<b> Project Preview: </b>

<img src="https://user-images.githubusercontent.com/92333005/206748642-ac747e6e-84e8-4285-9f80-38d95a9e57ac.png" width="800" />
