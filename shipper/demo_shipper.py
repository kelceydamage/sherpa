#!/usr/bin/env python
# Author: Kelcey Jamison-Damage
# Python: 2.66 +
# OS: CentOS | Other
# Portable: True
# License: Apache 2.0

#-----------------------------------------------------------------------#
# Copyright [2015] [Kelcey Jamison-Damage]

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
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from libs.socket_client import SocketClient 
from libs.sherpa import Sherpa 
from conf.nodes import nodes
import hashlib
import time

# Init Variables
#-----------------------------------------------------------------------#
params = {
	'key': 'testobj1',
        'value': 'testvalue1'
        }

# Classes
#-----------------------------------------------------------------------#
class Parcel(object):
	def __init__(self, params):
		super(Parcel, self).__init__()
		self.set_attributes(params)
	
	def set_attributes(self, params):
		for param in params:
			setattr(self, param, params[param])
	
class Shipment(object):
	def __init__(self):
		super(Shipment, self).__init__()
		self.manifest = {}
		self.id = hashlib.md5(str(time.time())).hexdigest()

	def assign(self, parcel):
		self.sort(self.calculate_route(parcel))
	
	def calculate_route(self, parcel):
		return sherpa.packer(parcel)

	def sort(self, parcel):
		if parcel.region in self.manifest.keys():
			self.manifest[parcel.region].append(parcel)
		else:
			self.manifest[parcel.region] = Container(nodes[parcel.region])
			self.manifest[parcel.region].append(parcel)

	def routes(self):
		return self.manifest.keys()

class Container(object):
        def __init__(self, address):
                super(Container, self).__init__()
		self.container = []
		self.address = address

	def append(self, parcel):
		self.container.append(parcel)

	def unpack(self):
		return self.container

# Main
#-----------------------------------------------------------------------#
if __name__ == '__main__':
	sherpa = Sherpa(routes=len(nodes))
	parcel = Parcel(params)	
	shipment = Shipment()
	shipment.assign(parcel)
	s = SocketClient()
	response = s.agent_query(shipment)
	
	print response.__dict__
