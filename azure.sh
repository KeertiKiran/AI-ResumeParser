cp -r src/ .
pip install -r requirements.txt
gunicorn app:app
