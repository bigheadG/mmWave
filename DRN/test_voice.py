import numpy as np
import sounddevice as sd

f = 3000
duration = 10
sample_rate = 44100

print("start")

t = np.linspace(0, 10, int(sample_rate * duration), endpoint=False)

tone = 0.5 * np.sin(2 * np.pi * f * t)
sd.play(tone, sample_rate)
sd.wait()

'''
audio = (tone * 32767).astype(np.int16)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels = 1, rate = sample_rate, output = True )

stream.write(audio.tobytes())

stream.stop_stream()
stream.close()

p.terminate()
'''
print("end")


