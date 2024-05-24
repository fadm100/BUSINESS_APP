def EVCharge(actualBatteryCapacity, minimumBatteryCapacity):
    if actualBatteryCapacity < minimumBatteryCapacity:
        stop = True
    else:
        stop = False
    return stop