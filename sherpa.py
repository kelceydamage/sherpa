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

import hashlib
import math
from perf import time_it

# This is not production ready as I have not added any form of error handling. That will be coming soon.
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
