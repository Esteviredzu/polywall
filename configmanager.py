import os
import shutil
import configparser
import logging
import numpy as np

logger = logging.getLogger(__name__)

class ConfigManager:
    BACKUP_FOLDER = "backup"

    @staticmethod
    def lighten_color(color, amount):
        """Lighten the given color by the specified amount."""
        color_array = np.array([int(color[i:i+2], 16) for i in (1, 3, 5)])
        lightened_color = np.minimum(color_array + amount, 255)
        lightened_color_str = '#' + ''.join(f'{c:02X}' for c in lightened_color)
        return lightened_color_str

    @staticmethod
    def darken_color(color, amount):
        """Darken the given color by the specified amount."""
        color_array = np.array([int(color[i:i+2], 16) for i in (1, 3, 5)])
        darkened_color = np.maximum(color_array - amount, 0)
        darkened_color_str = '#' + ''.join(f'{c:02X}' for c in darkened_color)
        return darkened_color_str

    @staticmethod
    def update_polybar_config(colors):
        """Update colors in the Polybar configuration file."""
        config_file_path = os.path.expanduser('~/.config/polybar/config.ini')
        if not os.path.exists(config_file_path):
            raise FileNotFoundError("Polybar configuration file not found.")
        
        config = configparser.ConfigParser()
        config.read(config_file_path)

        if 'colors' not in config:
            raise KeyError("'colors' section not found in the configuration.")

        if len(colors) < 3:
            raise ValueError("Insufficient colors in the array.")

        config['colors']['background'] = colors[0]
        config['colors']['background-alt'] = ConfigManager.lighten_color(colors[0], 20)
        config['colors']['primary'] = colors[2]

        with open(config_file_path, 'w') as configfile:
            config.write(configfile)

        logger.info("Colors in the Polybar configuration file have been successfully updated.")

    @staticmethod
    def update_i3_config(color):
        """Update color in the i3 configuration file."""
        config_file_path = os.path.expanduser('~/.config/i3/config')
        if not os.path.exists(config_file_path):
            raise FileNotFoundError("i3 configuration file not found.")

        with open(config_file_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith('client.focused'):
                parts = line.split()
                if len(parts) >= 4:
                    parts[2] = color
                    parts[4] = color
                    lines[i] = ' '.join(parts) + '\n'
                    break
        else:
            raise ValueError("Line for updating not found in the i3 configuration file.")

        with open(config_file_path, 'w') as f:
            f.writelines(lines)
        
        os.system("i3-msg restart")

        logger.info("Color in the i3 configuration file has been successfully updated.")

    @staticmethod
    def update_alacritty_config(color):
        """Update color in the Alacritty configuration file."""
        config_file_path = os.path.expanduser('~/.config/alacritty/alacritty.toml')
        if not os.path.exists(config_file_path):
            raise FileNotFoundError("Alacritty configuration file not found.")

        with open(config_file_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith('background'):
                lines[i] = f'background = "{color}"\n'
                break
        else:
            raise ValueError("Failed to find the 'background' line in the Alacritty configuration file.")

        with open(config_file_path, 'w') as f:
            f.writelines(lines)

        logger.info("Color in the Alacritty configuration file has been successfully updated.")

    @staticmethod
    def backup_colors():
        """Backup current configuration files."""
        os.makedirs(ConfigManager.BACKUP_FOLDER, exist_ok=True)
        config_files = [
            ('~/.config/polybar/config.ini', 'polybar_config.ini'),
            ('~/.config/i3/config', 'i3_config'),
            ('~/.config/alacritty/alacritty.toml', 'alacritty_config.toml')
        ]

        for src, dst in config_files:
            src_path = os.path.expanduser(src)
            dst_path = os.path.join(ConfigManager.BACKUP_FOLDER, dst)
            shutil.copy(src_path, dst_path)

        logger.info("Color backup created successfully.")

    @staticmethod
    def restore_colors():
        """Restore configuration files from backup."""
        for src, dst in config_files:
            src_path = os.path.join(ConfigManager.BACKUP_FOLDER, src)
            dst_path = os.path.expanduser(dst)
            shutil.copy(src_path, dst_path)

        logger.info("Colors successfully restored from backup.")
