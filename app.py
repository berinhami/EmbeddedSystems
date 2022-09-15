import RPi.GPIO as GPIO
from time import sleep
import threading
from flask import Flask, render_template, request
app = Flask(__name__)


global cycleAll
cycleAll = False

GPIO.setmode(GPIO.BCM)

# Store pins in directory
pins = {
   23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW},
   24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW},
   25 : {'name' : 'GPIO 25', 'state' : GPIO.LOW}
   }

# Set pins to off:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
   # store pin state in dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Put the pin dictionary into the template data dictionary, dont really need this
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html
return render_template('main.html', **templateData)


@app.route("/<changePin>/<action>")
def action(changePin, action):

   changePin = int(changePin)
   deviceName = pins[changePin]['name']

   def start_loop():
      while cycleAll == True:
         if stopthreads:
            break

         GPIO.output(23, GPIO.HIGH)
         sleep(5)
         if stopthreads:
            break
         GPIO.output(23, GPIO.LOW)
         GPIO.output(24, GPIO.HIGH)
         sleep(5)
         if stopthreads:
            break
         GPIO.output(24, GPIO.LOW)
         GPIO.output(25, GPIO.HIGH)
         sleep(5)
         if stopthreads:
            break
         GPIO.output(25, GPIO.LOW)

   # declare global
   global stopthreads
   stopthreads = False
   thread = threading.Thread(target=start_loop)

   # turn off all pins
   for pin in pins:
      GPIO.output(pin, GPIO.LOW)

   if action == "on":
      GPIO.output(changePin, GPIO.HIGH)
      message = "Turned " + deviceName + " on."

   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   if action == "alloff":
      #stop loop and set global to true, turn off pins before moving on
      cycleAll = False
      stopthreads = True
      for pin in pins:
         GPIO.output(pin, GPIO.LOW)

   if action == "cycle":
      cycleAll = True
      thread.start()

   # store state again
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # store message, dont really need this
   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
