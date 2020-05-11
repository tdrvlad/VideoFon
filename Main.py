import RPi.GPIO as GPIO
from omxplayer.player import OMXPlayer
import time
import os, random
import subprocess

button_in = 17 
pwr_relay_out = 2
screen_relay_out = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwr_relay_out,GPIO.OUT)
GPIO.setup(screen_relay_out,GPIO.OUT)
GPIO.setup(button_in, GPIO.IN, GPIO.PUD_DOWN)

def play_music():

	#Randomly select mp3 file
	time.sleep(0.5)
	print('Playing Music...')

	randomfile = random.choice(os.listdir('/home/pi/Music/'))
	file = '/home/pi/Music/'+ randomfile

	music_player = OMXPlayer(file, args='-o local -b --vol -1850')
	
	time.sleep(music_player.duration())

def play_intro():
	
	print('Playing Intro...')

	play_music()
	
	#Killing previous processes
	bash_command = 'pkill omxplayer'
	import subprocess 
	process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate() 

	file = '/home/pi/Videos/Intro.mp4'
	
	#GPIO.output(screen_relay_out,GPIO.LOW)
	#time.sleep(1.6)
	intro_player = OMXPlayer(file, args='-o local -b --vol -1700 --win 0,0,800,600')
	time.sleep(1.3)
	GPIO.output(screen_relay_out,GPIO.LOW)
	#time.sleep(7)
	#GPIO.output(screen_relay_out,GPIO.HIGH)
	#intro_player.quit()
	
def button_callback(channel):
	
	bash_command = 'pkill omxplayer'
	import subprocess 
	process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate() 
	
	bash_command = 'pkill chromium'
	#import subprocess 
	process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate() 
		
	bash_command = 'python3 Sequence.py'
	#import subprocess 
	process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate() 

def get_config():
	global chat_id
	chat_id = 'VideoFonApelCuBunicii'

def make_call():
	print('Opening chat...')
	global chat_id
	#import imfortmation about wifi and jitsi call
	url = 'https://meet.jit.si/'
	command = 'chromium-browser --kiosk --disable-session-crashed-bubble --disable-infobars --disable-restore-session-state '
	bash_command = command + url + chat_id
	
	import subprocess 
	process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate() 

GPIO.output(pwr_relay_out,GPIO.LOW)

GPIO.add_event_detect(button_in,GPIO.RISING,callback=button_callback)

get_config()

time.sleep(5)


play_intro()

make_call()

message = input()

