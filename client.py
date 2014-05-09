from subprocess import Popen, PIPE
from time import sleep
from nbstreamreader import NonBlockingStreamReader as NBSR

# run the shell as a subprocess:
p = Popen(['python', 'shell.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE)

nbsr = NBSR(p.stdout)

# issue command:
p.stdin.write('command\n')

# let the shell output the result:
sleep(0.1)

#get the output
while True:
	output = nbsr.readline(0.1)
	if not output:
		print '[No more data]'
		break
	print output


