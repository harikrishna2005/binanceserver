# from object_manager import server_objects
import asyncio
import time

from aiohttp import ClientConnectorDNSError
from binance import AsyncClient, BinanceSocketManager


api_bin_key ="Rfm2PZaBAgavqhZWJA2N8xOEUprsMcLg3rgE9jFyhy4FV4bZMTwDYlTsqWXrz387"
api_bin_secret = "xoyngETgiBGTmvQR5YOL9pVcbcXCiyJCaTfL8j85wDYdAo49CvVvEmRsvqDLw07y"

class HariBinanceSocketManager:
    _instances = {}
    def __init__(self, client, symbol: str):
        self.symbol = symbol
        # self.bsm =
        self.kline_socket = None
        self.depth_socket = None

    @classmethod
    async def create_socket_manager_async(cls):

        pass

class UserAccount:
    def __init__(self, user_socket):
        self.current_status= "STOPPED"
        self._start_indicator:bool = False
        self._user_socket = user_socket
        self._context_manager = None
        self._manual_context= None



    async def start_updates_async(self):
        if not self.current_status=="STARTED":
            self.current_status="STARTED"
            self._start_indicator = True
            self._manual_context = await self._user_socket.__aenter__()
            updates_task = asyncio.create_task(self._receive_updates_async())

            print(f"Before Awaiting TASK")
            print(f"Going to sleep for 60 seconds")
            # await asyncio.sleep(60)
            # asyncio.create_task(asyncio.to_thread(self._automatic_stopping,60))
            await updates_task
            self._start_indicator = False

            # await updates_task
            print(f"After Awaiting TASK")
            # num=1
            # async with self._user_socket  as tscm:
            #     while num <= 100:
            #         print(f"*======ENTRY :{num}========")
            #         res = await tscm.recv()
            #         print(res)
            #         await asyncio.sleep(1)
            #         num = num + 1




    async def _receive_updates_async(self):
        num = 1

        while self._start_indicator:
            print(f"*======ENTRY :{num}========")
            res = await self._manual_context.recv()
            print(res)
            # await asyncio.sleep(1)
            num = num + 1

    def _automatic_stopping(self, seconds):
        time.sleep(seconds)
        self._start_indicator=False


    async def stop_updates_async(self):
        if not self.current_status=="STOPPED":
            self.current_status="STOPPED"
            self._start_indicator=False
            await self._manual_context.__aexit__(None, None, None)


# class UserAccount(CommonSocket):
#     def __init__(self):
#         super().__init__()












class BinanceService:
    _instances = {}  # Class-level dictionary to store unique instances
    def __init__(self, async_client, bsm:BinanceSocketManager):
        self.client_async = async_client  # Instance variable assigned the constructor variable
        self.bsm =  bsm
        self.user_account =None

        print("Binance service got Initialized ")




    async def start_user_account_updates_async(self):
        if not self.user_account:
            self.user_account =UserAccount(self.bsm.user_socket())
        await self.user_account.start_updates_async()

        print("STARTED receiving user Account updates")


    async def stop_user_account_updates(self):
        print("STOPPED receiving user Account updates")


    async def close(self):
        # Properly close the client and socket manager
        if self.client_async:
            await self.client_async.close_connection()
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
            async_client = await cls._create_client_async(api_key=api_bin_key, api_secret=api_bin_secret, production_environment=production_environment)
            temp_bsm =  cls._create_socket_manager(async_client)
            cls._instances[key] = cls(async_client, temp_bsm)
            print(f"Binance Object created for account id: {account_id}  in {env} Environment ")

        return cls._instances[key]

    #TODDO: Need to update the method to handle exception handling and exponential back uff strategy
    @staticmethod
    async def _create_client_async(api_key:str, api_secret:str, production_environment: bool=False):
        async_client= None
        env = not production_environment
        try:
            async_client = await AsyncClient.create(api_key=api_bin_key, api_secret=api_bin_secret, testnet=env)
            print("\n ***************I AM CALLING THE BINANCE CLIENT********** ")
            return async_client
        except ClientConnectorDNSError:
            print("There is no internet for out local system. so unable to connect binance")
        # async_client = await asyncio.sleep(2)
        await async_client.close_connection()
        raise ConnectionError("Failed to connect to Binance after multiple retries.")
    @staticmethod
    def _create_socket_manager(client : AsyncClient):
        bsm =None
        bsm =  BinanceSocketManager(client)
        return bsm



async def test_binance():
    # test_client = await BinanceService.create_async(account_id="Hari", production_environment=False)
    # await test_client.close()
    # test_client.user_account.start_updates_async()
    # test_client.orders.start_updates_async()
    # test_client.ticker_data.start_updates_async()
    # test_client.socket_service.stop_user_account_updates()
    prod_client = await BinanceService.create_async(account_id="Hari", production_environment=True)
    print(f"Above prod client starting")
    await prod_client.start_user_account_updates_async()
    print(f"Below prod client starting")
    await prod_client.close()


    # server_objects.get_binance()
    # print(test_client)



if __name__ == "__main__":
    asyncio.run(test_binance())