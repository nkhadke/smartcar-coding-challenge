import unittest
import requests
import smartcar
from flask import abort

"""
This file extensively tests the various functions written in this project.
It also performs GET/POST requests for a Flask instance running on localhost:5000.
"""

class TestVehicleInfo(unittest.TestCase):
	"""
	Testing the get_vehicle_info function located in smartcar.py for valid input/output
	"""

	def test_invalid_input(self):

		#ensure that invalid inputs raise Errors
		with self.assertRaises(ValueError):
			smartcar.get_vehicle_info(123)
		with self.assertRaises(ValueError):
			smartcar.get_vehicle_info(0)
		with self.assertRaises(ValueError):
			smartcar.get_vehicle_info(-1234)
		with self.assertRaises(ValueError):
			smartcar.get_vehicle_info("123")
		with self.assertRaises(ValueError):
			smartcar.get_vehicle_info("invalid_input")
		with self.assertRaises(ValueError):
			smartcar.get_vehicle_info(None)

	def test_valid_output(self):

		ret_obj = smartcar.get_vehicle_info(1234)

		#check type of data being returned
		self.assertEqual(type(ret_obj), dict)
		self.assertEqual(type(ret_obj['vin']), unicode)
		self.assertEqual(type(ret_obj['color']), unicode)
		self.assertEqual(type(ret_obj['driveTrain']), unicode)
		self.assertEqual(type(ret_obj['doorCount']), int)

		#check value of data being returned
		self.assertEqual(ret_obj['vin'], '123123412412')
		self.assertEqual(ret_obj['color'], "Metallic Silver")
		self.assertEqual(ret_obj['driveTrain'], "v8")
		self.assertEqual(ret_obj['doorCount'], 4)

		ret_obj = smartcar.get_vehicle_info(1235)

		#check type of data being returned
		self.assertEqual(type(ret_obj), dict)
		self.assertEqual(type(ret_obj['vin']), unicode)
		self.assertEqual(type(ret_obj['color']), unicode)
		self.assertEqual(type(ret_obj['driveTrain']), unicode)
		self.assertEqual(type(ret_obj['doorCount']), int)

		#check value of data being returned
		self.assertEqual(ret_obj['vin'], '1235AZ91XP')
		self.assertEqual(ret_obj['color'], "Forest Green")
		self.assertEqual(ret_obj['driveTrain'], "electric")
		self.assertEqual(ret_obj['doorCount'], 2)

class TestDoorStatus(unittest.TestCase):
	"""
	Testing the get_door_status function located in smartcar.py for valid input/output
	"""

	def test_valid_input(self):

		#ensure that invalid inputs raise Errors
		with self.assertRaises(ValueError):
			smartcar.get_door_status(123)
		with self.assertRaises(ValueError):
			smartcar.get_door_status(0)
		with self.assertRaises(ValueError):
			smartcar.get_door_status(-1234)
		with self.assertRaises(ValueError):
			smartcar.get_door_status("123")
		with self.assertRaises(ValueError):
			smartcar.get_door_status("invalid_input")
		with self.assertRaises(ValueError):
			smartcar.get_door_status(None)

	def test_valid_output(self):
		ret_obj = smartcar.get_door_status(1234)

		#check type of data being returned
		self.assertEqual(type(ret_obj), list)
		for value in ret_obj:
			self.assertEqual(type(value), dict)
			self.assertEqual(type(value['locked']), bool)
			self.assertEqual(type(value['location']), unicode)

		#check for value of data being returned
		self.assertEqual(len(ret_obj), 4)
		#there is no way to check for booleans being returned right because they are being randomly generated
		#check that the exact 4 locations are present in the data being returned
		expected = ["frontLeft", "frontRight", "backRight", "backLeft"]
		for value in ret_obj:
			expected.remove(value['location'])
		self.assertEqual(len(expected), 0)

		ret_obj = smartcar.get_door_status(1235)

		#check type of data being returned
		self.assertEqual(type(ret_obj), list)
		for value in ret_obj:
			self.assertEqual(type(value), dict)
			self.assertEqual(type(value['locked']), bool)
			self.assertEqual(type(value['location']), unicode)

		#check that the exact 2 locations are present in the data being returned
		expected = ["frontLeft", "frontRight"]
		for value in ret_obj:
			expected.remove(value['location'])
		self.assertEqual(len(expected), 0)

