import Tkinter
import pyxdevkit
import requests
import re


class MainFrame(Tkinter.Frame):

    def __init__(self, parent):
        self.parent = parent
        self.ip_addr = Tkinter.StringVar()
        self.squad_id = Tkinter.StringVar()
        self.goalie_name = Tkinter.StringVar()
        self.card_color = Tkinter.StringVar()
        self.card_color.set("Don't Override Color")
        self.cheat_stats_enabled = Tkinter.IntVar()
        self.do_layout()

    def do_layout(self):
        self.parent.title('FUTCheat -- Created By Fire30')
        self.parent.minsize(width=400, height=200)
        self.parent.maxsize(width=400, height=200)

        layout_args = {
            'row': 0, 'column': 0, 'pady': (10, 0), 'padx': (10, 0), 'sticky': Tkinter.W}

        Tkinter.Label(text='Console IP:').grid(**layout_args)

        layout_args['column'] = 1

        Tkinter.Entry(textvariable=self.ip_addr).grid(**layout_args)

        layout_args['column'] = 0
        layout_args['row'] = 1

        Tkinter.Label(text='Futhead Squad ID:').grid(**layout_args)

        layout_args['column'] = 1
        layout_args['row'] = 1
        Tkinter.Entry(textvariable=self.squad_id).grid(**layout_args)

        layout_args['column'] = 0
        layout_args['row'] = 2
        Tkinter.Label(text='Goalie Name in Current Squad:').grid(**layout_args)

        layout_args['column'] = 1
        layout_args['row'] = 2
        Tkinter.Entry(textvariable=self.goalie_name).grid(**layout_args)

        layout_args['column'] = 0
        layout_args['row'] = 3
        Tkinter.Label(text='Override Card Color:').grid(**layout_args)

        OPTIONS = ["Nonrare", "Rare", "Inform", "TOTS"]
        layout_args['column'] = 1
        layout_args['row'] = 3
        Tkinter.OptionMenu(root, self.card_color, *OPTIONS).grid(**layout_args)

        layout_args['column'] = 0
        layout_args['row'] = 4
        Tkinter.Checkbutton(
            text="99 Overall Players", variable=self.cheat_stats_enabled).grid(**layout_args)

        layout_args['column'] = 1
        layout_args['row'] = 4
        button = Tkinter.Button(
            root, text="Send Command", command=self.sent_pressed)
        button.grid(**layout_args)

    def sent_pressed(self):
        send_command(self.ip_addr.get(), self.squad_id.get(),
                     self.goalie_name.get(), self.card_color.get(),
                     self.cheat_stats_enabled.get())


def match_class(target):
    target = target.split()

    def do_match(tag):
        try:
            classes = dict(tag.attrs)["class"]
        except KeyError:
            classes = ""
        classes = classes.split()
        return all(c in classes for c in target)
    return do_match


def send_command(ip_addr, squad_id, goalie_name, card_color, cheat_stats_enabled):

    con = pyxdevkit.Console(ip_addr)

    r = requests.get('http://www.futhead.com/15/squads/%s/' % squad_id)

    regex = '<img.+?src="http://futhead.cursecdn.com/static/img/15/players/(.+?)[\"\'].*?>'
    vals = map(lambda x: int(x.replace('.png', '')), re.findall(regex, r.text))

    print vals
    addr = 0xCDF00000
    length = 0x00100000

    mem = con.get_mem(addr, length)
    print len(mem)
    hh = mem.find(goalie_name.get().strip())

    idx = 0
    print vals
    for x in reversed(vals):
        if cheat_stats_enabled:
            con.set_mem(addr + hh - 0x10, 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00')
        con.set_mem(addr + hh - 0x14, '0001B265')
        con.set_mem(addr + hh + 0x91, '13')  # country
        con.set_mem(addr + hh + 0xA3, '%02X' % idx)
        con.set_mem(addr + hh + 0x9F, '35')
        con.set_mem(addr + hh - 0x68, x)
        con.set_mem(addr + hh - 0x64, x)
        con.set_mem(addr + hh - 0x60, x)
        print idx
        idx += 1
        hh += 0x140

root = Tkinter.Tk()
fram = MainFrame(root)
root.mainloop()
