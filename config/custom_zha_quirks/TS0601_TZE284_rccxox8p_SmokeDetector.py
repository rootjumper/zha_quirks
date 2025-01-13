from zhaquirks.tuya.builder import TuyaQuirkBuilder
from zhaquirks.tuya import TuyaLocalCluster
from zigpy.zcl.clusters.security import IasZone


class TuyaIasFire(IasZone, TuyaLocalCluster):
    """Tuya local IAS smoke/fire cluster."""

    _CONSTANT_ATTRIBUTES = {
        IasZone.AttributeDefs.zone_type.id: IasZone.ZoneType.Fire_Sensor
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint.device.ias_zone = self


# Ensure TuyaQuirkBuilder is correctly configured
(
    TuyaQuirkBuilder("_TZE284_rccxox8p", "TS0601")
    .tuya_dp(
        dp_id=1,
        ep_attribute=TuyaIasFire.ep_attribute,
        attribute_name=IasZone.AttributeDefs.zone_status.name,
        converter=lambda x: IasZone.ZoneStatus.Alarm_1 if x == 0 else 0,
    )
    .adds(TuyaIasFire)
    .skip_configuration()
    .add_to_registry()
)