# PowerShell script to set up audio for JARVIS on Windows
# Equivalent to setup_audio.sh for Linux

Write-Host "Setting up audio configuration for JARVIS on Windows..."

# Check for WASAPI support (Windows Audio Session API)
Write-Host "Checking for WASAPI support..."
$wasapiCheck = Get-Command -Name "powershell" -ErrorAction SilentlyContinue
if ($wasapiCheck) {
    Write-Host "WASAPI is available via PowerShell."
} else {
    Write-Host "WASAPI not detected. Ensure Windows Audio services are running."
}

# List available audio devices
Write-Host "Listing available audio input devices..."
try {
    Add-Type -AssemblyName System.Speech
    $recognizer = New-Object System.Speech.Recognition.SpeechRecognizer
    $audioDevices = [System.Speech.Recognition.SpeechRecognitionEngine]::InstalledRecognizers()
    if ($audioDevices.Count -gt 0) {
        Write-Host "Available speech recognizers:"
        $audioDevices | ForEach-Object { Write-Host " - $($_.Name)" }
    } else {
        Write-Host "No speech recognizers found. Install Windows Speech Recognition."
    }
} catch {
    Write-Host "Error listing audio devices: $_"
}

# Recommend installing sounddevice or PyAudio if needed
Write-Host "For advanced audio handling, ensure 'sounddevice' is installed via pip."
Write-Host "If using PyAudio, download the wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio"

# Test microphone access
Write-Host "Testing microphone access..."
try {
    $speechRecognizer = New-Object System.Speech.Recognition.SpeechRecognizer
    $speechRecognizer.SetInputToDefaultAudioDevice()
    Write-Host "Microphone access successful."
} catch {
    Write-Host "Microphone access failed: $_"
    Write-Host "Ensure microphone permissions are granted in Windows Settings > Privacy & Security > Microphone."
}

Write-Host "Audio setup complete. Reboot recommended if changes were made."
