# sherpa
SHERPA is a routing engine for data storage.

sherpa.py contains a simple algorithm class that will determine where to send a parcel(data_object). It will devide up all your parcels into packages, and return a mapping of which route each package should be sent to. Sherpa is both consistent and uniform. It assignes packages to routes in a circular fashion.

## Testing Sherpa
To test Sherpa simple run the `sherpa_test.py` utility
```bash
* -h | help
* -p | specify the minimum number of packages to ship
* -r | specify the amount of routes to ship to
* -c | specify the amount of parcels to package
* -s | specify the shape of the parcels [use a 2 value tupple] <= OPTIONAL
```
