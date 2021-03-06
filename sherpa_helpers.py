#!/usr/bin/env python
# Author: Kelcey Jamison-Damage
# Python: 2.66 +
# OS: CentOS | Other
# Portable: True
# License: Apache 2.0

# License
#-----------------------------------------------------------------------#
# Copyright [2016] [Kelcey Jamison-Damage]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-----------------------------------------------------------------------#

import string
import random

class Parcel(object):
        def __init__(self, params):
                super(Parcel, self).__init__()
		self.set_attributes(params)

        def set_attributes(self, params):
                for param in params:
                        setattr(self, param, params[param])

def debug_results(sherpa, packages, routes, parcels):
	print '\n\n'
	header = 'Sherpa routing results: {3} parcels in {0}[{1}] packages over {2} regions'.format(
		len(packages),
		sherpa.min_packages,
		len(routes.keys()),
		len(parcels)
		)
	print '-' * len(header)
	print header
	print '-' * len(header)
	total_parcels = sum([packages[x]['parcels'] for x in packages]) 
	for route in routes:
		print 'region: {0}'.format(route)
		print '\tpackages:\t\t{0}'.format(routes[route]['packages'].keys())
		for package in routes[route]['packages']:
			print '\tpackage:\t{0}\tparcels: {1}'.format(package, routes[route]['packages'][package])
		parcels = sum([routes[route]['packages'][x] for x in routes[route]['packages']])
		print '\t% total packages:\t{0}%'.format(round(float(len(routes[route]['packages'].keys())) / float(len(packages.keys())), 2) * 100)
		print '\t% total parcels:\t{0}%'.format(round(float(parcels) / float(total_parcels), 2) * 100)

def distribution(order):
	packages = {}
	routes = {}
	for parcel in order:
		if parcel.package in packages.keys():
			packages[parcel.package]['parcels'] += 1
			packages[parcel.package]['region'] = parcel.region
		else:
			packages[parcel.package] = {}
			packages[parcel.package]['parcels'] = 1	
			packages[parcel.package]['region'] = parcel.region
		if parcel.region in routes.keys():
			if parcel.package in routes[parcel.region]['packages']:
				routes[parcel.region]['packages'][parcel.package] += 1 
			else:
				routes[parcel.region]['packages'][parcel.package] = 1
		else:
			routes[parcel.region] = {}
			routes[parcel.region]['packages'] = {}
			routes[parcel.region]['packages'][parcel.package] = 1
	return routes, packages

def quartermaster(quantity, bounds=[4, 16]):
	def picker(upper, chars=string.ascii_lowercase):
		key = ''.join(random.choice(chars) for _ in range(2, int(upper)))
		return key
	items = []
	for n in range(1, quantity):
		items.append(Parcel({'key': picker(random.uniform(bounds[0], bounds[1]))}))
	return items
