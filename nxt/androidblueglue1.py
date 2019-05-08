
import kivy
from jnius import autoclass
from jnius import cast

RFCOMM=11

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')

def discover_devices(lookup_names=False):  # parameter is ignored
    "return a list of pairs of (MACaddress,Name)"
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    pairs = []
    for device in paired_devices:
        h = device.getAddress()
        n = device.getName()
        pairs.append((h, n))
        print(h,n)
    return pairs

class BluetoothSocket:

    def __init__(self, proto = RFCOMM, _sock=None):
        self._sock = _sock

    def connect(self, addrport):
        print('connect')
        addr, port = addrport
        print(addr,port)
        if self._sock is None:
            btAdapter = BluetoothAdapter.getDefaultAdapter(); 
            paired_devices = btAdapter.getBondedDevices().toArray()
            for device in paired_devices:
                if device.getAddress() == addr:
#                	socket = device.getClass().getMethod("createRfcommSocket", new Class[] {int.class}).invoke(device,1)
#                	self._sock = cast("BluetoothSocket", socket)
                    try:
                        self._sock = device.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805f9b34fb"))
                    except:
                        print("Socket error")
                    try:
                        self._sock.connect();
                        print("Connected")
                    except:
                        print("Fallback")
                        self._sock = cast(android.bluetooth.BluetoothSocket,
                                                        device.getClass().getMethod("createRfcommSocket", new Class[] {int.class}).invoke(device,1))
                        self._sock.connect()
    def send(self, data):
        print('send',data)
        send_stream = self._sock.getOutputStream()
        return send_stream.write( data )

    def recv(self, numbytes):
        print('recv')
        buffer = [0 for b in range(1024)]
        if numbytes is None:
            numbytes = 1024

        recv_stream = self._sock.getInputStream()
        nbytes = recv_stream.read(buffer,0,numbytes)
        if nbytes > 0:
            print(buffer[:nbytes])
            return ''.join(chr(d & 0xFF) for d in buffer[:nbytes])
        else:
            return ''
    
    def close(self):
        return self._sock.close()
    
class BluetoothError(IOError):
    pass    

