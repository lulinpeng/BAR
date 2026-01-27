// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test} from "forge-std/Test.sol";
import {console} from "forge-std/console.sol";
import {console2} from "forge-std/console2.sol";
// import {Script} from "forge-std/Script.sol";
import {SimpleStorage} from "../src/SimpleStorage.sol";

contract SimpleStorageTest is Test {
    SimpleStorage public simpleStorage;

    event DataChanged(uint256 oldValue, uint256 newValue, address changer);
    address owner = address(0x123);
    address nonOwner = address(0x456);
    address newOwner = address(0x789);
    
    function setUp() public {
        console.log("+++ owner address: %s,  non owner address: %s, new owner address: %s +++", owner, nonOwner, newOwner);
        vm.startPrank(owner); // set msg.sender as owner
        simpleStorage = new SimpleStorage(); // deploy the contract
        vm.stopPrank();
    }
    
    function testDeployment() public view {
        console.log("testDeployment");
        assertEq(simpleStorage.getOwner(), owner, "Owner should be set correctly");
        assertEq(simpleStorage.get(), 0, "Initial value should be 0");
        assertEq(simpleStorage.getBalance(), 0, "Contract balance should be 0");
    }
    
    function testSetAndGet() public {
        vm.startPrank(owner);
        console.log("testSetAndGet");
        simpleStorage.set(42);
        assertEq(simpleStorage.get(), 42, "Value should be set to 42");
        
        simpleStorage.set(100);
        assertEq(simpleStorage.get(), 100, "Value should be set to 100");
        
        vm.stopPrank();
    }
    
    function testOnlyOwnerCanSet() public {
        vm.startPrank(nonOwner);
        vm.expectRevert("Only owner can call this function");
        simpleStorage.set(99);
        vm.stopPrank();
        
        vm.startPrank(owner);
        simpleStorage.set(99);
        assertEq(simpleStorage.get(), 99, "Owner should be able to set value");
        vm.stopPrank();
    }
    
    function testTransferOwnership() public {
        assertEq(simpleStorage.getOwner(), owner, "Initial owner should be correct");
        
        vm.startPrank(owner);
        simpleStorage.transferOwnership(newOwner);
        vm.stopPrank();
        
        assertEq(simpleStorage.getOwner(), newOwner, "New owner should be set");
        
        vm.startPrank(owner);
        vm.expectRevert("Only owner can call this function");
        simpleStorage.set(50);
        vm.stopPrank();
        
        vm.startPrank(newOwner);
        simpleStorage.set(50);
        assertEq(simpleStorage.get(), 50, "New owner should be able to set value");
        vm.stopPrank();
    }
    
    function testCannotTransferToZeroAddress() public {
        vm.startPrank(owner);
        vm.expectRevert("New owner cannot be zero address");
        simpleStorage.transferOwnership(address(0));
        vm.stopPrank();
    }
    
    function testEventEmission() public {
        vm.startPrank(owner);
        vm.expectEmit(true, true, true, true);
        emit DataChanged(0, 123, owner); // define a expected event
        simpleStorage.set(123); // trigger an event
        vm.stopPrank();
    }
    
    function testReset() public {
        vm.startPrank(owner);

        simpleStorage.set(999);
        assertEq(simpleStorage.get(), 999, "Value should be 999");
        
        simpleStorage.reset();
        assertEq(simpleStorage.get(), 0, "Value should be reset to 0");
        
        vm.stopPrank();
    }
    
    function testReceiveEther() public {
        uint256 amount = 1 ether;
        vm.deal(owner, amount);  // give Ether to owner for testing

        vm.startPrank(owner);

        bool success;
        (success, ) = address(simpleStorage).call{value: 0.5 ether}("");
        require(success, "Transfer failed");
        console.log("balance: ", simpleStorage.getBalance());
        (success, ) = address(simpleStorage).call{value: 0.5 ether}("");
        console.log("balance: ", simpleStorage.getBalance());
        assertEq(address(simpleStorage).balance, amount, "Contract should receive ether");
        assertEq(simpleStorage.getBalance(), amount, "getBalance should return correct amount");
        console.log("balance: ", simpleStorage.getBalance());
        
        vm.stopPrank();
    }
    
    function testAnyoneCanGet() public {
        vm.startPrank(nonOwner);
        uint256 value = simpleStorage.get();
        assertEq(value, 0, "Anyone should be able to call get");
        vm.stopPrank();
        
        vm.startPrank(newOwner);
        value = simpleStorage.get();
        assertEq(value, 0, "Anyone should be able to call get");
        vm.stopPrank();
    }
    
    function testBoundaryConditions() public {
        vm.startPrank(owner);
        
        simpleStorage.set(type(uint256).max);
        assertEq(simpleStorage.get(), type(uint256).max, "Should handle max uint256");
        
        simpleStorage.set(0);
        assertEq(simpleStorage.get(), 0, "Should handle 0");

        simpleStorage.set(1);
        assertEq(simpleStorage.get(), 1, "Should handle 1");

        vm.stopPrank();
    }
    
    // Fuzz Testing: Foundry automatically generates various test values for uint256 x.
    function testFuzzSetAndGet(uint256 x) public {
        vm.startPrank(owner);
        console2.log("xxx testFuzzSetAndGet, x = %d xxx", x);
        simpleStorage.set(x);
        assertEq(simpleStorage.get(), x, "Should get what was set");
        vm.stopPrank();
    }
}