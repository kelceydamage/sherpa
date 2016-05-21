##!/usr/bin/env python
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
# Imports
#-----------------------------------------------------------------------#
import hashlib
import time

# Classes
#-----------------------------------------------------------------------#
class Parcel(object):
	def __init__(self, params):
		super(Parcel, self).__init__()
		self.set_attributes(params)
	
	def set_attributes(self, params):
		for param in params:
			setattr(self, param, params[param])

class Container(object):
	def __init__(self, address):
		super(Container, self).__init__()
		self.contents = []
		self.address = address

	def append(self, parcel):
		self.contents.append(parcel)

	def unpack(self):
		return self.contents
	
class Shipment(object):
	def __init__(self, sherpa):
		super(Shipment, self).__init__()
		self.sherpa = sherpa
		self.manifest = {}
		self.id = hashlib.md5(str(time.time())).hexdigest()

	def assign(self, parcel):
		self.sort(self.calculate_route(parcel))
	
	def calculate_route(self, parcel):
		return self.sherpa.packer(parcel)

	def sort(self, parcel):
		if parcel.region in self.manifest.keys():
			self.manifest[parcel.region].append(parcel)
		else:
			self.manifest[parcel.region] = Container(
				self.sherpa.regions[parcel.region]
				)
			self.manifest[parcel.region].append(parcel)

	def routes(self):
		return self.manifest.keys()