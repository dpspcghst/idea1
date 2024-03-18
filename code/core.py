# ensōurobo (enz-OH-rah-BOH)

from math import cos, radians, sin
from os import walk
from os.path import join
from random import choice, randint, uniform
from sys import exit

import pytmx
from pytmx.util_pygame import load_pygame as load_engine

import pygame
from pygame import FRect, Surface, quit
from pygame.display import get_surface, set_caption, set_mode, update
from pygame.draw import line, rect
from pygame.event import get
from pygame.font import Font
from pygame.image import load
from pygame.key import get_pressed
from pygame.mask import from_surface
from pygame.math import Vector2
from pygame.sprite import Group, Sprite, spritecollide
from pygame.time import Clock, get_ticks
from pygame.transform import flip

ANIMATION_SPEED = 6
RUNNING = True
TILE_SIZE = 64
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

# colors
black = (0, 0, 0)
light_tense_yellow = (220, 200, 70)
tense_yellow = (110, 100, 35)

#  layers
Z_LAYERS = {
    "bg": 0,
    "bg_details": 4,
    "bg_tiles": 2,
    "clouds": 1,
    "fg": 7,
    "main": 5,
    "path": 3,
    "water": 6
}


def import_folder(*path):

    frames = []

    for folder_path, sub_folders, image_names in walk(join(*path)):

        for image_name in sorted(image_names, key=lambda name: int(name.split(".")[0])):

            full_path = join(folder_path, image_name)
            frames.append(load(full_path).convert_alpha())

    return frames


def import_folder_dictionary(*path):

    frame_dictionary = {}

    for folder_path, _, image_names in walk(join(*path)):

        for image_name in image_names:

            full_path = join(folder_path, image_name)
            surface = load(full_path).convert_alpha()
            frame_dictionary[image_name.split(".")[0]] = surface

    return frame_dictionary


def import_image(*path, alpha=True, structure="png"):

    full_path = join(*path) + f".{structure}"

    return load(full_path).convert_alpha() if alpha else load(full_path).convert()


def import_sub_folders(*path):

    frame_dictionary = {}

    for _, sub_folders, __ in walk(join(*path)):

        if sub_folders:

            for sub_folder in sub_folders:

                frame_dictionary[sub_folder] = import_folder(*path, sub_folder)

    return frame_dictionary
