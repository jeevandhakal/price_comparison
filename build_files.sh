echo "BUILD START"
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
python3 -m playwright install chromium
echo "BUILD END"