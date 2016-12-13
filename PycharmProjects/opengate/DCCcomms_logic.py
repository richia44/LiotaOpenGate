# Communication with Opengate through HTTP

import requests
from liota.dcc_comms.dcc_comms import DCCComms


class CommandDCCComms(DCCComms):

    def __init__(self, url):
        super(CommandDCCComms, self).__init__()
        self.url = url
        self._connect()

    def _connect(self):
        pass

    def _disconnect(self):
        pass

    def send(self, message):

        # import json.dumps(message, indent=2)
        r = requests.post(self.url, message, headers={"X-ApiKey": "925f11cc-2b25-4cc1-a076-6a2df9472e57",
                                                      "Content-Type": "application/json"})
        print r.status_code
        print r.text
        print message

    def receive(self):
        pass
