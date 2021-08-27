import multiprocessing
import os

bind = "0.0.0.0:8000"
accesslog = "-"

if os.environ["DJANGO_ENV"] == "production":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "vending_machine.config.production.settings"
    )
else:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "vending_machine.config.development.settings"
    )

reload = "true"
timeout = 7200
workers = (2*multiprocessing.cpu_count())+1