import socket
import time

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
	
	def time(self, metric, **args):
		return _Timed(self, metric, **args)

class _Timed(object):
	def __init__(self, influx, metric, **args):
		self.influx = influx
		self.metric = metric
		self.args = args
	
	def __enter__(self):
		self.start = time.perf_counter()
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.influx.send(
			self.metric,
			time.perf_counter() - self.start,
			**self.args)
