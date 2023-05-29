"""
Example module for handling Open API from Sonoff eWeLink Cube API.
"""

import os
import asyncio
import json

from example_helpers import load_access_token, save_access_token
from sonoff_ewelink_cube_client_api import EWelinkCube

# iHost example settings
IHOST_BRIDGE_HOST_ADDRESS = os.getenv("IHOST_BRIDGE_HOST_ADDRESS", "ihost.local")
IHOST_BRIDGE_ACCESS_TOKEN = os.getenv("IHOST_BRIDGE_ACCESS_TOKEN", load_access_token(IHOST_BRIDGE_HOST_ADDRESS))

# Set None for disabling JSON output formatting
PRINT_JSON_INDENT = 4


async def main():
    """
    The main function of the example.
    """
    # Create an instance of the API
    ewelink_cube = EWelinkCube()
    api_rest = ewelink_cube.create_api(
        api_name='iHost',
        ip=IHOST_BRIDGE_HOST_ADDRESS,
        at=IHOST_BRIDGE_ACCESS_TOKEN,
    )

    access_token = api_rest.getAt()
    print(f'- Access token initialized: {access_token}')

    # Get iHost access token method:
    # After calling the [Access Token] interface, the iHost Web console page global
    # pop-up box prompts the user to confirm the acquisition of the interface call credentials.
    #
    # Note:
    # If you open more than one iHost web console page, the confirmation pop-up box will
    # appear on multiple web console pages together, and the pop-up box of other web console
    # pages will be closed after clicking the confirmation on one of the web console pages.
    if not access_token:
        print('- Access token process: press link button on iHost device!')
        await api_rest.getBridgeAT()

        access_token = api_rest.getAt()
        save_access_token(IHOST_BRIDGE_HOST_ADDRESS, access_token)
        print(f'- Access token received: {access_token}')

    # Set volume (0 - 100)
    set_volume = 50
    api_volume = await api_rest.updateBridgeConfig(volume=set_volume)
    if api_volume and not api_volume["error"]:
        print(f'- Volume set: {set_volume}%')
    else:
        print(f'- Volume set error: [{api_volume["error"]}] {api_volume["message"]}')

    # iHost info
    api_bridge_info = await api_rest.getBridgeInfo()
    if api_bridge_info and not api_bridge_info["error"]:
        print(f'- Bridge info: {json.dumps(api_bridge_info, indent=PRINT_JSON_INDENT)}')

    # Devices list with some info
    api_devices_list = await api_rest.getDeviceList()
    if api_devices_list and not api_devices_list["error"]:
        print(f'- Devices list: {json.dumps(api_devices_list, indent=PRINT_JSON_INDENT)}')


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
