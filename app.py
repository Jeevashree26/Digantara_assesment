from flask import Flask, request, jsonify
from config import sql_connection
from job_scheduler import JobScheduler
from datetime import datetime, timedelta

app = Flask(__name__)
scheduler = JobScheduler()

def serialize_job(job):
    for key, value in job.items():
        if isinstance(value, datetime):
            job[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, timedelta):
            total_seconds = int(value.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            job[key] = f"{hours:02}:{minutes:02}:{seconds:02}"
        elif isinstance(value, bytes):
            job[key] = value.decode('utf-8')
    return job

@app.route('/jobs', methods=['GET'])
def list_jobs():
    connection = sql_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    serialized_jobs = [serialize_job(job) for job in jobs]
    return jsonify({'jobs': serialized_jobs})

@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    connection = sql_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    job = cursor.fetchone()
    cursor.close()
    connection.close()
    if job:
        job = serialize_job(job)
        return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404

@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    job_name = data['name']
    day_of_week = data['day_of_week']
    time_of_day = data['time_of_day']
    frequency = data.get('frequency', None)
    priority = data.get('priority', None)

    connection = sql_connection()
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO jobs (name, day_of_week, time_of_day, frequency, priority)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (job_name, day_of_week, time_of_day, frequency, priority))
    connection.commit()
    job_id = cursor.lastrowid
    cursor.close()
    connection.close()

    scheduler.schedule_job(job_id, lambda: execute_job(job_id), day_of_week, time_of_day)

    return jsonify({'status': 'Job scheduled successfully', 'job_id': job_id}), 201

def execute_job(job_id):
    connection = sql_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE jobs SET last_run = %s WHERE id = %s", (datetime.now(), job_id))
    connection.commit()
    cursor.close()
    connection.close()
    print("Executed job with ID " + str(job_id))

if __name__ == '__main__':
    app.run(debug=True)
