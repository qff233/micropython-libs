import math.pi

class SerialServo:
    def __init__(self, uart, id, offset = 0):
        self.uart = uart
        self.id = id
        self.offset = offset
        self.move(offset, 1000)

    @staticmethod
    def check_sum(bufs):
        count = 0
        for buf in bufs:
            count += buf
        count = count & 0xFF
        return ~count

    # -120.0deg < rad < 120.0deg
    def move(self, rad, time):
        position = int (rad / math.radians(120.0) * 500 + 500 + self.offset)
        if position > 1000:
            position = 1000
        elif position < 0:
            position = 0
        position_low_byte = position & 0xFF
        position_high_byte = (position >> 8) & 0xFF
        time_low_byte = time & 0xFF
        time_high_byte = (time >> 8) & 0xFF
        buf = bytearray([0x55, 0x55, self.id, 7, 1, position_low_byte, position_high_byte, time_low_byte, time_high_byte])
        check = self.check_sum(buf[2:])
        buf.append(check)
        self.uart.write(buf)


