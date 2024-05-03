import argparse
import logging
from colorextractor import ColorExtractor
from configmanager import ConfigManager
import os

DEFAULT_IMAGE_PATH = 'default.jpg'
DEFAULT_NUM_COLORS = 3

logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Extract main colors from an image.')
    parser.add_argument('--image_path', type=str, default=DEFAULT_IMAGE_PATH, help='Path to the input image')
    parser.add_argument('--num_colors', type=int, default=DEFAULT_NUM_COLORS, help='Number of main colors to extract')
    parser.add_argument('--action', type=str, default="", help='Backup/restore')
    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

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

        if input("Do you want to set wallpaper? (y/n)") == 'y':
            os.system(f"feh --bg-scale {args.image_path}")

    logger.info("Goodbye")
