from flask import Flask, request, jsonify
from config import sql_connection
from job_scheduler import JobScheduler
from datetime import datetime, timedelta
current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
import json

app = Flask(__name__)
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, timedelta):
            return str(obj)  # Convert timedelta to string (e.g., '1 day, 3:00:00')
        elif isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO format string
        return super().default(obj)

app.json_encoder = CustomJSONEncoder
scheduler = JobScheduler()

@app.route('/jobs', methods=['GET'])
def list_jobs():
    """
    Lists all available jobs with their details.
    """
    connection = sql_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({'jobs': jobs})

# @app.route('/jobs/<int:job_id>', methods=['GET'])
@app.route('/jobs', methods=['GET'])
def get_job():
    """
    Retrieves details of a specific job by its ID.
    """

    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({'error': 'job_id is required'}), 400
    
    connection = sql_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    job = cursor.fetchone()
    cursor.close()
    connection.close()   
    if job:
        if job['last_run'] is not None:
            job['last_run'] = job['last_run'].isoformat()
        if job['next_run'] is not None:
            job['next_run'] = job['next_run'].isoformat()
        return jsonify(job) 
        # return json.loads(job)
    return jsonify({'error': 'Job not found'}), 404

@app.route('/jobs', methods=['POST'])
def create_job():
    """
    Creates a new job and schedules it.
    """

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    
    data = request.json
    job_name = data['name']
    day_of_week = data['day_of_week']
    time_of_day = data['time_of_day']
    frequency = data.get('frequency', None)
    priority = data.get('priority', None)

    if not all([job_name, day_of_week, time_of_day]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Insert the job into the database
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

    # Schedule the job in the scheduler
    scheduler.schedule_job(job_id, lambda: execute_job(job_id), day_of_week, time_of_day)

    return jsonify({'status': 'Job scheduled successfully', 'job_id': job_id}), 201

def execute_job(job_id):
    """
    Dummy job execution function. In a real scenario, this would contain the job logic.
    """
    connection = sql_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE jobs SET last_run = %s WHERE id = %s", (current_time_str, job_id))
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Executed job with ID {job_id}")

if __name__ == '__main__':
    app.run(debug=True)
