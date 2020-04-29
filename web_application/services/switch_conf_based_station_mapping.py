import logging

import pandas as pd

from environment import NETWORK_MAP_FILENAME, NETWORK_MAP_INCLUDE_HEADERS

logger = logging.getLogger(__name__)


class SwitchPortStationMap:
    def __init__(self):
        self.__network_map_df = pd.read_csv(
            NETWORK_MAP_FILENAME,
            index_col=0,
            skipinitialspace=True,
            skip_blank_lines=True,
            usecols=[0, 1],
            names=['switch_port', 'station'],
            header=0 if NETWORK_MAP_INCLUDE_HEADERS else None
        )

    def get_associated_station(self, switch_port):
        try:
            station = self.__network_map_df.at[switch_port, 'station']
        except KeyError:
            logger.warning(f'{switch_port} was not found in the network map')
            return None

        return station
