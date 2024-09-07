import asyncio
import aiohttp
import random
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

class DummyService:
    def __init__(self, name, registry_url, behavior):
        self.name = name
        self.registry_url = registry_url
        self.behavior = behavior
        self.is_alive = True
        self.ping_count = 0

    async def send_heartbeat(self):
        if not self.is_alive:
            return

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{self.registry_url}/heartbeat/{self.name}") as response:
                    if response.status == 200:
                        print(f"Heartbeat sent for {self.name}")
                    else:
                        print(f"Failed to send heartbeat for {self.name}")
            except aiohttp.ClientError as e:
                print(f"Error sending heartbeat for {self.name}: {e}")

        self.ping_count += 1

    async def run(self):
        while True:
            if self.behavior == ServiceBehavior.ALWAYS_ALIVE:
                await self.send_heartbeat()
                await asyncio.sleep(random.randint(5, 15) if DEBUG_MODE else random.randint(30, 90))
            elif self.behavior == ServiceBehavior.PING_ONCE_THEN_DIE:
                if self.ping_count == 0:
                    await self.send_heartbeat()
                self.is_alive = False
                break
            elif self.behavior == ServiceBehavior.PING_GO_SILENT_REVIVE:
                if self.ping_count < 3:
                    await self.send_heartbeat()
                    await asyncio.sleep(random.randint(5, 15) if DEBUG_MODE else random.randint(30, 90))
                elif self.ping_count < 10:
                    await asyncio.sleep(10 if DEBUG_MODE else 60)  # Silent period
                else:
                    self.ping_count = 0  # Reset and revive
            else:
                raise ValueError(f"Unknown behavior: {self.behavior}")

async def main():
async def main():
    registry_url = "http://localhost:8002"
    services = [
        DummyService("always_alive", registry_url, ServiceBehavior.ALWAYS_ALIVE),
        DummyService("ping_once_die", registry_url, ServiceBehavior.PING_ONCE_THEN_DIE),
        DummyService("ping_silent_revive", registry_url, ServiceBehavior.PING_GO_SILENT_REVIVE),
    ]

    tasks = [asyncio.create_task(service.run()) for service in services]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())