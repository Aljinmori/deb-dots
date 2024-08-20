#!/usr/bin/env python3

import sys
import time
import struct
import os
import subprocess
import configparser
from collections import OrderedDict

# Configurations
BAR_FACTOR = 100 / 7
BAR_CHARACTERS = OrderedDict([
    (0, '▁'),
    (BAR_FACTOR * 1, '▁'),
    (BAR_FACTOR * 2, '▂'),
    (BAR_FACTOR * 3, '▃'),
    (BAR_FACTOR * 4, '▄'),
    (BAR_FACTOR * 5, '▅'),
    (BAR_FACTOR * 6, '▆'),
    (BAR_FACTOR * 7, '▇'),
    (100, '█'),
])
SEPARATOR = ' '
HIDE_WHEN_EMPTY = False
OUTPUT_DELAY = 0.0005
EMPTY_OUTPUT_THRESHOLD = 5
PIPE_OUT = None
CAVA_CONFIG_PATH = "/tmp/cava_polybar.config"
PIPE_IN = "/tmp/cava_polybar_input.fifo"
CAVA_BARS_NUMBER = 6
CAVA_BIT_FORMAT = "16bit"
bytetype, bytesize, bytenorm = ("H", 2, 65535) if CAVA_BIT_FORMAT == "16bit" else ("B", 1, 255)

def output(string, file):
    if PIPE_OUT:
        file.write(string)
    else:
        print(string, end="")
        sys.stdout.flush()
    time.sleep(OUTPUT_DELAY)

def valueToCharacter(value):
    for bar_threshold in BAR_CHARACTERS:
        if value < bar_threshold:
            return BAR_CHARACTERS[bar_threshold]
    return BAR_CHARACTERS[100]

def run():
    createCavaConfig()
    FNULL = open(os.devnull, 'w')
    cavaProcess = subprocess.Popen(["cava", "-p", CAVA_CONFIG_PATH], stdout=FNULL, stderr=subprocess.STDOUT)

    outputPipe = None
    if PIPE_OUT:
        if os.path.exists(PIPE_OUT):
            os.remove(PIPE_OUT)
        os.mkfifo(PIPE_OUT)
        outputPipe = open(PIPE_OUT, "w")

    if not os.path.exists(PIPE_IN):
        os.mkfifo(PIPE_IN)
    
    inputPipe = open(PIPE_IN, "rb")

    try:
        convert(inputPipe, outputPipe)
    except KeyboardInterrupt:
        pass

    if PIPE_OUT:
        outputPipe.close()
        os.remove(PIPE_OUT)
    inputPipe.close()
    cavaProcess.kill()

def convert(inputPipe, outputPipe=None):
    chunk = bytesize * CAVA_BARS_NUMBER
    fmt = bytetype * CAVA_BARS_NUMBER
    emptyOutputs = 0

    while True:
        rawData = inputPipe.read(chunk)
        if len(rawData) < chunk:
            break

        tstring = ""
        emptyOutput = True

        for i in struct.unpack(fmt, rawData):
            value = int(i / bytenorm * 100)
            tstring += SEPARATOR if len(tstring) > 0 else ""
            tstring += valueToCharacter(value)
            if value != 0:
                emptyOutput = False

        if emptyOutput and HIDE_WHEN_EMPTY:
            emptyOutputs += 1
            if emptyOutputs > EMPTY_OUTPUT_THRESHOLD:
                output(" " * CAVA_BARS_NUMBER + os.linesep, outputPipe)
        else:
            emptyOutputs = 0
            output(tstring + os.linesep, outputPipe)

def createCavaConfig():
    config = configparser.ConfigParser()
    config.add_section('general')
    config.set('general', 'bars', str(CAVA_BARS_NUMBER))
    config.set('general', 'overshoot', '0')

    config.add_section('output')
    config.set('output', 'method', 'raw')
    config.set('output', 'channels', 'mono')
    config.set('output', 'mono_option', 'average')
    config.set('output', 'raw_target', PIPE_IN)
    config.set('output', 'bit_format', CAVA_BIT_FORMAT)

    config.add_section('smoothing')
    config.set('smoothing', 'integral', '0')

    with open(CAVA_CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    BAR_CHARACTERS = OrderedDict(sorted(BAR_CHARACTERS.items()))
    run()
