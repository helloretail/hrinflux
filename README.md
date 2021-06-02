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

### Sending general metrics
```
from hrinflux import Influx

# Make an instance. It's reusable and threadsafe:
influx = Influx()

# Send a metric with a value (4 in this case).
# Any additional keyword arguments are passed as tags.
influx.send('metric-name', 4, tag="tag-value", another_tag=42)
```

### Timing code blocks

The `time` method of an instance returns a context manager, which will submit
the time taken in seconds once the block ends:

```
from hrinflux import Influx

influx = Influx()

with influx.time("metric-name", tag_name="optional-tag-value"):
    some_expensive_calculation()
    some_more()
# A metric will be sent to `metric-name` with a value of how many seconds
# it took to run the block.
```