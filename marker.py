import PIL
import PIL.ImageDraw
import os.path

def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def make_support(picture, wide, rgb):
    '''Imposes the support image on the input picture 'picture', with a frame made with width 'wide' and color (stored as a 4 element tuple)
    'rgb'.
    '''
    if 'support' in picture:
        return None
    else:
        pass
    background = PIL.Image.open(picture)# Opens image and assigns it as the background.
    width, height = background.size
    mask = PIL.Image.open('support.png')
    width0, height0 = mask.size
    mersk = PIL.ImageDraw.Draw(mask,mode='RGBA')
    # Building a square frame (out of 4 polygons) on the frame1 and by extension the frame0 canvises 
    frame0 = PIL.Image.new('RGBA',(width,height),color=None)# Creates the frame0 canvis with the same dimensions as the original picture
    frame1 = PIL.ImageDraw.Draw(frame0)# 
    frame1.rectangle([(0,0),(width,wide)],fill=rgb)# Draws top box
    frame1.rectangle([(0,0),(wide,height)],fill=rgb)# Draws left box
    frame1.rectangle([(width,height),(0,height-wide)],fill=rgb)# Draws bottom box
    frame1.rectangle([(width,height),(width-wide,0)],fill=rgb)# Draws right box
    frame1.rectangle([(wide,wide),(width-wide,height-wide)],fill=rgb)# Draws clear area
    dwide = 2*wide # Creates the dwide variable set to 2* the width of the frame
    qwid, hhght = (width/4,height/2)
    ewid0, hhght0 = (width0/8,height0/2)
    newground = background.resize((width-dwide,height-dwide)) # Resizes the picture to fit within the frame
    frame0.paste(newground,box=(wide,wide))
    frame0.paste(mask,box=(qwid+ewid0,hhght))
    frame0.show()
    return frame0 # Returns the frame0 object

def make_images_support(wide, rgb):
    ''' Makes all images in the current directory support images (frames them and imposes the support image on the background)
    '''
    directory = os.getcwd() # Uses working directory
    new_directory = os.path.join(directory, 'support_images')# Create a new directory 'support_images'
    try: # Attempts
        os.mkdir(new_directory)# to make a new directory
    except OSError:# unless it throws an oserror
        pass # if the directory already exists, proceed
    # Load all the images
    image_list, file_list = get_images(directory)
    # Go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        print n
        filename, filetype = os.path.splitext(file_list[n])
        # Frames the image with the requested frame size
        curr_image = file_list[n]
        new_image = make_support(curr_image, wide, rgb)
        # Saves the altered image as PNG
        new_image_filename = os.path.join(new_directory, filename + '.png')
        try:
            new_image.save(new_image_filename)
        except AttributeError:
            pass

