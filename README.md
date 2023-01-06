Build instructions:

    python -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    pyinstaller --onefile export-telegram-members.py

Find the resulting executable in `dist/export-telegram-members`.
