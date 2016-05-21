# Sherpa
SHERPA is a routing engine for data storage.

`sherpa.py` contains a simple algorithm class that will determine where to send a parcel(data_object). It will divide up all your parcels into packages, and return a mapping of which route each package should be sent to. Sherpa is both consistent and uniform. It assignes packages to routes in a circular fashion. This means Sherpa forgoes the need for a hashmap/lookup table as it can compute the location of your object instantly. Simply feed the Sherpa the the string representation of your object's name/key/id and it will tell you where it is/will be stored. Simple!

### Testing Sherpa
To test Sherpa simply run the `sherpa_test.py` utility
```bash
* -h | help
* -p | specify the minimum number of packages to ship
* -r | specify the amount of routes to ship to
* -c | specify the amount of parcels to package
* -s | specify the shape of the parcels [use a 2 value tupple] <= OPTIONAL
```
Example: `./sherpa_test.py -p 20 -r 6 -c 4000`

The ouput will show the routing distribution as well as the timings for each method execution. Currently `id_gen` is the slowest component (above nanoseconds in the low microseconds per execution). I am aware of this and will be looking for more efficient hash algorithm or library.

Sherpa will also choose the nearest prime number for the amount of packages you request, which is why the init arg is called `min_packages`.

### Relationships
Sherpa `routes` lead to `pillarboxes` where `containers` are delivered or picked up. Each `container` will contain one or many `parcels`. A `parcel` is an object with properties as simple as a `key` and a `value`, or a complex as you want to make it. `parcels` also contain certain base attributes for routing and transmition.

It is completely possible to put any type of source data into a `parcel`. Once `parcels` are ready to be shipped, they are assigned to a `shipment` and Sherpa places them in the correct `container` as per the shipping manifest. Each container is then shipped to a waiting `pillarbox`. Retrieving objects is a similar process and only requires the `parcel` identifier(key/id). Sherpa will then locate your parcel and retrieve it for you.

### Pillar Box Demo
Basic functionality is available now for Pillar Box. To test it out you can launch Pillar Box by one of the following methods:
* run `pillarbox/pillarbox.sh start <PATH TO PILLARBOX.PY>` or `pillarbox/pillarbox.sh start .`
* run `pillarbox/pillarbox.py`

Using the first method will daemonize Pillar Box and register it's PID

Once Pillar Box is running execute `shipper/demo-shipper.py` to see it in action.

You can install pillar box on multiple servers. Make sure to update the `conf/nodes.py` file to register each of your servers hostnames.

### Making Use Of Sherpa In Its Current Shape
Currently Sherpa is only in a demo state, but it can be extended for actual use. `shipper/demo-shipper.py` can be used as an example for how to interact with Sherpa in order to send and receive packages.

To control what happens to a container once it arrives at a Pillar Box can be controlled by modifying and extending the `LocalTasks` class in `pillarbox/pillierbox.py` for an example you can look at the current `.unpack()` method which prints container and parcel details before sending a receipt container back to the sender.

Pillar Box sample output:
```bash
--------------------
delivery to: localhost, delivery_size: 280 bytes, container_size: 72 bytes, compressed_size: 291
--------------------
parcel_key: testobj1, parcel_id: 1293294176801013002297190993245407132226136516837
parcel_region: 0, parcel_package: 0
parcel_action: store, parcel_size: 1048 bytes
--------------------
delivery to: localhost, delivery_size: 280 bytes, container_size: 72 bytes, compressed_size: 282
--------------------
parcel_key: testobj2, parcel_id: 547321951627324108975181015563125624335359999533
parcel_region: 1, parcel_package: 17
parcel_action: retrieve, parcel_size: 280 bytes
```

Demo Shipper sample output:
```bash
{'requested': 'store', 'parcels': 1, 'receiver': 'localhost'}
{'requested': 'retrieve', 'meta': 'this would be the data object requested', 'receiver': 'localhost'}
{'requested': 'store', 'parcels': 0, 'receiver': 'localhost'}
```

### Comming Soon

* **Pillar Box** definitions and optional Piller Box server code. The Pillar Box can act as a data node or an interface to other database technologies. For example this means you could use Pillar Boxes to create a sharded MySQL backend, or to connect multiple <popular noSQL databases> into a cluster giving an increase in distributed read/write performance.
* **Parity Routes** which will allow replication of data using integer position shifting.
* **Writeback Replication** which will create aynchronous object duplication
* **Other Cool Stuff**

Thanks!

### output Sample
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
