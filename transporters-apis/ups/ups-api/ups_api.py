from flask import Flask
from ups_model import estimate_deliver_costs, get_ups_countries_sending
from flask import jsonify, request
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>API of Transporter</p>"

@app.route("/ups_countries_sending", methods=['GET'])
def ups_countries_sending():   
    data = json.loads(get_ups_countries_sending()) 
    return jsonify({'data': data})

@app.route("/delivery-costs", methods=['POST'])
def compute_delivery_costs():
    data = json.loads(request.data)
    dc = estimate_deliver_costs(data['charge_type'],data['service_type'], data['package_type'], data['weight'], data['zone'])
    return jsonify({'delivery_costs': dc})