import io,os
from google.cloud import vision




#Connect with the vision api. Certain key.json must be used
def googleClientConnection():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Key.json'

#Detect the Dominant colors of the uploaded Image
def dominantColors_Image():
    client = vision.ImageAnnotatorClient()
    image_path=f'Test.jpg'
    with io.open(image_path,'rb')as image_file:
        content=image_file.read()
    image=vision.Image(content=content)
    response=client.image_properties(image=image).image_properties_annotation
    dominant_colors=response.dominant_colors

    #print("dominant Colors:")
    #for color in dominant_colors.colors:
    #    print('pixel_fraction:{0}'.format(color.pixel_fraction))
    #    print('score:{0}'.format((color.score)))
    #    print('\tred:{0}'.format(color.color.red))
    #    print('\tgreen:{0}'.format(color.color.green))
    #    print('\tblue:{0}'.format(color.color.blue))
    #    print ('\t\t\t')
    return dominant_colors

#Detect the Dominant colors of the style theme industrial
def dominantColors_Industrial():
    client = vision.ImageAnnotatorClient()
    image_path = f'Industrial.jpg'
    with io.open(image_path, 'rb')as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.image_properties(image=image).image_properties_annotation
    dominant_colors = response.dominant_colors

    return dominant_colors

#Detect the Dominant colors of the style theme scandinavian
def dominantColors_Scandinavian():
    client = vision.ImageAnnotatorClient()
    image_path = f'Scandinavian.jpg'
    with io.open(image_path, 'rb')as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.image_properties(image=image).image_properties_annotation
    dominant_colors = response.dominant_colors

    return dominant_colors

#Detect the Dominant colors of the style theme bohemian
def dominantColors_Bohemian():
    client = vision.ImageAnnotatorClient()
    image_path = f'Bohemian.jpg'
    with io.open(image_path, 'rb')as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.image_properties(image=image).image_properties_annotation
    dominant_colors = response.dominant_colors

    return dominant_colors

#calculate the difference between the dominant color of the upload image and industrial.
#returns the gap between them. The lower it is, the more similar are they.
def compare_Industrial(dominant_colors_image,dominant_colors_industrial):
    for image in dominant_colors_image.colors:
        for industrial in dominant_colors_industrial.colors:
            red=image.color.red-industrial.color.red
            if(red<0):
                red=red*-1
            green=image.color.green-industrial.color.green
            if(green<0):
                green=green*-1
            blue=image.color.blue-industrial.color.blue
            if(blue<0):
                blue=blue*-1
            return red+green+blue

#calculate the difference between the dominant color of the upload image and scandinavian.
#returns the gap between them. The lower it is, the more similar are they.
def compare_Scandinavian(dominant_colors_image,dominant_colors_industrial):
    for image in dominant_colors_image.colors:
        for industrial in dominant_colors_industrial.colors:
            red = image.color.red - industrial.color.red
            if (red < 0):
                red = red * -1
            green = image.color.green - industrial.color.green
            if (green < 0):
                green = green * -1
            blue = image.color.blue - industrial.color.blue
            if (blue < 0):
                blue = blue * -1
            return red + green + blue

#calculate the difference between the dominant color of the upload image and bohemian.
#returns the gap between them. The lower it is, the more similar are they.
def compare_Bohemian(dominant_colors_image,dominant_colors_industrial):
    for image in dominant_colors_image.colors:
        for industrial in dominant_colors_industrial.colors:
            red = image.color.red - industrial.color.red
            if (red < 0):
                red = red * -1
            green = image.color.green - industrial.color.green
            if (green < 0):
                green = green * -1
            blue = image.color.blue - industrial.color.blue
            if (blue < 0):
                blue = blue * -1
            return red + green + blue

#Detects the objects in the uploaded image.
def objectDetection():
    client = vision.ImageAnnotatorClient()
    image_path = f'Test.jpg'
    with io.open(image_path,'rb')as image_file:
        content=image_file.read()
    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    localized_object_annotation=response.localized_object_annotations
    furnitures=[]
    n = 0
    for objects in localized_object_annotation:
        furnitures.append(objects.name)
        if (n > 0):
            if (furnitures[n - 1] == objects.name):
                furnitures.pop()
            else:
                n=n+1
        else:
            n = n + 1

    return furnitures

#Detect the final style of the picture, based on the gap of the themes (calculated by the compare functions).
#the lowest gap is the final style.
def detectStyle(dominant_colors_image):
    dominant_colors_industrial=dominantColors_Industrial()
    dominant_colors_scandinavian=dominantColors_Scandinavian()
    dominant_colors_bohemian=dominantColors_Bohemian()


    industrial_value=compare_Industrial(dominant_colors_image,dominant_colors_industrial)
    scandinavian_value=compare_Scandinavian(dominant_colors_image,dominant_colors_scandinavian)
    bohemian_value=compare_Bohemian(dominant_colors_image,dominant_colors_bohemian)

    if(industrial_value<scandinavian_value):
        if(industrial_value<bohemian_value):
            return "Industrial"
        else:
            return "Bohemian"
    elif(scandinavian_value<bohemian_value):
        return "Scandinavian"
    else:
        return "Bohemian"


#Detects the necessaryFurnitures, which we offer and not found in the list of the furnitures in the picture.
def detectNecessaryFurnitures(furnitures,necset):
    n=0
    necFunitures=[]
    for nec in necset:
        for furniture in furnitures:
            if(nec==furniture):
               n=n+1
        if(n>0):
            n=0
        else:
            necFunitures.append(nec)

    return necFunitures


if __name__ == "__main__":
    googleClientConnection()
    dominant_colors_image=dominantColors_Image()
    furnitures = []
    furnitures=objectDetection()
    style=detectStyle(dominant_colors_image)
    print(style)
    necFunitures=[]
    necset=['Bed','Chair','Couch','Lighting']
    necFunitures=detectNecessaryFurnitures(furnitures,necset)

    print (necFunitures)

