import uuid
import shutil
import zipfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from app.job_manager import JobManager
from src.pipeline import DatasetPipeline

app = FastAPI(
    title="Dataset Quality Engine",
    description="API for automated image dataset cleaning and quality analysis",
    version="1.0.0"
)

# Core workspace path setups
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Instantiate the thread-safe global manager
job_manager = JobManager()


@app.get("/")
def home():
    return {
        "message": "Dataset Quality Engine API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip archives are supported.")

    job_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{job_id}.zip"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Register the job state in our tracker
    job_manager.create_job(job_id)

    return {
        "job_id": job_id,
        "filename": file.filename,
        "status": "uploaded"
    }


@app.get("/status/{job_id}")
def get_status(job_id: str):
    job = job_manager.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job_id,
        **job
    }


# Separate worker function to process jobs completely asynchronously 
def process_dataset_job(job_id: str):
    try:
        job_manager.update_job(
            job_id,
            status="processing",
            progress=5,
            message="Preparing dataset"
        )

        zip_path = UPLOAD_DIR / f"{job_id}.zip"

        if not zip_path.exists():
            raise FileNotFoundError("Dataset ZIP file not found.")

        extract_path = UPLOAD_DIR / job_id
        output_path = OUTPUT_DIR / job_id

        extract_path.mkdir(parents=True, exist_ok=True)
        output_path.mkdir(parents=True, exist_ok=True)

        job_manager.update_job(
            job_id,
            progress=10,
            message="Extracting dataset"
        )

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        job_manager.update_job(
            job_id,
            progress=20,
            message="Running dataset pipeline"
        )

        # Triggers your dynamic cloud-isolated tracking pipeline configurations
        pipeline = DatasetPipeline(
            dataset_path=str(extract_path),
            output_root=str(output_path)
        )
        
        pipeline.run()

        job_manager.update_job(
            job_id,
            status="completed",
            progress=100,
            message="Dataset processing completed"
        )

    except Exception as error:
        job_manager.update_job(
            job_id,
            status="failed",
            message=str(error)
        )


@app.post("/process/{job_id}")
def process_dataset(
    job_id: str,
    background_tasks: BackgroundTasks
):
    job = job_manager.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job["status"] == "processing":
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Dataset is already being processed"
        }

    # Offload execution task onto background worker threads
    background_tasks.add_task(
        process_dataset_job,
        job_id
    )

    job_manager.update_job(
        job_id,
        status="queued",
        progress=0,
        message="Dataset processing queued"
    )

    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Dataset processing started"
    }


# --- ZIP CREATION UTILITY FUNCTION ---
def create_output_zip(job_id: str):
    output_path = OUTPUT_DIR / job_id

    if not output_path.exists():
        raise FileNotFoundError("Output directory not found")

    # This creates a base name path string target for make_archive
    zip_target_base = OUTPUT_DIR / f"{job_id}_cleaned"

    # Packages clean/, rejected/, and reports/ straight into the root of the ZIP
    archive_path = shutil.make_archive(
        base_name=str(zip_target_base),
        format="zip",
        root_dir=output_path
    )

    return Path(archive_path)


# --- DOWNLOAD ENDPOINT ROUTER ---
@app.get("/download/{job_id}")
def download_dataset(job_id: str):
    job = job_manager.get_job(job_id)

    # Security Check 1: Check if the Job ID exists at all
    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Security Check 2: Protect against downloading incomplete data chunks
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail="Dataset processing is not completed"
        )

    try:
        zip_path = create_output_zip(job_id)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Processed dataset files not found on disk"
        )

    # Stream the compressed file package directly to the browser
    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename="cleaned_dataset.zip"
    )
