from liota.core.package_manager import LiotaPackage
import psutil

dependencies = ["sierraWireless_package", "dmm_package_DCC"]

# ---------------------------------------------------------------------------
# User defined methods


def read_cpu_utilization(sample_duration_sec=1):
    return round(psutil.cpu_percent(interval=sample_duration_sec), 2)


def read_ram_used():
    return round(psutil.virtual_memory().used, 0)


class PackageClass(LiotaPackage):

    def run(self, registry):
        import copy
        from liota.entities.metrics.metric import Metric

        # Acquire resources from registry
        reg_edge_system = copy.copy(registry.get("sierra_edge_system"))
        opengate = registry.get("opengate_dmm_DCC")

        # Create metrics tuple
        self.metrics = []

        # Getting CPU utilization
        metric_cpu_utilization = Metric(name="EdgeSystem.CPU_Utilization",
                                             unit=None, interval=5,
                                             aggregation_size=1,
                                             sampling_function=read_cpu_utilization
                                        )
        reg_metric_cpu_utilization = opengate.register(metric_cpu_utilization)
        opengate.create_relationship(reg_edge_system, reg_metric_cpu_utilization)
        reg_metric_cpu_utilization.start_collecting()
        self.metrics.append(reg_metric_cpu_utilization)

        # Getting RAM used
        metric_ram_used = Metric(name="EdgeSystem.RAM_Used",
                                      unit=None, interval=5,
                                      aggregation_size=1,
                                      sampling_function=read_ram_used
                                 )
        reg_metric_ram_used = opengate.register(metric_ram_used)
        opengate.create_relationship(reg_edge_system, reg_metric_ram_used)
        reg_metric_ram_used.start_collecting()
        self.metrics.append(reg_metric_ram_used)

    def clean_up(self):
        for metric in self.metrics:
            metric.stop_collecting()

