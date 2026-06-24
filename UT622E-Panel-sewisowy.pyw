import threading
import time
import tkinter as tk
from tkinter import font
import serial

# --- USTAWIENIA PORTU ---
PORT = "COM90"
BAUDRATE = 9600


class MiernikApp:

    def __init__(self, root):
        self.root = root
        self.root.title("UT622E - Panel Serwisowy")
        self.root.geometry("650x300")
        self.root.configure(bg="#1e1e1e")  # Nowoczesne, ciemne tło pod OBS

        # Aktualny tryb pracy programu (domyślnie R)
        self.current_mode = "R"

        # Flaga do bezpiecznego zamykania portu
        self.running = True

        # --- TWORZENIE INTERFEJSU ---
        self.setup_styles()
        self.create_buttons()
        self.create_display()

        # --- URUCHOMIENIE ODCZYTU W TLE ---
        self.thread = threading.Thread(target=self.read_serial, daemon=True)
        self.thread.start()

        # Obsługa zamknięcia okna krzyżykiem
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_styles(self):
        """Konfiguracja dużych, czytelnych czcionek serwisowych"""
        self.btn_font = font.Font(family="Arial", size=12, weight="bold")
        self.lbl_font = font.Font(family="Arial", size=11, weight="bold")
        # Wielka czcionka inżynierska pod kamery/OBS
        self.val_font = font.Font(family="Consolas", size=26, weight="bold")

    def create_buttons(self):
        """Tworzy panel przełączania trybów na górze okna"""
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=15)

        self.modes = {
            "C": "KONDENSATOR (C)",
            "R": "REZYSTANCJA (R)",
            "L": "CEWKA (L)",
            "Z": "IMPEDANCJA (Z)",
            "DCR": "OPÓR DC (DCR)",
        }

        self.btn_objects = {}
        for code, text in self.modes.items():
            btn = tk.Button(
                btn_frame,
                text=code,
                font=self.btn_font,
                bg="#333333",
                fg="#ffffff",
                activebackground="#0078d7",
                activeforeground="#ffffff",
                width=6,
                command=lambda c=code: self.switch_mode(c),
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.btn_objects[code] = btn

        # Podświetlamy domyślny tryb (R)
        self.btn_objects[self.current_mode].configure(bg="#0078d7")

    def create_display(self):
        """Tworzy wielkie ekrany do wyświetlania wyników"""
        display_frame = tk.Frame(self.root, bg="#1e1e1e")
        display_frame.pack(expand=True, fill=tk.BOTH, padx=20)

        # Lewa strona - Parametr Główny
        self.main_label = tk.Label(
            display_frame,
            text="PARAMETR GŁÓWNY",
            font=self.lbl_font,
            bg="#1e1e1e",
            fg="#888888",
        )
        self.main_label.grid(row=0, column=0, sticky="w", padx=10)

        self.main_value = tk.Label(
            display_frame,
            text="---",
            font=self.val_font,
            bg="#252526",
            fg="#00ff66",
            width=15,
            relief=tk.RIDGE,
            bd=2,
        )
        self.main_value.grid(row=1, column=0, padx=10, pady=5)

        # Prawa strona - Parametr Dodatkowy
        self.sec_label = tk.Label(
            display_frame,
            text="PARAMETR DODATKOWY",
            font=self.lbl_font,
            bg="#1e1e1e",
            fg="#888888",
        )
        self.sec_label.grid(row=0, column=1, sticky="w", padx=10)

        self.sec_value = tk.Label(
            display_frame,
            text="---",
            font=self.val_font,
            bg="#252526",
            fg="#00bfff",
            width=15,
            relief=tk.RIDGE,
            bd=2,
        )
        self.sec_value.grid(row=1, column=1, padx=10, pady=5)

        # Ustawienie nagłówków na start
        self.update_labels()

    def switch_mode(self, new_mode):
        """Obsługuje kliknięcie przycisku i zmianę trybu w programie"""
        # Resetujemy kolory przycisków
        for code, btn in self.btn_objects.items():
            btn.configure(bg="#333333")
        # Podświetlamy nowy
        self.btn_objects[new_mode].configure(bg="#0078d7")

        self.current_mode = new_mode
        self.update_labels()

    def update_labels(self):
        """Zmienia teksty nad cyframi w zależności od wybranego przycisku"""
        if self.current_mode == "C":
            self.main_label.config(text="POJEMNOŚĆ (C)")
            self.sec_label.config(text="PARAMETR DODATKOWY (D/Q/X)")
        elif self.current_mode == "R":
            self.main_label.config(text="REZYSTANCJA (R)")
            self.sec_label.config(text="PARAMETR DODATKOWY (X/Q/Faza)")
        elif self.current_mode == "L":
            self.main_label.config(text="INDUKCYJNOŚĆ (L)")
            self.sec_label.config(text="PARAMETR DODATKOWY (Q/D/R)")
        elif self.current_mode == "Z":
            self.main_label.config(text="IMPEDANCJA (Z)")
            self.sec_label.config(text="REAKTANCJA / FAZA")
        elif self.current_mode == "DCR":
            self.main_label.config(text="REZYSTANCJA DC (DCR)")
            self.sec_label.config(text="---")
            self.sec_value.config(text="---", fg="#555555")

    # --- SZYBKIE I SPRAWDZONE SEKCJE PRZELICZANIA Z POPRZEDNICH KODÓW ---
    def clean_main_value(self, val_str):
        try:
            val = float(val_str)
            abs_val = abs(val)

            if self.current_mode == "C":
                if abs_val < 1e-14:
                    return "0.000 pF"
                if abs_val < 1e-9:
                    return f"{val * 1e12:.3f} pF"
                elif 1e-9 <= abs_val < 1e-6:
                    return f"{val * 1e9:.3f} nF"
                elif 1e-6 <= abs_val < 1e-3:
                    return f"{val * 1e6:.3f} uF"
                elif 1e-3 <= abs_val < 1:
                    return f"{val * 1e3:.3f} mF"
                else:
                    return f"{val:.3f} F"

            elif self.current_mode == "L":
                if abs_val < 1e-6:
                    return f"{val * 1e6:.3f} uH"
                elif 1e-3 <= abs_val < 1:
                    return f"{val * 1e3:.3f} mH"
                else:
                    return f"{val:.3f} H"

            else:  # Dla R, Z, DCR
                if abs_val >= 1e6:
                    return f"{val / 1e6:.3f} MOhm"
                elif abs_val >= 1e3:
                    return f"{val / 1e3:.3f} kOhm"
                else:
                    return f"{val:.3f} Ohm"
        except ValueError:
            return val_str

    def clean_sec_value(self, val_str):
        try:
            val = float(val_str)
            abs_val = abs(val)

            # Identyczna logika przedziałów matematycznych, którą dopracowaliśmy
            if abs_val >= 1000:
                if abs_val >= 1e6:
                    return f"{val / 1e6:.3f} M", "ESR / X"
                else:
                    return f"{val / 1000:.3f} k", "ESR / X"
            elif 10.0 <= abs_val < 180.0:
                return f"{val:.2f} deg", "KĄT FAZY"
            elif val < 0:
                return f"{val:.4f}", "DOBROĆ (Q)"
            elif 0 <= val < 0.5:
                return f"{val:.4f}", "STRATNOŚĆ (D)"
            else:
                return f"{val:.4f} rad", "KĄT FAZY"
        except ValueError:
            return val_str, "DODATKOWY"

    def read_serial(self):
        """Pętla działająca w tle - pobiera dane dokładnie co 0.7s (jak w CMD)"""
        try:
            with serial.Serial(
                PORT,
                BAUDRATE,
                timeout=1.0,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
            ) as ser:
                ser.reset_input_buffer()

                while self.running:
                    ser.write(b"FETC?\r\n")
                    res = ser.readline().decode("utf-8").strip()

                    if res:
                        parts = res.split(",")
                        if len(parts) >= 2:
                            # Przeliczanie wartości
                            m_val = self.clean_main_value(parts[0])
                            s_val, s_lbl = self.clean_sec_value(parts[1])

                            # Aktualizacja napisów na ekranie okienka
                            self.main_value.config(text=m_val)
                            if self.current_mode != "DCR":
                                self.sec_value.config(text=s_val, fg="#00bfff")
                                self.sec_label.config(
                                    text=f"PARAMETR: {s_lbl}"
                                )

                    time.sleep(0.7)
        except serial.SerialException:
            self.main_value.config(text="BŁĄD PORTU", fg="#ff3333")
            self.sec_value.config(text="ZAMKNIJ INNE", fg="#ff3333")

    def on_close(self):
        """Bezpieczne zamknięcie wątku i programu"""
        self.running = False
        self.root.destroy()


# --- URUCHOMIENIE INTERFEJSU ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MiernikApp(root)
    root.mainloop()