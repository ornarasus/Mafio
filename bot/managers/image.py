import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from bot.api.packet import Packet
from PIL.ImageFont import FreeTypeFont

from bot.misc.locale import Locale
from bot.misc.util import add_corners, size_text


class ImageManager:
    logo: Image
    font: FreeTypeFont
    rowVote: Image
    rowRole: Image

    def __init__(self, bot: str, server: str):
        self.font = ImageFont.truetype("resources/ubuntu.ttf", 30, encoding='UTF-8')
        self.init_logo(bot, server)
        self.init_rowVote()
        self.init_rowRole()

    def init_logo(self, bot: str, server: str):
        self.logo = Image.new(mode="RGBA", size=(125, 130))
        logoRequest = requests.get(bot)
        logo = Image.open(BytesIO(logoRequest.content))
        logo = logo.resize((120, 120))
        logo = add_corners(logo, 30)
        self.logo.paste(logo, (0, 0), logo)
        logoRequest = requests.get(server)
        logo = Image.open(BytesIO(logoRequest.content))
        logo = logo.resize((45, 45))
        logo = add_corners(logo, 15)
        self.logo.paste(logo, (80, 85), logo)

    def init_rowVote(self):
        self.rowVote = Image.new("RGBA", (736, 51), (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.rowVote)
        draw.rectangle((0, 0, 736, 51), outline=(255, 255, 255), width=3)
        draw.line([79, 3, 79, 48], (255, 255, 255,96), 3)

    def init_rowRole(self):
        self.rowRole = Image.new("RGBA", (736, 99), (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.rowRole)
        draw.rectangle((0, 0, 736, 99), outline=(255, 255, 255), width=3)
        draw.line([3, 49, 733, 49], (255, 255, 255, 96), 3)
        draw.line([365, 3, 365, 47], (255, 255, 255, 96), 3)

    def createImage(self, text: str, size: (int, int)) -> Image:
        img = Image.new(mode="RGBA", size=size, color=(54, 57, 63))
        img.paste(self.logo, (15, 10), self.logo)
        w, h = size_text(text)
        draw = ImageDraw.Draw(img)
        draw.text((150, (150 - h) / 2), text, (255, 255, 255), font=self.font)
        return img

    def vote(self, text: str, data: dict):
        height = 180 + len(data) * 45 + (len(data) + 1) * 3
        img = self.createImage(text, (765, height))
        draw = ImageDraw.Draw(img)
        for nick, emojiRaw in data.items():
            Y = list(data.keys()).index(nick)
            img.paste(self.rowVote, (15, 165 + Y * 48), self.rowVote)
            draw.text((115, 176 + Y * 48), nick, (255, 255, 255), font=self.font)
            emojiRequest = requests.get(emojiRaw)
            emoji = Image.open(BytesIO(emojiRequest.content))
            emoji = emoji.resize((35, 35))
            img.paste(emoji, (38, 173 + Y * 48), emoji)
        image_binary = BytesIO()
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        return image_binary

    def resultNight(self, data: list):
        height = 180 + len(data) * 45 + (len(data) + 1) * 3
        img = self.createImage(Locale.EndNight, (765, height))
        draw = ImageDraw.Draw(img)
        for i in range(len(data)):
            draw.rectangle((15, 165 + i * 48, 751, 165 + (i+1) * 51),
                           outline=(255, 255, 255), width=3)
            draw.text((25, 176 + i * 48), data[i], (255, 255, 255), font=self.font)
        image_binary = BytesIO()
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        return image_binary

    def info(self, text: str):
        image_binary = BytesIO()
        self.createImage(text, (765, 150)).save(image_binary, 'PNG')
        image_binary.seek(0)
        return image_binary

    def infoPacket(self, packet: Packet):
        height = 180 + len(packet.roles) * 90 + (len(packet.roles) * 2 + 1) * 3
        img = self.createImage(packet.info(), (765, height))
        draw = ImageDraw.Draw(img)
        for i in range(len(packet.roles)):
            img.paste(self.rowRole, (15, 165 + i * 96), self.rowRole)
            w, h = size_text(packet.roles[i].description)
            draw.text(((764 - w) / 2, 224 + i * 96), packet.roles[i].description,
                      (255, 255, 255), font=self.font)
            w, h = size_text(packet.roles[i].name)
            draw.text((18 + (361 - w) / 2, 176 + i * 96), packet.roles[i].name,
                      (255, 255, 255), font=self.font)
            text = Locale.PacketInfoTeam.format(packet.teams[packet.roles[i].teamID])
            w, h = size_text(text)
            draw.text((382 + (366 - w) / 2, 176 + i * 96), text, (255, 255, 255),
                      font=self.font)
        image_binary = BytesIO()
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        return image_binary