class TestFuelRange(unittest.TestCase):
	"""
	Testing the get_fuel_range function located in smartcar.py for valid input/output
	"""

	def test_valid_input(self):

		#ensure that invalid inputs raise Errors
		with self.assertRaises(ValueError):
			smartcar.get_fuel_range(123)
		with self.assertRaises(ValueError):
			smartcar.get_fuel_range(0)
		with self.assertRaises(ValueError):
			smartcar.get_fuel_range(-1234)
		with self.assertRaises(ValueError):
			smartcar.get_fuel_range("123")
		with self.assertRaises(ValueError):
			smartcar.get_fuel_range("invalid_input")
		with self.assertRaises(ValueError):
			smartcar.get_fuel_range(None)

	def test_valid_output(self):

		ret_obj = smartcar.get_fuel_range(1234)

		#check type of data being returned
		self.assertEqual(type(ret_obj['percent']), float)

		#check value of data being returned
		self.assertLessEqual(ret_obj['percent'], 100.0)
		self.assertGreaterEqual(ret_obj['percent'], 0.0)

		#check that an error is raised for a non-fuel powered vehicle
		with self.assertRaises(ValueError):
			smartcar.get_fuel_range(1235)

class TestBatteryRange(unittest.TestCase):
	"""
	Testing the get_battery_range function located in smartcar.py for valid input/output
	"""

	def test_valid_input(self):

		#ensure that invalid inputs raise Errors
		with self.assertRaises(ValueError):
			smartcar.get_battery_range(123)
		with self.assertRaises(ValueError):
			smartcar.get_battery_range(0)
		with self.assertRaises(ValueError):
			smartcar.get_battery_range(-1234)
		with self.assertRaises(ValueError):
			smartcar.get_battery_range("123")
		with self.assertRaises(ValueError):
			smartcar.get_battery_range("invalid_input")
		with self.assertRaises(ValueError):
			smartcar.get_battery_range(None)

	def test_valid_output(self):
		ret_obj = smartcar.get_battery_range(1235)

		#check type of data being returned
		self.assertEqual(type(ret_obj['percent']), float)

		#check value of data being returned
		self.assertLessEqual(ret_obj['percent'], 100.0)
		self.assertGreaterEqual(ret_obj['percent'], 0.0)

		#check that an error is raised for a non-fuel powered vehicle
		with self.assertRaises(ValueError):
			smartcar.get_battery_range(1234)

class TestControlEngine(unittest.TestCase):
	"""
	Testing the control_engine function located in smartcar.py for valid input/output
	"""

	def test_valid_input(self):

		#check valid parameter for ID
		with self.assertRaises(ValueError):
			smartcar.control_engine(123, "START")
		with self.assertRaises(ValueError):
			smartcar.control_engine(0, "START")
		with self.assertRaises(ValueError):
			smartcar.control_engine(-1234, "START")
		with self.assertRaises(ValueError):
			smartcar.control_engine("123", "START")
		with self.assertRaises(ValueError):
			smartcar.control_engine("invalid_input", "START")
		with self.assertRaises(ValueError):
			smartcar.control_engine(None, "START")

		#check valid parameter for action
		with self.assertRaises(ValueError):
			smartcar.control_engine(1234, "start")
		with self.assertRaises(ValueError):
			smartcar.control_engine(1234, "stop")
		with self.assertRaises(ValueError):
			smartcar.control_engine(1234, "sTaRt")
		with self.assertRaises(ValueError):
			smartcar.control_engine(1234, "sToP")
		with self.assertRaises(ValueError):
			smartcar.control_engine(1234, None)
		with self.assertRaises(ValueError):
			smartcar.control_engine(1234, "")
		with self.assertRaises(ValueError):
			smartcar.control_engine(1234, "invalid_input")
		with self.assertRaises(ValueError):
			smartcar.control_engine(1234, 123)

	def test_valid_output(self):

		ret_obj = smartcar.control_engine(1234, "START")

		#check type of data being returned
		self.assertEqual(type(ret_obj), dict)
		self.assertEqual(type(ret_obj['status']), str)


