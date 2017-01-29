
#centos_1=(a,b)
#centos_4=([a,b,c,d],[e,f,g,h])

ubuntu_1=10.0.10.90
ubuntu_4=10.0.10.94,10.0.10.92,10.0.10.99,10.0.10.93
ubuntu_1_n=10.0.10.91
ubuntu_4_n=10.0.10.95,10.0.10.97,10.0.10.96,10.0.10.98

ubuntu_8=
ubuntu_8_n=
#for i in ${ubuntu_4//,/ }
for i in `echo 10.0.10.{137..144}`
do
msg='Acquire::http::proxy \"http://10.0.10.72:3142\";'
ssh -o StrictHostKeyChecking=no ubuntu@$i "echo \"echo '"$msg"' > /etc/apt/apt.conf.d/02proxy\" > ssh_cmd.sh;sudo bash ssh_cmd.sh"
python cache.py apt.install.from.docker $i ubuntu &
done

#for i in ${ubuntu_4_n//,/ }
for i in `echo 10.0.10.{145..152}`
do
python cache.py apt.install.from.docker $i ubuntu &
done

array1=(one two three)
array2=(four five six)
#ubuntu_4=${array1[*]},${array2[*]}
#for i in $ubuntu_4
#do IFS=","
#set -- $i
#echo $1,$2
#done
