import argparse
import subprocess
from pathlib import Path

def convert_to_wav(file_path):
    input_path = Path(file_path).resolve()  # Get the absolute path
    output_name = input_path.with_suffix('.wav').name  # Change the extension to .wav
    output_directory = Path.cwd() / "out"
    output_directory.mkdir(parents=True, exist_ok=True)  # Create the out directory if it doesn't exist
    output_path = output_directory / output_name

    # Run ffmpeg to convert the file
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            str(input_path),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(output_path),
        ],
        check=True,
    )

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", type=str, required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    convert_to_wav(args.file_path)