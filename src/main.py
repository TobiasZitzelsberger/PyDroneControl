import asyncio
import subprocess

import aioconsole
from mavsdk import System

import Dronecontroller
import Waypointparser


async def main():

    print("####################################")
    print("########## PyDroneControl ###########")
    print("####################################")
    print("####################################")
    print()

    print("Trying to establish connection...")
    subprocess.Popen([r"src/MAVSDK/bin/mavsdk_server_bin.exe"])
    drone = System(mavsdk_server_address='localhost', port=50051)
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            print()
            break

    running = True

    while running:
        print()
        print("(1) Takeoff and land")
        print("(2) Check telemetry")
        print("(3) Fly to location")
        print("(4) Return to launch")
        print("(q) Quit program")

        print("Please enter a command:\n")
        try:
            command = await aioconsole.ainput()
        except Exception as e:
            print('Bad command: %s' % e, 'red')

        if command == '1':
            await Dronecontroller.takeoff(drone)
        elif command == "2":
            await Dronecontroller.telemetry_check(drone)
        elif command == '3':

            try:
                print("Please enter the latitude:\n")
                lat = float(await aioconsole.ainput())
                print("Please enter the longitude:\n")
                lon = float(await aioconsole.ainput())
            except Exception as e:
                print('Bad command: %s' % e, 'red')

            await Dronecontroller.goto_location(drone, lat, lon)
        elif command == '4':
            await Dronecontroller.return_to_launch(drone)
        elif command == 'q':
            running = False
        else:
            print("Invalid command!")


if __name__ == "__main__":

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.new_event_loop().run_until_complete(main())
