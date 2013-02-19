#-*- coding:utf-8 -*-
import sys, time, os
import subprocess, signal
from daemon import Daemon
import traceback

conf = {}


class FFMPEGencoder(Daemon):
	def run(self):
		print 'tutaj!'
		while True:
			self.encoding()
			time.sleep(2)

	def encoding(self):
		try:
			v_opts = "-b %s -s %s" % (str(int(conf['v_bitrate'])*4000), conf['v_dimension']) 
			a_opts = "-ab %s -ac 1 -ar 44100" % (str(int(conf['a_bitrate'])*1000))
			rtmp_link = "rtmp://127.0.0.1/stream/live"
			args = "%s -re -i %s -i %s %s %s -f flv \"%s\"" % (conf['ffmpeg'], conf['v_url'], conf['a_url'], v_opts, a_opts, rtmp_link)
			print str(args)
			p = subprocess.Popen(args, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			while True:
				line = p.stderr.readline()
				if 'Press [q] to stop, [?] for help' in line:
					f = open(conf['pid_file'][:-4] + '.tmp', "w")
					f.write('encoding')
					f.close()
					break
				#sys.stdout.flush()
		except:
			traceback.print_exc()
			sys.exit(0)
			

class Configuration:
	def __init__(self, pidfile):
		self.confile = pidfile[:-4] + '.conf'
		self.ffmpeg = ''
		self.v_url = ''
		self.a_url = ''
		self.v_bitrate = ''
		self.a_bitrate = ''
		self.v_dimension = ''
		self.a_sampling_rate = ''
		self.tmp_file = ''
		
	def loadFile(self):
		fileOpen = open(self.confile, 'r')
		while True:
			line = fileOpen.readline()
			if not line:
				break
			if 'ffmpeg' in line.strip():
				self.ffmpeg = line.strip().split(' ')[1]
			if 'v_url' in line.strip():
				self.v_url = line.strip().split(' ')[1]
			if 'a_url' in line.strip():
				self.a_url = line.strip().split(' ')[1]
			if 'v_bitrate' in line.strip():
				self.v_bitrate = line.strip().split(' ')[1]
			if 'a_bitrate' in line.strip():
				self.a_bitrate = line.strip().split(' ')[1]
			if 'v_dimension' in line.strip():
				self.v_dimension = line.strip().split(' ')[1]
			if 'a_sampling_rate' in line.strip():
				self.a_sampling_rate = line.strip().split(' ')[1]
			if 'tmp_file' in line.strip():
				self.tmp_file = line.strip().split(' ')[1]
		return { 
			'ffmpeg' : self.ffmpeg, 
			'v_url': self.v_url,
			'a_url': self.a_url,
			'v_bitrate': self.v_bitrate,
			'a_bitrate': self.a_bitrate,
			'v_dimension': self.v_dimension,
			'a_sampling_rate': self.a_sampling_rate,
			'tmp_file': self.tmp_file
		}

		
if __name__ == "__main__":
	if len(sys.argv) == 3:
		pid_path = sys.argv[2]
		#print pid_path
		try:
			conf = Configuration(pid_path).loadFile()
		except:
			traceback.print_exc()
			sys.exit(0)
		daemon = FFMPEGencoder(pid_path)
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)