import argparse
import subprocess
from pathlib import Path

path = Path


def convert_to_wav(file_path):
    input_name = path.absolute(file_path)
    output_name = input_name.name.format("wav")
    output_path = path.cwd() / "out" / output_name
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            f"{input_name}",
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            f"{output_path}",
        ],
        check=True,
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", type=str, required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    file_path = parse_args().file_path
    convert_to_wav(file_path)
