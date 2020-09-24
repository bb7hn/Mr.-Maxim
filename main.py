import uuid
import io
from math import ceil
from PIL import Image, ImageDraw, ImageFont
from json import loads
import textwrap
import os.path
from colorama import Fore, Back, Style, init

init()
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
    print(f'\r{prefix} |{Fore.LIGHTGREEN_EX}{bar}{Style.RESET_ALL}| {percent}% {suffix}', end=printEnd)
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
        logo=('./img/logo/logo.jpg', 'bottom', 'center'),
        logoResize=True,
        logoSize=(180, 180),
        specialBG=False,
        bgImage="./img/background/bg.jpg",
        margintop=10,
        externalImage=False,
        extimage="./img/external/default.jpg",
        extimgw=300,
        extimgh=300,
        extimgalign="center",
        opacity=0,
        islogotransparent=1
    ):
        self.specialBG = specialBG
        self.bgImage = bgImage
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
        self.externalImage = externalImage
        self.extimage = extimage
        self.extimgwidth = extimgw
        self.extimgheight = extimgh
        self.extimgalign = extimgalign
        self.margintop = margintop
        self.opacity = opacity
        self.islogotransparent = islogotransparent

    def Create(self, name=uuid.uuid1(), directory='./'):
        if self.specialBG:
            img = Image.open(self.bgImage)
            img = img.resize([self.width, self.height], Image.LANCZOS)
            layer = Image.new('RGB', (self.width, self.height),
                              color=self.bgColor)
            layer.putalpha(self.opacity)
            img.paste(layer, (0, 0), layer)
        else:
            img = Image.new('RGB', (self.width, self.height),
                            color=self.bgColor)
        d = ImageDraw.Draw(img)
        Text_Top = self.margintop
        # check text align
        # TextAlign = (Text_Left, Text_Top)
        lines = textwrap.wrap(self.text["quote"], width=ceil(self.width/20))
        y_text = Text_Top
        for line in lines:
            width, height = self.font.getsize(line)
            if self.textAlign == "center" or self.textAlign == "middle":
                d.text((ceil((self.width - width) / 2), y_text+5), line,
                       font=self.font, fill=self.textColor)
            elif self.textAlign == "right":
                d.text(((self.width - width) - 20, y_text+5), line,
                       font=self.font, fill=self.textColor)
            else:
                d.text((20, y_text+5), line,
                       font=self.font, fill=self.textColor)
            y_text += height+5
        width, height = self.font.getsize(self.text["author"])
        y_text += height
        d.text((ceil(self.width - width) / 2, y_text), self.text["author"],
               font=self.font, fill=self.textColor)

        logo_img = Image.open(self.logo)

        image_Width, image_Height = logo_img.size
        # check logo size
        if self.width <= image_Width or self.height <= image_Height:
            logo_img = logo_img.resize(self.logoSize, Image.NEAREST)
            image_Width, image_Height = logo_img.size
        elif self.logoResize:
            logo_img = logo_img.resize(self.logoSize, Image.BILINEAR)
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
        if self.islogotransparent:
            back_im.paste(logo_img, align, logo_img)
        else:
            back_im.paste(logo_img, align)

        if self.externalImage:
            ext_img = Image.open(self.extimage)
            ext_img = ext_img.resize([self.extimgwidth,
                                      self.extimgheight], Image.BILINEAR)
            image_Width, image_Height = ext_img.size
            width, height = self.font.getsize(self.text["author"])
            y_text += height
            y_extimg = y_text+15
            if self.extimgalign == "center" or self.extimgalign == "middle":
                align = (ceil((self.width-image_Width)/2), y_extimg)
            elif self.extimgalign == "right":
                align = ((self.width-image_Width-20), y_extimg)
            else:
                align = (20, y_extimg)
            back_im.paste(ext_img, align, ext_img)
            d = ImageDraw.Draw(back_im)
            width, height = self.font.getsize(self.text["underextimgtext"])
            d.text((ceil(self.width - width) / 2, y_extimg+image_Height+height+5), self.text["underextimgtext"],
                   font=self.font, fill=self.textColor)
        back_im.save(directory+str(name)+'.png', quality=100)

    def Default(self, instagram=False, instaStory=False):
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
        if configs["specialbg"] == 1:
            specialbg = True
        else:
            specialbg = False
        if configs["externalImage"] == 1:
            externalImage = True
            extimage = configs["extimageurl"]
        else:
            externalImage = False
            extimage = ''
        if configs["islogotransparent"] >= 1:
            islogotransparent = True
        else:
            islogotransparent = False
        backgroundimage = configs["backgroundimage"]
        logosize = (configs["logosizew"], configs["logosizeh"])
        font = configs["font"]
        extimgwidth = configs["extimgwidth"]
        extimgheight = configs["extimgheight"]
        margintop = configs["margintop"]
        extimagealign = configs["extimagealign"]
        opacity = configs["opacity"]
        counter = 1
        l = len(texts)
        printProgressBar(0, l, prefix='Progress:',
                         suffix='Complete', length=50)
        if instagram:
            width = 1080
            height = 1080
        if instaStory:
            width = 1080
            height = 1920
        for text in texts:
            photo = Maxim(
                [width,
                 height],
                [textcolor,
                 backgroundcolor], [
                    text, textalign],
                font, fontsize,
                logo,
                logoresize,
                logosize,
                specialbg,
                backgroundimage,
                margintop,
                externalImage,
                extimage,
                extimgwidth,
                extimgheight, extimagealign, opacity, islogotransparent)
            photo.Create(counter, './outputs/')
            counter += 1
            printProgressBar(counter-1, l, prefix='Progress:',
                             suffix='Complete', length=50)
        print(l, " Photos Created...\n")
        main()

    def DifferentBG(self):
        backgroundList = []
        for file in os.listdir("./img/background/"):
            if file.endswith(".jpg"):
                backgroundList.append(os.path.join("./img/background/", file))
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
        if configs["islogotransparent"] >= 1:
            islogotransparent = True
        else:
            islogotransparent = False
        logosize = (configs["logosizew"], configs["logosizeh"])
        font = configs["font"]
        margintop = configs["margintop"]
        opacity = configs["opacity"]
        indexer = 0
        indexerText = 0
        counter = 1
        if len(texts) > len(backgroundList):
            limit = len(texts)
        else:
            limit = len(backgroundList)
        printProgressBar(0, limit, prefix='Progress:',
                         suffix='Complete', length=50)
        for i in range(limit):
            if indexer == len(backgroundList):
                indexer = 0
            if indexerText == len(texts):
                indexerText = 0
            text = (texts[indexerText], textalign)
            photo = Maxim(
                [width,
                 height],
                [textcolor,
                 backgroundcolor],
                text,
                font,
                fontsize,
                logo,
                logoresize,
                logosize,
                True, backgroundList[indexer], margintop, opacity, islogotransparent)
            photo.Create(counter, './outputs/')
            counter += 1
            indexer += 1
            indexerText += 1
            printProgressBar(counter-1, limit, prefix='Progress:',
                             suffix='Complete', length=50)
        print(counter-1, " Photos created with " +
              str(len(backgroundList))+" different bg and "+str(len(texts))+"...\n")
        main()

    def DifferentLogo(self):
        logoList = []
        for file in os.listdir("./img/logo/"):
            if file.endswith(".jpg"):
                logoList.append(os.path.join("./img/logo/", file))
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
        if configs["logoresize"] >= 1:
            logoresize = True
        else:
            logoresize = False
        if configs["specialbg"] >= 1:
            specialbg = True
        else:
            specialbg = False
        if configs["islogotransparent"] >= 1:
            islogotransparent = True
        else:
            islogotransparent = False

        backgroundimage = configs["backgroundimage"]
        logosize = (configs["logosizew"], configs["logosizeh"])
        font = configs["font"]
        margintop = configs["margintop"]
        opacity = configs["opacity"]
        indexer = 0
        indexerText = 0
        counter = 1
        if len(texts) > len(logoList):
            limit = len(texts)
        else:
            limit = len(logoList)
        printProgressBar(0, limit, prefix='Progress:',
                         suffix='Complete', length=50)
        for i in range(limit):
            if indexer == len(logoList):
                indexer = 0
            if indexerText == len(texts):
                indexerText = 0
            logo = (logoList[indexer], configs["logovertical"],
                    configs["logohorizontal"])
            text = (texts[indexerText], textalign)
            photo = Maxim(
                [width,
                 height],
                [textcolor,
                 backgroundcolor],
                text,
                font,
                fontsize,
                logo,
                logoresize,
                logosize, specialbg, backgroundimage, margintop, opacity, islogotransparent)
            photo.Create(counter, './outputs/')
            counter += 1
            indexer += 1
            indexerText += 1
            printProgressBar(counter-1, limit, prefix='Progress:',
                             suffix='Complete', length=50)
        print(str(counter-1) + " Photos created with " +
              str(len(logoList))+" different logos and "+str(len(texts))+" different texts...\n")

        main()


