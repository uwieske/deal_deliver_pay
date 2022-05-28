// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.12;

interface ITransporter {
     function getName() external view returns(string memory);
     function transfer() external payable;
}