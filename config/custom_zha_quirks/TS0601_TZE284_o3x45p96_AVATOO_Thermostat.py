"""Map from manufacturer to standard clusters for thermostatic valves."""

import logging
from typing import Optional, Union

from zigpy.profiles import zha
import zigpy.types as t
from zigpy.zcl import foundation
from zigpy.zcl.clusters.general import (
    AnalogOutput,
    Basic,
    BinaryInput,
    Groups,
    Identify,
    OnOff,
    Ota,
    Scenes,
    Time,
)
from zigpy.zcl.clusters.hvac import Thermostat

from zhaquirks import Bus, LocalDataCluster
from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.tuya import (
    TuyaManufClusterAttributes,
    TuyaPowerConfigurationCluster2AA,
    TuyaThermostat,
    TuyaThermostatCluster,
    TuyaUserInterfaceCluster,
)
from zhaquirks.tuya.builder import TuyaQuirkBuilder
from zhaquirks.tuya.mcu import TuyaAttributesCluster

_LOGGER = logging.getLogger(__name__)

class TuyaThermostatSystemMode(t.enum8):
    """Tuya thermostat system mode enum."""

    Auto = 0x00
    Heat = 0x01
    Off = 0x02


class TuyaThermostatV2(Thermostat, TuyaAttributesCluster):
    """Tuya local thermostat cluster."""

    manufacturer_id_override: t.uint16_t = foundation.ZCLHeader.NO_MANUFACTURER_ID

    _CONSTANT_ATTRIBUTES = {
        Thermostat.AttributeDefs.ctrl_sequence_of_oper.id: Thermostat.ControlSequenceOfOperation.Heating_Only
    }

    def __init__(self, *args, **kwargs):
        """Init a TuyaThermostat cluster."""
        super().__init__(*args, **kwargs)
        self.add_unsupported_attribute(
            Thermostat.AttributeDefs.setpoint_change_source.id
        )
        self.add_unsupported_attribute(
            Thermostat.AttributeDefs.setpoint_change_source_timestamp.id
        )
        self.add_unsupported_attribute(Thermostat.AttributeDefs.pi_heating_demand.id)

    async def write_attributes(self, attributes, manufacturer=None):
        """Overwrite to force manufacturer code."""

        return await super().write_attributes(
            attributes, manufacturer=foundation.ZCLHeader.NO_MANUFACTURER_ID
        )


(
    TuyaQuirkBuilder("_TZE200_bvu2wnxz", "TS0601")
    .applies_to("_TZE200_6rdj8dzm", "TS0601")
    .applies_to("_TZE200_9xfjixap", "TS0601")
    .applies_to("_TZE200_p3dbf6qs", "TS0601")
    .applies_to("_TZE200_rxntag7i", "TS0601")
    .applies_to("_TZE200_yqgbrdyo", "TS0601")
    .applies_to("_TZE284_p3dbf6qs", "TS0601")
    .applies_to("_TZE200_rxq4iti9", "TS0601")
    .applies_to("_TZE200_hvaxb2tc", "TS0601")
    .applies_to("_TZE284_o3x45p96", "TS0601")
    .applies_to("_TZE284_c6wv4xyo", "TS0601")
    .applies_to("_TZE204_o3x45p96", "TS0601")
    .tuya_dp(
        dp_id=2,
        ep_attribute=TuyaThermostatV2.ep_attribute,
        attribute_name=TuyaThermostatV2.AttributeDefs.system_mode.name,
        converter=lambda x: {
            TuyaThermostatSystemMode.Auto: Thermostat.SystemMode.Auto,
            TuyaThermostatSystemMode.Heat: Thermostat.SystemMode.Heat,
            TuyaThermostatSystemMode.Off: Thermostat.SystemMode.Off,
        }[x],
        dp_converter=lambda x: {
            Thermostat.SystemMode.Auto: TuyaThermostatSystemMode.Auto,
            Thermostat.SystemMode.Heat: TuyaThermostatSystemMode.Heat,
            Thermostat.SystemMode.Off: TuyaThermostatSystemMode.Off,
        }[x],
    )
    .tuya_dp(
        dp_id=3,
        ep_attribute=TuyaThermostatV2.ep_attribute,
        attribute_name=TuyaThermostatV2.AttributeDefs.running_state.name,
        converter=lambda x: 0x01 if not x else 0x00,  # Heat, Idle
    )
    .tuya_dp(
        dp_id=4,
        ep_attribute=TuyaThermostatV2.ep_attribute,
        attribute_name=TuyaThermostatV2.AttributeDefs.occupied_heating_setpoint.name,
        converter=lambda x: x * 10,
        dp_converter=lambda x: x // 10,
    )
    .tuya_dp(
        dp_id=5,
        ep_attribute=TuyaThermostatV2.ep_attribute,
        attribute_name=TuyaThermostatV2.AttributeDefs.local_temperature.name,
        converter=lambda x: x * 10,
    )
    .tuya_dp(
        dp_id=47,
        ep_attribute=TuyaThermostatV2.ep_attribute,
        attribute_name=TuyaThermostatV2.AttributeDefs.local_temperature_calibration.name,
        converter=lambda x: x,
        dp_converter=lambda x: x + 0x100000000 if x < 0 else x,
    )
    .tuya_switch(
        dp_id=7,
        attribute_name="child_lock",
        translation_key="child_lock",
        fallback_name="Child lock",
    )
    .tuya_switch(
        dp_id=36,
        attribute_name="frost_protection",
        translation_key="frost_protection",
        fallback_name="Frost protection",
    )
    .tuya_switch(
        dp_id=39,
        attribute_name="scale_protection",
        translation_key="scale_protection",
        fallback_name="Scale protection",
    )
    .tuya_binary_sensor(
        dp_id=35,
        attribute_name="error",
        translation_key="error",
        fallback_name="Error or battery low",
    )
    .adds(TuyaThermostatV2)
    .skip_configuration()
    .add_to_registry()
)
