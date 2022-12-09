// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../interfaces/IERC721.sol";

contract Escrow {
    // addresses that will take part in the sale process
    address payable public seller;
    address public nftAddress;
    address public inspector;
    address public lender;

    // mappings to record data
    mapping(uint256 => bool) public isListed;
    mapping(uint256 => uint256) public purchasePrice;
    mapping(uint256 => uint256) public escrowAmount;
    mapping(uint256 => address payable) public buyer;
    mapping(uint256 => bool) public inspectionPassed;
    mapping(uint256 => mapping(address => bool)) public approval;

    // only the seller can call functions marked with this modifier
    modifier onlySeller() {
        require(
            msg.sender == seller,
            "Only the seller can call this function."
        );
        _;
    }

    // only the buyer can call functions marked with this modifier
    modifier onlyBuyer(uint256 _nftID) {
        require(
            msg.sender == buyer[_nftID],
            "Only the buyer can call this function."
        );
        _;
    }

    // only the inspector can call functions marked with this modifier
    modifier onlyInspector() {
        require(
            msg.sender == inspector,
            "Only the inspector can call this function."
        );
        _;
    }

    // event for when the property is listed
    event propertyListed(
        uint256 _id,
        uint256 _purchasPrice,
        uint256 _escrowPrice,
        uint256 _datetime
    );

    // event for when the buyer deposits earnest
    event earnestDeposted(address _buyer, uint256 _datetime);

    // event for when the inspection has been updated
    event inspectionUpdated(uint256 _nftid, bool _status, uint256 _datetime);

    // event for when an address approves a sale
    event saleApproved(uint256 _nftid, address _approver, uint256 _datetime);

    // event for when the seller finalises the sale
    event saleFinalised(uint256 _nftid, address _seller, uint256 _datetime);

    // event for if the sale was cancelled
    event saleCancelled(uint256 _nftid, address _canceller, uint256 _datetime);

    // initialising state variables
    constructor(
        address payable _seller,
        address _nftAddress,
        address _inspector,
        address _lender
    ) {
        seller = _seller;
        nftAddress = _nftAddress;
        inspector = _inspector;
        lender = _lender;
    }

    // allowing the contract to receive MATIC (from the lender)
    receive() external payable {}

    // function for the seller to list the property
    function list(
        uint256 _nftID,
        address payable _buyer,
        uint256 _purchasePrice,
        uint256 _escrowAmount
    ) external payable onlySeller {
        // transferring the NFT from the seller's wallet to this contract
        IERC721(nftAddress).transferFrom(msg.sender, address(this), _nftID);

        // marking the NFT as listed
        isListed[_nftID] = true;

        // updating relevant mappings
        buyer[_nftID] = _buyer;
        purchasePrice[_nftID] = _purchasePrice;
        escrowAmount[_nftID] = _escrowAmount;

        // emitting event
        emit propertyListed(
            _nftID,
            _purchasePrice,
            _escrowAmount,
            block.timestamp
        );
    }

    // function for the buyer to deposit the earnest for the property
    function depositEarnest(uint256 _nftID) external payable onlyBuyer(_nftID) {
        require(
            msg.value >= escrowAmount[_nftID],
            "You must deposit AT LEAST the escrow amount."
        );

        // emitting event
        emit earnestDeposted(msg.sender, block.timestamp);
    }

    // function for the inspector when looking at the property
    function updateInspectionStatus(uint256 _nftID, bool _passed)
        external
        onlyInspector
    {
        // updating the inspection status
        inspectionPassed[_nftID] = _passed;

        // emitting event
        emit inspectionUpdated(_nftID, _passed, block.timestamp);
    }

    // function for each participant to approve the sale
    function approveSale(uint256 _nftID) external {
        // approving the sale
        approval[_nftID][msg.sender] = true;

        // emitting event
        emit saleApproved(_nftID, msg.sender, block.timestamp);
    }

    // function to finalise the sale of the property
    function finaliseSale(uint256 _nftID) external {
        require(inspectionPassed[_nftID], "The inspection must first pass.");

        require(
            approval[_nftID][buyer[_nftID]],
            "The buyer must approve the sale."
        );
        require(approval[_nftID][seller], "The seller must approve the sale.");
        require(approval[_nftID][lender], "The lender must approve the sale.");

        require(
            address(this).balance >= purchasePrice[_nftID],
            "Contract balance is too low to finalise."
        );

        // updating the listed status
        isListed[_nftID] = false;

        // sending the funds to the seller
        (bool success, ) = payable(seller).call{value: address(this).balance}(
            ""
        );
        require(success, "Transfer of funds unsuccessful.");

        // transferring the property
        IERC721(nftAddress).transferFrom(address(this), buyer[_nftID], _nftID);

        // emitting event
        emit saleFinalised(_nftID, msg.sender, block.timestamp);
    }

    // function to cancel the sale of the property
    function cancelSale(uint256 _nftID) external {
        // if the inspection was not passed, give a refund to the buyer
        if (!inspectionPassed[_nftID]) {
            payable(buyer[_nftID]).transfer(address(this).balance);
        } else {
            // if the inspection passed, send the escrow amount to the seller
            payable(seller).transfer(address(this).balance);
        }

        // emitting event
        emit saleCancelled(_nftID, msg.sender, block.timestamp);
    }

    // function to get the balance of the contract
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
