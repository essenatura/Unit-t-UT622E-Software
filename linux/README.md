## 🐧 Running the Application on Linux

The application is fully cross-platform and runs natively on Linux distributions (such as Linux Mint, Ubuntu, or Debian). Because Linux treats Python script extensions (`.py` or `.pyw`) as plain text by default, follow these steps to make the script executable with a simple double-click.

### 1. Prerequisites (Installing Dependencies)
Before running the application for the first time, make sure Python 3 and the necessary serial communication package (`pyserial`) are installed on your system. Open your terminal and run:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-serial

2. File Configuration (Shebang & Execution Rights)
To configure the .pyw file so it behaves like a standalone executable program:

Open the UT622E-Panel-sewisowy.pyw file in a text editor and ensure that the very first line (above all import statements) contains the following shebang:

Python
#!/usr/bin/env python3
Grant execution permissions to the file. You can achieve this using one of the two methods:

GUI Method: Right-click the file -> Properties -> Permissions tab -> Check the box that says "Allow executing file as program".

Terminal Method: Navigate to the project directory and run the following command:

Bash
chmod +x UT622E-Panel-sewisowy.pyw
3. Launching the Application
Graphical Method (Double-click): Simply double-click the UT622E-Panel-serwisowy.pyw file. If the system prompts you with an action menu, click "Run".

Tip (Linux Mint/Cinnamon): If double-clicking still opens the file in a text editor, open your file manager and go to: Edit -> Preferences -> Behavior tab. Under the Executable Text Files section, select "Run them" or "Ask each time".

Terminal Method:
If you want to view real-time logs or debugging output in the background, launch the application via terminal using:

Bash
python3 UT622E-Panel-serwisowy.pyw
⚠️ Crucial Step: Fixing USB/Serial Port Access (Permission Denied)
On Linux, access to serial communication devices (/dev/ttyUSB* or /dev/ttyACM*) is restricted by default. If the app opens but fails to connect to your meter due to a "Permission Denied" or port error, you must add your user account to the system's dialout group.

Open your terminal and execute:

Bash
sudo usermod -aG dialout $USER
CRITICAL: For these changes to take effect, you must log out of your Linux session and log back in (or restart your computer).
