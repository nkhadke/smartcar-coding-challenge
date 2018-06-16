from flask import Flask, request, abort
import smartcar
import json

"""
This is the Flask instance that runs locally on localhost:5000. We can perform
GET/POST requests using curl on the routes that have been defined below.
"""

app = Flask("Smartcar API")

#Route for getting vehicle info based on ID
@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicle_info(id):
	if (request.method == 'GET'):
		try:
			ret = smartcar.get_vehicle_info(id)
		except ValueError as err:
			if (err.message == "404"):
				abort(404, "Vehicle not found")
			else:
				return (400, err.message)
		return json.dumps(ret, indent=4)

#Route for getting status of each door for a vehicle given an ID
@app.route('/vehicles/<int:id>/doors', methods=['GET'])
def get_door_status(id):
	if (request.method == 'GET'):
		try:
			ret = smartcar.get_door_status(id)
		except ValueError as err:
			if (err.message == "404"):
				abort(404, "Vehicle not found")
			else:
				return (400, err.message)
		return json.dumps(ret, indent=4)

#Route for getting the fuel range for a fuel-powered vehicle
@app.route('/vehicles/<int:id>/fuel', methods=['GET'])
def get_fuel_range(id):
	if (request.method == 'GET'):
		try:
			ret = smartcar.get_fuel_range(id)
		except ValueError as err:
			if (err.message == "404"):
				abort(404, "Vehicle not found")
			else:
				return (400, err.message)
		return json.dumps(ret, indent=4)

#Route for getting the battery range for an electric vehicle
@app.route('/vehicles/<int:id>/battery', methods=['GET'])
def get_battery_range(id):
	if (request.method == 'GET'):
		try:
			ret = smartcar.get_battery_range(id)
		except ValueError as err:
			if (err.message == "404"):
				abort(404, "Vehicle not found")
			else:
				return abort(400, err.message)
		return json.dumps(ret, indent=4)

#Route for start/stopping an engine of a vehicle given an ID and action (START|STOP)
@app.route('/vehicles/<int:id>/engine', methods=['POST'])
def control_engine(id):
	if (request.method == 'POST'):
		request_json = request.get_json()
		#get the desired action (START|STOP) from the request
		action = request_json.get('action')
		try:
			ret = smartcar.control_engine(id, action)
		except ValueError as err:
			if (err.message == "404"):
				abort(404, "Vehicle not found")
			else:
				return abort(400, err.message)
		return json.dumps(ret, indent=4)

if __name__ == '__main__':
	app.run(debug=True)