// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LoanSyndication is ERC1155, Ownable {
    // Token IDs: 0 = Master Loan NFT, 1 = Participation Shares
    uint256 public constant MASTER_LOAN = 0;
    uint256 public constant LOAN_SHARES = 1;

    constructor() ERC1155("") Ownable(msg.sender) {
        // Mint the Master Loan NFT to the Lead Bank (you)
        _mint(msg.sender, MASTER_LOAN, 1, "");
    }

    // Function to syndicate shares to partner banks
    function syndicateShares(address partnerBank, uint256 amount) public onlyOwner {
        _mint(partnerBank, LOAN_SHARES, amount, "");
    }
}
