import tensorflow as tf
import time
import csv
import sys
import os
import collections

# Import the event accumulator from Tensorboard. Location varies between Tensorflow versions. Try each known location until one works.

eventAccumulatorImported = False

# TF version < 1.1.0
if not eventAccumulatorImported:
    try:
        from tensorflow.python.summary import event_accumulator

        eventAccumulatorImported = True
    except ImportError:
        eventAccumulatorImported = False

# TF version = 1.1.0
if not eventAccumulatorImported:
    try:
        from tensorflow.tensorboard.backend.event_processing import event_accumulator

        eventAccumulatorImported = True
    except ImportError:
        eventAccumulatorImported = False

# TF version >= 1.3.0
if not eventAccumulatorImported:
    try:
        from tensorboard.backend.event_processing import event_accumulator

        eventAccumulatorImported = True
    except ImportError:
        eventAccumulatorImported = False

# TF version = Unknown
if not eventAccumulatorImported:
    raise ImportError('Could not locate and import Tensorflow event accumulator.')

summariesDefault = ['scalars', 'histograms', 'images', 'audio', 'compressedHistograms']


def get_lognames(path):
    paths = os.walk(path)

    tags = []
    for dir, child_dir, file in paths:
        if len(file) == 0:
            continue
        dir = dir.replace(path, '')
        if dir.startswith('/'):
            dir = dir[1:]
        tags.append(dir)

    return tags


def parse_tags(path, logname, tag):
    dir = os.path.join(path, logname)
    files = list(os.walk(dir))[0][2]
    # filename = max(files, key=lambda x: os.path.getctime(os.path.join(dir, x)))

    scalars = []
    for filename in files:
        if 'events.out.tfevents.' not in filename:
            continue

        l = parse_tag_by_filename(path, logname, tag, filename)
        scalars.extend(l)

    # sort is guaranteed to be stable
    scalars.sort(key=lambda x: x[0])
    scalars.sort(key=lambda x: x[1])

    return scalars


def parse_tag_by_filename(path, logname, tag, filename):
    ea = event_accumulator.EventAccumulator(os.path.join(path, logname, filename),
                                            size_guidance={
                                                # event_accumulator.COMPRESSED_HISTOGRAMS: 0,  # 0 = grab all
                                                # event_accumulator.IMAGES: 0,
                                                # event_accumulator.AUDIO: 0,
                                                event_accumulator.SCALARS: 0,
                                                # event_accumulator.HISTOGRAMS: 0,
                                            })
    ea.Reload()
    try:
        return ea.Scalars(tag)
    except:
        return []
