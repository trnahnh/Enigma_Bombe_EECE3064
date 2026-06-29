# WESS26 Poster Content — Group 10
# Speech Encryption and Decryption Using FFT-Based Frequency-Domain Scrambling

---

## POSTER SPECS (from workshop document)
- Size: A1 (594 × 841 mm) — portrait
- Layout: Conference-style (see template from Dr. Samarah)
- Sections: Introduction, Results, Findings, Conclusion & Future Work (template labels)
- Each team presents 5–7 minutes + 3-minute Q&A
- Poster PDF due: Monday, July 27, 2026

---

## TITLE BLOCK

**Poster Title:**
Speech Encryption and Decryption Using FFT-Based Frequency-Domain Scrambling

**Group Number:** Group 10

**Student Names:**
Krishna Maharajwala, Andre Tran, Chris [Last Name]

**Institution / Department:**
University of Cincinnati — Department of Electrical and Computer Engineering

**Supervisor / Instructor:**
Dr. Ashraf Samarah

**Course:**
Signals and Systems II — EECE 3064 | Summer 2026

---

## SECTION 1: INTRODUCTION

Speech signals carry information that must sometimes be protected from unauthorized listeners. In military communication, private phone calls, and online meetings, transmitting speech securely is essential. Speech encryption transforms a speech signal into an unintelligible form during transmission. Decryption reverses this process to recover the original speech at the receiver.

From a Signals and Systems perspective, speech is a time-varying discrete-time signal. Its frequency content can be analyzed and manipulated using the Fourier Transform. This project implements a speech encryption and decryption system using FFT-based frequency-domain scrambling — a method that directly applies core course concepts including sampling, Fourier Transform, frequency-domain analysis, and signal reconstruction.

**Key concepts demonstrated:**
- Discrete-time signal processing
- Fast Fourier Transform (FFT)
- Frequency-domain manipulation
- Inverse FFT and signal reconstruction
- Key-based secure communication

---

## SECTION 2: BACKGROUND / THEORY

### 2.1 Speech as a Discrete-Time Signal
A digital speech signal is represented as x[n], where n is the sample index. Each sample represents the signal amplitude at a specific point in time. The time-domain waveform shows the shape of the speech signal but does not directly reveal its frequency content.

### 2.2 Sampling
To process speech digitally, the continuous-time signal is sampled at a rate fs (sampling frequency). Common rates include 8,000 Hz, 16,000 Hz, and 44,100 Hz. A higher sampling frequency captures more detail.

### 2.3 Discrete Fourier Transform (DFT) / FFT
The DFT converts a finite discrete-time signal into its frequency-domain representation:

    X[k] = Σ x[n] · e^(−j2πkn/N),   n = 0, 1, ..., N−1

where X[k] are the complex frequency components, N is the number of samples, and k is the frequency index. The FFT is an efficient algorithm to compute the DFT.

### 2.4 Inverse DFT (IDFT)
The IDFT reconstructs the time-domain signal from its frequency components:

    x[n] = (1/N) Σ X[k] · e^(j2πkn/N),   k = 0, 1, ..., N−1

### 2.5 FFT-Based Encryption
The encryption process rearranges the frequency components X[k] using a key-generated permutation. The scrambled components no longer represent intelligible speech when converted back to the time domain via IFFT.

### 2.6 Decryption
The receiver uses the same key to generate the same permutation and reverse the scrambling. IFFT is then applied to recover the original speech signal.

---

## SECTION 3: METHODOLOGY

**Implementation tool:** Python (NumPy, SciPy, Matplotlib)

**Step 1 — Audio Input**
A short speech sample (~7 seconds) was recorded and saved in WAV format. The spoken sentence: "Hello, this is our Signals and Systems speech encryption project."

**Step 2 — Preprocessing**
The audio file was loaded using SciPy. Stereo was converted to mono. The signal was normalized to the range [−1, 1].

**Step 3 — FFT**
numpy.fft.fft() was applied to convert the speech signal from the time domain to the frequency domain. The magnitude spectrum was plotted to show the frequency content of the original speech.

**Step 4 — Encryption**
A secret integer key (KEY = 42) was used to seed a random number generator. The generator produced a repeatable permutation of N indices. The FFT components X[k] were rearranged according to this permutation. numpy.fft.ifft() was applied to convert the scrambled frequency signal back into the time domain, producing the encrypted audio.

**Step 5 — Decryption**
The same key was used to regenerate the same permutation. The frequency components of the encrypted signal were reordered back to their original positions using the inverse permutation. numpy.fft.ifft() was applied to recover the speech signal.

**Step 6 — Comparison**
Original, encrypted, and decrypted signals were compared using:
- Time-domain waveform plots
- Frequency-domain magnitude spectrum plots
- Audio playback

---

## SECTION 4: BLOCK DIAGRAM

Place this diagram on the poster. You can draw it as a clean flowchart:

