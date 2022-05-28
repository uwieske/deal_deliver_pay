import { expect } from "chai";
import { BigNumberish, Signer } from "ethers";
import { ethers } from "hardhat";
import { describe } from "mocha";
import { TxDS__factory, TxDS, UMC__factory, UMC } from "../typechain";


// const { network, deployments } = require("hardhat");
// const { developmentChains } = require("../../helper-hardhat-config");
// const { numToBytes32 } = require("@chainlink/test-helpers/dist/src/helpers");

// console.log('NETWORK NAME: ',network.name);


describe('TxDS', () => {
    let TxDS: TxDS__factory;
    let txDS: TxDS;
    let signers: Signer[];
    let owner: string;
    let seller: string;
    let buyer: string;
    let commitedValue: BigNumberish;
    let commitmentID: string;
    let client: string;
    let UMC: UMC__factory;
    let umc: UMC;
    let transporterName: string;
    let transporterAddress: string;

    beforeEach(async () => {
        UMC = await ethers.getContractFactory('UMC');
        TxDS = await ethers.getContractFactory('TxDS');
        signers = await ethers.getSigners();
        owner = await signers[9].getAddress();
        seller = await signers[1].getAddress();
        buyer = await signers[2].getAddress();
        commitedValue = 500;
        commitmentID = '123';
        client = '555666';

        // txDS = await TxDS.deploy(client, seller, buyer, commitedValue, commitmentID, 15, 0);
    });

    it('has version', async () => {
        umc = await UMC.deploy('umc');
        txDS = await TxDS.deploy(owner, seller, buyer, commitedValue, commitmentID, 15, 0, client, umc.address);
        expect(await txDS.version()).to.be.equal('1.0');
    });

    it('deposit totalCommitmentValue in state CREATED will error', async () => {
        txDS = await TxDS.deploy(owner, seller, buyer, commitedValue, commitmentID, 15, 0, client, umc.address);
        expect(await txDS.state()).to.be.equal(0);
        await expect(txDS.depositTotalCommitmentValue())
            .to.be.revertedWith('The invoked operation is not allowed in this state.');
    });

    it('deposit totalCommitmentValue emits', async () => {
        txDS = await TxDS.deploy(owner, seller, buyer, commitedValue, commitmentID, 15, 0, client, umc.address);
        await expect(txDS.requestDeliveryCosts(0, 'UPS Express', 'parcel', 12, '51')).to.emit(txDS, 'TRANSPORT_REACHED').withArgs(12);
    });


});

describe('constructor', () => {

    let TxDS: TxDS__factory;
    let txDS: TxDS;
    let signers: Signer[];
    let owner;
    let seller;
    let buyer;
    let commitedValue;
    let commitmentID;
    let client: string;
    let UMC: UMC__factory;
    let umc: UMC;


    beforeEach(async () => {
        signers = await ethers.getSigners();
    });

    it('created instance', async () => {

        UMC = await ethers.getContractFactory('UMC');
        TxDS = await ethers.getContractFactory('TxDS');
        owner = await signers[9].getAddress();
        seller = await signers[1].getAddress();
        buyer = await signers[2].getAddress();
        commitedValue = 500;
        commitmentID = '123';
        client = '555666';
        umc = await UMC.deploy("umc");
        txDS = await TxDS.deploy(owner, seller, buyer, commitedValue, commitmentID, 12, 0, client, umc.address);
        expect(txDS).to.exist;
    });
});