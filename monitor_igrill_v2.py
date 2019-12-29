import json
import time

from igrill import IGrillV2Peripheral
from prometheus_client import Gauge, push_to_gateway, CollectorRegistry
ADDRESSES = []
# DATA_FILE = '/tmp/igrill.json'

# MQTT Section
# client = mqtt.Client()
# client.connect(mqtt_server, 1883, 60)
# client.loop_start()

registry = CollectorRegistry()
probe_one = Gauge('bbq_probe_one_temp', 'Temp of probe one', registry=registry)
probe_two = Gauge('bbq_probe_two_temp', 'Temp of probe two', registry=registry)
probe_three = Gauge('bbq_probe_three_temp', 'Temp of probe three', registry=registry)
probe_four = Gauge('bbq_probe_four_temp', 'Temp of probe four', registry=registry)

probes = [ probe_one, probe_two, probe_three, probe_four ]
battery = Gauge('bbq_battery', 'Battery of the iGrill', registry=registry)

if __name__ == '__main__':
    periph = IGrillV2Peripheral('70:91:8f:0c:24:cf')
    while True:

        temperature=periph.read_temperature()
        # Probe 1
        if temperature[1] != 63536.0:
            print("bbq/probe1", temperature[1])
            probe_one.set(temperature[1])
      
        # Probe 2
        if temperature[2] != 63536.0:
            print("bbq/probe2", temperature[2])
            probe_two.set(temperature[2])

        # Probe 3
        if temperature[3] != 63536.0:
            print("bbq/probe3", temperature[3])
            probe_three.set(temperature[3])
      
        # Probe 4
        if temperature[4] != 63536.0:
            print("bbq/probe4", temperature[4])
            probe_four.set(temperature[4])
      
        print("bbq/battery", periph.read_battery())
        battery.set(periph.read_battery())
        push_to_gateway('https://grillitup.withfocus.com', job="igrill", registry=registry )
      
        time.sleep(5)
