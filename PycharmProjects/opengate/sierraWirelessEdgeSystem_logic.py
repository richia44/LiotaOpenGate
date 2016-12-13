from liota.entities.edge_systems.edge_system import EdgeSystem
from liota.lib.utilities.utility import systemUUID


class SierraWirelessEdgeSystem(EdgeSystem):

    def __init__(self, name):
        super(SierraWirelessEdgeSystem, self).__init__(
            name=name,
            entity_id=systemUUID().get_uuid(name)
        )
