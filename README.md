# Smartcar Backend Coding Challenge

## Usage
To emulate the API I developed a running local Flask instance with the routes specified in the API spec. To run this
server run `python app.py` and navigate to `localhost:5000/<route>` using your web browser where \<route\> is one of the routes specified in the Smartcar API spec.

E.g. `localhost:5000/vehicles/1234` or `localhost:5000/vehicles/1234/fuel`

While this local server is running it is also possible to execute curl commands to perform GET and POST requests.

E.g. `curl localhost:5000/vehicles/1235 -X GET -H "Content-Type: application/json"` which returns the following output:

```json
{
    "color": "Forest Green",
    "doorCount": 2,
    "driveTrain": "electric",
    "vin": "1235AZ91XP"
}
```

## Testing
I approached the testing of this API in two ways.

1. Testing internal functions to ensure validity of input and output
2. Testing GET/POST requests to the routes built to ensure validity of input and output