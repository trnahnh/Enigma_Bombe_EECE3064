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
# Scramble only positive frequencies and mirror (conjugate symmetry).
# This ensures IFFT produces a true real signal with no information loss.
# ─────────────────────────────────────────────────────────────
def encrypt(signal, key):
    X = np.fft.fft(signal)
    N = len(X)
    M = N // 2 - 1                          # number of positive freq bins to scramble

    rng  = np.random.default_rng(key)
    perm = rng.permutation(M)               # permutation of [0, 1, ..., M-1]

    X_scrambled = X.copy()
    X_scrambled[1:N//2] = X[perm + 1]      # rearrange positive frequencies
    X_scrambled[N//2+1:] = np.conj(X_scrambled[1:N//2][::-1])  # mirror → real output

    encrypted = np.fft.ifft(X_scrambled).real
    return encrypted, perm


# ─────────────────────────────────────────────────────────────
# STEP 3: DECRYPT
# ─────────────────────────────────────────────────────────────
def decrypt(encrypted_signal, perm):
    X_enc = np.fft.fft(encrypted_signal)
    N     = len(X_enc)

    inv_perm = np.argsort(perm)             # inverse permutation

    X_dec = X_enc.copy()
    X_dec[1:N//2] = X_enc[inv_perm + 1]    # restore original frequency order
    X_dec[N//2+1:] = np.conj(X_dec[1:N//2][::-1])  # mirror

    decrypted = np.fft.ifft(X_dec).real
    return decrypted


# ─────────────────────────────────────────────────────────────
# STEP 4: SNR CALCULATION
# ─────────────────────────────────────────────────────────────
def compute_snr(original, recovered):
    min_len      = min(len(original), len(recovered))
    original     = original[:min_len]
    recovered    = recovered[:min_len]
    noise        = original - recovered
    signal_power = np.mean(original ** 2)
    noise_power  = np.mean(noise ** 2)
    if noise_power == 0:
        return float('inf')
    return 10 * np.log10(signal_power / noise_power)


# ─────────────────────────────────────────────────────────────
# STEP 5: WRONG KEY TEST
# ─────────────────────────────────────────────────────────────
def wrong_key_test(encrypted, correct_perm, wrong_key, sample_rate, output_dir):
    N = len(encrypted)
    M = N // 2 - 1

    wrong_perm     = np.random.default_rng(wrong_key).permutation(M)
    wrong_inv_perm = np.argsort(wrong_perm)

    X_enc   = np.fft.fft(encrypted)
    X_wrong = X_enc.copy()
    X_wrong[1:N//2]  = X_enc[wrong_inv_perm + 1]
    X_wrong[N//2+1:] = np.conj(X_wrong[1:N//2][::-1])
    wrong_decrypted  = np.fft.ifft(X_wrong).real

    save_audio(os.path.join(output_dir, "wrong_key_attempt.wav"), sample_rate, wrong_decrypted)

    # Recompute correct decryption for plot
    inv_perm   = np.argsort(correct_perm)
    X_correct  = X_enc.copy()
    X_correct[1:N//2]  = X_enc[inv_perm + 1]
    X_correct[N//2+1:] = np.conj(X_correct[1:N//2][::-1])
    correct_dec = np.fft.ifft(X_correct).real

    t   = np.linspace(0, N / sample_rate, N)
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    fig.suptitle("Decryption: Correct Key vs Wrong Key — Group 10",
                 fontsize=13, fontweight="bold")

    axes[0].plot(t, correct_dec, color="seagreen", linewidth=0.5)
    axes[0].set_title("Correct Key — Recovered Speech")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Amplitude")
    axes[0].set_xlim([0, t[-1]])

    axes[1].plot(t, wrong_decrypted, color="darkorange", linewidth=0.5)
    axes[1].set_title("Wrong Key — Still Noise")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Amplitude")
    axes[1].set_xlim([0, t[-1]])

    plt.tight_layout()
    path = os.path.join(output_dir, "wrong_key_test.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Wrong key test plot saved → {path}")
    print("Audio saved → wrong_key_attempt.wav  (should sound like noise)")


# ─────────────────────────────────────────────────────────────
# STEP 6: SAVE AUDIO
# ─────────────────────────────────────────────────────────────
def save_audio(filepath, sample_rate, signal):
    normalized = signal / np.max(np.abs(signal))
    scaled = np.int16(normalized * 32767)
    write(filepath, sample_rate, scaled)


# ─────────────────────────────────────────────────────────────
# STEP 7: PLOT RESULTS
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
        axes[i][0].plot(t, sig, color=color, linewidth=0.5)
        axes[i][0].set_title(f"{label} Speech — Time Domain")
        axes[i][0].set_xlabel("Time (s)")
        axes[i][0].set_ylabel("Amplitude")
        axes[i][0].set_xlim([0, t[-1]])

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
    if os.path.exists(INPUT_FILE):
        sample_rate, original = load_audio(INPUT_FILE)
        print(f"Loaded: {INPUT_FILE}")
    else:
        print(f"'{INPUT_FILE}' not found — using synthetic test signal.")
        sample_rate, original = generate_test_signal()

    print(f"Sample rate : {sample_rate} Hz")
    print(f"Samples     : {len(original)}")

    # Encrypt
    encrypted, perm = encrypt(original, KEY)
    print("Encryption complete.")

    # Decrypt
    decrypted = decrypt(encrypted, perm)
    print("Decryption complete.")

    # SNR
    snr = compute_snr(original, decrypted)
    print(f"SNR (original vs decrypted) : {snr:.2f} dB")

    # Wrong key test
    WRONG_KEY = KEY + 1
    print(f"\nRunning wrong key test (wrong key = {WRONG_KEY})...")
    wrong_key_test(encrypted, perm, WRONG_KEY, sample_rate, OUTPUT_DIR)

    # Save audio files
    save_audio(os.path.join(OUTPUT_DIR, "original_speech_out.wav"), sample_rate, original)
    save_audio(os.path.join(OUTPUT_DIR, "encrypted_speech.wav"),    sample_rate, encrypted)
    save_audio(os.path.join(OUTPUT_DIR, "decrypted_speech.wav"),    sample_rate, decrypted)
    print("Audio files saved: original_speech_out.wav, encrypted_speech.wav, decrypted_speech.wav")

    # Plot
    plot_results(sample_rate, original, encrypted, decrypted,
                 output_path=os.path.join(OUTPUT_DIR, "results.png"))
