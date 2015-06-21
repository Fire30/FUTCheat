import Tkinter
import pyxdevkit
import requests
import re
import os


RAREFLAGS = {"Nonrare":0,"Rare":1,"Inform":3,"Purple":4,"Blue":5,"Blue with Red Interior":6,"Green":7,"Orange":8,"Pink":9,"Teal":10,"Legend":11,"Light Blue":14}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MyDialog():
    def __init__(self, parent,msg):

        self.top = Tkinter.Toplevel(parent)
        self.top.title('')
        self.top.geometry("+%d+%d" % (parent.winfo_rootx()+200,
                                  parent.winfo_rooty()+50))
        self.top.minsize(width=200, height=100)
        self.top.maxsize(width=200, height=100)
        layout_args = {'row': 0, 'column': 0, 'pady': (20, 0), 'padx': (20, 0)}
        Tkinter.Label(self.top, text=msg).grid(**layout_args)
        layout_args['row'] = 1
        layout_args['pady'] = (10, 0)
        button = Tkinter.Button(self.top, text="OK",command=self.button_pressed,width=10).grid(**layout_args)
    def button_pressed(self):
        self.top.destroy()

class MainFrame(Tkinter.Frame):

    def __init__(self, parent):
        self.parent = parent
        print(resource_path('res/favicon.ico'))
        self.parent.iconbitmap(resource_path('res/favicon.ico'))
        self.ip_addr = Tkinter.StringVar()
        self.squad_id = Tkinter.StringVar()
        self.goalie_name = Tkinter.StringVar()
        self.card_color = Tkinter.StringVar()
        self.cheat_stats_enabled = Tkinter.IntVar()
        self.do_layout()

    def do_layout(self):
        self.parent.title('FUTCheat -- Created By Fire30')
        self.parent.minsize(width=400, height=275)
        self.parent.maxsize(width=400, height=275)

        layout_args = {'row': 0, 'column': 0, 'pady': (10, 0), 'padx': (10, 0), 'sticky': Tkinter.W}

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

        self.card_color.set("Don't Override Color")
        layout_args['column'] = 1
        layout_args['row'] = 3
        Tkinter.OptionMenu(root, self.card_color, *RAREFLAGS.keys()).grid(**layout_args)

        layout_args['column'] = 0
        layout_args['row'] = 4
        Tkinter.Checkbutton(
            text="99 Overall Players", variable=self.cheat_stats_enabled).grid(**layout_args)

        layout_args['column'] = 1
        layout_args['row'] = 4
        button = Tkinter.Button(
            root, text="Send Command", command=self.sent_pressed)
        button.grid(**layout_args)
        layout_args['column'] = 0
        layout_args['columnspan'] = 3
        layout_args['row'] = 5
        instr = 'Note: You must send the command when the teams are choosing jerseys.' \
                ' If the command is succesful then in team management you will see the' \
                ' new players or if you back out you will see the new cards. You must do' \
                ' this every time you are choosing teams.'
        Tkinter.Label(text=instr,wraplength=350,anchor=Tkinter.W,justify=Tkinter.LEFT).grid(**layout_args)

    def sent_pressed(self):
        try:
            send_command(self.ip_addr.get(), self.squad_id.get(),
                     self.goalie_name.get(), self.card_color.get(),
                     self.cheat_stats_enabled.get())
            msg = 'Command Sent Sucesfully!'
        except:
            msg = 'Unable to Send Command!'
        d = MyDialog(self.parent,msg)
        self.parent.wait_window(d.top)

def send_command(ip_addr, squad_id, goalie_name, card_color, cheat_stats_enabled):
    con = pyxdevkit.Console(ip_addr)
    con.connect()
    r = requests.get('http://www.futhead.com/15/squads/%s/' % squad_id)

    regex = '<img.+?src="http://futhead.cursecdn.com/static/img/15/players/(.+?)[\"\'].*?>'
    vals = map(lambda x: '%08X' % int(x[:-4]), re.findall(regex, r.text))

    rareflag_id = RAREFLAGS.get(card_color)
    addr = 0xCDF00000
    length = 0x00100000
    mem = con.get_mem(addr, length)
    hh = mem.find(goalie_name)

    idx = 10
    for x in reversed(vals):
        if cheat_stats_enabled:
            con.set_mem(addr + hh - 0x10, 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00')
        con.set_mem(addr + hh - 0x14, '0001B265')
        con.set_mem(addr + hh + 0x91, '13')  # country
        if rareflag_id:
            con.set_mem(addr + hh + 0xA3, '%02X' % rareflag_id)
        con.set_mem(addr + hh + 0x9F, '35')
        con.set_mem(addr + hh - 0x68, x)
        con.set_mem(addr + hh - 0x64, x)
        con.set_mem(addr + hh - 0x60, x)
        idx += 1
        hh += 0x140

root = Tkinter.Tk()
fram = MainFrame(root)
root.mainloop()

