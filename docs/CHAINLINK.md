# Project Info

## Chainlink Local Node info
We have deployed a local Chainlink node running in a Docker container.
The purpose for deploying a Chainlink node is to get pricing information of transporter services from off-chain to on-chain.
The directory node contains a template of the relevant files in order to install and run a local Chainlink node.
We followed the installation instructions on https://www.youtube.com/watch?v=DO3O6ZUtwbs

## Chainlink External Adapter and a Transporter's Rest API
We created an external adapter in order to broker between chainlink node and the Rest API of fictive transporter (UMC).
The Rest API is programmed Python with Flask and exposed as a Rest API running in a Docker container.
Our external adapter implementation is programmed in NodeJS based on the Chainlink templates.

Chainlink (Kovan net)
* Oracle contract at 0x1E457b132FF582B3e1B842C316FC043BdC429664
* Chainlink Node Wallet address: 0x025a26461c9d43163831d6044fcc378FaBec5699


