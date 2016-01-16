#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Forta(a)"
__copyright__ = "Copyright 2016, Forta(a)"
__license__ = "GPL 3.0"
__version__ = "0.2"

DEFAULT_HOST="0.0.0.0"
DEFAULT_PORT=44100
DEFAULT_RATE=44100
DEFAULT_LATENCY=100

#will be replaced by the first command argument if supplied
DEFAULT_ALSASINK="hw:1,0"

# relevant for 2-ch 44.1kHz and 48kHz only
DEFAULT_CONFIG_MAP = {
    44100 : 40002420,
    48000 : 40002320,
}

import sys     
import gi
gi.require_version('Gst','1.0')
from gi.repository import GObject,Gst

Gst.init(None)

def run_client(card=DEFAULT_ALSASINK,host=DEFAULT_HOST,port=DEFAULT_PORT,rate=DEFAULT_RATE,latency=DEFAULT_LATENCY,config_map=DEFAULT_CONFIG_MAP):
    pipeline = Gst.Pipeline()
    
    src = Gst.ElementFactory.make("udpsrc", "source")
    src.set_property("address", host)
    src.set_property("port", port)
    pad_caps = "application/x-rtp, media=(string)audio, clock-rate=(int){0}, encoding-name=(string)MP4A-LATM, cpresent=(string)0, config=(string){1}, payload=(int)96".format(rate,config_map[rate])
    src.set_property("caps", Gst.caps_from_string(pad_caps))
    jitterbuf = Gst.ElementFactory.make("rtpjitterbuffer","jitterbuf")
    jitterbuf.set_property("latency",latency)
    deserializer = Gst.ElementFactory.make("rtpmp4adepay", "deserializer")
    decoder = Gst.ElementFactory.make("faad", "decoder")
    converter = Gst.ElementFactory.make("audioconvert", "converter")
    dac = Gst.ElementFactory.make("alsasink", "sink")
    dac.set_property("device", card)
    dac.set_property("sync", False)

    pipeline.add(src)
    pipeline.add(jitterbuf)
    pipeline.add(deserializer)
    pipeline.add(decoder)
    pipeline.add(converter)
    pipeline.add(dac)
    src.link(jitterbuf)
    jitterbuf.link(deserializer)
    deserializer.link(decoder)
    decoder.link(converter)
    converter.link(dac)
    pipeline.set_state(Gst.State.PLAYING)
     
    loop = GObject.MainLoop()
    loop.run()
    
if __name__ == "__main__":
    run_client(sys.argv[1]) if len(sys.argv) == 2 else run_client()
