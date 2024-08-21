import time
import asyncio
from typing import Awaitable

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    devices = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    async def run_sequence(*args: Awaitable):
        for function in args:
            await function

    async def run_parallel(*args: Awaitable):
        await asyncio.gather(*args)

    await run_parallel(
        service.send_msg(Message(devices[0], MessageType.SWITCH_ON)),
        service.send_msg(Message(devices[1], MessageType.SWITCH_ON))
    )
    await run_sequence(
        service.send_msg(Message(devices[1],
                         MessageType.PLAY_SONG,
                         "Rick Astley - Never Gonna Give You Up"))
    )
    await run_parallel(
        service.send_msg(Message(devices[0], MessageType.SWITCH_OFF)),
        service.send_msg(Message(devices[1], MessageType.SWITCH_OFF))
    )
    await run_sequence(
        service.send_msg(Message(devices[2], MessageType.FLUSH)),
        service.send_msg(Message(devices[2], MessageType.CLEAN))
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
