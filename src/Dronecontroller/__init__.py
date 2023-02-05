import asyncio
from mavsdk.mission import (MissionPlan)
from src import Datacontroller as dc


async def takeoff(drone):
    status_text_task = asyncio.ensure_future(dc.print_status_text(drone))
    # Checking if Global Position Estimate is ok
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

        # Arming the drone
    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(5)

    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(10)

    print("-- Landing")
    await drone.action.land()
    await asyncio.sleep(1)

    status_text_task.cancel()


async def telemetry_check(drone):
    asyncio.ensure_future(dc.print_battery(drone))
    asyncio.ensure_future(dc.print_gps_info(drone))
    asyncio.ensure_future(dc.print_in_air(drone))
    asyncio.ensure_future(dc.print_position(drone))
    await asyncio.sleep(1)


async def goto_location(drone, lat, lon):
    status_text_task = asyncio.ensure_future(dc.print_status_text(drone))
    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break
    print("absolute altitude. "+str(absolute_altitude))

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(10)
    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + 20.0
    curr_pos = await dc.get_position(drone)

    print("-- Rising to flying altitude")
    await drone.action.goto_location(float(curr_pos.latitude_deg), float(curr_pos.longitude_deg), flying_alt, 0)
    while float(curr_pos.absolute_altitude_m) < flying_alt:
        curr_pos = await dc.get_position(drone)
        print(curr_pos)
        await asyncio.sleep(5)

    print("-- Starting Goto maneuver")
    await drone.action.goto_location(lat, lon, flying_alt, 0)
    # goto_location() takes Absolute MSL altitude
    while float(curr_pos.latitude_deg) != lat and float(curr_pos.longitude_deg) != lon:
        curr_pos = await dc.get_position(drone)
        print(curr_pos)
        await asyncio.sleep(5)

    print("-- Arrived at location")
    status_text_task.cancel()


# return drone to launch position and periodically display position and status
async def return_to_launch(drone):
    status_text_task = asyncio.ensure_future(dc.print_status_text(drone))
    await asyncio.sleep(1)
    await drone.action.return_to_launch()
    while await dc.get_is_armed(drone):
        print(await dc.get_position(drone))
        await asyncio.sleep(5)
    status_text_task.cancel()


async def start_waypoint_mission(drone, mission_items):
    print_mission_progress_task = asyncio.ensure_future(
        dc.print_mission_progress(drone))

    mission_plan = MissionPlan(mission_items)

    await drone.mission.set_return_to_launch_after_mission(True)

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting mission")
    await drone.mission.start_mission()

    await asyncio.sleep(30)
    print_mission_progress_task.cancel()