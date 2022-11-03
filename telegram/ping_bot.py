from ping_bot_base import ping_dispatcher, ping_bot
from handlers               import ping_bot_pm_handler

import asyncio, itertools, random

async def dispatcher_perform_polling() -> None:
    """
    Start polling of the bot dispatcher in async loop.
    """
    await ping_dispatcher.start_polling()

async def async_main() -> None:
    """
    Main async loop.
    """
    await asyncio.gather(
       dispatcher_perform_polling(),
    )

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(async_main())