if not os.path.exists("./outputs"):
    os.mkdir("./outputs")
if not os.path.exists("./img"):
    print("img directory is missing")
    exit()
if not os.path.exists("./fonts"):
    print("fonts directory is missing")
    exit()


def main():

    print(Style.RESET_ALL+'OPTIONS:\n')
    print(Fore.LIGHTCYAN_EX+'1.)'+Style.RESET_ALL +
          'Start with '+Fore.GREEN + 'default options')
    print(Fore.LIGHTCYAN_EX+'2.)'+Style.RESET_ALL +
          'Start with '+Fore.GREEN + 'different background images')
    print(Fore.LIGHTCYAN_EX+'3.)'+Style.RESET_ALL +
          'Start with '+Fore.GREEN + 'different logos')
    print(Fore.LIGHTCYAN_EX+'4.)'+Style.RESET_ALL +
          'Start with '+Fore.GREEN + 'Instagram Post')
    print(Fore.LIGHTCYAN_EX+'5.)'+Style.RESET_ALL +
          'Start with '+Fore.GREEN + 'Instagram Story')
    print(Fore.LIGHTCYAN_EX+'H.)'+Style.RESET_ALL +
          'I need '+Fore.GREEN + 'HELP')
    print(Fore.LIGHTCYAN_EX+'E.)'+Style.RESET_ALL + Fore.RED + 'EXIT')

    print(Fore.YELLOW+"Option:"+Fore.WHITE)
    x = input().lower()

    if x == '1':
        print(Style.RESET_ALL)
        photo = Maxim()
        photo.Default()
    elif x == '2':
        print(Style.RESET_ALL)
        photo = Maxim()
        photo.DifferentBG()
    elif x == '3':
        print(Style.RESET_ALL)
        photo = Maxim()
        photo.DifferentLogo()
    elif x == '4':
        print(Style.RESET_ALL)
        photo = Maxim()
        photo.Default(True)
    elif x == '5':
        print(Style.RESET_ALL)
        photo = Maxim()
        photo.Default(False, True)
    elif x == 'h' or x == 'help':
        print("\n\n" +
              Fore.WHITE + "If You choose "+Fore.GREEN+"1st "+Fore.WHITE +
              "option Maxim will start with default settings which configured in config.txt"
              "\n\nIf You choose "+Fore.GREEN+"2nd "+Fore.WHITE +
              "option Maxim will Create images with different backgrounds by the way maxim will use all the backgrounds you give it even if count of backgrounds greater than count of sentences which located in texts.txt file"
              "\n\nIf You choose "+Fore.GREEN+"3rd "+Fore.WHITE +
              "option Maxim will Create images with different logos and even if count of logos greater than count of sentences it will use all the logos"
              "\n\n Finally don't forget specialize configs because for 3 options maxim will use some infos from config."
              )
        main()
    elif x == 'e' or x == 'exit' or x == 'quit':
        exit()
    else:
        print(Fore.RED + 'Invalid option'+Style.RESET_ALL)
        main()


if __name__ == "__main__":
    print('WELCOME TO '+Fore.RED + 'MR. MAXIM')
    main()
