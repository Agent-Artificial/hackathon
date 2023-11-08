from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
import subprocess
import logging
from pathlib import Path
import shutil
import os
import uuid

app = FastAPI()

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def run_whisper(whisper_bin, file_path, outdir, model_path):
    logging.info(f"Starting transcription for {file_path}")

    # Ensure that file_path and model_path are absolute paths
    file_path = Path(file_path).resolve()
    model_path = Path(model_path).resolve()
    # Use the absolute path for the whisper binary
    whisper_bin = Path(whisper_bin).resolve()

    # Prepare output file base name and path
    output_file_base = file_path.stem
    output_dir = Path(outdir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)  # Create the output directory if it doesn't exist
    logging.debug(f"Output directory resolved to {output_dir}")

    # Prepare the command
    command = [
        str(whisper_bin),
        "-m", str(model_path),
        "-f", str(file_path),
        "-of", output_file_base,  # Output file base name, without extension
        "-otxt",  # Output result in a text file
        # Add any additional options you require here
    ]

    # Change working directory to the output directory before running the command
    current_dir = Path.cwd()
    try:
        os.chdir(output_dir)
        logging.debug(f"Running command: {' '.join(command)} in directory {output_dir}")
        subprocess.run(command, check=True)
        logging.info(f"Transcription completed successfully for {file_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while running the transcription: {e}")
        raise
    finally:
        os.chdir(current_dir)  # Change back to the original directory

@app.post("/audio/transcriptions")
async def transcribe(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    whisper_bin: str = "whisper.cpp/main",
    model_path: str = "whisper.cpp/models/ggml-base.en.bin",
    outdir: str = "out"
):
    # Ensure the output directory exists
    outdir = Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    # Generate a unique filename to avoid collisions
    unique_filename = str(uuid.uuid4())
    input_filepath = outdir / f"{unique_filename}.wav"
    output_filepath = outdir / f"{unique_filename}.txt"

    # Save the uploaded file to the filesystem
    with open(input_filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Use background tasks to run the potentially long-running process
    #background_tasks.add_task(
    #    run_whisper, whisper_bin, input_filepath, outdir, model_path
    #)

    print("Run whisper")
    run_whisper( whisper_bin=whisper_bin, file_path=input_filepath, outdir=outdir, model_path=model_path)

    with open(output_filepath, 'r', encoding='utf-8') as file:
      file_contents = file.read()

    print("file_contents: ", file_contents)

    # Return the name of the output file to check for status
    return {"text": file_contents, "output_file": output_filepath.name}

@app.get("/transcribe/{filename}")
async def get_transcription(filename: str, outdir: str = "out"):
    output_filepath = Path(outdir).resolve() / filename

    # Check if the output file exists and return its content
    if output_filepath.is_file():
        return "it worked"
        #return FileResponse(path=output_filepath, filename=filename, media_type='text/plain')
    else:
        raise HTTPException(status_code=404, detail="Output not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)