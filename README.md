# PyPortal_BME680_Starter
Starter App for a PyPortal and BME680 sensor
</BR>
Coded on a PyPortal Titano and STEMMA Connected BME680. The BME680 sensor host temperature, humidity,</BR>
barometric pressure and VOC gas sensors. Reading over the documentation we find, "We recommend that you run</BR>
this sensor for 48 hours when you first receive it to "burn it in", and then 30 minutes in the desired mode</BR>
every time the sensor is in use."</BR>
</BR>
I created this App to complete the 48 hour burn in of the VOC gas sensor. It will countdown 48 hours and alert</BR>
you once done.</BR>
</BR>
Code is easy to follow and modify for use on any PyPortal. Change the "scale=" on Labels!</BR>
</BR>
--Reqiured Libraries--</BR>
Adafruit_bitmap_font</BR>
Adafruit_bus_device</BR>
Adafruit_display_text</BR>
Adafruit_esp32spi</BR>
Adafruit_io</BR>
Adafruit_bme680</BR>
Adafruit_pyportal</BR>
Adafruit_requests</BR>
Adafruit_sdcard</BR>
Adafruit_touchscreen</BR>
neopixel</BR>
