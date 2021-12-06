import socket
import time
from types import TracebackType
from typing import Any, Dict, Optional, Type

class Influx(object):
	def __init__(self, host: str = 'influxdb.addwish.com', port: int = 4444):
		self.addr = host, int(port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	def send(self, name: str, value: Any, **args: Dict[str, str]) -> None:
		self.sock.sendto(
			("{}{} value={}".format(
				name,
				"".join(",{}={}".format(k, v) for k, v in args.items()),
				str(value))).encode(),
			self.addr)
	
	def time(self, metric: str, **args: Dict[str, str]) -> '_Timed':
		return _Timed(self, metric, **args)

class _Timed(object):
	def __init__(self, influx: Influx, metric: str, **args: Dict[str, str]):
		self.influx = influx
		self.metric = metric
		self.args = args
	
	def __enter__(self) -> None:
		self.start = time.perf_counter()
	
	def __exit__(self,
			exc_type: Optional[Type[BaseException]],
			exc_val: Optional[BaseException],
			exc_tb: Optional[TracebackType]) -> None:
		self.influx.send(
			self.metric,
			time.perf_counter() - self.start,
			**self.args)
