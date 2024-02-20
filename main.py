import asyncio
from discord_rpc import DiscordRPC
from media_info import get_media_info

CLIENT_ID = '1209469955611951164'

async def main():
    rpc = DiscordRPC(CLIENT_ID)
    await rpc.connect()  # Connect to Discord RPC within the async function

    current_song = None
    remaining_duration = 0

    try:
        while True:
            media_info = await get_media_info()
            if media_info and media_info['title'] != current_song:
                current_song = media_info['title']
                remaining_duration = media_info['duration']
                link = media_info['link']
            elif media_info and media_info['title'] == current_song:
                remaining_duration -= 15  # Subtract the sleep duration from the remaining duration

            if remaining_duration > 0:
                await rpc.update_rpc(media_info['artist'], current_song, remaining_duration, link)
            else:
                await rpc.clear_rpc()
                current_song = None  # Reset the current song

            await asyncio.sleep(15)  # Sleep for 15 seconds before checking again.
    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        rpc.close()

if __name__ == '__main__':
    asyncio.run(main())