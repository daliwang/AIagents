## GrammarAgent

Lightweight Flask tools for grammar refinement and image-to-text assistance. Includes:
- Email and paper refiner powered by OpenAI
- Simple image handler (describe/translate OCR-like via GPT-4o)
- Optional grammar checker API using LanguageTool Public API

### Features
- **Email Refiner**: Improves tone and grammar; surfaces change notes when available.
- **Paper Refiner**: Academic-style rewriting with listed modifications.
- **Image Handler**: Upload or path-based image input; describe content or apply a custom instruction (e.g., translate text in image).
- **Grammar Checker API (optional)**: Checks text using `language_tool_python` Public API and returns detected issues.

### Requirements
- Python 3.9+
- OpenAI API key (for AI features)

### Installation
```bash
cd /Users/7xw/Documents/Work/ELM_ECP/GrammarAgent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Optional: If you plan to run the grammar checker API
pip install language_tool_python
```

### Environment
Set your OpenAI key before running AI features:
```bash
export OPENAI_API_KEY="<your-key>"
```

### Running the OpenAI-powered web app
This starts the refiner UI and image handler defined in `AI_agent2024.py`.
```bash
python3 AI_agent2024.py
# App will listen on http://0.0.0.0:5008
```

Routes:
- `/` — Home with links
- `/email` — Email Grammar Refiner UI
- `/paper` — Paper Grammar Refiner UI
- `/image` — Image handler (upload or path)

Notes:
- The app uses OpenAI’s SDK (`from openai import OpenAI`). Make sure your `openai` package is recent (>=1.0.0).
- The Flask `secret_key` is hard-coded for demo. For production, replace with a strong random value.

### Running the Grammar Checker API (optional)
`grammar_api.py` provides a simple UI plus JSON API using LanguageTool’s Public API.
```bash
python3 grammar_api.py
# Default port: 5008
```

Endpoints:
- `GET /` — Minimal UI form
- `POST /check` — JSON body: `{ "text": "..." }` → returns `{ matches, count }`

Port collision warning: both apps default to port `5008`. Run only one at a time, or edit one file to use a different port (e.g., `5009`).

### Deployment

#### Using Procfile (e.g., Heroku/Render)
`Procfile` is set to run `python3 AI_agent2024.py`.
```bash
# Example Heroku flow
heroku create
heroku config:set OPENAI_API_KEY="<your-key>"
git push heroku main
```

#### macOS launchd (optional)
`com.user.aigent24.plist` shows how to run the app at login via launchd. Adjust paths and load with:
```bash
launchctl load ~/Library/LaunchAgents/com.user.aigent24.plist
launchctl start com.user.aigent2024
```
To unload:
```bash
launchctl unload ~/Library/LaunchAgents/com.user.aigent24.plist
```

### Development tips
- Prefer running in a virtualenv.
- If you add `grammar_api.py` to your workflow, install `language_tool_python`.
- If you need image OCR-like extraction, the image handler posts base64 to OpenAI vision-capable models.

### Repository layout
```
AI_agent2024.py        # Flask app with email/paper refiners + image handler
grammar_api.py         # Optional grammar checker API (LanguageTool Public API)
Procfile               # Process definition for platforms (web: python3 AI_agent2024.py)
requirements.txt       # Base dependencies (Flask, OpenAI SDK, IPython)
com.user.aigent24.plist# Example launchd config (macOS)
temp_upload/           # Runtime temp folder for uploaded images
```

### Troubleshooting
- "ModuleNotFoundError: language_tool_python": install it if you run `grammar_api.py`.
- OpenAI auth errors: ensure `OPENAI_API_KEY` is exported in your shell/session.
- Port already in use: stop the other app or change the port in code.

### License
Add your license here (e.g., MIT).


