# Python Low Resolution Virtual Timer 
# Developed for ESP32 running on uPython platform 

#API :
	# To add a new Timer or to change an argument 
	# VirtualTimer.add( "TimerOne",period=5000,mode=ONE_SHOT,callback=TimeronCallback)
	# To remove a Timer 
	# VirtualTimer.remove("TimerOne")
	
#=======================================
#This platform use Timer 1 by default , this is a noneOOP module

from utime import ticks_diff , ticks_ms 
from machine import Timer 

_isChanging = False 
_virtualTimerStack = [] # nextTimeInt , mode , timerName , period , callback
def beginVirtualTimer(resolution,timer = -1 ):
	try:
		Timer(timer).deinit()
	except NameError:
		pass
	global _timer 
	_virtualTimer = Timer(-1).init(period=resolution, mode=Timer.PERIODIC, callback=_virtualTimerHandler)

def _virtualTimerHandler(a):
	if _isChanging == True : #avoid accidentally while in deleteTimer and this interrupt is call which may lead to list error
		return 
	global _virtualTimerStack
	nowTime = ticks_ms()
	for i in range(len(_virtualTimerStack)):
		if _virtualTimerStack[i][0] < nowTime:
			if _virtualTimerStack[i][1] == Timer.PERIODIC:
				_virtualTimerStack[i][0] = nowTime + _virtualTimerStack[i][3]
				#how to remove it ?
			_virtualTimerStack[i][4](1) #CallBack
			if _virtualTimerStack[i][1] == Timer.ONE_SHOT:
				_virtualTimerStack.pop(i) #remove the timer 
	_virtualTimerStack.sort()
def addTimer ( timerName , period , mode , callback):
	_isChanging = True
	global _virtualTimerStack
	if len(_virtualTimerStack) == 0:
		_virtualTimerStack.append([ticks_ms()+period,mode,timerName,period,callback])
	else:
		for i in range(len(_virtualTimerStack)):
			if _virtualTimerStack[i][2] == timerName:
				_virtualTimerStack[i][1] = mode
				_virtualTimerStack[i][3] = period
				_virtualTimerStack[i][4] = callback
			else :
				_virtualTimerStack.append([ticks_ms()+period,mode,timerName,period,callback])
			break
	_virtualTimerStack.sort()
	_isChanging = False 
def deleteTimer( timerName ):
	_isChanging = True 
	for i in range(len(_virtualTimerStack)):
		if _virtualTimerStack[i][2] == timerName:
			_virtualTimerStack.pop(i)
			break
	_isChanging = False 
		
