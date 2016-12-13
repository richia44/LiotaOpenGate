from liota.core.package_manager import LiotaPackage
import random
import time

dependencies = ["sierraWireless_package", "iot_package_DCC"]

# ---------------------------------------------------------------------------
# User defined methods


def simulated_sampling_function():
    # format of data: "timestamp: random_number"
    data = str(long(round(time.time())))+":"+str(random.randint(0, 10))
    print data
    return data


class PackageClass(LiotaPackage):

    def run(self, registry):
        import copy
        from liota.entities.metrics.metric import Metric

        # Acquire resources from registry
        reg_edge_system = copy.copy(registry.get("sierra_edge_system"))
        opengate = registry.get("opengate_iot_DCC")

        # Create metrics tuple
        self.metrics = []

        # Getting CPU utilization
        simulated_metric = Metric(name='Random.Metric',
                                       unit=None, interval=3,
                                       aggregation_size=3,
                                       sampling_function=simulated_sampling_function
                                  )
        reg_simulated_metric = opengate.register(simulated_metric)
        opengate.create_relationship(reg_edge_system, reg_simulated_metric)
        reg_simulated_metric.start_collecting()
        self.metrics.append(reg_simulated_metric)

    def clean_up(self):
        for metric in self.metrics:
            metric.stop_collecting()
