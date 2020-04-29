import logging

from flask import Flask, jsonify, request

from services.switch_conf_based_station_mapping import SwitchPortStationMap
from services.switch_conn_based_mac_mapping import SwitchMacAddressTable

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify(
        name='Station and Port Tracker',
        version='0.1'
    )


@app.route('/heartbeat')
def get_heartbeat():
    return jsonify(alive=True)


@app.route('/station/associations', methods=['GET'])
def get_station_associations():
    raw_mac_list = request.args.get('mac_list', None)
    if not raw_mac_list:
        response = jsonify(
            error='You must specify at least one MAC address in the '
                  '`mac_list` parameter'
        )
        response.status_code = 400
        return response

    mac_address_list = [
        address for address in [
            item.strip() for item in (
                request.args.get('mac_list', '').split(',')
            )
        ] if address
    ]

    try:
        mac_table = SwitchMacAddressTable()
        port_station_map = SwitchPortStationMap()
    except Exception as e:
        error_msg = 'Something went wrong trying to initialize the' \
                    'Port and Station services'
        logger.error(error_msg, exc_info=True)

        response = jsonify(error_msg=error_msg)
        response.status_code = 500
        return response

    associations = {}
    for mac_address in mac_address_list:
        associated_port = mac_table.get_associated_port(mac_address)

        associated_station = port_station_map.get_associated_station(
            associated_port
        ) if associated_port else None

        associations[mac_address] = dict(
            switch_port=associated_port,
            station_name=associated_station
        ) if associated_station else None

    return jsonify(associations=associations)

