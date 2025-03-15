from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import colorsys
import numpy as np

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def adjust_saturation(image, factor):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def adjust_hue(image, hue_factor):
    image = image.convert('RGBA')
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            r, g, b, a = pixels[x, y]
            h, s, l = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            h = (h + hue_factor) % 1.0  # Wrap around
            r, g, b = colorsys.hls_to_rgb(h, s, l)
            pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255), a)
    return image

def rotate_image(image, angle):
    return image.rotate(angle, expand=True)

def resize_image(image, width, height):
    return image.resize((width, height))

def sharpen_image(image):
    return image.filter(ImageFilter.SHARPEN)

def blur_image(image):
    return image.filter(ImageFilter.BLUR)

def invert_colors(image):
    return ImageOps.invert(image)

def grayscale_image(image):
    return ImageOps.grayscale(image)

def adjust_color_balance(image, red_factor=1.0, green_factor=1.0, blue_factor=1.0):
    image = image.convert('RGB')
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixels[x, y]
            r = int(r * red_factor)
            g = int(g * green_factor)
            b = int(b * blue_factor)
            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))
            pixels[x, y] = (r, g, b)
    return image

def adjust_exposure(image, factor):
    return adjust_brightness(image, factor)

def add_vignette(image, strength=0.5):
    image = image.convert('RGBA')
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            dist_x = abs(x - width / 2)
            dist_y = abs(y - height / 2)
            distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
            max_distance = (width ** 2 + height ** 2) ** 0.5 / 2
            vignette_factor = 1 - (distance / max_distance) * strength
            r, g, b, a = pixels[x, y]
            pixels[x, y] = (int(r * vignette_factor), int(g * vignette_factor), int(b * vignette_factor), a)
    return image

def add_noise(image, factor=10):
    import random
    image = image.convert('RGB')
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixels[x, y]
            noise_r = random.randint(-factor, factor)
            noise_g = random.randint(-factor, factor)
            noise_b = random.randint(-factor, factor)
            r = max(0, min(r + noise_r, 255))
            g = max(0, min(g + noise_g, 255))
            b = max(0, min(b + noise_b, 255))
            pixels[x, y] = (r, g, b)
    return image

def adjust_levels(image, black_point=0, white_point=255, midtones=1.0):
    image = image.convert('RGB')
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixels[x, y]
            r = int((r - black_point) * (255 / (white_point - black_point)) ** midtones)
            g = int((g - black_point) * (255 / (white_point - black_point)) ** midtones)
            b = int((b - black_point) * (255 / (white_point - black_point)) ** midtones)
            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))
            pixels[x, y] = (r, g, b)
    return image

def adjust_curves(image, red_curve=None, green_curve=None, blue_curve=None):
    image = image.convert('RGB')
    pixels = image.load()
    if red_curve is None:
        red_curve = list(range(256))
    if green_curve is None:
        green_curve = list(range(256))
    if blue_curve is None:
        blue_curve = list(range(256))
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixels[x, y]
            r = red_curve[r]
            g = green_curve[g]
            b = blue_curve[b]
            pixels[x, y] = (r, g, b)
    return image

def add_color_tint(image, red_tint=0, green_tint=0, blue_tint=0):
    image = image.convert('RGB')
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixels[x, y]
            r = max(0, min(r + red_tint, 255))
            g = max(0, min(g + green_tint, 255))
            b = max(0, min(b + blue_tint, 255))
            pixels[x, y] = (r, g, b)
    return image

def adjust_channel_mixer(image, red_r=1.0, red_g=0.0, red_b=0.0,
                             green_r=0.0, green_g=1.0, green_b=0.0,
                             blue_r=0.0, blue_g=0.0, blue_b=1.0):
    image = image.convert('RGB')
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixels[x, y]
            new_r = int(r * red_r + g * red_g + b * red_b)
            new_g = int(r * green_r + g * green_g + b * green_b)
            new_b = int(r * blue_r + g * blue_g + b * blue_b)
            new_r = max(0, min(new_r, 255))
            new_g = max(0, min(new_g, 255))
            new_b = max(0, min(new_b, 255))
            pixels[x, y] = (new_r, new_g, new_b)
    return image

def adjust_color_factors(image_pil, red_factor, green_factor, blue_factor):
    """Adjusts the red, green, and blue color channels of a PIL image.

    Args:
        image_pil: The input PIL image.
        red_factor: The factor to multiply the red channel by.
        green_factor: The factor to multiply the green channel by.
        blue_factor: The factor to multiply the blue channel by.

    Returns:
        The adjusted PIL image.
    """
    image_np = np.array(image_pil)
    image_np = image_np.astype(np.float32)

    image_np[:, :, 0] *= red_factor  # Red channel
    image_np[:, :, 1] *= green_factor  # Green channel
    image_np[:, :, 2] *= blue_factor  # Blue channel

    image_np = np.clip(image_np, 0, 255)
    image_np = image_np.astype(np.uint8)

    return Image.fromarray(image_np)


def motion_blur(image, size=10, angle=0):
    kernel = np.zeros((size, size))
    kernel[int((size - 1) / 2), :] = np.ones(size)
    kernel /= size
    return image.filter(ImageFilter.Kernel((size, size), kernel.flatten()))

def dehaze(image, contrast_factor=1.5):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(contrast_factor)

def add_film_grain(image, intensity=10):
    image = image.convert('RGB')
    pixels = np.array(image, dtype=np.int16)
    noise = np.random.normal(0, intensity, pixels.shape)
    pixels = np.clip(pixels + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(pixels)

def hdr_effect(image, detail_factor=2.0):
    return image.filter(ImageFilter.DETAIL).filter(ImageEnhance.Contrast(image).enhance(detail_factor))

def apply_warm_filter(image, intensity=20):
    image = image.convert('RGB')
    pixels = np.array(image, dtype=np.int16)
    pixels[..., 0] = np.clip(pixels[..., 0] + intensity, 0, 255)  # Increase red
    pixels[..., 2] = np.clip(pixels[..., 2] - intensity, 0, 255)  # Decrease blue
    return Image.fromarray(pixels.astype(np.uint8))

def apply_cool_filter(image, intensity=20):
    image = image.convert('RGB')
    pixels = np.array(image, dtype=np.int16)
    pixels[..., 0] = np.clip(pixels[..., 0] - intensity, 0, 255)  # Decrease red
    pixels[..., 2] = np.clip(pixels[..., 2] + intensity, 0, 255)  # Increase blue
    return Image.fromarray(pixels.astype(np.uint8))