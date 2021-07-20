import pygame
import os

from typing import List

def load_animations(animation_directory: str, scale: int = 1) -> List[pygame.Surface]:
    files = os.listdir(animation_directory)
    frames = []
    for file in files:
        raw_file_path = f"{animation_directory}/{file}"
        frame = pygame.image.load(raw_file_path).convert_alpha()
        scaled = (frame.get_width() * scale, frame.get_height() * scale)
        frame = pygame.transform.scale(frame, scaled)
        frames.append(frame)

    return frames

