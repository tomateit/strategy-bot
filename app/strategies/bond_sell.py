import tinvest as ti
import logging
import datetime
from functools import reduce

async def bond_sell():
    global SANDBOX
    global TOKEN
    try:
        client = ti.AsyncClient(TOKEN, use_sandbox=SANDBOX)
        accounts_response = await client.get_accounts()
        # print("F:", accounts_response.payload.accounts)
        broker_account_id = accounts_response.payload.accounts[0].broker_account_id
        portfolio_response = await client.get_portfolio(broker_account_id)
        
        # GET bonds from portfolio
        bond_positions = {}
        for position in portfolio_response.payload.positions:
            if position.instrument_type == ti.InstrumentType.bond:
                bond_positions[position.figi] = position

        for bond_position in bond_positions.values():
            print(bond_position.name)
            print(bond_position.instrument_type)
            print("-----")

        # get their markets for 2 weeks before
        today = datetime.datetime.now()
        two_weeks_ago = today - datetime.timedelta(weeks=2)

        for bond_position_figi in bond_positions.keys():
            market_data = await client.get_market_candles(
                bond_position_figi, 
                two_weeks_ago, 
                today, 
                ti.CandleResolution.day
            )
            setattr(bond_positions[bond_position_figi], "market_data", market_data)
            # print(bond_positions[bond_position_figi])
            # print("-----")
        
        # take mean - 5%  (ensure is higher than mean 2w close)
        for bond_figi, position in bond_positions.items():
            n = len(position.market_data)
            mean_high = reduce(lambda candle, acc: acc+candle.h, position.market_data, 0) / n
            mean_close = reduce(lambda candle, acc: acc+candle.c, position.market_data, 0) / n
            mean_high *= 0.95
            setattr(bond_positions[bond_figi], "mean_high", mean_high)
            setattr(bond_positions[bond_figi], "mean_close", mean_close)
            print(f"For bond {position.name} 0.95 of mean high price was {mean_high} considering price {mean_close}")

        async with ti.Streaming(TOKEN) as streaming:
            # subscribe price. In case of hit - place market order
            for bond_position_figi in bond_positions.keys():
                await streaming.candle.subscribe(bond_position_figi, ti.CandleResolution.min1)
            # await streaming.orderbook.subscribe('BBG0013HGFT4', 5)
            # await streaming.instrument_info.subscribe('BBG0013HGFT4')
            async for event in streaming:
                print(event)


                    # body = MarketOrderRequest(
                    #     lots=2,
                    #     operation='Buy'
                    # )
                    # await client.post_orders_market_order(figi, body, broker_account_id)

                    # body = LimitOrderRequest(
                    #     lots=2,
                    #     operation='Buy',
                    #     price=100.85,
                    # )
                    # await client.post_orders_limit_order(figi, body, broker_account_id)
    except Exception as e:
        logging.exception(e)
    finally:
        await client.close()