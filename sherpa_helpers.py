#!/usr/bin/env python
# Author: Kelcey Jamison-Damage
# Python: 2.66 +
# OS: CentOS | Other
# Portable: True
# License: Apache 2.0

import string
import random

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
		print '\tpackages: {0}'.format(routes[route]['packages'].keys())
		for package in routes[route]['packages']:
			print '\tpackage: {0} - parcels: {1}'.format(package, routes[route]['packages'][package])
		parcels = sum([routes[route]['packages'][x] for x in routes[route]['packages']])
		print '\t% total packages: {0}%'.format(round(float(len(routes[route]['packages'].keys())) / float(len(packages.keys())), 2) * 100)
		print '\t% total parcels: {0}%'.format(round(float(parcels) / float(total_parcels), 2) * 100)

def distribution(order):
	packages = {}
	routes = {}
	for n in order:
		if n[0] in packages.keys():
			packages[n[0]]['parcels'] += 1
			packages[n[0]]['region'] = n[1]
		else:
			packages[n[0]] = {}
			packages[n[0]]['parcels'] = 1	
			packages[n[0]]['region'] = n[1] 
		if n[1] in routes.keys():
			if n[0] in routes[n[1]]['packages']:
				routes[n[1]]['packages'][n[0]] += 1 
			else:
				routes[n[1]]['packages'][n[0]] = 1
		else:
			routes[n[1]] = {}
			routes[n[1]]['packages'] = {}
			routes[n[1]]['packages'][n[0]] = 1
	return routes, packages

def quartermaster(quantity, bounds=[4, 16]):
	def picker(upper, chars=string.ascii_lowercase):
		key = ''.join(random.choice(chars) for _ in range(2, int(upper)))
		return key
	items = []
	for n in range(1, quantity):
		items.append(picker(random.uniform(bounds[0], bounds[1])))	
	return items
