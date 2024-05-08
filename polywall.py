import argparse
import logging
from colorextractor import ColorExtractor
from configmanager import ConfigManager
import os
import random
import glob


DEFAULT_IMAGE_PATH = 'images/default.jpg'
DEFAULT_NUM_COLORS = 3

logger = logging.getLogger(__name__)

def get_random_image(src_file):
    with open(src_file, 'r') as file:
        paths = file.readlines()
        
    paths = [path.strip() for path in paths]

    # Собираем все изображения из указанных директорий
    images = []
    for path in paths:
        images.extend(glob.glob(os.path.join(path, '*.jpg')))  

    if images:
        return random.choice(images)
    else:
        return "No images found in the specified directories"


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Extract main colors from an image.')
    parser.add_argument('--image_path', type=str, default=DEFAULT_IMAGE_PATH, help='Path to the input image')
    parser.add_argument('--num_colors', type=int, default=DEFAULT_NUM_COLORS, help='Number of main colors to extract')
    parser.add_argument('--action', type=str, default="", help='Backup/restore')

    #Insert your wallpaper directories into "src" file
    parser.add_argument('--random', action='store_true', help='Use a random image from the specified directories')
    return parser.parse_args()

import os

def set_wallpaper(image_path):
    os.system(f"nitrogen --set-zoom-fill {image_path} > /dev/null 2>&1")

    text = f'''[xin_-1]
file={image_path}
mode=0
bgcolor=#000000'''
    try:
        file_path = os.path.expanduser("~/.config/nitrogen/bg-saved.cfg")
        with open(file_path, 'w') as file:
            file.write(text)
        print("Текст успешно записан в файл", file_path)
    except Exception as e:
        print("Произошла ошибка при записи в файл:", e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    if args.random:
        args.image_path = get_random_image("src") 

    if args.action == "backup":
        ConfigManager.backup_colors()
    elif args.action == "restore":
        ConfigManager.restore_colors()
    else:
        color_extractor = ColorExtractor(args.num_colors)
        main_colors = color_extractor.extract_main_colors(args.image_path)

        hex_main_colors = [ColorExtractor.rgb_to_hex(color) for color in main_colors]

        for color in main_colors:
            ColorExtractor.print_color_square(color)
            print(f" {ColorExtractor.rgb_to_hex(color)}")

        ConfigManager.update_polybar_config(hex_main_colors)
        ConfigManager.update_i3_config(hex_main_colors[2])
        ConfigManager.update_alacritty_config(hex_main_colors[0])

        # if input("Do you want to set wallpaper? (y/n)") == 'y':
        #     os.system(f"feh --bg-scale {args.image_path}")
    set_wallpaper(args.image_path)
    logger.info("Goodbye")
