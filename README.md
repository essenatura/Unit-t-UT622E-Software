# UT622E - LCR Service Panel (GUI for OBS / Stream Deck)

A Python-based graphical user interface (Tkinter) designed to fetch real-time measurement data from the professional **UNI-T UT622E** LCR meter via a serial port (USB-RS232). 

This project was built specifically for **bench electronics repair live streaming (OBS Studio)** and **Stream Deck** integration. Instead of squinting at the meter's small built-in display or managing a raw command-line terminal, you get massive, high-contrast, color-coded digits perfectly legible on your bench repair videos and live streams, complete with an interactive anime assistant.

---

## 🚀 Key Features

* **Full Linux & Windows Cross-Platform Support:** Built from the ground up to run flawlessly on both Windows (`.pyw` / standalone `.exe`) and Linux distributions (such as **Linux Mint** and **Ubuntu**). Includes native handling for Linux POSIX serial device paths (`/dev/ttyUSB*` / `/dev/ttyACM*`) alongside standard Windows COM ports.
* **Advanced Multi-Language Support:** Interface instantly translates across **7 languages** with a single click: English, Polish, Spanish, French, Indonesian, Hindi, and Chinese.
* **Reactive Anime Avatar Assistant:** Features an integrated slot for stream graphics (`images/happy.png` and `images/sad.png`). The character dynamically reacts on stream—**Happy** during successful stable measurements, and **Sad/Frustrated** when the meter encounters an Overload (`OL`), open probes, or gets disconnected.
* **Symmetric Centered Layout:** Measurement mode selections (`C`, `R`, `L`, `Z`, `DCR`) are arranged in a horizontal centered layout positioned perfectly above the dual results boxes for maximum visual aesthetic on stream overlays.
* **Automatic Engineering Unit Scaling:** Full support for pico-, nano-, and micro-farads (pF, nF, uF, mF), milli-Henries, and Mega-Ohms with built-in tolerance for negative open-probe calibration noise.
* **Smart Secondary Parameter Labeling:** Automatically detects and displays secondary values such as Quality Factor (Q), Dissipation Factor (D), Phase Angle (deg/rad), and ESR / Reactance (X).
* **Stream-Ready High Contrast UI:** Features a sleek dark theme (`#1e1e1e`) with vibrant neon green and cyan text, optimized for OBS Window Capture and clean cropping/chroma-keying.
* **Stream Deck Native Layout:** Easily packages into a standalone file to launch silently with a single physical keypress.

---

## 📦 Requirements

* **Python 3.x**
* **`pyserial` library** (Handles cross-platform communication for both Windows COM and Linux dialout/tty devices)

### Dependencies Installation:

pip install pyserial

<p align="center"> <img src="images/UT622E-C.png" width="220" alt="Main Screen"> <img src="images/UT622E-L.png" width="220" alt="Future Weather">  </p>
<p align="center"> <img src="images/UT622E-R.png" width="220" alt="Languages"> </p>


