from core.strategy_one import Fetch_liveData  ,strategyone
from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    # def add_arguments(self, parser):
    help = 'Clears the data of TodaysOpenAvd model at the end of each day'

    def handle(self, *args, **options):
        strategyone()
        # data = Fetch_liveData()
        # data.exit_position()