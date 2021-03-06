# Smartcar Backend Coding Challenge

## Usage
To emulate the Smartcar API, I developed a local Flask instance with the routes specified in the API spec that runs on localhost. To run this server run `python app.py` and navigate to `localhost:5000/<route>` using your web browser where &lt;route&gt; is one of the routes specified in the Smartcar API spec.

E.g. `localhost:5000/vehicles/1234` or `localhost:5000/vehicles/1234/fuel`

While this local server is running, it is also possible to execute curl commands to perform GET and POST requests.

E.g. `curl localhost:5000/vehicles/1235 -X GET -H "Content-Type: application/json"` which returns the following response:

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

### Testing internal functions to ensure validity of input and output

This involved testing the functions in `smartcar.py` to ensure that they are parsing input correctly and are returning the right outputs in the intended formats.

### Testing GET/POST requests to the routes built to ensure validity of input and output

This involved testing the routing logic built in `app.py` to ensure that the routes have been developed properly and that the API is taking in the right inputs and providing the right outputs in the intended formats. This was done to ensure that client requests to the Smartcar API exhibit the intended behaviour and have the right responses if they are valid.