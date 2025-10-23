import socket
import time
from types import TracebackType
from typing import Dict, Optional, Type, Union, Callable
import sys

class Influx(object):
	def __init__(
			self,
			host: str = 'influxdb.addwish.com',
			port: int = 4444,
			logger: Optional[Callable[[str], None]] = None):
		self.addr = host, int(port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.logger: Callable[[str], None] = Influx._default_logger
		if logger:
			self.logger = logger
	
	@staticmethod
	def _default_logger(msg: str) -> None:
		print(msg, file=sys.stderr)
	
	def _log(self, msg: str) -> None:
		self.logger(f"[hrinflux] {msg}")
	
	def send(self, name: str, value: Union[int, float], **args: str) -> str:
		msg = "{}{} value={}".format(
			name,
			"".join(",{}={}".format(k, v) for k, v in args.items()),
			str(value))

		try:
			self.sock.sendto(msg.encode(), self.addr)
		except Exception as e:
			self._log(f"Ignoring an exception: {e}. (Metric will not be sent)")
		
		return msg
	
	def close(self) -> None:
		"""Close the socket connection."""
		if hasattr(self, 'sock') and self.sock:
			try:
				self.sock.close()
			except OSError:
				pass # Socket already closed
	
	def time(self, metric: str, **args: str) -> '_Timed':
		return _Timed(self, metric, **args)

class _Timed(object):
	def __init__(self, influx: Influx, metric: str, **args: str):
		self.influx = influx
		self.metric = metric
		self.args = args
	
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
			**self.args)
