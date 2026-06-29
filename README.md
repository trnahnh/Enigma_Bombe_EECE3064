# Speech Encryption and Decryption

### EECE 3064 — Signals and Systems II | Summer 2026

### Group 10 — WESS26

---

## Overview

FFT-based speech encryption and decryption system. Takes a speech signal, scrambles its
positive frequency components using a secret key, and recovers it perfectly using the same key.
Achieves SNR of 301.50 dB — mathematically perfect reconstruction.

## Group Members

- Krishna Maharajwala
- Anh Tran
- Chris Bramley

## Method

FFT-based Frequency-Domain Scrambling with conjugate symmetry preservation:

1. Apply FFT to speech signal
2. Permute positive frequency components (indices 1 to N/2-1) using a secret key
3. Mirror to negative frequencies to maintain conjugate symmetry
4. Apply IFFT → real encrypted audio with no information loss
5. Reverse permutation with same key
6. Apply IFFT → perfectly recovered audio (SNR = 301.50 dB)

## Requirements

```
pip install numpy scipy matplotlib
```

## How to Run

1. Place your speech file in the project folder named `original_speech.wav`
2. Run:

```
python speech_encryption.py
```

If no WAV file is found, it runs on a synthetic test signal automatically.

## Output Files

| File                     | Description                              |
|--------------------------|------------------------------------------|
| `original_speech_out.wav`| Normalized original audio                |
| `encrypted_speech.wav`   | Encrypted (scrambled) audio              |
| `decrypted_speech.wav`   | Perfectly recovered audio                |
| `wrong_key_attempt.wav`  | Failed decryption with wrong key (noise) |
| `results.png`            | 6-plot figure (waveforms + spectra)      |
| `wrong_key_test.png`     | Correct key vs wrong key comparison      |

## Settings

Edit these at the top of `speech_encryption.py`:

```python
INPUT_FILE = "original_speech.wav"   # your audio file
KEY        = 42                       # secret key (any integer)
```

## Results

| Signal    | Time Domain            | Frequency Spectrum        | Audio                          |
|-----------|------------------------|---------------------------|--------------------------------|
| Original  | Clear speech bursts    | Energy below 5 kHz        | Fully intelligible             |
| Encrypted | Flat noise-like signal | Spread across all freq    | Unintelligible                 |
| Decrypted | Identical to original  | Identical to original     | Fully intelligible — 301.50 dB |

## Tools

- Python, NumPy, SciPy, Matplotlib

## Workshop

3rd WESS26 — Thursday, July 30, 2026 — Lindner Hall, University of Cincinnati
Poster PDF due: Monday, July 27, 2026
