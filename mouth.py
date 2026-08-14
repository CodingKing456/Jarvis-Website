

import os
import time
import asyncio
import tempfile
import edge_tts
import pygame

VOICE = "en-GB-RyanNeural"
def speak(text):
    print(f"Jarvis: {text}")

    async def _generate_and_play():
        pygame.mixer.init()

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                audio_path = fp.name

            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(audio_path)

            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.wait(10)

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.quit()

            time.sleep(0.1) 
            if os.path.exists(audio_path):
                os.remove(audio_path)

        except Exception as e:
            print(f"Speech error: {e}")

    asyncio.run(_generate_and_play())
