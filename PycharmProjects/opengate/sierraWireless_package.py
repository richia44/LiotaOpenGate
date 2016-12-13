from liota.core.package_manager import LiotaPackage


class PackageClass(LiotaPackage):

    """
    This package contains specifications of Sierra Wireless and properties to import
    from configuration file.
    It registers "edge system" in package manager's resource registry.
    """

    def run(self, registry):
        from sierraWirelessEdgeSystem_logic import SierraWirelessEdgeSystem

        # Initialize edgesystem
        edge_system = SierraWirelessEdgeSystem("Sierra Wireless")
        registry.register("sierra_edge_system", edge_system)

    def clean_up(self):
        pass