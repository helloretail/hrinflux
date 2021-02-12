import socket

class Influx(object):
	def __init__(self, host='influxdb.addwish.com', port=4444):
		self.addr = host, int(port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	def send(self, name, value, **args):
		self.sock.sendto(
			("{}{} value={}".format(
				name,
				"".join(",{}={}".format(k, v) for k, v in args.items()),
				str(value))).encode(),
			self.addr)

