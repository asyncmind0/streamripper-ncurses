import ipdb
import urwid
import logging
import ripper, player

def read_m3u_playlist(filename):
    info = []
    urls = []
    for line in file(filename):
        if line.startswith('#EXTINF'):
            info.append(line.replace("#EXTINF:", "").strip().split(',')[1])
        if line.startswith('http'):
            urls.append(line)

    return [ urwid.AttrMap(urwid.Text(i), {'url':u, 'title': i}, 'reveal focus') for i,u in zip(info,urls) ]

palette = [('header', 'white', 'black'),
    ('reveal focus', 'black', 'dark cyan', 'standout'),]
content = urwid.SimpleListWalker(read_m3u_playlist('playlist.m3u'))
listbox = urwid.ListBox(content)
show_key = urwid.Text("", wrap='clip')
ripper_status = urwid.Text("", wrap='clip')
foot = urwid.AttrMap(ripper_status, 'footer')
head = urwid.AttrMap(show_key, 'header')
top = urwid.Frame(listbox, head, foot)


def show_all_input(input, raw):
    show_key.set_text("Pressed: " + " ".join([
        unicode(i) for i in input]))
    curr_index = content.get_focus()[1]
    count = len(content)
    for key in input:
        if key == 'down':
            next = content.get_next(curr_index)[1]
            next = next if next else 0
            content.set_focus(next) 
            listbox.set_focus_valign('middle')
            input.remove(key)
        elif key == 'up':
            prev = content.get_prev(curr_index)[1]
            prev = prev if prev else count
            content.set_focus(prev)
            input.remove(key)
    
    return input

def exit_on_cr(input):
    if input == 'enter':
        url = listbox.get_focus()[0].get_attr_map()['url']
        ripper_status.set_text("Ripping from %s" % listbox.get_focus()[0].get_attr_map()['title'])
        logging.warn(url)
        ripper.start(url)
    elif input == 'p':
        player.start()
    elif input == 'q':
        ripper.stop()
        player.stop()
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(top, palette,
    input_filter=show_all_input, unhandled_input=exit_on_cr)
loop.run()
