# Run the Meridian University Assistant in VS Code

A step-by-step guide for Windows (macOS/Linux notes are included). No prior experience needed.

## What you need
- **Python 3.10 or newer** (3.11 recommended): https://www.python.org/downloads/ — on the first installer screen, tick **"Add python.exe to PATH"**.
- **Visual Studio Code**: https://code.visualstudio.com/
- A free **Gemini API key**: https://aistudio.google.com/apikey
- Internet connection (first run downloads packages and the embedding model).

## Step 1 — Get the project
**Option A (easiest): Download ZIP**
1. Open https://github.com/daneshbhimani55555-blip/meridian-university-assistant
2. Click the green **Code** button → **Download ZIP**.
3. Right-click the ZIP → **Extract All**.

**Option B: Git clone**
```bash
git clone https://github.com/daneshbhimani55555-blip/meridian-university-assistant.git
```

## Step 2 — Open the project folder in VS Code
1. Open VS Code.
2. **File → Open Folder...** and select the extracted folder `meridian-university-assistant-main` (or `meridian-university-assistant`). You should see `app.py`, `rag.py`, and the `data` folder in the left panel.
3. When VS Code suggests it, install the **Python** extension (by Microsoft).

## Step 3 — Open the terminal
Press **Ctrl + `** (the key above Tab), or use **Terminal → New Terminal**.

## Step 4 — Create a virtual environment and install packages
Windows (PowerShell):
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
You should see `(.venv)` at the start of the terminal line. Installation can take a few minutes.

If VS Code asks "We noticed a new environment", click **Yes**. Otherwise press **Ctrl + Shift + P**, type **Python: Select Interpreter**, and pick the one inside `.venv`.

## Step 5 — Add your API key
1. In the left panel, find the file `.env.example`. Right-click it → **Copy**, then right-click in an empty area → **Paste**, and rename the copy to **`.env`**.
   (Or in the terminal: `copy .env.example .env` on Windows, `cp .env.example .env` on macOS/Linux.)
2. Open `.env` and replace `PASTE_YOUR_GEMINI_API_KEY_HERE` with your real key:
```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```
3. Save with **Ctrl + S**.

> Never upload `.env` to GitHub or share your key. The `.gitignore` file already blocks it.

## Step 6 — Build the knowledge index
```bash
python ingest.py
```
Expected output: `Successfully indexed ... chunks.` The first run downloads the embedding model, so wait a little.

**Important:** every time you add or edit a file in the `data/` folder, run `python ingest.py` again (or press **Rebuild knowledge index** in the app sidebar).

## Step 7 — Start the assistant
```bash
streamlit run app.py
```
Your browser opens at `http://localhost:8501`. Type a question, for example:
- What is the tuition fee for Web Development?
- Compare the old and current standard tuition refund rules.
- What percentage sibling discount is available? *(the correct answer is that it could not find enough information)*

Stop the app with **Ctrl + C** in the terminal.

## Step 8 (optional) — Run the 20-question test set
```bash
python run_tests.py
```
Results are saved in `reports/actual_test_results.csv`.

## Common problems
| Problem | Fix |
|---|---|
| `py` or `python` is not recognized | Reinstall Python and tick **Add python.exe to PATH**, then reopen VS Code. |
| PowerShell says scripts are disabled | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. |
| `GEMINI_API_KEY is missing` | Check that the file is named exactly `.env` (not `.env.txt`) and the key is saved. |
| `ModuleNotFoundError` | Activate `.venv` (you should see `(.venv)`) and run `pip install -r requirements.txt` again. |
| New data is not used in answers | Run `python ingest.py` again. |
| Port 8501 is busy | Run `streamlit run app.py --server.port 8502`. |

## Prefer Google Colab?
Open the notebook `Meridian_Assistant_Colab.ipynb` in this repository, or use this link:
https://colab.research.google.com/github/daneshbhimani55555-blip/meridian-university-assistant/blob/main/Meridian_Assistant_Colab.ipynb
