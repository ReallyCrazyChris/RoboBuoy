import uasyncio as asyncio
import ubluetooth
from transport import bencode


class BLEUART():
    '''Bluetooth Low Energy - Nordic UART Service (NUS)'''

    _instance = None # is a singleton
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self, name="RoboBuoy"):   
        self.mtu = 20 
        self.name = name
        self.message = None
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertise()
        self.is_connected = False

        # Asyncrouns Flags that are emitted
        self.connect_flag     =  asyncio.ThreadSafeFlag()
        self.disconnect_flag  =  asyncio.ThreadSafeFlag()
        self.exchange_mtu_flag =  asyncio.ThreadSafeFlag()
        self.received_flag     =  asyncio.ThreadSafeFlag()

        # A resource lock for BLEUART
        self.lock = asyncio.Lock()
        # A b-encode decode Transformer
        self.decoder = bencode.decodeTransformer(self.message_received,0)     
        
    def message_received(self, result, conn_handle):
        self.message = result
        self.received_flag.set()
        

    def ble_irq(self, event, data):
        ''' handles incomeing ble events and their data'''

        if event == 1:
            '''CENTRAL_CONNECT'''
            self.is_connected = True
            self.connect_flag.set()

 
        elif event == 2:
            '''CENTRAL_DISCONNECT'''
            self.advertise()
            self.is_connected = True
            self.disconnect_flag.set()
            
      
        elif event == 3:
            '''GATTS_WRITE message received'''            
            chunk = self.ble.gatts_read(self.rx)
            self.decoder(chunk)

        elif event == 21:
            '''MTU Exchanged'''
            _handler, mtu  = data            
            self.mtu = mtu or 20  
            self.exchange_mtu_flag.set()

    def register(self):        
        ''' Constructs a Nordic UART Service (NUS) '''
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def advertise(self):
        ''' advertises the robobouy by name and servive UUID on the ble network'''
        name = bytes("RoboBuoy", 'UTF-8')
        service = bytes(ubluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E"))
        self.ble.gap_advertise(100, bytearray(b'\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name + bytearray((len(service) + 1, 0x07)) + service)        


    async def notify(self, data):
        ''''notifies the client by sending the data in bencode format in mtu chunks'''

        if len(data) == 0:
            return False

        generator = bencode.encodeTransformer(data,self.mtu)
        
        for chunk in generator:
            try:
                self.ble.gatts_notify(0, self.tx, chunk )
                await asyncio.sleep_ms(15)
            except OSError:
                pass
        return True

    def disconnect(self):
        ''' disconnects the client'''
        self.ble.gap_disconnect(0)
      

        




   