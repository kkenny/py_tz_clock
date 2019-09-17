"""Python Timezone Clock with TKinter interface."""

from tkinter import Tk, Frame, W, Label
from datetime import datetime
import pytz
import yaml

with open("config.yml", 'r') as ymlfile:
    CFG = yaml.load(ymlfile, Loader=yaml.SafeLoader)

LABEL_T = {}
LABEL_D = {}
LABEL_DESC = {}
FRAME = {}
TZ = {}

def draw():
    """draw the default layout."""
    c_row = 0
    for region in CFG['TimeZones']:
        for city in CFG['TimeZones'][region]:
            o_city = CFG['TimeZones'][region][city]
            c_row += 1
            FRAME[city] = {}
            LABEL_DESC[city] = {}

            for i in range(0, 3):
                FRAME[city][i] = Frame(ROOT,
                                       width=CFG['defaults']['frame']['width'],
                                       height=CFG['defaults']['frame']['height'],
                                       background=CFG['defaults']['colors']['background'])

                FRAME[city][i].grid(
                    row=c_row-1,
                    column=i,
                    sticky=W)

            if 'description' in o_city:
                desc = o_city["description"]
            else:
                desc = o_city["tz"]

            COLORS = {}

            if 'colors' in o_city:
                if 'description' in o_city['colors']:
                    print(o_city['colors']['description'])
                    COLORS['description'] = o_city['colors']['description']
                else:
                    print(CFG['defaults']['colors']['description'])
                    COLORS['description'] = CFG['defaults']['colors']['description']

                if 'time' in o_city['colors']:
                    COLORS['time'] = o_city['colors']['time']
                else:
                    COLORS['time'] = CFG['defaults']['colors']['time']

                if 'date' in o_city['colors']:
                    COLORS['date'] = o_city['colors']['date']
                else:
                    COLORS['date'] = CFG['defaults']['colors']['date']
            else:
                COLORS = CFG['defaults']['colors']

            LABEL_DESC[city] = Label(
                FRAME[city][0],
                text=desc,
                background=CFG['defaults']['colors']['background'],
                fg=COLORS['description'],
                font=(
                    CFG['defaults']['label']['font']['face'],
                    CFG['defaults']['label']['font']['size'],
                    CFG['defaults']['label']['font']['weight']),
                padx=CFG['defaults']['label']['padding']['x'],
                pady=CFG['defaults']['label']['padding']['y'],
                justify=CFG['defaults']['label']['justify'])

            LABEL_T[city] = Label(
                FRAME[city][1],
                text=desc,
                background=CFG['defaults']['colors']['background'],
                fg=COLORS['time'],
                font=(
                    CFG['defaults']['label']['font']['face'],
                    CFG['defaults']['label']['font']['size'],
                    CFG['defaults']['label']['font']['weight']),
                padx=CFG['defaults']['label']['padding']['x'],
                pady=CFG['defaults']['label']['padding']['y'],
                justify=CFG['defaults']['label']['justify'])

            LABEL_D[city] = Label(
                FRAME[city][2],
                text=desc,
                background=CFG['defaults']['colors']['background'],
                fg=COLORS['date'],
                font=(
                    CFG['defaults']['label']['font']['face'],
                    CFG['defaults']['label']['font']['size'],
                    CFG['defaults']['label']['font']['weight']),
                padx=CFG['defaults']['label']['padding']['x'],
                pady=CFG['defaults']['label']['padding']['y'],
                justify=CFG['defaults']['label']['justify'])

            LABEL_DESC[city].pack()
            LABEL_T[city].pack()
            LABEL_D[city].pack()


def refresher():
    """Refresh the layout every second with new time and date."""


    for region in CFG['TimeZones']:
        for city in CFG['TimeZones'][region]:
            o_city = CFG['TimeZones'][region][city]
            TZ[city] = pytz.timezone(o_city['tz'])

            LABEL_T[city].configure(
                text=datetime.now(
                    TZ[city]).strftime(
                    CFG['defaults']['format']['time']))

            LABEL_D[city].configure(
                text=datetime.now(
                    TZ[city]).strftime(
                    CFG['defaults']['format']['date']))

    ROOT.after(1000, refresher)

ROOT = Tk()
#ROOT.wm_attributes('-alpha',0.6)
ROOT.wm_minsize(
    width=CFG['defaults']['window']['width'],
    height=CFG['defaults']['window']['height'])

ROOT.title(
    string=CFG['appName'])

ROOT.configure(
    background=CFG['defaults']['colors']['background'])

draw()
refresher()
ROOT.mainloop()
