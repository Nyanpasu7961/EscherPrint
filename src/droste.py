from PIL import Image
import cairosvg
import io

def search_magenta(image, magenta):
    width, height = image.size

    left = None
    right = None
    top = None
    bottom = None

    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y)) == magenta:
                if left is None or x < left:
                    left = x
                if right is None or x > right:
                    right = x
                if top is None or y < top:
                    top = y
                if bottom is None or y > bottom:
                    bottom = y

    if left is None:
        return None, None, None, None

    return left, right, top, bottom

def transformed_image(image, left, right, top, bottom):
    width, height = image.size

    modified_width = right - left + 1
    modified_height = bottom - top + 1
    image_aspect = width / height
    modified_aspect = modified_width / modified_height

    # Match aspect ratios.
    if image_aspect < modified_aspect:
        width_ratio = modified_width / width
        modified_image = image.resize(
            (modified_width, int(height*width_ratio) + 1), 
            Image.Resampling.NEAREST
        )
    
    else:
        height_ratio = modified_height / height
        modified_image = image.resize(
            (int(height*height_ratio) + 1, modified_height), 
            Image.Resampling.NEAREST
        )

    return modified_image

def replace_magenta(image, modified_image, left, right, top, bottom, magenta):
    # Mod image origin at (left, top)
    for x in range(left, right + 1):
        for y in range(top, bottom + 1):
            if image.getpixel((x, y)) == magenta:
                color = modified_image.getpixel((x - left, y - top))
                image.putpixel((x, y), color)
    
    return image

def droste(image, depth = 10):
        
    if depth == 0:
        return image
    
    if image.mode == "RGBA":
        magenta = (255, 0, 255, 255)
    elif image.mode == "RGB":
        magenta = (255, 0, 255)

    # Establish a bounding box of the magenta painted area.
    left, right, top, bottom = search_magenta(image, magenta)

    if left is None: 
        return image
    
    modified_image = transformed_image(image, left, right, top, bottom)
    

    #print(left, right, top, bottom)
    #print(image.getpixel((left, top)))
    # Replace magenta pixels

    image = replace_magenta(image, modified_image, left, right, top, bottom, magenta)
    
    return droste(image, depth - 1)
