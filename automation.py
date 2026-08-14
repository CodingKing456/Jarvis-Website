
import os
import platform
import webbrowser
import urllib.parse

try:
    from ctypes import cast, POINTER
    from comtypess import CLSCTX_ALL  
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    VOLUME_AVAILABLE = True
except ImportError:
    VOLUME_AVAILABLE = False


def run_os_command(commands):
    system = platform.system()
    if system in commands:
        os.system(commands[system])

#  SYSTEM CONTROLS

def lock_computer():
    try:
        run_os_command({
            "Windows": "rundll32.exe user32.dll,LockWorkStation",
            "Linux": "loginctl lock-session",
            "Darwin": """/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend"""
        })
    except Exception as e:
        print(f"Lock error: {e}")


def shutdown_computer():
    try:
        run_os_command({
            "Windows": "shutdown /s /t 0",
            "Linux": "shutdown now",
            "Darwin": "sudo shutdown -h now"
        })
    except Exception as e:
        print(f"Shutdown error: {e}")


def restart_computer():
    try:
        run_os_command({
            "Windows": "shutdown /r /t 0",
            "Linux": "reboot",
            "Darwin": "sudo reboot"
        })
    except Exception as e:
        print(f"Restart error: {e}")


def sleep_computer():
    try:
        run_os_command({
            "Windows": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0",
            "Linux": "systemctl suspend",
            "Darwin": "pmset sleepnow"
        })
    except Exception as e:
        print(f"Sleep error: {e}")



#WEB ACTIONS
def open_google():
    webbrowser.open("https://www.google.com")


def open_youtube():
    webbrowser.open("https://www.youtube.com")


def search_google(query):
    query = urllib.parse.quote(query)
    webbrowser.open(f"https://www.google.com/search?q={query}")


def search_youtube(query):
    query = urllib.parse.quote(query)
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")


#VOLUME CONTROL

def get_volume_interface():
    if not VOLUME_AVAILABLE:
        return None

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )
    return cast(interface, POINTER(IAudioEndpointVolume))


def set_volume(percent):
    system = platform.system()

    #  MAC VOLUME
    if system == "Darwin":
        percent = max(0, min(100, percent))
        os.system(f"osascript -e 'set volume output volume {percent}'")
        return

    # WINDOWS VOLUME
    if not VOLUME_AVAILABLE:
        return

    try:
        percent = max(0, min(100, percent))
        volume = get_volume_interface()
        volume.SetMasterVolumeLevelScalar(percent / 100, None)
    except Exception as e:
        print(f"Volume error: {e}")


def mute_volume():
    system = platform.system()

    if system == "Darwin":
        os.system("osascript -e 'set volume output muted true'")
        return

    if not VOLUME_AVAILABLE:
        return

    try:
        get_volume_interface().SetMute(1, None)
    except Exception as e:
        print(f"Mute error: {e}")


def unmute_volume():
    system = platform.system()

    if system == "Darwin":
        os.system("osascript -e 'set volume output muted false'")
        return

    if not VOLUME_AVAILABLE:
        return

    try:
        get_volume_interface().SetMute(0, None)
    except Exception as e:
        print(f"Unmute error: {e}")


def volume_up():
    system = platform.system()

    if system == "Darwin":
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
        return

    if not VOLUME_AVAILABLE:
        return

    try:
        volume = get_volume_interface()
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
    except Exception as e:
        print(f"Volume up error: {e}")


def volume_down():
    system = platform.system()

    if system == "Darwin":
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
        return

    if not VOLUME_AVAILABLE:
        return

    try:
        volume = get_volume_interface()
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
    except Exception as e:
        print(f"Volume down error: {e}")