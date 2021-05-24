import asyncio
import logging
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

import tinvest as ti
TOKEN = os.environ["TOKEN"]
SANDBOX = False if os.environ.get("IS_SANDBOX") == "False" else True

from strategies.bond_sell import bond_sell


if __name__=="__main__":
    try:
        asyncio.run(bond_sell())
    except KeyboardInterrupt:
        print("Closing")