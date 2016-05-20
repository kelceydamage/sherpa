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

import time
from functools import wraps

global perf
perf = {'count': 1}

def time_it(func):
        def _decorator(*args):
                start = time.time()
                response = func(*args)
                took = time.time() - start
		if func.__name__ not in perf.keys():
			perf[func.__name__] = {}
			perf[func.__name__]['raw'] = []
			perf[func.__name__]['raw'].append(took)
			perf[func.__name__]['count'] = 1
		else:
			perf[func.__name__]['raw'].append(took)
			perf[func.__name__]['count'] += 1
		perf['count'] += 1
                return response
        return wraps(func)(_decorator)

def perf_analysis():
	for method in perf:
		if method != 'count':
			perf[method]['average'] = float(sum(perf[method]['raw'])) / float(perf[method]['count'])
			perf[method]['aggregate'] = sum(perf[method]['raw'])
			perf[method]['min'] = min(perf[method]['raw'])
			perf[method]['max'] = max(perf[method]['raw'])

def number_sanitizer(number):
	number = number * 1000000000
	length = len(str(int(number)))
	if length >= 10:
		return 's (seconds)', round(number / 1000000000, 2)
	elif length >= 7 and length < 10:
		return 'm (milliseconds)', round(number / 1000000, 2)
	elif length >= 4 and length < 7:
		return 'p (microseconds)', round(number / 1000, 2)
	elif length < 4:
		return 'n (nanoseconds)', round(number, 2)

def perf_results():
	perf_analysis()
	for method in perf:
		if method != 'count':
			print 'method:\t{0}'.format(method)
			print '\tcount:\t\t{0}'.format(
				perf[method]['count']
				)
			print '\taverage:\t{0[1]}\t{0[0]}'.format(
				number_sanitizer(perf[method]['average'])
				)
			print '\tmin:\t\t{0[1]}\t{0[0]}'.format(
				number_sanitizer(perf[method]['min'])
				)
			print '\tmax:\t\t{0[1]}\t{0[0]}'.format(
				number_sanitizer(perf[method]['max'])
				)
			print '\taggregate:\t{0[1]}\t{0[0]}'.format(
				number_sanitizer(perf[method]['aggregate'])
				)
