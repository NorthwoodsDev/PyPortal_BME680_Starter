import time, rtc, board, busio, displayio, terminalio, adafruit_bme680
from adafruit_display_text.label import Label
from adafruit_pyportal import PyPortal

# We turn off the display after 2 mins to save it from burn out
def AFKCheck(lastTick, isAFK):
    nowTick = time.monotonic()
    if (nowTick - lastTick) >= (60 * 2):
        isAFK = True
    else:
        isAFK = False
    return lastTick, isAFK

# Set PyPortal
pyportal = PyPortal()

# GUI Setup
display = board.DISPLAY
display.auto_brightness = False
display.brightness = 0.6
mainScreen = displayio.Group(max_size=2)
text_group = displayio.Group(max_size=5)

atextbox = Label(terminalio.FONT,text="Please",color=0xFFFFFF,background_color=0x000000,scale=2,max_glyphs=60,x=20,y=20)
text_group.append(atextbox)

btextbox = Label(terminalio.FONT,text="Wait",color=0xFFFFFF,background_color=0x000000,scale=2,max_glyphs=60,x=20,y=50)
text_group.append(btextbox)

ctextbox = Label(terminalio.FONT,text="Loading",color=0xFFFFFF,background_color=0x000000,scale=2,max_glyphs=60,x=20,y=80)
text_group.append(ctextbox)

dtextbox = Label(terminalio.FONT,text="Time",color=0xFFFFFF,background_color=0x000000,scale=2,max_glyphs=60,x=int(display.width/6),y=int(display.height-60))
text_group.append(dtextbox)

etextbox = Label(terminalio.FONT,text="Time",color=0xFFFFFF,background_color=0x000000,scale=2,max_glyphs=60,x=int(display.width/6),y=int(display.height-30))
text_group.append(etextbox)

mainScreen.append(text_group)
display.show(mainScreen)

# BME680 Setup
i2c = busio.I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False, refresh_rate=2)
bme680.sea_level_pressure = 1014.0

# AFK Vars
lastTick = time.monotonic()
isAFK = False

# Setup a dates 48 hours apart for our timer
dueDate = time.struct_time((2020, 1, 3, 0, 0, 0, 4, -1, -1))
r = rtc.RTC()
r.datetime = time.struct_time((2020, 1, 1, 0, 0, 0, 4, -1, -1))
start_timestamp = r.datetime

while True:
    try:
        touch = pyportal.touchscreen.touch_point

        # Calculate remaining time for timer
        current_time = r.datetime
        remaining = time.mktime(dueDate) - time.mktime(current_time)
        secs_remaining = remaining % 60
        remaining //= 60
        mins_remaining = remaining % 60
        remaining //= 60
        hours_remaining = remaining % 24
        remaining //= 24
        days_remaining = remaining

        lastTick, isAFK = AFKCheck(lastTick, isAFK)

        # The BME680 returns celsius so we need to convert it to fahrenheit
        tempF = (float(bme680.temperature) * 1.8) + 32
        atextbox.text = "Temperature: {0:.2f}f Humidity: {1:.2f}%".format(tempF, bme680.humidity)
        btextbox.text = "Pressure: {0:.2f}hPA Altitude: {1:.2f}".format(bme680.pressure, bme680.altitude)
        ctextbox.text = "Gas: {0:.2f}ohm".format(bme680.gas)

        #A timer for our GAS Sensor that needs 48 hours to be ready
        if remaining <= 0:
            while True:
                dtextbox.text = "Gas Sensor Burned In"
                etextbox.text = "Your BME680 is ready"
                #Make some noise to get your attention
                pyportal.play_file("/pyportal_startup.wav", wait_to_finish=True)
        else:
            dtextbox.text = "{} days, {} hours".format(days_remaining, hours_remaining)
            etextbox.text = "{} minutes and {} seconds".format(mins_remaining, secs_remaining)

        #Reset AFK timer on touch
        if touch:
            lastTick = time.monotonic()
            isAFK = False
            print("Touched!")

        #Not burn out our screen while we burn in the BME680
        if isAFK:
            display.brightness = 0
        else:
            display.brightness = 0.5

    except (ValueError, RuntimeError) as e:
        print("Error:", e)
        atextbox.text = "Error"