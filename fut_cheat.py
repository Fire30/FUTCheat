import Tkinter as tk
from Tkinter import *
import requests
import BeautifulSoup
import pyxdevkit

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

def displayText():
    ip_addr =  entryWidget.get().strip()
    con = pyxdevkit.Console(ip_addr)

    r = requests.get('http://www.futhead.com/15/squads/%s/' % url_entry.get().strip())

    soup = BeautifulSoup.BeautifulSoup(r.text)
    vals = []
    for x in soup.findAll(match_class("player filled")):
        for y in x.findAll(match_class("playercard-picture")):
            c = y.find('img')['src'].split('/')
            c = int(c[len(c) - 1].split('.')[0])
            c = '%08X' % c
            vals.append(c)

    addr = 0xCDF00000
    length = 0x00100000

    mem = con.get_mem(addr,length)
    print len(meme)
    hh = mem.find(goalie_name.get().strip())

    idx = 0
    print vals
    for x in reversed(vals):
        if cheat_stats.get():
            con.set_mem(addr+hh - 0x10,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00')
        con.set_mem(addr+hh - 0x14,'0001B265')
        con.set_mem(addr+hh + 0x91,'13') # country
        con.set_mem(addr+hh + 0xA3,'%02X' % idx)
        con.set_mem(addr+hh + 0x9F,'35')
        con.set_mem(addr+hh - 0x68,x)
        con.set_mem(addr+hh - 0x64,x)
        con.set_mem(addr+hh - 0x60,x)
        print idx
        idx += 1
        hh += 0x140


root = tk.Tk()
root.minsize(width=350, height=200)
root.maxsize(width=350, height=200)

entryLabel = tk.Label(text='Console IP:')
entryLabel.grid(row=0,column=0,pady=(10,0),padx=(10,10),sticky=W)
# Create an Entry Widget in textFrame
entryWidget = tk.Entry()
entryWidget.grid(row=0,column=1,sticky=W)

entryLabel = tk.Label(text='Futhead Squad ID:')
entryLabel.grid(row=1,column=0,pady=(10,0),padx=(10,10),sticky=W)

url_entry = tk.Entry()
url_entry.grid(row=1,column=1,sticky=W)

entryLabel = tk.Label(text='Goalie Name in Current Squad:')
entryLabel.grid(row=2,column=0,pady=(10,0),padx=(10,10),sticky=W)

goalie_name = tk.Entry()
goalie_name.grid(row=2,column=1,sticky=W)

entryLabel = tk.Label(text='Override Card Color:')
entryLabel.grid(row=3,column=0,pady=(10,0),padx=(10,10),sticky=W)

var = StringVar(root)
var.set("Do Not Override")
option = OptionMenu(root, var, "Nonrare", "Rare", "Inform", "TOTS")
option.grid(row=3,column=1,pady=(10,10),padx=(10,10),sticky=W)
cheat_stats = IntVar()
c = Checkbutton(text="99 Overall Players",variable=cheat_stats)
c.grid(row=4,column=0,pady=(10,0),padx=(10,10),sticky=W)

button = Button(root, text="Send Command", command=displayText)
button.grid(row=4,column=1,padx=(10,10))

root.mainloop()
