// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.12;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./ITransporter.sol";

contract UMC is ITransporter {
    using SafeMath for uint256;
    
    uint256 private _balance;
    string private _name;

    constructor(string memory name)   {
        _name = name;
    }

    function transfer() external payable {
        _balance = _balance.add(msg.value);
    }

    function getName() external view override returns (string memory) {
        return _name;
    }
}
