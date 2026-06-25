#!/usr/bin/env python3

import threading
import time
import tkinter as tk
from tkinter import font
import serial
import serial.tools.list_ports

# --- DOMYŚLNE USTAWIENIA STARTOWE ---
DEFAULT_PORT = "COM90"
BAUDRATE = 9600


class MiernikApp:

    def __init__(self, root):
        self.root = root
        self.root.title("UT622E - Panel Serwisowy")
        self.root.geometry("880x340")
        self.root.configure(bg="#1e1e1e")

        self.current_mode = "R"
        self.lang = "PL"
        self.running = True

        self.trans = {
            "PL": {
                "port": "PORT:", "lang_lbl": "JĘZYK:", "err_port": "BŁĄD PORTU", "err_close": "ZAMKNIJ INNE", "prefix": "PARAMETR:",
                "C_m": "POJEMNOŚĆ (C)", "C_s": "PARAMETR DODATKOWY (D/Q/X)",
                "R_m": "REZYSTANCJA (R)", "R_s": "PARAMETR DODATKOWY (X/Q/Faza)",
                "L_m": "INDUKCYJNOŚĆ (L)", "L_s": "PARAMETR DODATKOWY (Q/D/R)",
                "Z_m": "IMPEDANCJA (Z)", "Z_s": "REAKTANCJA / FAZA",
                "DCR_m": "REZYSTANCJA DC (DCR)",
                "phase": "KĄT FAZY", "q_fact": "DOBROĆ (Q)", "disp": "STRATNOŚĆ (D)"
            },
            "EN": {
                "port": "PORT:", "lang_lbl": "LANG:", "err_port": "PORT ERROR", "err_close": "CLOSE OTHERS", "prefix": "PARAM:",
                "C_m": "CAPACITANCE (C)", "C_s": "SECONDARY PARAMETER (D/Q/X)",
                "R_m": "RESISTANCE (R)", "R_s": "SECONDARY PARAMETER (X/Q/Phase)",
                "L_m": "INDUCTANCE (L)", "L_s": "SECONDARY PARAMETER (Q/D/R)",
                "Z_m": "IMPEDANCE (Z)", "Z_s": "REACTANCE / PHASE",
                "DCR_m": "DC RESISTANCE (DCR)",
                "phase": "PHASE ANGLE", "q_fact": "QUALITY FACTOR (Q)", "disp": "DISSIPATION (D)"
            },
            "ES": {
                "port": "PUERTO:", "lang_lbl": "IDIOMA:", "err_port": "ERROR DE PUERTO", "err_close": "CERRAR OTROS", "prefix": "PARÁM:",
                "C_m": "CAPACITANCIA (C)", "C_s": "PARÁMETRO SECUNDARIO (D/Q/X)",
                "R_m": "RESISTENCIA (R)", "R_s": "PARÁMETRO SECUNDARIO (X/Q/Fase)",
                "L_m": "INDUCTANCIA (L)", "L_s": "PARÁMETRO SECUNDARIO (Q/D/R)",
                "Z_m": "IMPEDANCIA (Z)", "Z_s": "REACTANCIA / FASE",
                "DCR_m": "RESISTENCIA DC (DCR)",
                "phase": "ÁNGULO DE FASE", "q_fact": "FACTOR DE CALIDAD (Q)", "disp": "DISIPACIÓN (D)"
            },
            "FR": {
                "port": "PORT:", "lang_lbl": "LANGUE:", "err_port": "ERREUR DE PORT", "err_close": "FERMER LES AUTRES", "prefix": "PARAM:",
                "C_m": "CAPACITANCE (C)", "C_s": "PARAMÈTRE SECONDAIRE (D/Q/X)",
                "R_m": "RÉSISTANCE (R)", "R_s": "PARAMÈTRE SECONDAIRE (X/Q/Phase)",
                "L_m": "INDUCTANCE (L)", "L_s": "PARAMÈTRE SECONDAIRE (Q/D/R)",
                "Z_m": "IMPÉDANCE (Z)", "Z_s": "RÉACTANCE / PHASE",
                "DCR_m": "RÉSISTANCE DC (DCR)",
                "phase": "ANGLE DE PHASE", "q_fact": "FACTEUR DE QUALITÉ (Q)", "disp": "DISSIPATION (D)"
            },
            "ID": {
                "port": "PORT:", "lang_lbl": "BAHASA:", "err_port": "KESALAHAN PORT", "err_close": "TUTUP YANG LAIN", "prefix": "PARAM:",
                "C_m": "KAPASITANSI (C)", "C_s": "PARAMETER SEKUNDER (D/Q/X)",
                "R_m": "RESISTANSI (R)", "R_s": "PARAMETER SEKUNDER (X/Q/Fase)",
                "L_m": "INDUKTANSI (L)", "L_s": "PARAMETER SEKUNDER (Q/D/R)",
                "Z_m": "IMPEDANSI (Z)", "Z_s": "REAKTANSI / FASE",
                "DCR_m": "RESISTANSI DC (DCR)",
                "phase": "SUDUT FASE", "q_fact": "FAKTOR KUALITAS (Q)", "disp": "DISIPASI (D)"
            },
            "HI": {
                "port": "पोर्ट:", "lang_lbl": "भाषा:", "err_port": "पोर्ट त्रुटि", "err_close": "अन्य बंद करें", "prefix": "पैरामीटर:",
                "C_m": "धारिता (C)", "C_s": "द्वितीयक पैरामीटर (D/Q/X)",
                "R_m": "प्रतिरोध (R)", "R_s": "द्वितीयक पैरामीटर (X/Q/फेज)",
                "L_m": "प्रेरकत्व (L)", "L_s": "基层 (Q/D/R)",
                "Z_m": "प्रतिबाधा (Z)", "Z_s": "रिएक्टेंस / फेज",
                "DCR_m": "डीसी प्रतिरोध (DCR)",
                "phase": "फेज कोण", "q_fact": "गुणवत्ता कारक (Q)", "disp": "अपव्यय (D)"
            },
            "ZH": {
                "port": "端口:", "lang_lbl": "语言:", "err_port": "端口错误", "err_close": "关闭其他", "prefix": "参数:",
                "C_m": "电容 (C)", "C_s": "辅助参数 (D/Q/X)",
                "R_m": "电阻 (R)", "R_s": "辅助参数 (X/Q/相位)",
                "L_m": "电感 (L)", "L_s": "辅助参数 (Q/D/R)",
                "Z_m": "阻抗 (Z)", "Z_s": "电抗 / 相位",
                "DCR_m": "直流电阻 (DCR)",
                "phase": "相位角", "q_fact": "品质因数 (Q)", "disp": "损耗因数 (D)"
            }
        }

        # --- ŁADOWANIE OBRAZKÓW ANIME ---
        try:
            # Pomniejszamy o 50%. Jeśli będzie dalej za duża zmień subsample(3, 3) na np (3, 3)
            raw_happy = tk.PhotoImage(file="images/happy.png")
            self.img_happy = raw_happy.subsample(6, 6) 
            
            raw_sad = tk.PhotoImage(file="images/sad.png")
            self.img_sad = raw_sad.subsample(6, 6)
        except Exception:
            self.img_happy = None
            self.img_sad = None

        self.setup_styles()
        self.create_config_bar()
        self.create_main_area() 

        self.thread = threading.Thread(target=self.read_serial, daemon=True)
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_styles(self):
        self.btn_font = font.Font(family="Arial", size=12, weight="bold")
        self.lbl_font = font.Font(family="Arial", size=11, weight="bold")
        self.val_font = font.Font(family="Consolas", size=26, weight="bold")

    def create_config_bar(self):
        config_frame = tk.Frame(self.root, bg="#1e1e1e")
        config_frame.pack(fill=tk.X, padx=20, pady=10)

        active_ports = [p.device for p in serial.tools.list_ports.comports()]
        standard_range = [f"COM{i}" for i in range(1, 51)]
        full_ports_list = active_ports + [p for p in standard_range if p not in active_ports]
        
        if DEFAULT_PORT not in full_ports_list:
            full_ports_list.insert(0, DEFAULT_PORT)

        self.port_label = tk.Label(config_frame, text="", bg="#1e1e1e", fg="#ffffff", font=self.lbl_font)
        self.port_label.pack(side=tk.LEFT, padx=5)

        self.port_var = tk.StringVar(value=DEFAULT_PORT)
        self.port_menu = tk.OptionMenu(config_frame, self.port_var, *full_ports_list)
        self.port_menu.config(bg="#333333", fg="#ffffff", font=self.lbl_font, relief="flat", highlightthickness=0)
        self.port_menu["menu"].config(bg="#333333", fg="#ffffff")
        self.port_menu.pack(side=tk.LEFT, padx=5)

        self.lang_var = tk.StringVar(value="PL")
        self.lang_menu = tk.OptionMenu(config_frame, self.lang_var, "PL", "EN", "ES", "FR", "ID", "HI", "ZH", command=self.change_language)
        self.lang_menu.config(bg="#333333", fg="#ffffff", font=self.lbl_font, relief="flat", highlightthickness=0)
        self.lang_menu["menu"].config(bg="#333333", fg="#ffffff")
        self.lang_menu.pack(side=tk.RIGHT, padx=5)

        self.lang_label = tk.Label(config_frame, text="", bg="#1e1e1e", fg="#ffffff", font=self.lbl_font)
        self.lang_label.pack(side=tk.RIGHT, padx=5)

    def create_main_area(self):
        content_frame = tk.Frame(self.root, bg="#1e1e1e")
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=5)

        # --- PRAWA STRONA: Dziewczyna ---
        avatar_frame = tk.Frame(content_frame, bg="#1e1e1e")
        avatar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        self.avatar_label = tk.Label(avatar_frame, bg="#1e1e1e")
        self.avatar_label.pack(side=tk.TOP, pady=(10, 0)) # Przypięcie u góry, by była bliżej języków

        # --- LEWA STRONA: Przyciski u góry, Wyniki na dole ---
        data_frame = tk.Frame(content_frame, bg="#1e1e1e")
        data_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Poziomy pasek na przyciski
        btn_frame = tk.Frame(data_frame, bg="#1e1e1e")
        btn_frame.pack(side=tk.TOP, pady=(0, 20))
        
        self.modes = ["C", "R", "L", "Z", "DCR"]
        self.btn_objects = {}
        for code in self.modes:
            btn = tk.Button(
                btn_frame, text=code, font=self.btn_font, bg="#333333", fg="#ffffff",
                activebackground="#0078d7", activeforeground="#ffffff", width=6,
                command=lambda c=code: self.switch_mode(c)
            )
            btn.pack(side=tk.LEFT, padx=5) # Przyciski obok siebie
            self.btn_objects[code] = btn
        self.btn_objects[self.current_mode].configure(bg="#0078d7")

        # Ramka na dwa ekrany z wynikami
        results_frame = tk.Frame(data_frame, bg="#1e1e1e")
        results_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # Wynik Główny (Lewy ekran)
        main_box = tk.Frame(results_frame, bg="#1e1e1e")
        main_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        self.main_label = tk.Label(main_box, text="", font=self.lbl_font, bg="#1e1e1e", fg="#888888")
        self.main_label.pack(anchor="w")
        self.main_value = tk.Label(main_box, text="---", font=self.val_font, bg="#252526", fg="#00ff66", width=14, relief=tk.RIDGE, bd=2)
        self.main_value.pack(pady=5, fill=tk.X)

        # Wynik Dodatkowy (Prawy ekran)
        sec_box = tk.Frame(results_frame, bg="#1e1e1e")
        sec_box.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)
        self.sec_label = tk.Label(sec_box, text="", font=self.lbl_font, bg="#1e1e1e", fg="#888888")
        self.sec_label.pack(anchor="w")
        self.sec_value = tk.Label(sec_box, text="---", font=self.val_font, bg="#252526", fg="#00bfff", width=14, relief=tk.RIDGE, bd=2)
        self.sec_value.pack(pady=5, fill=tk.X)

        self.update_labels()
        self.update_avatar("sad")

    def update_avatar(self, state):
        if state == "happy" and self.img_happy:
            self.avatar_label.config(image=self.img_happy, text="")
        elif state == "sad" and self.img_sad:
            self.avatar_label.config(image=self.img_sad, text="")
        else:
            txt = "‿" if state == "happy" else "☹"
            color = "#00ff66" if state == "happy" else "#ff3333"
            self.avatar_label.config(image="", text=txt, font=("Arial", 36), fg=color)

    def change_language(self, selected_lang):
        self.lang = selected_lang
        self.update_labels()

    def switch_mode(self, new_mode):
        for code, btn in self.btn_objects.items():
            btn.configure(bg="#333333")
        self.btn_objects[new_mode].configure(bg="#0078d7")
        self.current_mode = new_mode
        self.update_labels()

    def update_labels(self):
        t = self.trans[self.lang]
        self.port_label.config(text=t["port"])
        self.lang_label.config(text=t["lang_lbl"])
        self.main_label.config(text=t.get(f"{self.current_mode}_m", ""))
        
        if self.current_mode == "DCR":
            self.sec_label.config(text="---")
            self.sec_value.config(text="---", fg="#555555")
        else:
            self.sec_label.config(text=t.get(f"{self.current_mode}_s", ""))

    def clean_main_value(self, val_str):
        try:
            val = float(val_str)
            abs_val = abs(val)

            if self.current_mode == "C":
                if abs_val < 1e-14: return "0.000 pF"
                if abs_val < 1e-9: return f"{val * 1e12:.3f} pF"
                elif 1e-9 <= abs_val < 1e-6: return f"{val * 1e9:.3f} nF"
                elif 1e-6 <= abs_val < 1e-3: return f"{val * 1e6:.3f} uF"
                elif 1e-3 <= abs_val < 1: return f"{val * 1e3:.3f} mF"
                else: return f"{val:.3f} F"
            elif self.current_mode == "L":
                if abs_val < 1e-6: return f"{val * 1e6:.3f} uH"
                elif 1e-3 <= abs_val < 1: return f"{val * 1e3:.3f} mH"
                else: return f"{val:.3f} H"
            else:
                if abs_val >= 1e6: return f"{val / 1e6:.3f} MOhm"
                elif abs_val >= 1e3: return f"{val / 1e3:.3f} kOhm"
                else: return f"{val:.3f} Ohm"
        except ValueError:
            return val_str

    def clean_sec_value(self, val_str):
        try:
            val = float(val_str)
            abs_val = abs(val)
            t = self.trans[self.lang]

            if abs_val >= 1000:
                if abs_val >= 1e6: return f"{val / 1e6:.3f} M", "ESR / X"
                else: return f"{val / 1000:.3f} k", "ESR / X"
            elif 10.0 <= abs_val < 180.0:
                return f"{val:.2f} deg", t["phase"]
            elif val < 0:
                return f"{val:.4f}", t["q_fact"]
            elif 0 <= val < 0.5:
                return f"{val:.4f}", t["disp"]
            else:
                return f"{val:.4f} rad", t["phase"]
        except ValueError:
            return val_str, "DODATKOWY"

    def read_serial(self):
        ser = None
        last_port = None

        while self.running:
            current_port = self.port_var.get()
            t = self.trans[self.lang]

            if current_port != last_port:
                if ser and ser.is_open:
                    try: ser.close()
                    except: pass
                ser = None
                last_port = current_port

            if ser is None:
                try:
                    ser = serial.Serial(current_port, BAUDRATE, timeout=1.0, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
                    ser.reset_input_buffer()
                except serial.SerialException:
                    ser = None
                    self.main_value.config(text=t["err_port"], fg="#ff3333")
                    self.sec_value.config(text=t["err_close"], fg="#ff3333")
                    self.update_avatar("sad")
                    time.sleep(1.0)
                    continue

            try:
                ser.write(b"FETC?\r\n")
                res = ser.readline().decode("utf-8").strip()

                if res:
                    raw_upper = res.upper()
                    if "OL" in raw_upper or "---" in raw_upper or "OVERLOAD" in raw_upper:
                        is_measurement_valid = False
                    else:
                        is_measurement_valid = True

                    parts = res.split(",")
                    if len(parts) >= 2:
                        m_val = self.clean_main_value(parts[0])
                        s_val, s_lbl = self.clean_sec_value(parts[1])

                        if self.current_mode != "DCR":
                            self.sec_value.config(text=s_val, fg="#00bfff")
                            self.sec_label.config(text=f"{t['prefix']} {s_lbl}")

                        if is_measurement_valid:
                            self.main_value.config(text=m_val, fg="#00ff66")
                            self.update_avatar("happy")
                        else:
                            self.main_value.config(text=m_val, fg="#ffaa00")
                            self.update_avatar("sad")
                            
            except Exception:
                try: ser.close()
                except: pass
                ser = None
                self.update_avatar("sad")
                time.sleep(1.0)

            time.sleep(0.7)

    def on_close(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MiernikApp(root)
    root.mainloop()