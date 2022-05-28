const { Requester, Validator } = require('@chainlink/external-adapter')
// require('dotenv').config()

// Define custom error scenarios for the API.
// Return true for the adapter to retry.
const customError = (data) => {
  if (data.Response === 'Error') return true
  return false
}

// Define custom parameters to be used by the adapter.
// Extra parameters can be stated in the extra object,
// with a Boolean value indicating whether or not they
// should be required.
const customParams = {
  charge_type: ['charge_type' ],
  service_type: ['service_type'],
  package_type: ['package_type'],
  weight: ['weight'],
  zone: ['zone'],


  // base: ['base', 'from', 'coin'],
  // quote: ['quote', 'to', 'market'],
  // endpoint: false
}

const createRequest = (input, callback) => {
  console.log('INPUT: ', input);
  // The Validator helps you validate the Chainlink request data
  const validator = new Validator(callback, input, customParams)
  const jobRunID = validator.validated.id  
  // const endpoint = validator.validated.data.endpoint || 'price'
  const url = `http://localhost:5000/delivery-costs`
  // const fsym = validator.validated.data.base.toUpperCase()
  // const tsyms = validator.validated.data.quote.toUpperCase()
  console.log('charge_type', validator.validated.data.charge_type);
  console.log('service_type', validator.validated.data.service_type);
  console.log('package_type', validator.validated.data.package_type);
  console.log('weight', validator.validated.data.weight);
  console.log('zone', validator.validated.data.zone);

  charge_type = validator.validated.data.charge_type;
  service_type = validator.validated.data.service_type;
  package_type = validator.validated.data.package_type;
  weight =  validator.validated.data.weight;
  zone = validator.validated.data.zone;

  //'{"charge_type": 0, "service_type":"UPS Express", "package_type": "parcel", "weight": 46.4, "zone": "1"}' 
  const params = {
    // fsym,
    // tsyms
  }
  
  
  const method = 'post'
  const headers = {'Content-Type': 'application/json'}

  // This is where you would add method and headers
  // you can add method like GET or POST and add it to the config
  // The default is GET requests
  // method = 'get' 
  // headers = 'headers.....'
  const config = {    
    url,
    params,
    method,
    headers,
    data: { charge_type, service_type, package_type, weight, zone}
  }

  // The Requester allows API calls be retry in case of timeout
  // or connection failure
  Requester.request(config, customError)
    .then(response => {
      // It's common practice to store the desired value at the top-level
      // result key. This allows different adapters to be compatible with
      // one another.
      // console.log('Response data: ', response);
      // response.data.result = Requester.validateResultNumber(response.data, [tsyms])
      callback(response.status, Requester.success(jobRunID, response))
    })
    .catch(error => {
      callback(500, Requester.errored(jobRunID, error))
    })
}

// This is a wrapper to allow the function to work with
// GCP Functions
exports.gcpservice = (req, res) => {
  createRequest(req.body, (statusCode, data) => {
    res.status(statusCode).send(data)
  })
}

// This is a wrapper to allow the function to work with
// AWS Lambda
exports.handler = (event, context, callback) => {
  createRequest(event, (statusCode, data) => {
    callback(null, data)
  })
}

// This is a wrapper to allow the function to work with
// newer AWS Lambda implementations
exports.handlerv2 = (event, context, callback) => {
  createRequest(JSON.parse(event.body), (statusCode, data) => {
    callback(null, {
      statusCode: statusCode,
      body: JSON.stringify(data),
      isBase64Encoded: false
    })
  })
}

// This allows the function to be exported for testing
// or for running in express
module.exports.createRequest = createRequest
