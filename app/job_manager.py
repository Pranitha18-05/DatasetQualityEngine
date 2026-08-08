from threading import Lock


class JobManager:

    def __init__(self):

        self.jobs = {}

        self.lock = Lock()

    def create_job(self, job_id):

        with self.lock:

            self.jobs[job_id] = {

                "status": "uploaded",

                "progress": 0,

                "message": "Dataset uploaded"

            }

    def update_job(
        self,
        job_id,
        status=None,
        progress=None,
        message=None
    ):

        with self.lock:

            if job_id not in self.jobs:
                return

            if status is not None:
                self.jobs[job_id]["status"] = status

            if progress is not None:
                self.jobs[job_id]["progress"] = progress

            if message is not None:
                self.jobs[job_id]["message"] = message

    def get_job(self, job_id):

        with self.lock:

            return self.jobs.get(job_id)