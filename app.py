from flask import Flask, request, abort
import smartcar
import json

app = Flask("Smartcar API")

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

@app.route('/vehicles/<int:id>/engine', methods=['POST'])
def control_engine(id):
	if (request.method == 'POST'):
		request_json = request.get_json()
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