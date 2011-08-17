import ipdb
import urwid
import logging

def read_m3u_playlist(filename):
    info = []
    urls = []
    for line in file(filename):
        if line.startswith('#EXTINF'):
            info.append(urwid.Text(line.replace("#EXTINF:", "").strip().split(',')[1]))
        if line.startswith('http'):
            urls.append(line)

    return [ urwid.AttrMap(i, {'url':u}, 'reveal focus') for i,u in zip(info,urls) ]

palette = [('header', 'white', 'black'),
    ('reveal focus', 'black', 'dark cyan', 'standout'),]
content = urwid.SimpleListWalker(read_m3u_playlist('playlist.m3u'))
#        [
#    urwid.AttrMap(w, None, 'reveal focus') for w in [
#    urwid.Text("This is a text string that is fairly long"),
#    urwid.Divider("-"),
#    urwid.Text("Short one"),
#    urwid.Text("Another"),
#    urwid.Divider("-"),
#    urwid.Text("What could be after this?"),
#    urwid.Text("The end."),]])
listbox = urwid.ListBox(content)
show_key = urwid.Text("", wrap='clip')
head = urwid.AttrMap(show_key, 'header')
top = urwid.Frame(listbox, head)


def show_all_input(input, raw):
    show_key.set_text("Pressed: " + " ".join([
        unicode(i) for i in input]))
    curr_index = content.get_focus()[1]
    count = len(content)
    #for key in input:
    #    if key == 'down':
    #        next = content.get_next(curr_index)[1]
    #        next = next if next else 0
    #        content.set_focus(next) 
    #        input.remove(key)
    #    elif key == 'up':
    #        prev = content.get_prev(curr_index)[1]
    #        prev = prev if prev else count
    #        content.set_focus(prev)
    #        input.remove(key)
    
    return input

def exit_on_cr(input):
    if input == 'enter':
        logging.warn( listbox.get_focus()[0].get_attr_map()['url'])
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(top, palette,
    input_filter=show_all_input, unhandled_input=exit_on_cr)
loop.run()
