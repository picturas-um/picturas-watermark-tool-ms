import random

from PIL import Image, ImageEnhance

from .core.tool import Tool
from .watermark_request_message import WatermarkParameters


class WatermarkTool(Tool):

    def __init__(
        self,
        watermark_image_path: str,
        opacity: float = 0.7,
    ) -> None:
        """
        Initialize the WatermarkTool with the path to the watermark image.

        Args:
            watermark_image_path (str): Path to the watermark image.
            opacity (float): Transparency level of the watermark (0.0 to 1.0).
        """
        self.watermark_image = Image.open(watermark_image_path).convert("RGBA")
        self.opacity = opacity

    def _apply_opacity(self, image: Image.Image) -> Image.Image:
        alpha = image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(self.opacity)
        image.putalpha(alpha)
        return image

    def apply(self, parameters: WatermarkParameters):
        """
        Apply the watermark with an overlay effect to the input image and save the result.

        Args:
            parameters (WatermarkParameters): watermark parameters.
        """
        # Open the input image
        input_image = Image.open(parameters.inputImageURI).convert("RGBA")

        # Resize and adjust the watermark's opacity
        watermark = self.watermark_image.copy()

        # Scale watermark to fit the smallest dimension of the input image
        # Set watermark size to 30% of the smallest dimension
        smallest_dimension = min(input_image.size)
        scale_factor = smallest_dimension * 0.3
        new_watermark_size = (
            int(watermark.size[0] * scale_factor / smallest_dimension),
            int(watermark.size[1] * scale_factor / smallest_dimension),
        )
        watermark = watermark.resize(new_watermark_size)
        watermark = self._apply_opacity(watermark)

        # Generate random position for the watermark
        random_x = random.randint(0, max(0, input_image.size[0] - new_watermark_size[0]))
        random_y = random.randint(0, max(0, input_image.size[1] - new_watermark_size[1]))
        watermark_position = (random_x, random_y)

        # Create a transparent overlay
        overlay = Image.new("RGBA", input_image.size, (0, 0, 0, 0))
        overlay.paste(watermark, watermark_position, mask=watermark)

        # Blend the input image and the overlay
        blended_image = Image.alpha_composite(input_image, overlay)

        # Save the final image
        # Convert back to RGB for saving
        final_image = blended_image.convert("RGB")
        final_image.save(parameters.outputImageURI)
