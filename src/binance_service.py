# from object_manager import server_objects
import asyncio
from binance import AsyncClient, BinanceSocketManager


api_bin_key ="Rfm2PZaBAgavqhZWJA2N8xOEUprsMcLg3rgE9jFyhy4FV4bZMTwDYlTsqWXrz387"
api_bin_secret = "xoyngETgiBGTmvQR5YOL9pVcbcXCiyJCaTfL8j85wDYdAo49CvVvEmRsvqDLw07y"

class HariBinanceSocketManager:
    def __init__(self, client, symbol: str):
        self.symbol = symbol
        # self.bsm =
        self.kline_socket = None
        self.depth_socket = None


class BinanceService:
    _instances = {}  # Class-level dictionary to store unique instances
    def __init__(self, async_client):
        self.client_async = async_client  # Instance variable assigned the constructor variable
        print("Binance service got Initialized ")

    @classmethod
    async def create_async(cls, account_id:str, production_environment: bool= False):
        if account_id is None or not account_id.strip():
            raise ValueError("Account ID cannot be None or empty.")

        if not isinstance(production_environment, bool):
            raise TypeError("Production environment flag must be a boolean")

        env="Prod" if production_environment else "Test"
        key = (account_id, env)
        # Check if an instance already exists for the key
        if key not in cls._instances:

            # async_client = await AsyncClient.create(api_key=api_bin_key, api_secret=api_bin_secret)
            async_client = await cls._create_client_async(api_key=api_bin_key, api_secret=api_bin_secret)
            cls._instances[key] = cls(async_client)
            print(f"Binance Object created for account id: {account_id}  in {env} Environment ")

        return cls._instances[key]

    @staticmethod
    async def _create_client_async(api_key:str, api_secret:str, production_environment: bool=False):
        first_line = "This is the first line of code."

        # async_client = await AsyncClient.create(api_key=api_bin_key, api_secret=api_bin_secret, testnet=production_environment)
        async_client = await asyncio.sleep(2)
        print("\n ***************I AM CALLING THE BINANCE CLIENT********** ")
        return async_client



async def test_binance():
    test_client = await BinanceService.create_async(account_id="Hari", production_environment=False)
    # server_objects.get_binance()
    print(test_client)



if __name__ == "__main__":
    asyncio.run(test_binance())