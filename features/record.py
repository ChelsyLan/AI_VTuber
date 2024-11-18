import keyboard
import pyaudio
import wave

def _wait_until_key_pressed():
    while True:
        if keyboard.is_pressed('RIGHT_SHIFT'):
            break

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "input.wav"
    
    print("Press and Hold Right Shift to record audio")
    _wait_until_key_pressed()
    
    print("Recording...")
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    
    while keyboard.is_pressed('RIGHT_SHIFT'):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Stopped recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    ### Write recorded frames as a wave file ###
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
