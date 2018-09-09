import logging
import os
import socket
import json

sources = {}

def serve(configpath):
	if "/" in configpath and not configpath.startswith("./"):
		botname = "_" + configpath.split("/")[-2]
	else:
		botname = ""
	sockpath = "/tmp/secretlounge" + botname

	ssock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	if os.path.exists(sockpath): os.remove(sockpath)
	ssock.bind(sockpath)
	ssock.listen()

	logging.info("Statistic collector ready on %s", sockpath)
	while True:
		sock, _ = ssock.accept()

		while True:
			try:
				data = sock.recv(512).strip()
			except:
				data = b""
			if not data: break

			res = {}
			for name, callback in sources.items():
				try:
					res[name] = callback()
				except Exception as e:
					logging.exception("Exception in stat callback")

			try:
				sock.send(json.dumps(res).encode('utf-8'))
			except:
				break
		sock.close()

	ssock.close()

def register_source(name, callback):
	sources[name] = callback

def countable_source(name):
	value = 0
	def push(n):
		nonlocal value
		value += n
	def callback():
		nonlocal value
		ret = value
		value = 0
		return ret
	register_source(name, callback)
	return push

def settable_source(name):
	value = 0
	def set(n):
		nonlocal value
		value = n
	def callback():
		nonlocal value
		return value
	register_source(name, callback)
	return set