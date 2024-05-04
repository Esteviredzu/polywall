# polywall
# Color Extractor

This script is designed to extract main colors from an image and use them as a color scheme for configuration files of certain Linux applications.

## Usage

### Requirements

- Python 3.x
- Python libraries: `argparse`, `logging`, `PIL`, `sklearn`, `numpy`, `configparser`

### Installation of Dependencies

Run the following command to install all necessary dependencies:

```bash
pip install argparse Pillow scikit-learn numpy
```

### Commands

```python
--image_path: Path to the input image (default: 'default.jpg')
--num_colors: Number of main colors to extract (default: 3)
--action: Action (backup/restore configuration)
--random: Use a random image from the specified directories
```

### Usage Examples

1. **Extracting main colors and updating configurations:**

```bash
python color_extractor.py --image_path example.jpg
```

2. **Backup and restore configurations:**

```bash
python color_extractor.py --action backup
python color_extractor.py --action restore
```

3. **Setting desktop wallpaper:**

```bash
python color_extractor.py --image_path wallpaper.jpg
```

4. **Using a random image for color extraction:**

```bash
python color_extractor.py --random
```

### Note

- When using backup or restore action, the script saves/restores current configuration files from the 'backup' folder.
- Now, with the `--random` flag, you can use random images for color extraction.
