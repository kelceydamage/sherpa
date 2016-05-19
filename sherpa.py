#!/usr/bin/env python
# Author: Kelcey Jamison-Damage
# Python: 2.66 +
# OS: CentOS | Other
# Portable: True
# License: Apache 2.0

import hashlib
import math
from perf import time_it

class Sherpa(object):
	@time_it
	def __init__(self, packages=30):
		super(Sherpa, self).__init__()
		self.min_packages = packages
		self.packages = self.gen_primes(packages).next()		

	@time_it
	def gen_primes(self, packages):
		d = {}
		q = 2
		while True:
			if q not in d:
				if q >= packages:
					yield q
				d[q * q] = [q]
			else:
				for p in d[q]:
					d.setdefault(p + q, []).append(p)
				del d[q]
			q += 1
		
	def director(self):
		pass

	@time_it
	def packer(self, parcel, routes):
		@time_it	
		def id_gen(parcel):
			id = int(hashlib.sha1(parcel).hexdigest(), 16)
			return id
		@time_it
		def package_assignment(id):
			package = id % self.packages
			return package
		@time_it
		def region_assignment(package, routes):
			region = package % routes
			return region
		id = id_gen(parcel)
		package = package_assignment(id)
		region = region_assignment(package, routes)
		return int(package), int(region)
