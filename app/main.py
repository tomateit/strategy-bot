import asyncio
import logging
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

import tinvest as ti
TOKEN = os.environ["TOKEN"]
SANDBOX = False if os.environ.get("IS_SANDBOX") == "False" else True


async def main():
    # GET bonds from portfolio
    try:
        client = ti.AsyncClient(TOKEN, use_sandbox=SANDBOX)
        accounts_response = await client.get_accounts()
        print("F:", accounts_response.payload.accounts)
        broker_account_id = accounts_response.payload.accounts[0].broker_account_id
        portfolio_response = await client.get_portfolio(broker_account_id)
        for position in portfolio_response.payload.positions:
            print(position.name)
            print(position.instrument_type)
            print("-----")
    # get their highs for 2 weeks before

    # take mean - 5%  (ensure is higher than mean 2w close)
    except Exception as e:
        logging.exception(e)
    finally:
        await client.close()
    # async with ti.Streaming(TOKEN) as streaming:
    #     # subscribe price. In case of hit - place market order


    #     await streaming.candle.subscribe('BBG0013HGFT4', ti.CandleResolution.min1)
    #     # await streaming.orderbook.subscribe('BBG0013HGFT4', 5)
    #     await streaming.instrument_info.subscribe('BBG0013HGFT4')
    #     async for event in streaming:
    #         print(event)

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Closing")