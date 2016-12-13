import psutil
import time
from liota.dccs.dcc import DataCenterComponent
from liota.entities.metrics.registered_metric import RegisteredMetric
from liota.entities.metrics.metric import Metric
from liota.entities.registered_entity import RegisteredEntity


class OpenGateDmmDCC(DataCenterComponent):

    def __init__(self, comms):
        super(OpenGateDmmDCC, self).__init__(comms)
        self.comms = comms

    def register(self, entity_obj):
        print("Registering {0} on OpenGateDCC".format(entity_obj.name))

        if isinstance(entity_obj, Metric):
            return RegisteredMetric(entity_obj, self, None)
        else:
            return RegisteredEntity(entity_obj, self, None)

    def create_relationship(self, reg_entity_parent, reg_entity_child):
        reg_entity_child.parent = reg_entity_parent

    def _format_data(self, reg_metric):

        # Checking if there is any data collected to publish
        size_values = reg_metric.values.qsize()
        if size_values == 0:
            return

        # Creating the JSON to send wit the information collected
        # This part of the JSON is common

        message = '''{"version": "1.0","event": {"id": "","device": {"id": "d5130252-6ea5-5c71-910b-759c66dc6d8d","name": "liota_test",
        "description": "Testing Liota", "location" : { "timestamp": "%d", "coordinates": {"latitude": "40.41675",
        "longitude": "-3.7028"}},''' % int(round(time.time() * 1000))

        # If I get a CPU Usage Metric, building a CPU Usage JSON
        if reg_metric.ref_entity.name == "EdgeSystem.CPU_Utilization":
            for _ in range(size_values):
                v = reg_metric.values.get(block=True)  # Block if necessary until an item is available
                if v is not None:
                    message += '''"cpuUsage": {"unit": "%%","current": "%s"}}}}''' % (v[1])
                return message

        # If I get a RAM Usage Metric, building a RAM Usage JSON
        if reg_metric.ref_entity.name == "EdgeSystem.RAM_Used":
            for _ in range(size_values):
                v = reg_metric.values.get(block=True)  # Block if necessary until an item is available
                if v is not None:
                    message += '''"ram": {"unit": "B","total": "%d","usage": {"unit": "%%","current": "%s"}}}}}''' \
                               % (psutil.virtual_memory().total, v[1])
                return message

    def publish(self, reg_metric):
        message = self._format_data(reg_metric)
        self.comms.send(message)

    def set_properties(self, reg_entity, properties):
        pass

"""
JSON MODEL

{
    "version": "1.0",
    "event": {
        "id": "12345566678",
        "device": {
            "id": "5130252-6ea5-5c71-910b-759c66dc6d8d",
            "name": "liota_test",
            "description": "Testing Liota"
        },
        "location" : {
                "timestamp" : "epoch time in seconds",
                "coordinates": {
                    "latitude": 40.41675,
                    "longitude": -3.7028
                }
            },
        "cpuUsage": {
            "unit": "%",
            "current": "float"
        },
        "ram": {
            "unit": "MB",
            "total": "int",
            "usage": {
                "unit": "%",
                "current": "float"
            }
        }
    }
}
"""