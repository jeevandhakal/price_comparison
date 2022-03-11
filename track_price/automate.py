from datetime import datetime
import imp
from apscheduler.schedulers.background import BackgroundScheduler
from .script import track_wishlist

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(track_wishlist, 'interval', minutes=24*60)
    scheduler.start()