```
┌─────────────────────┐
│  Original Speech    │  x[n] — time-domain speech signal
│  Signal x[n]        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Audio Sampling &   │  fs = 44,100 Hz (or 48,000 Hz)
│  Preprocessing      │  Stereo → Mono, Normalize
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│        FFT          │  X[k] = FFT{x[n]}
│  (Time → Frequency) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Frequency-Domain   │  X_scrambled[k] = X[perm(k)]
│  Scrambling         │  using Secret Key
│  (Secret Key)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Inverse FFT        │  x_enc[n] = IFFT{X_scrambled[k]}
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Encrypted Speech   │  Sounds distorted / unintelligible
│  Signal x_enc[n]    │
└──────────┬──────────┘
           │
           ▼ (Decryption path)
┌─────────────────────┐
│  FFT of Encrypted   │  X_enc[k] = FFT{x_enc[n]}
│  Signal             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Reverse Scrambling │  X_original[perm(k)] = X_enc[k]
│  (Same Secret Key)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Inverse FFT        │  x_dec[n] = IFFT{X_original[k]}
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Recovered Speech   │  Sounds close to original
│  Signal x_dec[n]    │
└─────────────────────┘
```

---

## SECTION 5: RESULTS

**Place results.png on the poster here.** It contains all 6 plots below.

### What to write about the plots:

**Original Speech (Blue):**
The time-domain waveform shows distinct speech bursts corresponding to spoken words, with silence at the beginning. The frequency spectrum shows energy concentrated in the low-frequency range (below 5,000 Hz), which is typical for human speech.

**Encrypted Speech (Red):**
The time-domain waveform appears as a continuous noise-like signal with no visible speech structure. The frequency spectrum shows energy spread uniformly across the entire frequency range (0–22,000 Hz). The scrambling successfully hides the structure of the original speech.

**Decrypted Speech (Green):**
The time-domain waveform closely matches the shape of the original speech, with speech bursts visible in the same locations. The frequency spectrum partially recovers the original distribution. Audio playback of the decrypted signal is intelligible with minor residual noise, which is a known limitation due to floating-point rounding from the real-part extraction after IFFT.

### Results Summary Table (add this to poster):

| Signal     | Time Domain              | Frequency Spectrum               | Audibility        |
|------------|--------------------------|----------------------------------|-------------------|
| Original   | Clear speech bursts      | Energy concentrated below 5 kHz  | Fully intelligible |
| Encrypted  | Flat noise-like signal   | Energy spread across all freq.   | Unintelligible     |
| Decrypted  | Matches original shape   | Partially recovered              | Mostly intelligible |

---

## SECTION 6: CONCLUSION

This project successfully demonstrated speech encryption and decryption using FFT-based frequency-domain scrambling. By transforming a speech signal into the frequency domain and rearranging its components using a secret key, the speech was made unintelligible. Using the same key to reverse the scrambling and applying inverse FFT recovered the original speech.

The system directly applies Signals and Systems concepts including sampling, Fourier Transform, frequency-domain analysis, and signal reconstruction. The results confirm that the encryption is effective and the decryption is reversible when the correct key is used. A small amount of residual noise in the decrypted signal is present due to floating-point precision, which is expected in a software-based implementation.

---

## SECTION 7: FUTURE WORK

- Real-time microphone input and speaker output
- Stronger encryption using multiple keys or block-based scrambling
- Noise filtering applied before decryption to reduce residual distortion
- Signal quality measurement using Signal-to-Noise Ratio (SNR)
- Testing with different speakers and speech samples
- Implementing a graphical user interface (GUI)
- Deploying the system on an embedded microcontroller
- Combining with modulation-based encryption for added security

---

## SECTION 8: REFERENCES

1. Lathi, B. P. *Linear Systems and Signals*, 3rd ed. Oxford University Press.
2. Oppenheim, A. V., Willsky, A. S., and Nawab, S. H. *Signals and Systems*, 2nd ed. Pearson.
3. Smith, S. W. *The Scientist and Engineer's Guide to Digital Signal Processing*. California Technical Publishing.
4. MathWorks. "Fast Fourier Transform." MATLAB Documentation. www.mathworks.com
5. SciPy Documentation. "scipy.fft and scipy.io.wavfile." docs.scipy.org

---

## LAYOUT NOTES FOR POSTER DESIGNER

- Follow the A1 template from Dr. Samarah (Introduction | Results | Findings | Conclusion & Future Work)
- Map sections as follows:
  - INTRODUCTION → Sections 1 + 2 (Introduction + Background/Theory)
  - RESULTS → Section 5 (results.png + summary table)
  - FINDINGS → Section 3 + 4 (Methodology + Block Diagram)
  - CONCLUSION & FUTURE WORK → Sections 6 + 7
  - Footer: References + Contact Info (samaraaf@ucmail.uc.edu)
- Keep text brief on the poster — use bullet points, not paragraphs
- The block diagram and results.png are the two main visuals
- Use the DFT and IDFT equations in the Theory section as visual elements
- Group number (10) goes in the top-right GROUP box on the template
