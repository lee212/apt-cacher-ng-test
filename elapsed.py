import re
import sys
import json
from pprint import pprint

with open(sys.argv[1]) as f:
	lines=f.read()
	data = json.loads(lines)

for k, v in data.iteritems():
	stdout = v['stdout']
	m = re.search('Fetched.*', stdout)
	if m:
		pprint(m.group())
	else:
		pass#print k
	
