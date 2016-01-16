#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Forta(a)"
__copyright__ = "Copyright 2016, Forta(a)"
__license__ = "GPL 3.0"
__version__ = "0.1"

DEFAULT_BROADCAST="192.168.10.255"
DEFAULT_PORT=44100

#will be replaced by the first command argument if supplied
DEFAULT_ALSASRC="hw:1,1"

import sys     
import gi
gi.require_version('Gst','1.0')
from gi.repository import GObject,Gst

Gst.init(None)

def run_server(alsadev=DEFAULT_ALSASRC,audience=DEFAULT_BROADCAST,port=DEFAULT_PORT):     
    pipeline = Gst.Pipeline()
     
    src = Gst.ElementFactory.make("alsasrc", "source")
    src.set_property("device", alsadev)
    converter = Gst.ElementFactory.make("audioconvert", "converter")
    serializer = Gst.ElementFactory.make("rtpL24pay", "serializer")
    server = Gst.ElementFactory.make("udpsink", "server")
    server.set_property("host", audience)
    server.set_property("port", port)

    pipeline.add(src)
    pipeline.add(converter)
    pipeline.add(serializer)
    pipeline.add(server)
    src.link(converter)
    converter.link(serializer)
    serializer.link(server)
    pipeline.set_state(Gst.State.PLAYING)
     
    loop = GObject.MainLoop()
    loop.run()

if __name__ == "__main__":
    run_server(sys.argv[1]) if len(sys.argv) == 2 else run_server()
