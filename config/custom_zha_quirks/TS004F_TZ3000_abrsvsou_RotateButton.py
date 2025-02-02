"""Tuya TS004F devices."""
from __future__ import annotations
from zhaquirks.tuya.mcu import EnchantedDevice #old versions
#from zhaquirks.tuya import EnchantedDevice #2024.2 onward
from zigpy.profiles import zha
from zigpy.zcl.clusters.general import (
    Basic,
    Groups,
    Identify,
    LevelControl,
    OnOff,
    Ota,
    PowerConfiguration,
    Scenes,
    Time,
)
from zigpy.zcl.clusters.lighting import Color
from zigpy.zcl.clusters.lightlink import LightLink
from zhaquirks.const import (
    ALT_SHORT_PRESS,
    BUTTON,
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    CLUSTER_ID,
    COMMAND,
    COMMAND_MOVE,
    COMMAND_MOVE_SATURATION,
    COMMAND_OFF,
    COMMAND_ON,
    COMMAND_STEP,
    COMMAND_STOP,
    COMMAND_STOP_MOVE_STEP,
    COMMAND_TOGGLE,
    DEVICE_TYPE,
    DIM_DOWN,
    DIM_UP,
    DOUBLE_PRESS,
    ENDPOINT_ID,
    ENDPOINTS,
    INPUT_CLUSTERS,
    LEFT,
    LONG_PRESS,
    LONG_RELEASE,
    MODEL,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PARAMS,
    PROFILE_ID,
    RIGHT,
    ROTATED,
    ROTATED_FAST,
    ROTATED_SLOW,
    SHORT_PRESS,
    TURN_OFF,
    TURN_ON,
    ARGS,
    
)
from zhaquirks.tuya import (
    TuyaNoBindPowerConfigurationCluster,
    TuyaSmartRemoteOnOffCluster,
    TuyaZBExternalSwitchTypeCluster,
)

#Some of the TZ3000_abrsvsou TS004F Customizations
ROTATED_PRESSED = "Press Rotate Knob HUE Mode Only"
COMMAND_STEP_COLOR_TEMP = "step_color_temp"
PRESSED = "pressed"
TOGGLE = "toggle"
ATTRIBUTE_UPDATED = "attribute_updated"
TRIPPLE_PRESSED = "Tripple Press"
TRIPPLE_PRESSED_NORMAL_MODE = "Tripple press to Normal Mode"
TRIPPLE_PRESSED_HUE_MODE = "Tripple press to HUE Mode"
ROTATED_HUE = "Rotate in HUE Mode"
ROTATED_NORMAL = "Rotate in Normal Mode"
DOUBLE_PRESS = "Double Click in Normal Mode"
LONG_PRESS = "Long Press in Normal Mode"
LONG_PRESS_HUE = "Long Press in HUE Mode"
BUTTON_1_HUE = "Button 1 in Hue Mode"
BUTTON_1_NORMAL = "Button 1 in Normal Mode"

class TuyaSmartRemote004FROK(EnchantedDevice):
    """Tuya Smart (rotating) Knob device."""

    signature = {
        # "node_descriptor": "NodeDescriptor(byte1=2, byte2=64, mac_capability_flags=128, manufacturer_code=4098, maximum_buffer_size=82, maximum_incoming_transfer_size=82, server_mask=11264, maximum_outgoing_transfer_size=82, descriptor_capability_field=0, *allocate_address=True, *complex_descriptor_available=False, *is_alternate_pan_coordinator=False, *is_coordinator=False, *is_end_device=True, *is_full_function_device=False, *is_mains_powered=False, *is_receiver_on_when_idle=False, *is_router=False, *is_security_capable=False, *is_valid=True, *logical_type=<LogicalType.EndDevice: 2>, *user_descriptor_available=False)",
        # SizePrefixedSimpleDescriptor(endpoint=1, profile=260, device_type=260, device_version=1, input_clusters=[0, 1, 3, 4, 6, 4096], output_clusters=[25, 10, 3, 4, 5, 6, 8, 4096])
        MODELS_INFO: [
            ("_TZ3000_4fjiwweb", "TS004F"),
            ("_TZ3000_uri7ongn", "TS004F"),
            ("_TZ3000_ixla93vd", "TS004F"),
            ("_TZ3000_qja6nq5z", "TS004F"),
            ("_TZ3000_csflgqj2", "TS004F"),
            ("_TZ3000_abrsvsou", "TS004F"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.DIMMER_SWITCH,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    OnOff.cluster_id,
                    LightLink.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id,
                    Time.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    LightLink.cluster_id,
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.NON_COLOR_CONTROLLER,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    TuyaNoBindPowerConfigurationCluster,
                    Identify.cluster_id,
                    Groups.cluster_id,  # Is needed for adding group then binding is not working.
                    LightLink.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id,
                    Time.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    TuyaSmartRemoteOnOffCluster,
                    LevelControl.cluster_id,
                    Color.cluster_id,
                    LightLink.cluster_id,
                ],
            },
        },
    }

    device_automation_triggers = {
        #HUE MODE STUFF 
        (LONG_PRESS_HUE, BUTTON): {
            COMMAND: COMMAND_MOVE_SATURATION,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 768,
            PARAMS: {"move_mode": 1},
        },
        (ROTATED_HUE, RIGHT): {
            COMMAND: COMMAND_STEP,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 8,
            PARAMS: {"step_mode": 0},
        },
        (ROTATED_HUE, LEFT): {
            COMMAND: COMMAND_STEP,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 8,
            PARAMS: {"step_mode": 1},
        },
        (ROTATED_PRESSED, RIGHT): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 768,
            PARAMS: {"step_mode": 1, "color_temp_min_mireds": 153},
        },
        (ROTATED_PRESSED, LEFT): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 768,
            PARAMS: {"step_mode": 3, "color_temp_min_mireds": 153},
        },
        (TOGGLE, BUTTON_1_HUE): {
            COMMAND: TOGGLE,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 6,
        },
        (TRIPPLE_PRESSED_NORMAL_MODE, BUTTON_1_HUE): {
            COMMAND: ATTRIBUTE_UPDATED,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 6,
            ARGS: {"attribute_name": "switch_mode", "attribute_id": 32772, "value": 1},
        },
        (TRIPPLE_PRESSED_HUE_MODE, BUTTON_1): {
            COMMAND: ATTRIBUTE_UPDATED,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 6,
            ARGS: {"attribute_name": "switch_mode", "attribute_id": 32772, "value": 0},
        },
        (SHORT_PRESS, BUTTON_1_NORMAL): {ENDPOINT_ID: 1, COMMAND: SHORT_PRESS},
        (LONG_PRESS, BUTTON_1_NORMAL): {ENDPOINT_ID: 1, COMMAND: LONG_PRESS},
        (DOUBLE_PRESS, BUTTON_1_NORMAL): {ENDPOINT_ID: 1, COMMAND: DOUBLE_PRESS},
        (ROTATED_NORMAL, RIGHT): {
            COMMAND: RIGHT,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 6,
        },
        (ROTATED_NORMAL, LEFT): {
            COMMAND: LEFT,
            ENDPOINT_ID: 1,
            CLUSTER_ID: 6,
        },
    }
