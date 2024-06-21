import pyttsx3
import pyaudio
import wave

def text_to_speech(text, filename):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

def play_audio(filename):
    chunk = 1024  # 1 KB buffer size

    # Open the WAV file
    wf = wave.open(filename, 'rb')

    # Create an audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks and play
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

# Convert text to speech and save to a file
text = "Alert! Alert! Alert! Immediate attention needed: A person may have encountered an issue. Please check on them right away.\n" * 3
print(text)
output_filename = "output.wav"
text_to_speech(text, output_filename)

# Play the generated audio file
play_audio(output_filename)

