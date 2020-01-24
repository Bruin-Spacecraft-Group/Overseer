# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from digi.xbee.devices import XBeeDevice
import cutdown as cd

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM1"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600
CUTDOWN_VALUE = 99   # Value indicating to cutdown balloon
SAFE_VALUE = 0       # Value indicating to not cutdown

def main():

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        def data_receive_callback(xbee_message):
            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                     xbee_message.data.decode()))
            message = xbee_message.data.decode()
            if message == "cutdown":
                print("CUTTING DOWN THE BALLOON\N")
                cd.cut_down()
            else:
                return SAFE_VALUE

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
