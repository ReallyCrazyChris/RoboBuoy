import csv
import sys
import asyncio
import bencode

from bleak import BleakScanner, BleakClient, BleakError
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

# All BLE devices have MTU of at least 23. Subtracting 3 bytes overhead, we can
# safely send 20 bytes at a time to any device supporting this service.
UART_SAFE_SIZE = 20

async def find(SERVICE_UUID) -> BLEDevice:

    def filter_by_uuid(device: BLEDevice, adv: AdvertisementData):
        '''Filters BLEDevice by the Servus UUID's in the Advertising Data'''
        #Servus UUID's must be specifically placed in the devices Advertising Data
        if SERVICE_UUID.lower() in adv.service_uuids:
            return True
        return False     

    return await BleakScanner.find_device_by_filter(filterfunc=filter_by_uuid,timeout=2000.0)
    

async def connect(device: BLEDevice, disconnect_Event: asyncio.Event) -> BleakClient:

    def disconnected_callback( client:BleakClient ):
        ''' called when the client disconnects'''
        disconnect_Event.set()

    client = BleakClient( device, disconnected_callback=disconnected_callback )
    
    await client.connect(timeout=5)

    return client


async def receiveTask(client: BleakClient):

    try:
        #open a file to write the data to
        file =  open('robobuoy.csv', 'w', newline='') 
        writer = csv.writer(file)

        def data_received_handler(data, conn_handle):
            print(data)
            writer.writerow(data)

        decodeChunk = bencode.decodeTransformer(data_received_handler,0) 

        def receive_handler(conn_handle: int, chunk: bytearray):
            decodeChunk(chunk)  

        while True:
            # receive notifications
            await client.start_notify(UART_TX_CHAR_UUID, receive_handler)

    except asyncio.CancelledError:
        print('receiveTask stopped')
    finally:
        file.close()


async def sendTask(client: BleakClient ):
    
    try:
        loop = asyncio.get_running_loop()
        print(' Disconnect - CTRL+D')
        while True:
            # This waits until you type a line and press ENTER.
            # A real terminal program might put stdin in raw mode so that things
            # like CTRL+C get passed to the remote device.
            data = await loop.run_in_executor(None, sys.stdin.buffer.readline)

            # data will be empty on EOF (e.g. CTRL+D on *nix)
            if not data:
                break

            #CTRL+D
            if data == b'\x04\r\n':
                break

            await client.write_gatt_char(UART_RX_CHAR_UUID, data)
            print("sent:", data)    

    except asyncio.CancelledError:
        print('sendTask stopped')

  


async def main():

    disconnect = asyncio.Event()

    while True:
        
        print('scanning for robobouy')
        device = await find( UART_SERVICE_UUID )
        print('connecting to robobouy')
        client = await connect( device, disconnect )
        print('connected to robobouy')

        receive_Task = asyncio.create_task( receiveTask( client ))
        send_Task = asyncio.create_task( sendTask( client ))

        # wait for the sendTask to complete, CTRL+D
        await send_Task
        # gracefully disconnect from the ble periferal
        print('disconncting from robobouy')
        await client.disconnect()
        # stop the receive task
        receive_Task.cancel()
        # end the program
        break
   
            
if __name__ == "__main__":
        asyncio.run(main())


    











