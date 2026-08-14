
import speech_recognition as sr

WAKE_WORD = "jarvis"


def listen_for_wake_word():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        while True:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower()

                if WAKE_WORD in text:
                    return

            except sr.UnknownValueError:
                continue
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Wake word listening error: {e}")
                continue