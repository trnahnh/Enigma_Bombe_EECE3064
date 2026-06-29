import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write
import os

# ─────────────────────────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────────────────────────
INPUT_FILE = "original_speech.wav"   # Place your WAV file here
OUTPUT_DIR = "."                      # Output folder
KEY        = 42                       # Secret key (any integer)


# ─────────────────────────────────────────────────────────────
# STEP 1: LOAD AUDIO
# ─────────────────────────────────────────────────────────────
def load_audio(filepath):
    sample_rate, data = wavfile.read(filepath)
    if data.ndim == 2:               # stereo → mono
        data = data.mean(axis=1)
    data = data.astype(np.float64)
    data /= np.max(np.abs(data))     # normalize to [-1, 1]
    return sample_rate, data


def generate_test_signal(duration=5, sample_rate=16000):
    """Synthetic speech-like signal for testing when no WAV file is available."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    signal = (0.5 * np.sin(2 * np.pi * 200  * t) +
              0.3 * np.sin(2 * np.pi * 500  * t) +
              0.2 * np.sin(2 * np.pi * 1000 * t) +
              0.1 * np.random.randn(len(t)))
    signal /= np.max(np.abs(signal))
    return sample_rate, signal


# ─────────────────────────────────────────────────────────────
# STEP 2: ENCRYPT
# ─────────────────────────────────────────────────────────────
def encrypt(signal, key):
    X = np.fft.fft(signal)                  # time → frequency domain
    N = len(X)
    rng     = np.random.default_rng(key)
    indices = rng.permutation(N)            # repeatable scramble pattern from key
    X_scrambled = X[indices]                # rearrange frequency components
    encrypted   = np.fft.ifft(X_scrambled).real   # back to time domain
    return encrypted, indices


# ─────────────────────────────────────────────────────────────
# STEP 3: DECRYPT
# ─────────────────────────────────────────────────────────────
def decrypt(encrypted_signal, indices):
    X_scrambled = np.fft.fft(encrypted_signal)
    N = len(X_scrambled)
    X_original = np.zeros(N, dtype=complex)
    X_original[indices] = X_scrambled       # reverse the scrambling
    decrypted = np.fft.ifft(X_original).real
    return decrypted


# ─────────────────────────────────────────────────────────────
# STEP 4: SAVE AUDIO
# ─────────────────────────────────────────────────────────────
def save_audio(filepath, sample_rate, signal):
    normalized = signal / np.max(np.abs(signal))
    scaled = np.int16(normalized * 32767)
    write(filepath, sample_rate, scaled)


# ─────────────────────────────────────────────────────────────
# STEP 5: PLOT RESULTS
# ─────────────────────────────────────────────────────────────
def plot_results(sample_rate, original, encrypted, decrypted,
                 output_path="results.png"):
    N     = len(original)
    t     = np.linspace(0, N / sample_rate, N)
    half  = N // 2
    freqs = np.fft.fftfreq(N, 1 / sample_rate)[:half]

    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    fig.suptitle("Speech Encryption and Decryption — Group 10",
                 fontsize=14, fontweight="bold")

    signals = [original,      encrypted,      decrypted]
    labels  = ["Original",    "Encrypted",    "Decrypted"]
    colors  = ["steelblue",   "crimson",      "seagreen"]

    for i, (sig, label, color) in enumerate(zip(signals, labels, colors)):
        # Time-domain waveform
        axes[i][0].plot(t, sig, color=color, linewidth=0.5)
        axes[i][0].set_title(f"{label} Speech — Time Domain")
        axes[i][0].set_xlabel("Time (s)")
        axes[i][0].set_ylabel("Amplitude")
        axes[i][0].set_xlim([0, t[-1]])

        # Frequency spectrum
        mag = np.abs(np.fft.fft(sig))[:half]
        axes[i][1].plot(freqs, mag, color=color, linewidth=0.5)
        axes[i][1].set_title(f"{label} Speech — Frequency Spectrum")
        axes[i][1].set_xlabel("Frequency (Hz)")
        axes[i][1].set_ylabel("Magnitude")
        axes[i][1].set_xlim([0, sample_rate // 2])

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Plot saved → {output_path}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Load audio or fall back to test signal
    if os.path.exists(INPUT_FILE):
        sample_rate, original = load_audio(INPUT_FILE)
        print(f"Loaded: {INPUT_FILE}")
    else:
        print(f"'{INPUT_FILE}' not found — using synthetic test signal.")
        sample_rate, original = generate_test_signal()

    print(f"Sample rate : {sample_rate} Hz")
    print(f"Samples     : {len(original)}")

    # Encrypt
    encrypted, scramble_indices = encrypt(original, KEY)
    print("Encryption complete.")

    # Decrypt
    decrypted = decrypt(encrypted, scramble_indices)
    print("Decryption complete.")

    # Save audio files
    save_audio(os.path.join(OUTPUT_DIR, "original_speech_out.wav"), sample_rate, original)
    save_audio(os.path.join(OUTPUT_DIR, "encrypted_speech.wav"),    sample_rate, encrypted)
    save_audio(os.path.join(OUTPUT_DIR, "decrypted_speech.wav"),    sample_rate, decrypted)
    print("Audio files saved: original_speech_out.wav, encrypted_speech.wav, decrypted_speech.wav")

    # Plot and save
    plot_results(sample_rate, original, encrypted, decrypted,
                 output_path=os.path.join(OUTPUT_DIR, "results.png"))
