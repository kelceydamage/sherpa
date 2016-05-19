#!/usr/bin/env python

import optparse
from sherpa import Sherpa
from sherpa_helpers import debug_results, distribution, quartermaster
from perf import *

parser = optparse.OptionParser()
parser.add_option('-p', '--packages', dest='packages', help='specify the minimum number of packages to ship')
parser.add_option('-r', '--routes', dest='routes', help='specify the amount of routes to ship to')
parser.add_option('-c', '--parcels', dest='parcels', help='specify the amount of parcels to package')
parser.add_option('-s', '--shape', dest='shape', help='specify the shape of the parcels [use a 2 value tupple]')
(options, args) = parser.parse_args()
if not options.packages and not options.routes and not options.parcels:
	quit()
min_packages = int(options.packages)
routes = int(options.routes)
parcels = quartermaster(int(options.parcels), [4, 16])
order = []

# Actual code for using sherpa
sherpa = Sherpa(min_packages)
for parcel in parcels:
	order.append(sherpa.packer(parcel, routes))

routes, packages = distribution(order)
debug_results(
	sherpa,
	packages,
	routes,
	parcels
	)
perf_results()

