import { expect } from "chai";
import { BigNumberish, Signer } from "ethers";
import { ethers } from "hardhat";
import { describe } from "mocha";
import { TxDSMan__factory, TxDSMan, UMC__factory, UMC, TxDS } from "../typechain";

describe('TxDSMan', () => {
    let TxDSMan: TxDSMan__factory;
    let txDSMan: TxDSMan;
    let UMC: UMC__factory;
    let umc: UMC;
    let signers: Signer[];
    let seller: string;
    let buyer: string;
    let commitedValue: BigNumberish;
    let commitmentID: string;
    let client: string;
    let transporterName: string;


    beforeEach(async () => {
        
        UMC= await ethers.getContractFactory('UMC');
        TxDSMan = await ethers.getContractFactory('TxDSMan');
        signers = await ethers.getSigners();
        seller = await signers[1].getAddress();
        buyer = await signers[2].getAddress();
        commitedValue = 500;
        commitmentID = '123';
        client = '555666'; 
        transporterName = 'UMC';       
        umc = await UMC.deploy("umc");                
        txDSMan = await TxDSMan.deploy();                
    });

    it('has name', async () => {
        await txDSMan.name();
    });

    it('createTransaction', async () => {
        await txDSMan.registerTransporter(umc.address, "UMC");
        const tx = await txDSMan.createTransaction(seller, buyer, commitedValue, commitmentID,23, 0, client, transporterName);
        const a = await txDSMan.getTxDSByCommitment(seller, buyer,23,commitmentID,0,client);
                        
    });

    it('getHashTxDSByCommitment', async () => {
        const tx = await txDSMan.createTransaction(seller, buyer, commitedValue, commitmentID, 24,0, client,transporterName);        
        const hashed = await txDSMan.getHashTxDSByCommitment(seller, buyer, commitedValue, commitmentID,0, client);
        console.log(hashed);        
    });


});

