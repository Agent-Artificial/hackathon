import argparse
import subprocess
import logging
from pathlib import Path
import os  # This is the missing import

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

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

def parse_args():
    parser = argparse.ArgumentParser(description="Run Whisper transcription.")
    parser.add_argument("-f", "--file_path", help="Path to the input .wav file", required=True)
    parser.add_argument("-m", "--model_path", help="Path to the Whisper model file", required=True)
    parser.add_argument("-w", "--whisper_bin", help="Path to the Whisper binary", default="whisper.cpp/main")
    parser.add_argument("-o", "--outdir", help="Output directory path", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run_whisper(args.whisper_bin, args.file_path, args.outdir, args.model_path)