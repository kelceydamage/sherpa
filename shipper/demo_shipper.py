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
from libs.data_types import *
from conf.nodes import nodes

# Init Variables
#-----------------------------------------------------------------------#
params = {
	'key': 'testobj1',
	'value': 'testvalue1',
	'action': 'store'
	}

params2 = {
	'key': 'testobj2',
	'action': 'retrieve'
	}

# Main
#-----------------------------------------------------------------------#
if __name__ == '__main__':
	# Instantiate Sherp and provide it with the node registry
	sherpa = Sherpa(regions=nodes)

	# Create a shipment assign sherpa to it
	shipment = Shipment(sherpa)

	# Add some parcels to the shipment
	shipment.assign(Parcel(params))
	shipment.assign(Parcel(params2))

	# instantiate the Pillar Box client
	s = SocketClient()

	# Send the shipment and receive it's response
	response = s.agent_query(shipment)
	
	# Unpack all the containers listed in the shipments manifest
	for container in response.manifest:
		# Unpacking a container removes all of it's parcels so it can be
		# reused and is totally optional
		for parcel in response.manifest[container].unpack():
			# Examine all the parcel contents
			print parcel.get_contents()
