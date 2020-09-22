import uuid
import io
from math import ceil
from PIL import Image, ImageDraw, ImageFont
from json import loads
import textwrap
import os.path
textColor = (0, 0, 0)
bgColor = (255, 255, 255)


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


class Maxim:
    def __init__(
        self,
        size=(1080, 1080),
        Colors=(textColor, bgColor),
        text=('MR. MAXIM', 'center_bottom'),
        font='./fonts/constani.ttf',
        fontsize=36,
        logo=('./img/logo.jpg', 'bottom', 'center'),
        logoResize=True,
        logoSize=(180, 180)
    ):
        self.bgColor = Colors[1]
        self.width = size[0]
        self.height = size[1]
        self.text = text[0]
        self.textAlign = text[1]
        self.textColor = Colors[0]
        self.font = ImageFont.truetype(font, fontsize)
        self.logo = logo[0]
        self.logoAlign_Vertical = logo[1]
        self.logoAlign_Horizontal = logo[2]
        self.logoSize = logoSize
        self.logoResize = logoResize

    def Start(self):
        f = io.open("texts.txt", mode="r", encoding="utf-8")
        texts = f.read()
        texts = loads(texts)
        f = io.open("config.txt", mode="r", encoding="utf-8")
        configs = f.read()
        configs = loads(configs)
        textcolor = []
        for number in configs["textcolor"]:
            textcolor.append(number)
        textcolor = (
            textcolor[0], textcolor[1], textcolor[2])
        backgroundcolor = []
        for number in configs["backgroundcolor"]:
            backgroundcolor.append(number)
        backgroundcolor = (
            backgroundcolor[0], backgroundcolor[1], backgroundcolor[2])
        width = configs["width"]
        height = configs["height"]
        textalign = configs["textalign"]
        fontsize = configs["fontsize"]
        logo = (configs["logo"], configs["logovertical"],
                configs["logohorizontal"])
        if configs["logoresize"] == 1:
            logoresize = True
        else:
            logoresize = False
        logosize = (configs["logosizew"], configs["logosizeh"])
        font = configs["font"]

        counter = 1
        l = len(texts)
        printProgressBar(0, l, prefix='Progress:',
                         suffix='Complete', length=50)
        for text in texts:
            photo = Maxim(
                [width,
                 height],
                [textcolor,
                 backgroundcolor], [
                    text, textalign], font, fontsize, logo, logoresize, logosize)
            photo.Create(counter, './outputs/')
            counter += 1
            printProgressBar(counter-1, l, prefix='Progress:',
                             suffix='Complete', length=50)
        print(l, " Photos Created...\n Press Enter To Exit")
        input()

    def Create(self, name=uuid.uuid1(), directory='./'):
        img = Image.new('RGB', (self.width, self.height), color=self.bgColor)
        d = ImageDraw.Draw(img)
        w, h = d.textsize(self.text["quote"], font=self.font)
        Text_Left = 10
        Text_Top = 200
        # check text align
        if self.textAlign.lower() == "left":
            Text_Left = 10
        elif self.textAlign.lower() == "right":
            Text_Left = ceil(self.width-w)
        elif self.textAlign.lower() == "center_bottom":
            Text_Left = ceil(self.width-w)/2
            Text_Top = ceil(self.height-h)-10
        elif self.textAlign.lower() == "left_bottom":
            Text_Left = 10
            Text_Top = ceil(self.height-h)-10
        elif self.textAlign.lower() == "right_bottom":
            Text_Left = ceil(self.width-w)
            Text_Top = ceil(self.height-h)-10
        elif self.textAlign.lower() == "center_top":
            Text_Left = ceil(self.width-w)/2
            Text_Top = 10
        elif self.textAlign.lower() == "left_top":
            Text_Left = 10
            Text_Top = 200
        elif self.textAlign.lower() == "right_top":
            Text_Left = ceil(self.width-w)
            Text_Top = 200
        else:
            Text_Left = ceil((self.width-w)/2)
            Text_Top = ceil((self.height-h)/2)-10
        TextAlign = (Text_Left, Text_Top)
        Text_Top = 300
        lines = textwrap.wrap(self.text["quote"], width=ceil(self.width/36))
        y_text = Text_Top
        for line in lines:
            width, height = self.font.getsize(line)
            d.text(((self.width - width) / 2, y_text+5), line,
                   font=self.font, fill=self.textColor)
            y_text += height+5
        width, height = self.font.getsize(self.text["author"])
        y_text += height
        d.text(((self.width - width) / 2, y_text), self.text["author"],
               font=self.font, fill=self.textColor)
        logo_img = Image.open(self.logo)
        image_Width, image_Height = logo_img.size
        # check logo size
        if self.width <= image_Width or self.height <= image_Height:
            logo_img = logo_img.resize(self.logoSize, Image.LANCZOS)
            image_Width, image_Height = logo_img.size
        elif self.logoResize:
            logo_img = logo_img.resize(self.logoSize, Image.LANCZOS)
            image_Width, image_Height = logo_img.size
        # check logo align
        if self.logoAlign_Horizontal.lower() == "center":
            Left = ceil((self.width - image_Width)/2)
        elif self.logoAlign_Horizontal.lower() == "right":
            Left = ceil(self.width-image_Width)-5
        else:
            Left = 5
        if self.logoAlign_Vertical.lower() == "center":
            Top = ceil((self.height - image_Height)/2)
        elif self.logoAlign_Vertical.lower() == "bottom":
            Top = ceil(self.height-image_Height)-5
        else:
            Top = 25

        align = (Left, Top)
        back_im = img.copy()
        back_im.paste(logo_img, align)

        back_im.save(directory+str(name)+'.jpg', quality=100)


if not os.path.exists("./outputs"):
    os.mkdir("./outputs")
if not os.path.exists("./img"):
    print("img directory is missing")
    exit()
if not os.path.exists("./fonts"):
    print("fonts directory is missing")
    exit()
photo = Maxim()
photo.Start()
