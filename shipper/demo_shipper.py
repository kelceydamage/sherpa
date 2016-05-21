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
	sherpa = Sherpa(regions=nodes)
	shipment = Shipment(sherpa)
	shipment.assign(Parcel(params))
	shipment.assign(Parcel(params2))
	s = SocketClient()
	response = s.agent_query(shipment)
	
	print response.__dict__