// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.12;

import "./TxDS.sol";
import "./ITransporter.sol";

/**
 * This contract creates and manages all escrow contracts.
 *
 */
contract TxDSMan {
    string public name = "Transaction Delivery Service Management";
    mapping(address => TxDS) private escrows;
    mapping(bytes32 => TxDS) private escrowsByCommitment;
    mapping(address => ITransporter) private _transporterContracts;
    mapping(string => address) private _transporterAddresses;
    string[] _transporterNames;
    mapping(string => address) private registryTransporters;
    mapping(bytes32 => address) private escrowsByHash;

    enum HandlingChargesBy {
        SELLER,
        BUYER,
        OTHER
    }

    constructor() {
    }

    /**
     * This function creates a new escrow contract based on
     * the passed arguments.
     *
     */
    function createTransaction(
        address payable seller,
        address payable buyer,
        uint256 committedValue,
        string memory commitmentID,
        uint256 weight,
        uint8 handlingChargesBy,
        string memory client,
        string memory transporterName
    ) external {
        address transporterAddress = _transporterAddresses[transporterName];
        TxDS txDS = new TxDS(
            address(this),
            seller,
            buyer,
            committedValue,
            commitmentID,
            weight,
            handlingChargesBy,
            client,
            transporterAddress
        );
        escrows[address(txDS)] = txDS;
        bytes32 hashValue = keccak256(
            abi.encodePacked(
                seller,
                buyer,
                committedValue,
                commitmentID,
                handlingChargesBy,
                client
            )
        );
        escrowsByHash[hashValue] = address(txDS);
    }

    /**
     * Return the address of the escrow TxDS contract given the arguments.
     */
    function getTxDSByCommitment(
        address payable seller,
        address payable buyer,
        uint256 committedValue,
        string memory commitmentID,
        uint8 handlingChargesBy,
        string memory client
    ) external view returns (TxDS) {
        return
            escrowsByCommitment[
                keccak256(
                    abi.encodePacked(
                        seller,
                        buyer,
                        committedValue,
                        commitmentID,
                        handlingChargesBy,
                        client
                    )
                )
            ];
    }

    function getHashTxDSByCommitment(
        address payable seller,
        address payable buyer,
        uint256 committedValue,
        string memory commitmentID,
        uint8 handlingChargesBy,
        string memory client
    ) external view returns (bytes32) {
        return
            keccak256(
                abi.encodePacked(
                    seller,
                    buyer,
                    committedValue,
                    commitmentID,
                    handlingChargesBy,
                    client
                )
            );
    }

    function getTxDSContractAddressByHash(
        address payable seller,
        address payable buyer,
        uint256 committedValue,
        string memory commitmentID,
        uint8 handlingChargesBy,
        string memory client
    ) external view returns (address) {
        return
            escrowsByHash[
                keccak256(
                    abi.encodePacked(
                        seller,
                        buyer,
                        committedValue,
                        commitmentID,
                        handlingChargesBy,
                        client
                    )
                )
            ];
    }

    /**
     * Get list of transporters with their corresponding pricing.
     */
    function getTransportsAndPricing() internal view returns (string memory) {
        return "";
    }

    function registerTransporter(
        address transporterAddress,
        string memory transporterName
    ) external {
        _transporterAddresses[transporterName] = transporterAddress;
        _transporterContracts[transporterAddress] = ITransporter(
            payable(transporterAddress)
        );
        _transporterNames.push(transporterName);
    }

    function getTransportContract(string memory transporterName)
        external
        view
        returns (ITransporter)
    {
        return _transporterContracts[_transporterAddresses[transporterName]];
    }
}
