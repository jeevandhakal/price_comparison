from apscheduler.schedulers.background import BackgroundScheduler
from track_price.script import check_func

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_func, 'interval', hours=10)
    scheduler.start()