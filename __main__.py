import os
import urwid
import logging
from player import Player
from ripper import Ripper
import atexit

class StreamRipPlayer:
    def __init__(self):
        self.palette = [
                ('header', 'black', 'dark green'),
                ('footer', 'black', 'brown'),
                ('reveal focus', 'black', 'dark cyan', 'standout'),
                ]
        self.content = urwid.SimpleListWalker(self.read_m3u_playlist('playlist.m3u'))
        self.listbox = urwid.ListBox(self.content)
        self.show_key = urwid.Text("StreamRipPlayer - "
                +"Rip [Enter], Play [p] VolUp [+,*] VolDn [/,-]", 
                wrap='clip')
        self.show_status = urwid.Text("Stopped", wrap='clip')
        foot = urwid.AttrMap(self.show_status, 'footer')
        head = urwid.AttrMap(self.show_key, 'header')
        self.top = urwid.Frame(self.listbox, head, foot)

    def read_m3u_playlist(self,filename):
        info = []
        urls = []
        for line in file(filename):
            if line.startswith('#EXTINF'):
                info.append(line.replace("#EXTINF:", "").strip().split(',')[1])
            if line.startswith('http'):
                urls.append(line)
    
        return [ urwid.AttrMap(urwid.Text(i), {'url':u, 'title': i}, 'reveal focus') for i,u in zip(info,urls) ]



    def show_all_input(self,input, raw):
        #self.show_key.set_text("Pressed: " + " ".join([
        #    unicode(i) for i in input]))
        curr_index = self.content.get_focus()[1]
        count = len(self.content)
        for key in input:
            if key == 'down':
                next = self.content.get_next(curr_index)[1]
                next = next if next else 0
                self.content.set_focus(next) 
                self.listbox.set_focus_valign('middle')
                input.remove(key)
            elif key == 'up':
                prev = self.content.get_prev(curr_index)[1]
                prev = prev if prev else count
                self.content.set_focus(prev)
                input.remove(key)
        return input

    def exit_on_cr(self,input):
        if input == 'enter':
            url = self.listbox.get_focus()[0].get_attr_map()['url']
            self.show_status.set_text("Ripping from %s" % self.listbox.get_focus()[0].get_attr_map()['title'])
            logging.warn(url)
            Ripper.start(url)
        elif input == 'p':
            Player.start()
        elif input == ' ':
            Player.pause()
        elif input in ['/','-']:
            Player.voldown()
        elif input in ['*','+']:
            Player.volup()
        elif input == 'q':
            raise urwid.ExitMainLoop()
    
    def start(self):
        loop = urwid.MainLoop(self.top, self.palette,
            input_filter=self.show_all_input, unhandled_input=self.exit_on_cr)
        loop.run()

@atexit.register
def stop():
    Player.stop()
    Ripper.stop()
    logging.info("Bye ...")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='srmp.log',
                    filemode='w')
    srmp = StreamRipPlayer()
    srmp.start()
