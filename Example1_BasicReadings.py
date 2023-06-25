import qwiicscale_esp32, time

myScale = qwiicscale_esp32.NAU7802()

if myScale.begin():
    while True:
        currentReading = myScale.getReading()
        print('Reading: ' + str(currentReading))
        time.sleep(2)