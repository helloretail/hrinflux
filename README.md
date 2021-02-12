# A class for sending metrics to the Hello Retail InfluxDB by UDP.

This package has a class, `Influx`, which can be used to ship ad-hoc metrics to
the Hello Retail InfluxDB server. It's sending the metrics by UDP, and has no
facility for authentication. This works withing Hello Retail, an the influxdb
is running in an isolated environment.

While the class can be configured to send metrics somewhere else, it's probably
not of great use outside of Hello Retail.

## Installation

```
pipenv install git+https://bitbucket.org/addwish/hrinflux.git#egg=hrinflux
```

## Usage

```
from hrinflux import Influx

# Make an instance. It's reusable and threadsafe:
influx = Influx()

# Send a metric with a value (4 in this case).
# Any additional keyword arguments are passed as tags.
influx.send('metric-name', 4, tag="tag-value", another_tag=42)
```
