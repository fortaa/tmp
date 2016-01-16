#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Forta(a)"
__copyright__ = "Copyright 2016, Forta(a)"
__license__ = "GPL 3.0"
__version__ = "0.1"

DEFAULT_HOST="0.0.0.0"
DEFAULT_PORT=44100
DEFAULT_RATE=44100

#will be replaced by the first command argument if supplied
DEFAULT_ALSASINK="hw:1,0"

import sys     
import gi
gi.require_version('Gst','1.0')
from gi.repository import GObject,Gst

Gst.init(None)

def run_client(card=DEFAULT_ALSASINK,host=DEFAULT_HOST,port=DEFAULT_PORT,rate=DEFAULT_RATE):
    pipeline = Gst.Pipeline()
    
    src = Gst.ElementFactory.make("udpsrc", "source")
    src.set_property("address", host)
    src.set_property("port", port)
    pad_caps = "application/x-rtp, media=(string)audio, clock-rate=(int){0}, encoding-name=(string)L24, encoding-params=(string)2, channels=(int)2, payload=(int)96".format(rate)
    src.set_property("caps", Gst.caps_from_string(pad_caps))
    deserializer = Gst.ElementFactory.make("rtpL24depay", "deserializer")
    converter = Gst.ElementFactory.make("audioconvert", "converter")
    dac = Gst.ElementFactory.make("alsasink", "sink")
    dac.set_property("device", card)
    dac.set_property("sync", False)

    pipeline.add(src)
    pipeline.add(deserializer)
    pipeline.add(converter)
    pipeline.add(dac)
    src.link(deserializer)
    deserializer.link(converter)
    converter.link(dac)
    pipeline.set_state(Gst.State.PLAYING)
     
    loop = GObject.MainLoop()
    loop.run()
    
if __name__ == "__main__":
    run_client(sys.argv[1]) if len(sys.argv) == 2 else run_client()
