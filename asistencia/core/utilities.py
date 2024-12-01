from PIL import Image, ExifTags
from crum import get_current_request


# Funciona para validar si el usuario puede eliminar un registro
def validate_delete(perms):
    request = get_current_request()
    p = perms.split('_')
    if request.user.is_superuser:
        return True
    # Verificamos si el permiso esta dividio por mas de 2 '_'
    if len(p) >= 3:
        perm = f'delete_{p[1]}_{p[2]}'

    if len(p) == 2:
        perm = f'delete_{p[1]}'

    if 'group' in request.session:
        group = request.session['group']
        if group.permissions.filter(codename=perm).exists():
            return True
    return False


"""
Funcionar para redimencionar las imagenes
la redimencionamos segun el tamaño desedo y le baamos el paso
par que al momento de cargar la imagen no haya delay
"""

def resize_img(path):
    size = 800
    img = Image.open(path)

    # # Corrige la orientación de la imagen
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    # Obtiene los metadatos EXIF
    exif = img._getexif()

    if exif is not None:
        orientation_value = exif.get(orientation)
        if orientation_value == 3:
            img = img.rotate(180, expand=True)
        elif orientation_value == 6:
            img = img.rotate(270, expand=True)
        elif orientation_value == 8:
            img = img.rotate(90, expand=True)

    # Check if the height exceeds 800 pixels
    if img.height > 800:
        # Calculate the new width to maintain aspect ratio
        new_width = int(img.width * size / img.height)
        img = img.resize((size, new_width))

    # Save the resized image with optimized settings
    img.save(path, quality=85, optimize=True)
