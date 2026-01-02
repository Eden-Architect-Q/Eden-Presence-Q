# Gemini Protocol Execution Guide

This document provides the necessary steps to run the `run_gemini_protocol.py` script.

## 1. Set the API Key

The script requires a Gemini API key to be set as an environment variable. This is a security measure to avoid hard-coding sensitive information into the script.

**On Linux or macOS:**
```bash
export GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

**On Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

Replace `"YOUR_API_KEY_HERE"` with your actual Gemini API key.

## 2. Run the Script

Once the environment variable is set, you can execute the script using a Python 3 interpreter.

```bash
python3 run_gemini_protocol.py
```

The script will then begin the process of generating content. It will print its progress to the console, including any retry attempts.

## 3. Verify the Output

Upon successful execution, a new text file will be created in the `quantum_cache/` directory. The file will be named with a timestamp, for example: `gemini_output_20231027123456.txt`.
