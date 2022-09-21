from asyncio.windows_events import NULL
import functions as f, speech_recognition as sr;

# General config
keyword = "Nero";

# Speech recognition
RequestError = sr.RequestError;
UnknownValueError = sr.UnknownValueError;

recognizer = sr.Recognizer();
recognizer.energy_threshold = 500;
recognizer.pause_threshold = 0.5;
recognizer.operation_timeout = 2;

microphone = sr.Microphone();

# Display
hasDisplay = False;
fullscreen = True;
window = NULL;
displayThread = NULL;

# Testing
displayStatusWindow = True;
statusWindow = NULL;
statusDisplayThread = NULL;

#Status bar colours
statusbar_Base = 'white';
statusbar_Listening = 'blue';
statusbar_Thinking = 'orange';
statusbar_Functioning = 'grey';
statusbar_Success = 'green';
statusbar_Error = 'red';


# Internal config
active = False;
hasInternet = True;
synthConnection = False;