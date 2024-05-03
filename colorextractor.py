from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

class ColorExtractor:
    """Extract main colors from an image."""

    def __init__(self, num_colors=5):
        self.num_colors = num_colors

    def extract_main_colors(self, image_path):
        """Extract main colors from the image."""
        image = Image.open(image_path)
        image_array = np.array(image)
        h, w, _ = image_array.shape
        image_array = image_array.reshape((h * w, 3))

        kmeans = KMeans(n_clusters=self.num_colors)
        kmeans.fit(image_array)

        main_colors = kmeans.cluster_centers_.astype(int)
        main_colors = sorted(main_colors, key=lambda x: np.mean(x))

        return main_colors

    @staticmethod
    def rgb_to_hex(rgb):
        """Convert RGB color to hexadecimal."""
        return '#' + ''.join(f'{c:02x}' for c in rgb)

    @staticmethod
    def print_color_square(color):
        """Print color square."""
        r, g, b = color
        color_str = f'\033[48;2;{r};{g};{b}m  \033[0m'
        print(color_str, end='')
