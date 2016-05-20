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

import optparse
from libs.sherpa import Sherpa
from sherpa_helpers import debug_results, distribution, quartermaster
from libs.perf import perf_results

parser = optparse.OptionParser()
parser.add_option('-p', '--packages', dest='packages', help='specify the minimum number of packages to ship')
parser.add_option('-r', '--routes', dest='routes', help='specify the amount of routes to ship to')
parser.add_option('-c', '--parcels', dest='parcels', help='specify the amount of parcels to package')
parser.add_option('-s', '--shape', dest='shape', help='specify the shape of the parcels [use a 2 value tupple]')
(options, args) = parser.parse_args()
if not options.packages and not options.routes and not options.parcels:
	quit()
min_packages = int(options.packages)
routes = int(options.routes)
parcels = quartermaster(int(options.parcels), [4, 16])
order = []

# Actual code for using sherpa
sherpa = Sherpa(min_packages)
for parcel in parcels:
	order.append(sherpa.packer(parcel, routes))

routes, packages = distribution(order)
debug_results(
	sherpa,
	packages,
	routes,
	parcels
	)
perf_results()

