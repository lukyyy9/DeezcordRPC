import asyncio
from discord_rpc import DiscordRPC
from media_info import get_media_info

CLIENT_ID = '1209469955611951164'

async def main():
    rpc = DiscordRPC(CLIENT_ID)
    await rpc.connect()  # Connect to Discord RPC within the async function
    try:
        while True:
            media_info = await get_media_info()
            if media_info:
                await rpc.update_rpc(media_info['artist'], media_info['title'], media_info['duration'])
            else:
                await rpc.clear_rpc()
            await asyncio.sleep(15)  # Sleep for 15 seconds before checking again.
    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        rpc.close()

if __name__ == '__main__':
    asyncio.run(main())
