#! /usr/bin/env python

import argparse
import os
import sys
from tornado import autoreload
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

# Add the ConvNet scripts to the import path
sys.path.append(os.path.join(os.path.dirname(__file__), "../scripts"))

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True)
parser.add_argument("--caffe", type=str)
parser.add_argument("--image-corpus", type=str)
parser.add_argument("--port", type=int, default=5000)
parser.add_argument("--debug", action="store_true")

# TODO: Restore data loading and model stats w/Caffe+ImageNet compat
#parser.add_argument("--cifar", type=str, required=True)
#parser.add_argument("--model-stats", type=str, required=True)

parser.set_defaults(debug=False, caffe=None)
args = parser.parse_args()

# Needed in order to run on a server without an X GUI:
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
pyplot.ioff()

from deepviz_webui.app import app

app.config["TRAINED_MODEL_PATH"] = args.model
app.config["CAFFE_SPEC_PATH"] = args.caffe
app.config["IMAGE_CORPUS_PATH"] = args.image_corpus

# TODO: Restore data and stats w/Caffe+Imagenet
#app.config["CIFAR_10_PATH"] = args.cifar
#app.config["MODEL_STATS_DB"] = args.model_stats
app.debug = args.debug

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(args.port)
ioloop = IOLoop.instance()
if args.debug:
    autoreload.start(ioloop)
ioloop.start()

