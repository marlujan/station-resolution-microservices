from netmiko import Netmiko

from environment import (SWITCH_DEVICE_TYPE, SWITCH_HOST,
                         SWITCH_USERNAME, SWITCH_PASSWORD)

cisco_conf = {
    "device_type": SWITCH_DEVICE_TYPE,
    "host": SWITCH_HOST,
    "username": SWITCH_USERNAME,
    "password": SWITCH_PASSWORD,
}


class SwitchMacAddressTable:
    def __init__(self):
        """
            self.__switch_mac_address_map = [
                {
                    'destination_address': '0011.5ccc.5c00',
                    'destination_port': 'GigabitEthernet1/0/31'
                },
                {
                    'destination_address': '0025.2266.d104',
                    'destination_port': 'GigabitEthernet1/0/38'
                }
            ]
        """
        net_connect = Netmiko(**cisco_conf)

        self.__switch_mac_address_map = net_connect.send_command(
            'show mac address-table', use_textfsm=True
        )

        net_connect.disconnect()

    def get_associations(self):
        return self.__switch_mac_address_map

    def get_associated_port(self, mac_address):
        for assignation in self.__switch_mac_address_map:
            mac_address_in_switch = assignation.get('destination_address')
            if mac_address == mac_address_in_switch:
                return assignation.get('destination_port')

        return None
