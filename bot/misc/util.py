import importlib
import random
import sys

import discord
from PIL import Image, ImageDraw

from bot.api.server import Server


def import_module(module_name, module_dir=None):
    if module_dir:
        sys.path.insert(0, module_dir)
    try:
        module = importlib.import_module(module_name)
    finally:
        if module_dir:
            sys.path.pop(0)
        return module


async def random_packet(packets: list, server: Server, debug: bool, image):
    server.version = packets[1 if debug else random.randint(2, len(packets)-1)]
    server.packet = server.version.info()
    server.isNight = True
    with image.infoPacket(server.packet) as infoPacket:
        await server.text.send(file=discord.File(infoPacket, "infoPacket.png"))
    await server.voice.edit(user_limit=server.packet.countPlayers)


def get_nick(member: discord.Member) -> str:
    return f"{member.nick if member.nick is not None else member.name}"


def random_emojis(count: int, allEmojis: tuple) -> list:
    allEmojis = list(allEmojis)
    emojis = list()
    for i in range(count):
        emoji = random.choice(allEmojis)
        emojis.append(emoji)
        allEmojis.remove(emoji)
    return emojis


def random_roles(allRoles: tuple) -> list:
    roles = list()
    for role in allRoles:
        for i in range(role.countPlayers):
            roles.append(role)
    random.shuffle(roles)
    return roles


def size_text(text: str) -> (int, int):
    w = max([len(line) for line in text.split('\n')])
    w *= 15
    countLines = len(text.split("\n"))
    h = countLines * 25 + (countLines-1) * 4
    return w, h


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


async def edit_attachments(message: discord.Message, files: discord.File):
    await message.remove_attachments(*message.attachments)
    await message.add_files(files)
