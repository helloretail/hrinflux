import socket
import time
from types import TracebackType
from typing import Any, Dict, Optional, Type
import sys

class Influx(object):
	def __init__(self, host: str = 'influxdb.addwish.com', port: int = 4444):
		self.addr = host, int(port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	def send(self, name: str, value: Any, __debug: bool = False, **args: str) -> None:
		msg = "{}{} value={}".format(
			name,
			"".join(",{}={}".format(k, v) for k, v in args.items()),
			str(value))
		if __debug:
			print(f"[hrinflux] sending: {msg}", file=sys.stderr)
		self.sock.sendto(msg.encode(), self.addr)
	
	def time(self, metric: str, __debug: bool = False, **args: str) -> '_Timed':
		return _Timed(self, metric, **args)

class _Timed(object):
	def __init__(self, influx: Influx, metric: str, __debug: bool = False, **args: str):
		self.influx = influx
		self.metric = metric
		self.args = args
		self.debug = __debug
	
	def __enter__(self) -> None:
		self.start = time.perf_counter()
	
	def __exit__(
			self,
			exc_type: Optional[Type[BaseException]],
			exc_val: Optional[BaseException],
			exc_tb: Optional[TracebackType]) -> None:
		self.influx.send(
			self.metric,
			time.perf_counter() - self.start,
			__debug=self.debug,
			**self.args)
