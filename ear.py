

import os
import numpy as np
import speech_recognition as sr
from resemblyzer import VoiceEncoder, preprocess_wav

OWNER_VOICE_PATH = "./voices/owner.wav"
MATCH_THRESHOLD = 0.50

if not os.path.exists(OWNER_VOICE_PATH):
    print("\nCRITICAL ERROR: 'voices/owner.wav' is missing!")
    print("Record a 5-10 second clip of your voice, name it 'owner.wav', "
          "and put it in the 'voices' folder.\n")
    raise FileNotFoundError("Owner voice profile not found.")

print("Loading voice recognition engine...")
encoder = VoiceEncoder(device="cpu")
owner_wav = preprocess_wav(OWNER_VOICE_PATH)
owner_embedding = encoder.embed_utterance(owner_wav)
print("Voice recognition active! Jarvis will only respond to the owner's voice.")


def verify_owner(audio, threshold=MATCH_THRESHOLD):
    temp_path = "temp_voice.wav"
    with open(temp_path, "wb") as f:
        f.write(audio.get_wav_data())

    try:
        wav = preprocess_wav(temp_path)
        speaker_embedding = encoder.embed_utterance(wav)

        similarity = np.dot(owner_embedding, speaker_embedding)
        print(f"Voice match score: {similarity:.2f}")

        return similarity >= threshold

    except Exception as e:
        print(f"Voice verification error: {e}")
        return False

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.0

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=6)

            if not verify_owner(audio):
                print("Unauthorized voice detected - command ignored.")
                return ""

            text = recognizer.recognize_google(audio).lower()
            print(f"Owner said: {text}")
            return text

        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"Listening error: {e}")
            return ""
