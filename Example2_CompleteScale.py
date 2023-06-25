import qwiicscale_esp32, time

myScale = qwiicscale_esp32.NAU7802() # Create instance of the NAU7802 class

# Create an array to take average of weights. This helps smooth out jitter.
AVG_SIZE = 4
avgWeights = []
avgWeightSpot = 0

# Gives user the ability to set a known weight on the scale and calculate a calibration factor
def calibrateScale():
    print('')
    print('')
    print('Scale calibration')
    
    _ = input('Setup scale with no weight on it. Press a key when ready.')

    myScale.calculateZeroOffset(64)    # Zero or Tare the scale. Average over 64 readings.
    print('New zero offset: ', myScale.getZeroOffset())

    _ = input('Place known weight on scale. Press a key when weight is in place and stable.')

    weightOnScale = input("Please enter the weight, without units, currently sitting on the scale (for example '4.25'): ")
    print('')

    myScale.calculateCalibrationFactor(float(weightOnScale), 64)    # Tell the library how much weight is currently on it
    print('New cal factor: ', round(myScale.calibrationFactor, 2))

    print('New Scale Reading: ', round(myScale.getWeight(), 2))

#
# Begin void setup() equivalent
#

print('Qwiic Scale Example')

if not myScale.begin():
    print('Scale not detected. Please check wiring. Freezing...')
    while True:
        pass

print('Scale detected!')

myScale.setSampleRate(qwiicscale_esp32.NAU7802_SPS_Values['NAU7802_SPS_320'])    # Increase to max sample rate
myScale.calibrateAFE()    # Re-cal analog front end when we change gain, sample rate, or channel

print('Zero offset: ', myScale.getZeroOffset())
print('Calibration factor: ', myScale.calibrationFactor)

#
# Begin void loop() equivalent
#

while True:
    
    if myScale.available():
        currentReading = myScale.getReading()
        currentWeight = myScale.getWeight()
        
        print('Reading: ', currentReading, end = '')
        print('\tWeight: ', round(currentWeight, 2), end = '')    # Print 2 decimal places
        
        avgWeights.append(currentWeight)
        if len(avgWeights) == AVG_SIZE:
            avgWeights.pop(0)
        
        avgWeight = 0
        for x in range(len(avgWeights)):
            avgWeight += avgWeights[x]
        avgWeight /= AVG_SIZE
        
        print('\tAvgWeight: ', round(avgWeight, 2))    # Print 2 decimal places
        
        r = input('Calibrate (c), Tare (t), or Read (r) ')
        if r == 'c':
            calibrateScale() # Calibrate
        elif r == 't':
            myScale.calculateZeroOffset(64) # Tare the scale
        
        print('')
        time.sleep(2)
