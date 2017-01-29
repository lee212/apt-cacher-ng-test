import re
import sys
import json
from pprint import pprint

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

if __name__ == "__main__":
	with open(sys.argv[1]) as f:
		lines=f.read()
		data = json.loads(lines)

	tot = 0
	for k, v in data.iteritems():
		stdout = v['stdout']
		m = re.search('Fetched.*', stdout)
		if m:
			fetched=m.group()
			m2 = re.search('\(.*\)', fetched)
			tmp = m2.group()[1:-1]
			sp_unit = tmp.split()
			s = sp_unit[0].replace(",","")
			m_k_b = sp_unit[1]
			if s == "0":
				continue
			if m_k_b[0] == "k":
				s = float(s) / 1024
			tot = mean([tot, float(s)])
		else:
			pass#print k

	print tot
		
