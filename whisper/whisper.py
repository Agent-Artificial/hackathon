import argparse
import subprocess
from pathlib import Path

from loguru import logger

path = Path


def run_whisper(
    whisper_bin="whisper.cpp/main",
    file_path="in/jfk.wav",
    model_path="whisper.cpp/models/ggml-base.en.bin",
):
    file_path = path.cwd() / file_path
    model_path = path.cwd() / model_path
    try:
        result = subprocess.run(
            [f"{whisper_bin}", "-m", f"{model_path}", "-f", f"{file_path}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        logger.debug(result.stdout.decode("utf-8"))
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as error:
        logger.error(error)
        return error
    except RuntimeError as error:
        logger.error(error)
        return error


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file_path", default="input/jfk.wav", type=str, required=False
    )
    parser.add_argument(
        "-m",
        "--model_path",
        default="whisper.cpp/models/ggml-base.en.bin",
        type=str,
        required=False,
    )
    parser.add_argument("-w", "--whisper_bin", default="whisper.cpp/main", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    run_whisper(**vars(args))
