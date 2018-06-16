"""
This contains utility functions that are used in functions in smartcar.py.
They are primarily being used to assist with data parsing/verification
"""

def check_valid_input(params):
	"""
	To check if inputs for an API request is of the correct form and
	returns relevant params that are ready to be passed to GM API
	"""
	#Check for valid ID input
	if ("id" in params):
		if (params['id'] is None):
			raise ValueError("Please provide a valid option for the vehicle ID.")
		if (type(params['id']) != int):
			raise ValueError("Please provide a valid option for the vehicle ID. " + params['id'] + " is not a valid option")
	#Check for valid command input
	if ("command" in params):
		if (params['command'] is None):
			raise ValueError("Please provide a value input for the action (START|STOP)")
		elif (type(params['command']) != str and type(params['command']) != unicode):
			raise ValueError("Please provide a valid input for the action (START|STOP). " + str(params['command']) + " is not a valid input")
		elif (params['command'] == 'START'):
			params["command"] = "START_VEHICLE"
		elif (params['command'] == 'STOP'):
			params["command"] = "STOP_VEHICLE"
		else:
			raise ValueError("Please provide a valid input for the action (START|STOP). " + params['command'] + " is not a valid input")

	return params