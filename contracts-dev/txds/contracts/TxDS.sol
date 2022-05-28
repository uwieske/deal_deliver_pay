// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.12;
import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./TxDSMan.sol";

/** 
This contract represents an escrow which tracks the state of a 
transaction and delivery process. 
*/
contract TxDS is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;
    using SafeMath for uint256;

    string public version = "1.0";
    string public name = "Transaction Delivery Service";
    uint256 private constant ORACLE_PAYMENT = 1 * LINK_DIVISIBILITY; // 1 * 10**18
    string private _jobId;
    address private _oracle;

    address payable private _seller;
    address payable private _buyer;
    uint256 private _committedValue;
    string private _commitmentID;
    string private _clientID;
    uint256 private _weight;
    address private _factoryAddress;
    uint8 _handlingChargesBy;

    uint256 private _balance;
    uint256 private _balanceHandlingCosts;
    uint256 private _balanceGoodValue;
    uint256 private _deliveryCosts;
    string _transporterName;
    address _transporterAddress;

    // State definitions
    enum States {
        CREATED,
        COSTS_PENDING,
        COSTS_KNOWN,
        DEPOSITED,
        DROPPED_OFF,
        HANDED_OVER,
        RECEIVED,
        RELEASING,
        RELEASED
    }
    // current state
    States public state = States.CREATED;

    event RequestDeliveryCostsFulfilled(
        bytes32 indexed requestId,
        uint256 indexed price
    );

    //events
    event TxDS_CREATED(
        address txDSAddress,
        address seller,
        address buyer,
        uint256 committedValue,
        string commitmentID,
        uint8 handlingChargesBy
    );
    event TRANSPORT_REACHED(uint256 weight);
    event DEPOSITTED_GOOD_VALUE(uint256 depositGoodValue);
    event DEPOSITTED_HANDLING_COSTS(uint256 depositHandlingCosts);
    event DEPOSITTED(uint256 totalValue);
    event DROPPED_OFF(string clientID, string commitmentID);
    event HANDED_OVER(string clientID, string commitmentID);
    event RECEIVED(string clientID, string commitmentID);
    event RELEASING();
    event RELEASED_HANDLING_COSTS(uint256 handlingCosts);
    event RELEASED_GOOD_VALUE(uint256 goodValue);
    event RELEASED_BUYER_REFUNDED(uint256 refundValue);
    event RELEASED(uint256 depositValue, uint256 goodValue);


    constructor(
        address factoryAddress,
        address payable seller,
        address payable buyer,
        uint256 committedValue,
        string memory commitmentID,
        uint256 weight,
        uint8 handlingChargesBy,
        string memory client,
        address transporterAddress
    ) ConfirmedOwner(msg.sender) {
        require(
            factoryAddress != address(0),
            "factoryAddress must be defined."
        );
        require(seller != address(0), "seller must be defined.");
        require(buyer != address(0), "buyer must be defined.");
        require(committedValue >= 0, "committedValue must be defined.");
        require(
            bytes(commitmentID).length >= 0,
            "commitmentID must be defined."
        );
        require(bytes(client).length >= 0, "client must be defined.");
        require(weight > 0, "weight must be specified.");
        setChainlinkToken(0xa36085F69e2889c224210F603D836748e7dC0088);
        _jobId = "fb7c77cdb70341dd9599d348e385887d";
        _oracle = 0x1E457b132FF582B3e1B842C316FC043BdC429664;
        setChainlinkOracle(_oracle);

        _factoryAddress = factoryAddress;
        _seller = seller;
        _buyer = buyer;
        _committedValue = committedValue;
        _commitmentID = commitmentID;
        _weight = weight;
        _handlingChargesBy = handlingChargesBy;
        _transporterAddress = transporterAddress;
        emit TxDS_CREATED(
            _factoryAddress,
            _seller,
            _buyer,
            _committedValue,
            _commitmentID,
            _handlingChargesBy
        );
    }

    /**
     */
    function requestDeliveryCosts(
        int256 charge_type,
        string memory service_type,
        string memory package_type,
        uint256 weight,
        string memory zone
    ) public {
        require(
            state == States.CREATED,
            "The invoked operation is not allowed in this state."
        );

        Chainlink.Request memory req = buildChainlinkRequest(
            stringToBytes32(_jobId),
            address(this),
            this.fulfillDeliveryCosts.selector
        );

        req.addInt("charge_type", charge_type);
        req.add("service_type", service_type);
        req.add("package_type", package_type);
        req.addInt("weight", int(weight));
        req.add("zone", zone);

        sendChainlinkRequest(req, ORACLE_PAYMENT);
        state = States.COSTS_PENDING;
        emit TRANSPORT_REACHED(weight);
    }

    function fulfillDeliveryCosts(bytes32 _requestId, uint256 _price)
        public
        recordChainlinkFulfillment(_requestId)
    {
        require(
            state == States.COSTS_PENDING,
            "The invoked operation is not allowed in this state."
        );
        emit RequestDeliveryCostsFulfilled(_requestId, _price);
        _deliveryCosts = _price;
        state = States.COSTS_KNOWN;
    }

    /**
     * Deposit good value plus delivery costs
     */
    function depositTotalCommitmentValue() external payable {
        require(
            state == States.COSTS_KNOWN,
            "The invoked operation is not allowed in this state."
        );
        uint256 calculatedAmount = _committedValue.add(_balanceHandlingCosts);        
        require(msg.value >= calculatedAmount, "Not enough funds deposited.");
        _balanceHandlingCosts = _balanceHandlingCosts.add(_committedValue);
        _balanceGoodValue = _balanceGoodValue.add(_balanceHandlingCosts);
        _balance = _balance.add(msg.value);
        state = States.DEPOSITED;
        emit DEPOSITTED(msg.value);
    }

    function acceptPackage() external {
        require(
            state == States.DEPOSITED,
            "The invoked operation is not allowed in this state."
        );
        state = States.DROPPED_OFF;
        emit DROPPED_OFF(_clientID, _commitmentID);
    }

    function handoverPackage() external {
        require(
            state == States.DROPPED_OFF,
            "The invoked operation is not allowed in this state."
        );
        state = States.HANDED_OVER;
        emit HANDED_OVER(_clientID, _commitmentID);
    }

    function receivePackage() external {
        require(
            state == States.HANDED_OVER,
            "The invoked operation is not allowed in this state."
        );
        state = States.RECEIVED;
        emit RECEIVED(_clientID, _commitmentID);
    }

    function release() external {
        require(
            state == States.HANDED_OVER,
            "The invoked operation is not allowed in this state."
        );

        payable(_seller).transfer(_committedValue);
        _balance = _balance.sub(_committedValue);
        emit RELEASED_GOOD_VALUE(_committedValue);        
        payable(_transporterAddress).transfer(_deliveryCosts);
        _balance = _balance.sub(_deliveryCosts);
        emit RELEASED_HANDLING_COSTS(_deliveryCosts);
        if (_balance > 0) {
            uint256 refundValue = _balance;
            payable(_buyer).transfer(refundValue);
            _balance = 0;
            emit RELEASED_BUYER_REFUNDED(refundValue);
        }
        state = States.RELEASED;
    }

    function deliveryCosts() external view returns (uint256) {
        return _deliveryCosts;
    }

    modifier buyerOnly() {
        require(msg.sender == _buyer);
        _;
    }

    modifier sellerOnly() {
        require(msg.sender == _seller);
        _;
    }

    modifier factoryOnly() {
        require(msg.sender == _factoryAddress);
        _;
    }

    function stringToBytes32(string memory source)
        private
        pure
        returns (bytes32 result)
    {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
            return 0x0;
        }

        assembly {
            // solhint-disable-line no-inline-assembly
            result := mload(add(source, 32))
        }
    }
}
