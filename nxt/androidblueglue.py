# bluetooth.py module -- Glue code from NXT_Python to Android API
# via pyjnius to tun on android devices.  Supports subset of
# PyBluez/bluetooth.py used by NXT_Python.
#
# Copyright (C) 2015 Rupert Lloyd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from jnius import autoclass

RFCOMM=11

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
# BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket') THIS MAY BE WRONG DONT TRUST ME
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
            paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
            for device in paired_devices:
                if device.getAddress() == addr:
                    self._sock = device.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
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

