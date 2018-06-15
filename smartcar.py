import requests
import json

def get_vehicle_info(id):
	"""
	Get vehicle information based on ID
	:param id: A unqiue idenitifer to locate a car
	:rtype: ret_data: JSON object containing relevant vehicle details if found
	"""
	headers = {
	    'Content-Type': 'application/json'
	}

	if (id is None):
		raise ValueError("Please provide a valid option for the vehicle ID.")

	if (type(id) != int):
		raise ValueError("Please provide a valid option for the vehicle ID. " + id + " is not a valid option")

	params = {
		"id": id,
		"responseType": "JSON"
	}

	r = requests.post('http://gmapi.azurewebsites.net/getVehicleInfoService', headers=headers, json=params)

	ret_data = None
	# we have what we need and check for 4XX or 5XX status codes
	if (r.status_code == requests.codes.ok and r.raise_for_status() is None):
		r  = r.json()

		#Validate that a car with specified id exists
		if ('data' in r):
			data = r['data']
		else:
			raise ValueError("404")

		#Grab relevant data if present

		if ('vin' in data):
			vin = data['vin']['value']
		else:
			raise ValueError('No VIN present for this vehicle')

		if ('color' in data):
			color = data['color']['value']
		else:
			raise ValueError("No Color specified for this vehicle")

		door_count = 0
		if ('fourDoorSedan' in data and 'twoDoorCoupe' in data):
			if (data['fourDoorSedan']['value'] == 'True'):
				door_count = 4
			if (data['twoDoorCoupe']['value'] == 'True'):
				door_count = 2
		else:
			raise ValueError("No door count specified for this vehicle")

		if ('driveTrain' in data):
			drive_train = data['driveTrain']['value']
		else:
			raise ValueError("No drive train specified for this vehicle")

		#return the data we have in a JSON
		ret_data = {
			"vin" : vin,
			"color" : color,
			"doorCount" : door_count,
			"driveTrain" : drive_train
		}
	else:
		r.raise_for_status()
	return ret_data

"""
Get status of each door (LOCKED/UNLOCKED)
"""
def get_door_status(id):

	headers = {
	    'Content-Type': 'application/json'
	}

	if (id is None):
		raise ValueError("Please provide a value option for the vehicle ID.")

	if (type(id) != int):
		raise ValueError("Please provide a valid option for the vehicle ID. " + id + " is not a valid option")

	params = {
		"id": id,
		"responseType": "JSON"
	}

	r = requests.post('http://gmapi.azurewebsites.net/getSecurityStatusService', headers=headers, json=params)

	ret_data = None
	# we have what we need and check for 4XX or 5XX status codes
	if (r.status_code == requests.codes.ok):
		r  = r.json()
		if ('data' in r):
			data = r['data']
		else:
			raise ValueError("404")

		ret_data = []
		if ('doors' in data):
			if ('values' in data['doors']):
				values = data['doors']['values']
				for value in values:
					if (value['locked']['value'] == "True"):
						locked = True
					if (value['locked']['value'] == "False"):
						locked = False
					ret_value = {
						"location" : value['location']['value'],
						"locked": locked
					}
					ret_data.append(ret_value)
		else:
			raise ValueError("There are no doors for this vehicle")

	return ret_data

"""
Obtains fuel range if the car is gas-operated
"""
def get_fuel_range(id):
	headers = {
	    'Content-Type': 'application/json'
	}

	if (id is None):
		raise ValueError("Please provide a value option for the vehicle ID.")

	if (type(id) != int):
		raise ValueError("Please provide a valid option for the vehicle ID. " + id + " is not a valid option")

	params = {
		"id": id,
		"responseType": "JSON"
	}

	r = requests.post('http://gmapi.azurewebsites.net/getEnergyService', headers=headers, json=params)

	ret_data = None
	# we have what we need and check for 4XX or 5XX status codes
	if (r.status_code == requests.codes.ok):
		r  = r.json()
		if ('data' in r):
			data = r['data']
		else:
			raise ValueError("404")

		ret_data = {}

		if (data['tankLevel']['value'] != 'null'):
			ret_data['percent'] = float(data['tankLevel']['value'])
		else:
			raise ValueError("404")
	else:
		r.raise_for_status()

	return ret_data

"""
Obtains the battery range if the car is electric
"""
def get_battery_range(id):
	headers = {
	    'Content-Type': 'application/json'
	}

	params = {
		"id": id,
		"responseType": "JSON"
	}

	r = requests.post('http://gmapi.azurewebsites.net/getEnergyService', headers=headers, json=params)

	ret_data = None
	# we have what we need and check for 4XX or 5XX status codes
	if (r.status_code == requests.codes.ok):
		r  = r.json()
		if ('data' in r):
			data = r['data']
		else:
			raise ValueError("404")

		ret_data = {}

		if (data['batteryLevel']['value'] != 'null'):
			ret_data['percent'] = float(data['batteryLevel']['value'])
		else:
			raise ValueError("404")
	else:
		r.raise_for_status()

	return ret_data

"""
Allows user to start/stop a car
"""
def control_engine(id, action):
	headers = {
	    'Content-Type': 'application/json'
	}
	#add case checking
	if (id is None):
		raise ValueError("Please provide a value option for the vehicle ID.")

	if (type(id) != int):
		raise ValueError("Please provide a valid option for the vehicle ID. " + id + " is not a valid option")

	if (action is None):
		raise ValueError("Please provide a value input for the action (START|STOP)")

	if (type(action) != str and type(action) != unicode):
		raise ValueError("Please provide a valid input for the action (START|STOP). " + str(action) + " is not a valid input")

	if (action == 'START'):
		command = "START_VEHICLE"
	elif (action == 'STOP'):
		command = "STOP_VEHICLE"
	else:
		raise ValueError("Please provide a valid input for the action (START|STOP). " + action + " is not a valid input")

	params = {
		"id": id,
		"command" : command,
		"responseType": "JSON"
	}

	r = requests.post('http://gmapi.azurewebsites.net/actionEngineService', headers=headers, json=params)

	ret_data = None
	# we have what we need and check for 4XX or 5XX status codes
	if (r.status_code == requests.codes.ok):
		data  = r.json()

		ret_data = {}
		if ('actionResult' in data):
			if (data['actionResult']['status'] == "EXECUTED"):
				ret_data['status'] = 'success'
			if (data['actionResult']['status'] == "FAILED"):
				ret_data['status'] = 'error'
		else:
			raise ValueError("404")
	
	else:
		r.raise_for_status()

	return ret_data
