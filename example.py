import VirtualTimer
import utime

from machine import Timer

def do_something(timer):
	print(timer,utime.ticks_ms())
  
VirtualTimer.beginVirtualTimer(10)

VirtualTimer.addTimer("sayHi" , mode = Timer.PERIODIC,callback = do_something , period = 400)


while True :
	if utime.ticks_ms () > 200000:
		VirtualTimer._virtualTimerStack.clear()
		#VirtualTimer.deleteTimer("sayHi")
