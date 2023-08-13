from apscheduler.schedulers.background import BackgroundScheduler
from .script import check_func

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_func, 'interval', minutes=1)
    scheduler.start()