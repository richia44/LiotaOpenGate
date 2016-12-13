from liota.dccs.dcc import DataCenterComponent
from liota.entities.metrics.registered_metric import RegisteredMetric
from liota.entities.metrics.metric import Metric
from liota.entities.registered_entity import RegisteredEntity


class OpenGateIoTDCC(DataCenterComponent):

    def __init__(self, comms):
        super(OpenGateIoTDCC, self).__init__(comms)
        self.comms = comms

    def register(self, entity_obj):
        print("Registering {0} on OpenGateDCC" .format(entity_obj.name))

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

        message = '''{"version": "1.0","datastreams": [{"id" : "random stream",
        "feed" : "random feed", "datapoints":['''

        for index in range(size_values):
            v = reg_metric.values.get(block=True)  # Block if necessary until an item is available
            if v is not None:
                if index+1 == size_values:  # Checks if is the last value collected to close the JSON
                    values = v[1].split(':')  # Divide the value on timestamp and data
                    message += '''{"at":"%s","value":"%s"}]}]}''' \
                               % (values[0], values[1])
                else:
                    values = v[1].split(':')  # Divide the value on timestamp and data
                    message += '''{"at":"%s","value":"%s"},''' \
                               % (values[0], values[1])
        return message

    def publish(self, reg_metric):
        message = self._format_data(reg_metric)
        self.comms.send(message)

    def set_properties(self, reg_entity, properties):
        pass

"""
JSON MODEL

{
  "version":"1.0.0",
  "datastreams" : [
    {
      "id" : "example",
      "feed" : "feed_1",
      "datapoints":[
        {"at":1431602523123,"value":41},
        {"at":1431602623123,"value":84},
        {"at":1431607623123,"value":41},
        {"at":1431608623123,"value":83}
      ]
    },
    {
      "id" : "key",
      "feed" : "feed_2",
      "datapoints":[
        {"at":1431602523123,"value":"revalue"},
        {"at":1431602623123,"value":"string value"},
        {"at":1431607623123,"value":"any string"},
        {"at":1431608623123,"value":"structured data"}
      ]
    },
    {
      "id" : "datastream",
      "datapoints":[
        {"at":1431602523123,"value":51, "tags":["tag_1","tag_2"]},
        {"at":1431602623123,"value":102, "tags":["tag_2","tag_3"]},
        {"at":1431607623123,"value":32},
        {"at":1431608623123,"value":16, "tags":["tag_3"]}
      ]
    }
  ]
}
"""