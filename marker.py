'''Code basis. The end result will look very much different.'''

import PIL
import os.path

def frame_one(picture, wide, rgb):

    # Opens image and assigns it as the back ground. Also graphs image size.
    background = PIL.Image.open(picture)
    background.convert(mode='RGBA')
    width, height = background.size
    # Creates a new mask that will cover the borders of the image.
    frame0 = PIL.Image.new('RGBA',(width,height),color=None)
    frame1 = PIL.ImageDraw.Draw(frame0)
    frame1.rectangle([(0,0),(width,wide)],fill=rgb)#top box
    frame1.rectangle([(0,0),(wide,height)],fill=rgb)#left box
    frame1.rectangle([(width,height),(0,height-wide)],fill=rgb)#bottom box
    frame1.rectangle([(width,height),(width-wide,0)],fill=rgb)#right box
    frame1.rectangle([(wide,wide),(width-wide,height-wide)],fill=rgb)#clear area
    #framed = PIL.Image.alpha_composite(background, frame0)
    #return framed
    ##background.paste(frame0)
    ##return background
    dwide = 2*wide
    newground = background.resize((width-dwide,height-dwide))
    frame0.paste(newground, box=(wide,wide))
    return frame0


def frame_all_images(wide, rgb):

    directory = os.getcwd() # Use working directory if unspecified

    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'framed')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed

    # Load all the images
    image_list, file_list = get_images(directory)

    # Go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        print n
        filename, filetype = os.path.splitext(file_list[n])

        # Round the corners with default percent of radius
        curr_image = file_list[n]
        new_image = frame_one(curr_image, wide, rgb)

        # Save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)
       
