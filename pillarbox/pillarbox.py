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
# Imports
#-----------------------------------------------------------------------#
import SocketServer
import subprocess
import socket
import pickle
import ssl
import json
import os
import re
import bz2
from libs.data_types import *

# Init Variables
#-----------------------------------------------------------------------#
ar_methods = {'test': 'test'}

# Classes
#-----------------------------------------------------------------------#
class LocalTasks(object):
	methods = ar_methods

	@classmethod
	def run_task(cls, method):
		def gather_data(cls, boolean, method):
			proc = subprocess.Popen(
				cls.methods[method].function,
				stdout=subprocess.PIPE,
				stdin=subprocess.PIPE,
				shell=boolean
				)
			return cls.methods[method](proc.stdout.read()).format()
		if method in cls.methods:
				return gather_data(cls, False, method)
		else:
			return 'Invalid Method'

	@classmethod
	def unpack(cls, container):
		for parcel in container.contents:
			print '-' * 20
			print 'delivery to: {0}, delivery_size: {1} bytes, container_size: {2} bytes, compressed_size: {3}'.format(
				container.address, 
				(container.__sizeof__() + container.__dict__.__sizeof__()), 
				container.contents.__sizeof__(),
				container.csize
				)
			print '-' * 20
			print 'parcel_key: {0}, parcel_id: {1}'.format(parcel.key, parcel.id)
			print 'parcel_region: {0}, parcel_package: {1}'.format(parcel.region, parcel.package)
			print 'parcel_action: {0}, parcel_size: {1} bytes'.format(
				parcel.action, 
				(parcel.__sizeof__() + parcel.__dict__.__sizeof__())
				)
		delivery = container.unpack()
		rc = 0
		for parcel in delivery:
			if parcel.action == 'retrieve':
				container.append(Parcel({'requested': 'retrieve', 'receiver': container.address, 'meta': 'this would be the data object requested'}))
				rc += 1		
		container.append(Parcel({'requested': 'store', 'receiver': container.address, 'parcels': len(delivery) - rc}))
		return container

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	daemon_threads = True
	allow_reuse_address = True

	def server_bind(self):
		SocketServer.TCPServer.server_bind(self)
		self.socket = ssl.wrap_socket(
			self.socket,
			server_side=True,
			certfile="ssl/server_crt.pem",
			keyfile='ssl/server_key.pem',
			do_handshake_on_connect=False,
			ssl_version=ssl.PROTOCOL_TLSv1
			)

	def get_request(self):
		(socket, addr) = SocketServer.TCPServer.get_request(self)
		socket.do_handshake()

		return (socket, addr)

class TCPHandler(SocketServer.BaseRequestHandler):
	white_list = [
		'127.0.0.1',
		'10.',
		'172.31.'
		]
	api_version = {
		'version_name': 'Applewood',
		'version_number': '1.1.1'
		}

	def handle(self):
		compressed = self.request.recv(1024).strip()
		self.container = bz2.decompress(compressed)
		for entry in self.white_list:
			if re.search(entry, self.client_address[0]):
				match_token = True
				break
		else:
			match_token = False
		if match_token == True:
			self.container = pickle.loads(self.container)
			container = LocalTasks.unpack(self.container)
			compressed = bz2.compress(pickle.dumps(container))
			self.request.sendall(compressed)
		else:
			compressed = bz2.compress(pickle.dumps({'error': 'Connection Refused'}))
			self.request.sendall(compressed)

# Functions
#-----------------------------------------------------------------------#
def write_pid_file():
		pid = str(os.getpid())
		f = open('/var/run/pillarbox.pid', 'w')
		f.write(pid)
		f.close()

# Main
#-----------------------------------------------------------------------#
if __name__ == '__main__':
		write_pid_file()
		HOST = socket.gethostbyname(socket.gethostname())
		PORT = 9999
		server = SimpleServer(('', PORT), TCPHandler)
		server.serve_forever()
