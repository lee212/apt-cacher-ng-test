import sys
import paramiko
from pprint import pprint
import time
import itertools
from multiprocessing import Pool, Process
import json

def read_grepped_file(filename):
	with open (filename) as f:
		lines = f.read().splitlines()
	new_lines = []
	for line in lines:
		#lines = [ x[x.find(":") + 1: ].strip() for x in lines ]
		tmp = line[line.find(":") + 1:].strip()
		if tmp.startswith('"') and tmp.endswith('"'):
			tmp = tmp[1:-1]
		elif tmp.startswith('"') and tmp.endswith(','):
			tmp = tmp[1:-2]
		new_lines.append(tmp)

	return new_lines

def ssh_call(server, username, cmd_to_execute):
	#k = paramiko.RSAKey.from_private_key_file("/home/ubuntu/.ssh/id_rsa")
	#cmd_to_execute = ["ifconfig"]
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(server, username=username, look_for_keys=False)# pkey = k)
	#ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)

	res = {}

	line = 0
	for command in cmd_to_execute:
		print "Executing {}".format( command )
		command = "echo '%s' > ssh_cmd.sh;sudo sh ssh_cmd.sh"%command
		start_time = time.time()
		stdin , stdout, stderr = ssh.exec_command(command)
		elapsed_time = time.time() - start_time
		res[str(line)] = {
				'time': elapsed_time,
				'stdout': stdout.read(),
				'stderr': stderr.read()
			}
	ssh.close()
	return res

def multi_call(a_b_c):
	return ssh_call(*a_b_c)

def save_file(name, data):
	with open(name, 'w') as f:
		json.dump(data, f, indent=4, sort_keys=True)
	
if __name__ == "__main__":
	cmds = read_grepped_file(sys.argv[1])
	servers = sys.argv[2].split(",")
	cnt = 0
	if len(servers) > 1:
		pool = Pool(processes=len(servers))
		start_time = time.time()
		ret = pool.map(multi_call, itertools.izip(servers, itertools.repeat(sys.argv[3]), itertools.repeat(cmds)))
		end = time.time() - start_time
		save_file(".".join(sys.argv[1:2]), ret)
		print end
			
	else:
		res = ssh_call(sys.argv[2], sys.argv[3], cmds)
		save_file(".".join(sys.argv[1:2]), res)

