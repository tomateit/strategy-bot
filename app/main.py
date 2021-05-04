from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.
TOKEN = os.environ["TOKEN"]

import asyncio
import tinvest as ti

async def main():
    async with ti.Streaming(TOKEN) as streaming:
        await streaming.candle.subscribe('BBG0013HGFT4', ti.CandleResolution.min1)
        # await streaming.orderbook.subscribe('BBG0013HGFT4', 5)
        await streaming.instrument_info.subscribe('BBG0013HGFT4')
        async for event in streaming:
            print(event)

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Closing")