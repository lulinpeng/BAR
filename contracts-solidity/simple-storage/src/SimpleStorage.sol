// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleStorage {
    uint256 private storedData;
    address public owner;

    event DataChanged(uint256 oldValue, uint256 newValue, address changer);

    modifier onlyOwner() {
        _onlyOwner();
        _;
    }
    
    function _onlyOwner() internal view {
        require(msg.sender == owner, "Only owner can call this function");
    }

    constructor() {
        owner = msg.sender;
    }

    function set(uint256 x) public onlyOwner {
        emit DataChanged(storedData, x, msg.sender);
        storedData = x;
    }

    function get() public view returns (uint256) {
        return storedData;
    }

    function getOwner() public view returns (address) {
        return owner;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "New owner cannot be zero address");
        owner = newOwner;
    }

    function reset() public onlyOwner {
        emit DataChanged(storedData, 0, msg.sender);
        storedData = 0;
    }

    receive() external payable {
        // the contract can receive ETH
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
