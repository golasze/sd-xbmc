#-*- coding:utf-8 -*-
import sys, time, os
import subprocess, signal
from daemon import Daemon
import rtmp
import multitask

class RTMPDaemon(Daemon):
	def run(self):
		while True:
			try:
				agent = rtmp.FlashServer()
				agent.start()
				multitask.run()
			except:
				sys.exit(0)		
			time.sleep(2)


'''class Daemon:
	def __init__(self, pid):
		if pid != "":
			self.daemon = RTMPDaemon(pid)
		else:
			exit()
		
	def start(self):
		self.daemon.start()
		
	def stop(self):
		self.daemon.stop()'''
		
if __name__ == "__main__":
	if len(sys.argv) == 3:
		pid_path = sys.argv[2]
		daemon = RTMPDaemon(pid_path)
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