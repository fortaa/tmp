#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Forta(a)"
__copyright__ = "Copyright 2016, Forta(a)"
__license__ = "GPL 3.0"
__version__ = "0.2"

DEFAULT_BROADCAST="192.168.10.255"
DEFAULT_PORT=44100
DEFAULT_RATE=44100

DEFAULT_BITRATE=320000

#will be replaced by the first command argument if supplied
DEFAULT_ALSASRC="hw:1,1"

import sys     
import gi
gi.require_version('Gst','1.0')
from gi.repository import GObject,Gst

Gst.init(None)

def run_server(alsadev=DEFAULT_ALSASRC,audience=DEFAULT_BROADCAST,port=DEFAULT_PORT,bitrate=DEFAULT_BITRATE,alsarate=DEFAULT_RATE):     
    pipeline = Gst.Pipeline()
     
    src = Gst.ElementFactory.make("alsasrc", "source")
    src.set_property("device", alsadev)
    converter = Gst.ElementFactory.make("audioconvert", "converter")
    encoder = Gst.ElementFactory.make("faac", "encoder")
    encoder.set_property("bitrate", bitrate)
    serializer = Gst.ElementFactory.make("rtpmp4apay", "serializer")
    server = Gst.ElementFactory.make("udpsink", "server")
    server.set_property("host", audience)
    server.set_property("port", port)

    pipeline.add(src)
    pipeline.add(converter)
    pipeline.add(encoder)
    pipeline.add(serializer)
    pipeline.add(server)
    src.link_filtered(converter,Gst.caps_from_string("audio/x-raw,format=(string)S32LE,channels=(int)2,rate=(int){0}".format(alsarate)))
    converter.link(encoder)
    encoder.link(serializer)
    serializer.link(server)
    pipeline.set_state(Gst.State.PLAYING)
     
    loop = GObject.MainLoop()
    loop.run()

if __name__ == "__main__":
    run_server(sys.argv[1]) if len(sys.argv) == 2 else run_server()
