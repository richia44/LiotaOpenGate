# Logic to connect with OpenGate through HTTP

from liota.core.package_manager import LiotaPackage

dependencies = ["sierraWireless_package"]


class PackageClass(LiotaPackage):
    # Creates a DCC object and registers system on
    def run(self, registry):
        import copy
        from dmm_DCC_logic import OpenGateDmmDCC
        from DCCcomms_logic import CommandDCCComms

        # Acquire resources from registry
        # Creating a copy of system object to keep original object "clean"
        edge_system = copy.copy(registry.get("sierra_edge_system"))
        print ("Edge System ID: %s" % edge_system.entity_id)

        """# Get values from configuration file
        config_path = registry.get("package_conf")
        config = {}
        execfile(config_path + '/sampleProp.conf', config)"""

        # Formatting URL to fit OpenGate parameters
        # URL format: http://[your_opengate_addres]/v70/{device.id}?xHyKZ={ApiKey}

        """url = '{0}/v70/{1}?xHyKZ={2}' .format(config['AmpliaURL'], str(edge_system.entity_id), config['ApiKey'])
        port = config['port']"""

        port = 9955

        url = '{0}:{1}/v70/devices/{2}/collect/dmm?xHyKZ={3}'\
            .format('http://cloud.opengate.es', str(port), str(edge_system.entity_id), '925f11cc-2b25-4cc1-a076-6a2df9472e57')

        print (url)

        # Initialize DCC object with transport
        self.opengate = OpenGateDmmDCC(CommandDCCComms(url))

        # Register gateway system on DCC
        opengate_edge_system = self.opengate.register(edge_system)

        # Keep on registry the registered DCC and edge system
        registry.register("opengate_dmm_DCC", self.opengate)
        registry.register("opengate_dmm_edge_system", opengate_edge_system)

    pass

    def clean_up(self):
        pass
