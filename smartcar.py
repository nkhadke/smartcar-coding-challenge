import requests
import json
import utility
"""
This contains the functions that parse input from client requests, obtain relevant 
data from the GM API and return the required data in a clean format to the client
"""

def get_vehicle_info(id):
	"""
	Get vehicle information based on ID
	:param id: A unqiue idenitifer to locate a car
	:rtype: ret_data: JSON object containing relevant vehicle details if found
	"""

	headers = {
	    'Content-Type': 'application/json'
	}

	params = {
		"id": id,
		"responseType": "JSON"
	}

	#check for valid input
	params = utility.check_valid_input(params)

	#perform POST request to GM API to obtain relevant data
	r = requests.post('http://gmapi.azurewebsites.net/getVehicleInfoService', headers=headers, json=params)

	ret_data = None
	# proceed with constructing the return object only if we have recieved data correctly
	if (r.status_code == requests.codes.ok and r.raise_for_status() is None):
		r  = r.json()

		#Validate that a car with specified id exists
		if ('data' in r):
			data = r['data']
		else:
			#this will trigger a 404 status code to be returned
			raise ValueError("404")

		#Grab relevant data if present

		if ('vin' in data):
			vin = data['vin']['value']
		else:
			raise ValueError("No VIN present for this vehicle")

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
		#Raise an exception for any 4XX or 5XX status code being returned from GM API
		r.raise_for_status()

	return ret_data

def get_door_status(id):
	"""
	Get status of each door for a given ID corresponding to a vehicle (LOCKED/UNLOCKED)
	:param id: A unqiue idenitifer to locate a car
	:rtype: ret_data: JSON object containing relevant vehicle details if found
	"""

	headers = {
	    'Content-Type': 'application/json'
	}

	params = {
		"id": id,
		"responseType": "JSON"
	}

	#check for a valid input
	params = utility.check_valid_input(params)

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

def get_fuel_range(id):
	"""
	Gets fuel range of a vehicle given its ID if applicable (if vehicle is fuel powered)
	:param id: A unqiue idenitifer to locate a car
	:rtype: ret_data: JSON object containing relevant vehicle details if found
	"""

	headers = {
	    'Content-Type': 'application/json'
	}

	params = {
		"id": id,
		"responseType": "JSON"
	}

	#check for a valid input
	params = utility.check_valid_input(params)

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

def get_battery_range(id):
	"""
	Gets battery range of a vehicle given its ID if applicable (if vehicle is electric)
	:param id: A unqiue idenitifer to locate a car
	:rtype: ret_data: JSON object containing relevant vehicle details if found
	"""

	headers = {
	    'Content-Type': 'application/json'
	}

	params = {
		"id": id,
		"responseType": "JSON"
	}

	#check for a valid input
	params = utility.check_valid_input(params)

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
	"""
	Allows clients to start/stop a vehicle given a unique ID and corresponding action
	:param id: A unqiue idenitifer to locate a car
	:param action: Corresponding action to take (START|STOP)
	:rtype: ret_data: JSON object containing relevant vehicle details if found
	"""

	headers = {
	    'Content-Type': 'application/json'
	}

	params = {
		"id": id,
		"command" : action,
		"responseType": "JSON"
	}

	#check for a valid input
	params = utility.check_valid_input(params)

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
