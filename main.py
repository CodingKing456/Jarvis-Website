

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

import time
from core import JarvisCore
from ear import listen
from wakeword import listen_for_wake_word

COMMAND_TIMEOUT = 10  # seconds of silence before Jarvis returns to standby


def main():
    print("Jarvis activated.")
    jarvis = JarvisCore()

    while True:
        listen_for_wake_word()  # blocks until "jarvis" is heard

        jarvis.wake()
        last_activity = time.time()

        while jarvis.active:
            query = listen()

            if not query:
                if time.time() - last_activity > COMMAND_TIMEOUT:
                    jarvis.sleep()
                    break
                continue

            last_activity = time.time()
            jarvis.handle(query)


if __name__ == "__main__":
    main()
