import board
import time
i2c = board.I2C()
device_address = 0x2A
register_address = 0x03 # Channel 1 OFFSET register
value = bytearray([0x12])
while not i2c.try_lock():
    pass
i2c.writeto(device_address, bytes([register_address]) + value)
time.sleep(0.1)
buffer = bytearray(1)
i2c.writeto(device_address, bytes([register_address]))
i2c.readfrom_into(device_address, buffer)
i2c.unlock()
print("Read back:", buffer[0])

# Success if 18 is printed to serial console