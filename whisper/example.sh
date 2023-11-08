#! /bin/bash

cp whisper.cpp/samples/jfk.wav in

python convert_file.py -f in/jfk.wav

python whisper.py -f in/jfk.wav -m whisper.cpp/models/ggml-base.en.bin -o out -w whisper.cpp/main