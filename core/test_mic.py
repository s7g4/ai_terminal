import speech_recognition as sr
import wave
import traceback

def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()
    print("Available audio devices:")
    for i, name in enumerate(mic_list):
        print(f"{i}: {name}")
    return mic_list

def find_analog_device(mic_list):
    for i, name in enumerate(mic_list):
        if 'alc3227' in name.lower() or 'analog' in name.lower():
            return i
    return None

def record_audio(device_index, duration=5, filename="test_record.wav"):
    recognizer = sr.Recognizer()
    audio = None
    try:
        try:
            with sr.Microphone(device_index=device_index) as source:
                print(f"Recording from device index {device_index} for {duration} seconds...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=duration)
                if audio is not None:
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())
                    print(f"Audio recorded and saved to {filename}")
                else:
                    print("No audio data captured.")
        except Exception as e:
            print(f"Error recording audio with device index {device_index}: {e}")
            traceback.print_exc()
            if device_index != 0:
                print("Trying default device index 0...")
                with sr.Microphone(device_index=0) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=duration)
                    if audio is not None:
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                        print(f"Audio recorded and saved to {filename} using default device")
                    else:
                        print("No audio data captured on default device.")
    except Exception as e:
        print(f"Error recording audio: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    mic_list = list_microphones()
    device_index = find_analog_device(mic_list)
    if device_index is None:
        print("No analog microphone device found. Using default device 0.")
        device_index = 0
    else:
        print(f"Selected analog microphone device index: {device_index}")
    record_audio(device_index)
