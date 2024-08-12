import schedule
import time
import threading

class JobScheduler:
    def __init__(self):
        self.jobs = {}
        self.scheduler_thread = threading.Thread(target=self.run_pending, daemon=True)
        self.scheduler_thread.start()

    def schedule_job(self, job_id, job_func, day_of_week, time_of_day):
        job = schedule.every().day.at(time_of_day)
        if day_of_week == 'Monday':
            job = schedule.every().monday.at(time_of_day)
        elif day_of_week == 'Tuesday':
            job = schedule.every().tuesday.at(time_of_day)
        elif day_of_week == 'Wednesday':
            job = schedule.every().wednesday.at(time_of_day)
        elif day_of_week == 'Thursday':
            job = schedule.every().thursday.at(time_of_day)
        elif day_of_week == 'Friday':
            job = schedule.every().friday.at(time_of_day)
        elif day_of_week == 'Saturday':
            job = schedule.every().saturday.at(time_of_day)
        elif day_of_week == 'Sunday':
            job = schedule.every().sunday.at(time_of_day)

        self.jobs[job_id] = job.do(job_func)

    def run_pending(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
