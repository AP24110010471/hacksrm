# Geo-Intelligent Platform - Setup Guide

## 1. Install Python (The Right Way)
1. Go to [python.org/downloads](https://www.python.org/downloads/).
2. Download the latest version for Windows.
3. run the installer.
4. **CRITICAL STEP**: At the bottom of the first screen, check the box:
   **[x] Add Python to PATH**
5. Click "Install Now".

## 2. Verify Installation
Open a NEW Setup terminal (Command Prompt or PowerShell) and run:
```cmd
python --version
pip --version
```
If both return versions, you are ready.

## 3. Setup Project
Open a terminal in the `hacksrm` folder.

1. **Install Libraries**:
   ```cmd
   pip install -r requirements.txt
   ```

2. **Run Server**:
   ```cmd
   python app/app.py
   ```

3. **Run Demo** (in a new terminal):
   ```cmd
   python demo_scenario.py
   ```

## Troubleshooting "No module named pip"
If you see `No module named pip`, your Python installation might be corrupted or from a minimal environment (like MSYS2).
- **Solution**: Uninstall your current Python and strictly follow Step 1 above using the official installer.
