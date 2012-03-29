#!/usr/bin/env python

import sys
import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')
import gst

class MuzikCalar:
    def __init__(self, location):
        # Pipeline ekleniyor
        self.pipeline=gst.Pipeline()

        # Bus uretiyoruz ve cesitli isleyicilere baglaniyoruz
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        #self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::tag', self.on_tag)
        self.bus.connect('message::error', self.on_error)

        # Elementler uretiliyor
        self.srcdec = gst.element_factory_make('uridecodebin')
        self.conv = gst.element_factory_make('audioconvert')
        self.rsmpl = gst.element_factory_make('audioresample')
        self.sink = gst.element_factory_make('alsasink')

        # Uri ozelligini MuzikCalar uzerine ayarliyoruz
        self.srcdec.set_property('uri', location)

        # 'pad-added' sinyali ile isleyiciye baglaniyoruz
        self.srcdec.connect('pad-added', self.on_pad_added)

        # Pipeline'a elementleri ekliyoruz
        self.pipeline.add(self.srcdec, self.conv, self.rsmpl, self.sink)

        # Bazi elementler baglaniyor
        # Bu self.on_new_decoded_pad()'de tamamlandi
        gst.element_link_many(self.conv, self.rsmpl, self.sink)

        # Kaynak self.on_new_decoded_pad()'de kullanildi
        self.apad = self.conv.get_pad('sink')

        # Ana dongu
        self.mainloop = gobject.MainLoop()

        # Ve calistiriyoruz
        self.pipeline.set_state(gst.STATE_PLAYING)
        self.mainloop.run()

        # Bazi fonksiyonlari tanimliyoruz
        def on_pad_added(self, element, pad):
           caps = pad.get_caps()
           name = caps[0].get_name()
           print 'on_pad_added:', name
           if name == 'audio/x-raw-float' or name == 'audio/x-raw-int':
               if not self.apad.is_linked():
                    pad.link(self.apad)

        def on_eos(self, bus, msg):
            print 'on_eos'
            self.pipeline.set_state(gst.STATE_NULL)
            self.mainloop.quit()

        def on_tag(self, bus, msg):
            taglist = msg.parse_tag()
            print 'on_tag:'
            for key in taglist.keys():
                print '\t%s = %s' % (key, taglist[key])

        def on_error(self, bus, msg):
            error = msg.parse_error()
            print 'on_error:', error[1]
            self.mainloop.quit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        MuzikCalar(sys.argv[1])
    else:
        print 'Usage: %s file:///path/to/media/file' %sys.argv[0],
	pygst._pygst_dir
