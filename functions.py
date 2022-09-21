import socket, re, variables as v, requests as http, threading, time, json;
from datetime import datetime;
from playsound import playsound;
from tkinter import *;
from urllib import parse;

def initialize():
	log(1, 'Initializing');
	# launch display if system has a screen
	checkDisplay();
	if v.hasDisplay:
		# Initialise the Display winfow if system has a screen
		#v.displayThread = threading.Thread(target=display, name=v.keyword.capitalize()+" Personal assistant Display")
		#v.displayThread.start();
		# Initialise the status bar if enabled
		if v.displayStatusWindow:
			v.statusDisplayThread = threading.Thread(target=statusDisplay, name=v.keyword.capitalize()+" Status display")
			v.statusDisplayThread.start();
	# Check internet connection
	checkInternet(True);
	v.networkCheckThread = threading.Thread(target=monitorInternet, name="Internet monitor")
	v.networkCheckThread.start();
	# Check synthesizer connection
	checkSynth(True);
	v.synthCheckThread = threading.Thread(target=monitorSynth, name="Synthesizer monitor")
	v.synthCheckThread.start();
	# import the intents json file
	v.intentions = json.load(open('./scripts/intentions.json',));
	time.sleep(1)
	log(1, 'Initialized');
	playSound(1);

def takeCommand():
	log(0, 'Listening...');
	v.statusWindow.configure(bg=v.baseColour);
	with v.microphone as source:
		v.recognizer.adjust_for_ambient_noise(source)
		audio = v.recognizer.listen(source);
	try:
		log(0, 'Understanding...');
		v.statusWindow.configure(bg=v.statusbar_Thinking)
		statement = v.recognizer.recognize_google(audio, language="en-gb");
		v.statusWindow.configure(bg=v.statusbar_Success);
		log(0, 'heard: "'+statement+'"');
	except Exception:
		v.statusWindow.configure(bg=v.statusbar_Error)
		log(0, 'Nothing was said.');
		statement = "null";
	return statement;
def comprehend(statement):
	statement = statement.lower()
	log(0, 'Comprehending the spoken text: ' + statement);
	v.statusWindow.configure(bg=v.statusbar_Thinking);
	# Time
	if re.search("^(ava )?what*.+time*.+$", statement):
		speak('time/foreign');
	elif re.search("^(ava )?what*.+time*.+$", statement):
		speak('time/local');
	# Conversational
	elif re.search("^(ava )?how are you*.+$", statement):
		speak('conversational/wellbeing');
	# Null
	else:
		log(0, 'No text');
	log(0, 'comprehension complete');
def speak(script, filename="voice.wav"):
	open(filename, 'wb').write(http.get('http://localhost:5500/api/tts?voice=coqui-tts%3Aen_ljspeech&lang=en&vocoder=high&denoiserStrength=0.005&text='+parse.quote(readScript(script))+'&speakerId=p227&ssml=true&ssmlNumbers=true&ssmlDates=true&ssmlCurrency=true&cache=false').content);
	playsound(filename);
def playSound(id):
	log(1, 'Playing sound. ID: %s' % id);
	playsound('./tones/%s.wav' % id);

def readScript(fn, raw=False):
	with open('./scripts/'+fn+'.ssml') as f:
		text = f.read();
	if raw==False:
		text = text.replace('[var]localtime[/var]', time.strftime("%I %M %p"));
		if "[rand]" in text:
			text.replace('[rand]', '');
			phrases = text.split('[split]');
			print(phrases);
	return text;
def log(level, text, timestamp=datetime.now()):
	if level == 0:
		level="LOG: ";
	elif level == 1:
		level="INFO: ";
	elif level == 2:
		level="WARN: ";
	elif level == 3:
		level="ERROR: ";
	else:
		level="FATAL: ";
	line = "[" + timestamp.strftime("%A %d-%b-%Y %H:%M:%S") + "] " + level + text;
	print(line)
	open('./logs/log.txt', 'a').write(line+'\n');

def checkInternet(doLog):
	IPaddress=socket.gethostbyname(socket.gethostname())
	if IPaddress=="127.0.0.1":
		v.hasInternet = False;
		v.baseColour = 'orange';
		if doLog:
			log(2, 'Unable to connecto to the internet')
	else:
		v.hasInternet = True;
		v.baseColour = 'white';
		v.IPadress = IPaddress;
		if doLog:
			log(1, 'Successfully connected to the internet. IP Address: '+IPaddress)
def monitorInternet():
	while True:
		checkInternet(False);
def checkSynth(doLog):
	try:
		http.head('http://localhost:5500/',verify=False,timeout=5);
		v.statusWindow.configure(bg=v.baseColour);
		v.synthConnection = True;
		if doLog:
			log(1, 'Speech synthesizer connected successfully');
	except:
		v.statusWindow.configure(bg=v.statusbar_Error);
		v.synthConnection = False;
		if doLog:
			log(3, 'unable to connect to the speech synthesizer');
def monitorSynth():
	while True:
		checkSynth(False);
def checkDisplay():
	v.hasDisplay = True;
def display():
		v.window = Tk();
		v.window.title(v.keyword.capitalize() + ' Personal assistant');
		if v.fullscreen:
			v.window.attributes('-fullscreen',True);
		else:
			v.window.geometry("300x200+10+20");
		v.window.mainloop();
def statusDisplay():
		v.statusWindow = Tk();
		w = v.statusWindow.winfo_screenwidth(); h = 5;
		x = 0;
		y = v.statusWindow.winfo_screenheight()-52;
		v.statusWindow.geometry('%dx%d+%d+%d' % (w, h, x, y));
		v.statusWindow.overrideredirect(True);
		v.statusWindow.attributes('-topmost', 'true')
		v.statusWindow.mainloop();

def toggleActive(mode):
	if(mode):
		v.active = True;
		v.statusWindow.configure(bg=v.statusbar_Listening);
	else:
		v.active = False;
		v.statusWindow.configure(bg=v.statusbar_Base);