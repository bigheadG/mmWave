import pyttsx3

def text_to_speech(text, filename):
    # Initialize pyttsx3 with a valid driver for Ubuntu (e.g., 'espeak')
    engine = pyttsx3.init(driverName='espeak')  # Adjust driverName as necessary

    # Set properties (optional)
    engine.setProperty('rate', 150)    # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1

    # Save the text to speech as a WAV file
    engine.save_to_file(text, filename)
    engine.runAndWait()

# Convert text to speech and save to a file
text = "Alert! Alert! Alert! Immediate attention needed: A person may have encountered an issue. Please check on them right away.\n" * 3
output_filename = "output.wav"
text_to_speech(text, output_filename)
