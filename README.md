# sherpa
SHERPA is a routing engine for data storage.

`sherpa.py` contains a simple algorithm class that will determine where to send a parcel(data_object). It will devide up all your parcels into packages, and return a mapping of which route each package should be sent to. Sherpa is both consistent and uniform. It assignes packages to routes in a circular fashion.

## Testing Sherpa
To test Sherpa simple run the `sherpa_test.py` utility
```bash
* -h | help
* -p | specify the minimum number of packages to ship
* -r | specify the amount of routes to ship to
* -c | specify the amount of parcels to package
* -s | specify the shape of the parcels [use a 2 value tupple] <= OPTIONAL
```
The ouput will show the routing distribution as well as the timings for each method execution. Currently `id_gen` is the slowest component (above nanoseconds in the low microseconds per execution). I am aware of this and will be looking for more efficient hash algorithm or library.

Sherpa will also choose the nearest prime number for the amount of packages you request, which is why the setting is called `min_packages`.

Thanks!

## output Sample
```bash
----------------------------------------------------------------------
Sherpa routing results: 9999 parcels in 23[20] packages over 7 regions
----------------------------------------------------------------------
region: 0
	packages:		    [0, 21, 14, 7]
	package:	0	    parcels: 424
	package:	21	    parcels: 446
	package:	14	    parcels: 461
	package:	7	    parcels: 477
	% total packages:	17.0%
	% total parcels:	18.0%
region: 1
	packages:		    [8, 1, 22, 15]
	package:	8	    parcels: 452
	package:	1	    parcels: 420
	package:	22	    parcels: 440
	package:	15	    parcels: 453
	% total packages:	17.0%
	% total parcels:	18.0%
region: 2
	packages:		    [16, 9, 2]
	package:	16	    parcels: 437
	package:	9	    parcels: 428
	package:	2	    parcels: 437
	% total packages:	13.0%
	% total parcels:	13.0%
region: 3
	packages:		    [17, 10, 3]
	package:	17	    parcels: 410
	package:	10	    parcels: 415
	package:	3	    parcels: 396
	% total packages:	13.0%
	% total parcels:	12.0%
region: 4
	packages:		    [18, 11, 4]
	package:	18	    parcels: 382
	package:	11	    parcels: 479
	package:	4	    parcels: 433
	% total packages:	13.0%
	% total parcels:	13.0%
region: 5
	packages:		    [19, 12, 5]
	package:	19	    parcels: 453
	package:	12	    parcels: 450
	package:	5	    parcels: 370
	% total packages:	13.0%
	% total parcels:	13.0%
region: 6
	packages:		    [20, 13, 6]
	package:	20	    parcels: 445
	package:	13	    parcels: 447
	package:	6	    parcels: 444
	% total packages:	13.0%
	% total parcels:	13.0%
method:	packer
	count:		9999
	average:	13.22	p (microseconds)
	min:		11.92	p (microseconds)
	max:		1.01	m (milliseconds)
	aggregate:	132.22	m (milliseconds)
method:	gen_primes
	count:		1
	average:	953.67	n (nanoseconds)
	min:		953.67	n (nanoseconds)
	max:		953.67	n (nanoseconds)
	aggregate:	953.67	n (nanoseconds)
method:	region_assignment
	count:		9999
	average:	377.79	n (nanoseconds)
	min:		0.0	    n (nanoseconds)
	max:		42.92	p (microseconds)
	aggregate:	3.78	m (milliseconds)
method:	id_gen
	count:		9999
	average:	1.74	p (microseconds)
	min:		953.67	n (nanoseconds)
	max:		24.8	p (microseconds)
	aggregate:	17.44	m (milliseconds)
method:	package_assignment
	count:		9999
	average:	412.29	n (nanoseconds)
	min:		0.0	    n (nanoseconds)
	max:		34.09	p (microseconds)
	aggregate:	4.12	m (milliseconds)
method:	__init__
	count:		1
	average:	37.19	p (microseconds)
	min:		37.19	p (microseconds)
	max:		37.19	p (microseconds)
```