class TestGetPostRequests(unittest.TestCase):
	"""
	This is to test whether GET and POST requests are being performed and handled correctly.
	This class is testing the various functions in smartcar.py by performing GET/POST requests
	on a Flask instance running on a local server.

	*** IMPORTANT ***
	Please run the local server using python app.py to successfully utilize
	this testing suite
	"""
	def test_vehicle_info(self):

		r = requests.get('http://127.0.0.1:5000/vehicles/1235')
		# test if a valid GET request is fulfilled correctly
		self.assertEqual(r.status_code, 200)
		data = r.json()
		self.assertEqual(data['vin'], '1235AZ91XP')
		self.assertEqual(data['color'], "Forest Green")
		self.assertEqual(data['driveTrain'], "electric")
		self.assertEqual(data['doorCount'], 2)

		r = requests.get('http://127.0.0.1:5000/vehicles/1234')
		# test if a valid GET request is fulfilled correctly
		self.assertEqual(r.status_code, 200)
		data = r.json()
		self.assertEqual(data['vin'], '123123412412')
		self.assertEqual(data['color'], "Metallic Silver")
		self.assertEqual(data['driveTrain'], "v8")
		self.assertEqual(data['doorCount'], 4)

		#test if a bad GET request is fulfilled correctly
		r = requests.get('http://127.0.0.1:5000/vehicles/1230')
		#check if it is indeed a bad request (404)
		self.assertEqual(r.status_code, 404)

		#test if a POST request is denied
		r = requests.post('http://127.0.0.1:5000/vehicles/1234')
		#check if it is indeed a bad request (405: method not allowed)
		self.assertEqual(r.status_code, 405)

	def test_security(self):

		#test if a valid GET request is fulfilled correctly
		r = requests.get('http://127.0.0.1:5000/vehicles/1234/doors')
		self.assertEqual(r.status_code, 200)
		data = r.json()
		self.assertEqual(len(data), 4)
		#there is no way to check for booleans being returned right because they are being randomly generated
		#so we check that the exact 4 locations are present in the data being returned
		expected = ["frontLeft", "frontRight", "backRight", "backLeft"]
		for value in data:
			expected.remove(value['location'])
		self.assertEqual(len(expected), 0)

		#test if a valid GET request is fulfilled correctly
		r = requests.get('http://127.0.0.1:5000/vehicles/1235/doors')
		self.assertEqual(r.status_code, 200)
		data = r.json()
		self.assertEqual(len(data), 2)
		#there is no way to check for booleans being returned right because they are being randomly generated
		#check that the exact 4 locations are present in the data being returned
		expected = ["frontLeft", "frontRight"]
		for value in data:
			expected.remove(value['location'])
		self.assertEqual(len(expected), 0)

		#test if a bad GET request is fulfilled correctly
		r = requests.get('http://127.0.0.1:5000/vehicles/1230/doors')
		#check if it is indeed a bad request (404)
		self.assertEqual(r.status_code, 404)

		#test if a POST request is denied
		r = requests.post('http://127.0.0.1:5000/vehicles/1234/doors')
		#check if it is indeed a bad request (405: method not allowed)
		self.assertEqual(r.status_code, 405)

	def test_fuel_range(self):

		#test if a valid GET request is fulfilled correctly
		r = requests.get('http://127.0.0.1:5000/vehicles/1234/fuel')
		self.assertEqual(r.status_code, 200)
		data = r.json()
		#check type of data being returned
		self.assertEqual(type(data['percent']), float)

		#check value of data being returned
		self.assertLessEqual(data['percent'], 100.0)
		self.assertGreaterEqual(data['percent'], 0.0)

		#test if a bad request (since this is an electric car) is being fulfilled
		r = requests.get('http://127.0.0.1:5000/vehicles/1235/fuel')
		#check if it is indeed a bad request (500)
		self.assertEqual(r.status_code, 404)

		#test if a POST request is denied
		r = requests.post('http://127.0.0.1:5000/vehicles/1234/fuel')
		#check if it is indeed a bad request (405: method not allowed)
		self.assertEqual(r.status_code, 405)

	def test_battery_range(self):

		#test if a valid GET request is fulfilled correctly
		r = requests.get('http://127.0.0.1:5000/vehicles/1235/battery')
		self.assertEqual(r.status_code, 200)
		data = r.json()
		#check type of data being returned
		self.assertEqual(type(data['percent']), float)

		#check value of data being returned
		self.assertLessEqual(data['percent'], 100.0)
		self.assertGreaterEqual(data['percent'], 0.0)

		##test if a bad request (since this is an electric car) is being fulfilled
		r = requests.get('http://127.0.0.1:5000/vehicles/1234/battery')
		#check if it is indeed a bad request (500)
		self.assertEqual(r.status_code, 404)

		#test if a POST request is denied
		r = requests.post('http://127.0.0.1:5000/vehicles/1235/battery')
		#check if it is indeed a bad request (405: method not allowed)
		self.assertEqual(r.status_code, 405)

	def test_control_engine(self):

		#test if valid POST requests are being fulfilled correctly with intended outputs
		r = requests.post('http://127.0.0.1:5000/vehicles/1235/engine', json={"action" : "START"})
		self.assertEqual(r.status_code, 200)
		data = r.json()
		self.assertIn(data['status'], ['success', 'error'])

		#test if valid POST requests are being fulfilled correctly with intended outputs
		r = requests.post('http://127.0.0.1:5000/vehicles/1235/engine', json={"action" : "STOP"})
		self.assertEqual(r.status_code, 200)
		data = r.json()
		self.assertIn(data['status'], ['success', 'error'])

		#test if valid POST requests are being fulfilled correctly with intended outputs
		r = requests.post('http://127.0.0.1:5000/vehicles/1234/engine', json={"action" : "START"})
		self.assertEqual(r.status_code, 200)
		data = r.json()
		self.assertIn(data['status'], ['success', 'error'])

		#test if valid POST requests are being fulfilled correctly with intended outputs
		r = requests.post('http://127.0.0.1:5000/vehicles/1234/engine', json={"action" : "STOP"})
		self.assertEqual(r.status_code, 200)
		data = r.json()
		self.assertIn(data['status'], ['success', 'error'])

		#test if bad request with bad input is denied
		r = requests.post('http://127.0.0.1:5000/vehicles/1235/engine', json={"action" : "stop"})
		#test if 400 (malformed request) is being returned
		self.assertEqual(r.status_code, 400)
		#ensure error message is being passed through
		self.assertIn("Please provide a valid input for the action (START|STOP). stop is not a valid input", r.content)

		#test if bad request with bad input is denied
		r = requests.post('http://127.0.0.1:5000/vehicles/1235/engine', json={"action" : "invalid"})
		#test if 400 (malformed request) is being returned
		self.assertEqual(r.status_code, 400)
		#ensure error message is being passed through
		self.assertIn("Please provide a valid input for the action (START|STOP). invalid is not a valid input", r.content)

		#test if bad request with id that does not exist is fulfilled correctly
		r = requests.post('http://127.0.0.1:5000/vehicles/123/engine', json={"action" : "START"})
		self.assertEqual(r.status_code, 404)

		#test if a GET request is denied
		r = requests.get('http://127.0.0.1:5000/vehicles/1234/engine')
		#check if it is indeed a bad request (405: method not allowed)
		self.assertEqual(r.status_code, 405)

if __name__ == '__main__':
	unittest.main()