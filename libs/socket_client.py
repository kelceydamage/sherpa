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
import socket
import time
import sys
import ssl
import json
from processing import Processing
from multiprocessing import current_process
from re import search
from sys import getsizeof
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from conf.nodes import nodes

# Class
#-----------------------------------------------------------------------#
class SocketClient(object):
	def __init__(self):
		pass

	def agent_query(self, shipment):
		current_process().daemon = False
		processing_object = Processing()
		self.q = processing_object.create_queue()
		response = {}
		p = processing_object.new_process(
			self._child_process,
			[processing_object, shipment]
			)
		response = []	
		for route in shipment.routes:
			queue_response = self.q.get(timeout=4)
			shipment.ack = queue_response
		p.join()
		return shipment

	def _child_process(self, processing_object, shipment):
		process_list = []

		def __lookup_address(route):
			return nodes[route]

		def __connect(self, address, packages):
			client_socket = socket.socket(
				socket.AF_INET,
				socket.SOCK_STREAM
				)
			tls_sock = ssl.wrap_socket(
				client_socket,
				cert_reqs=ssl.CERT_NONE,
				do_handshake_on_connect=False,
				ssl_version=ssl.PROTOCOL_TLSv1
				)
			tls_sock.settimeout(1)
			try:
				tls_sock.connect((address,9999))
			except Exception, e:
				pass
			try:
				tls_sock.send(packages)
			except Exception, e:
				pass
			return tls_sock

		def __spawn(self, route, packages):
			tls_sock = __connect(
				self,
				__lookup_address(route),
				packages
				)
			try:
				reply = json.loads(tls_sock.recv(10244))
			except Exception, e:
				pass
			self.q.put(reply)

		def __kill_proc(process_list):
			for process in process_list:
				process.join()

		for route in shipment.routes:
			p = processing_object.new_process(
				__spawn,
				[self, route, shipment.routes[route]]
				)
			process_list.append(p)
		__kill_proc(process_list)
