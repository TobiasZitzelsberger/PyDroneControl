import asyncio


async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent}")
        return


async def print_gps_info(drone):
    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS info: {gps_info}")
        return


async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")
        return


async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position)
        return


async def get_position(drone):
    position_stream = drone.telemetry.position()
    await asyncio.sleep(1)
    async for position in position_stream:
        return position


# returns bool
async def get_is_armed(drone):
    is_armed_stream = drone.telemetry.armed()
    await asyncio.sleep(1)
    async for is_armed in is_armed_stream:
        return is_armed


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")
