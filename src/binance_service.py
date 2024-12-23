# from object_manager import server_objects
import asyncio
import json
import time

from aiohttp import ClientConnectorDNSError
from binance import AsyncClient, BinanceSocketManager


api_bin_key ="abcdef"
api_bin_secret = "abc"

class UserAccount:
    """
    { 'e' : 'executionReport'    ====>   order details
     'e' : 'outboundAccountPosition'   ===>
     'e': 'error',
            type - BinanceWebsocketClosed
    """
    def __init__(self, bsm:BinanceSocketManager):
        self._started:bool = False
        self._bsm = bsm
        self._user_socket = self._bsm.user_socket()
        self._manual_context= None
        self._task = None



    async def start_updates_async(self):
        if not self._started:
            self._started = True
            self._manual_context = await self._user_socket.__aenter__()
            self._task = asyncio.create_task(self._receive_updates_async())
            print("Immediatly going out of  start updes. But continue receiving the updates")




    async def _receive_updates_async(self):
        num = 1

        while self._started:
            print(f"*======ENTRY :{num}========")
            res = await self._manual_context.recv()

            print(f"Hello - {res}")
            parsed_message = json.loads(res)
            if parsed_message.get("e") == "error":
                if parsed_message.get("type") == "BinanceWebsocketClosed":
                    await asyncio.sleep(5)
                    self._user_socket = self._bsm.user_socket()




            await asyncio.sleep(1)
            num = num + 1


    async def stop_updates_async(self):
        if self._started:
            self._started=False
            # await self._manual_context.__aexit__(None, None, None)
            # if self._manual_context:
            #     await self._manual_context.close()

            if self._manual_context:
                try:
                    # Explicitly close the WebSocket connection
                    await self._manual_context.close()
                except AttributeError:
                    # If `close` is not implemented, ignore the error
                    print("The WebSocket context does not support explicit close.")
                except Exception as e:
                    print(f"Error while closing WebSocket: {e}")
                finally:
                    # Ensure the context manager exits cleanly
                    await self._manual_context.__aexit__(None, None, None)

            if self._task:
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    print("Task was cancelled successfully.")












class BinanceService:
    _instances = {}  # Class-level dictionary to store unique instances
    def __init__(self, async_client, bsm:BinanceSocketManager):
        self.client_async = async_client  # Instance variable assigned the constructor variable
        self.bsm =  bsm
        self.user_account =None

        print("Binance service got Initialized ")




    async def start_user_account_updates_async(self):
        if not self.user_account:
            self.user_account = UserAccount(self.bsm)
        await self.user_account.start_updates_async()

        print("STARTED receiving user Account updates")


    async def stop_user_account_updates_async(self):
        if self.user_account:
            await self.user_account.stop_updates_async()
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
        bsm =  BinanceSocketManager(client, user_timeout=540)   # user_timeout value is based on seconds  ==   9 * 60 seconds = 540 seconds =  9 minnutes
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
    print("I came back.  Updates will be receiving continuioulsy for 60 seconds....")
    await asyncio.sleep(20*60)
    await prod_client.stop_user_account_updates_async()
    print("Going to stop the client")

    print(f"Below prod client starting")
    await prod_client.close()


    # server_objects.get_binance()
    # print(test_client)



if __name__ == "__main__":
    asyncio.run(test_binance())
