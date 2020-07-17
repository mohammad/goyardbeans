import requests 
from PIL import Image

def crop_photo(image_url): 
    r = requests.get(image_url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        goya = Image.open('goya.jpeg')
        overlay = Image.open(r.raw)
        resizedOverlay = overlay.resize((220, 338))


        goya.paste(resizedOverlay, (359, 457))

        return goya.save("goyard.jpeg")
       
    else:
        print('Image Couldn\'t be retreived')
    
