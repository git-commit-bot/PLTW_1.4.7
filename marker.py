import PIL
import PIL.ImageDraw
import os.path

def get_images():
    """ Returns PIL.Image objects for all the images in directory.
    
    Uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    directory = os.getcwd() # Uses working directory for indexing     
    image_list = [] # Initializes a new aggregatory list for holding the names of image files in the current directory
    file_list = [] # Initializes a new aggregatory list for the names of the files in the current directory
    directory_list = os.listdir(directory) # Gets a list of files in the current directory
    for entry in directory_list: # Loops through all of the filenames in the directory
        absolute_filename = os.path.join(directory, entry) # Sets the variable absolute_filename to the directory listing of the iterated filename
        try: # Trys to:
            image = PIL.Image.open(absolute_filename) # Test opening file specified by the filename in PIL
            file_list += [entry] # Adds the filename to the file_list aggregator
            image_list += [image] # Adds the filename to the image_list aggregator
        except IOError: # Unless the operations throw an IOError
            pass # Then do nothing with errors tying to open non-images
    return image_list, file_list # Returns the aggregators

def make_support(picture, wide, rgb):
    '''Imposes the support image on the input picture in the current directory, 
    as well as a frame around the image
    
    Takes the argumets 'picture' (a string which is the filename of the picture which to apply the frame to)
    'wide' (an unsigned integer which is used to determine frame thiccness)
    and 'rgb' (a 4 element tuple which determines the rgb color value of the frame)
    '''
    if 'support' in picture: # Checks whether the input image is the support picture
        return None # Ends execution if it is
    else: # Else if it isn't
        pass # Continue execution
    background = PIL.Image.open(picture) # Opens the image specified by 'picture' and sets background to an instance of it
    width, height = background.size # Sets the variables width and height to the values of the 2-tuple size attribue of background
    mask = PIL.Image.open('support.png') # Opens the image 'support.png' and sets mask to an instance of it
    width0, height0 = mask.size # Sets the variables width and height to the values of the 2-tuple size attribute of mask
    mersk = PIL.ImageDraw.Draw(mask,mode='RGBA') # Sets mersk to an instance
    # Building a square frame (out of 4 polygons) on the frame1 and by extension the frame0 canvises 
    frame0 = PIL.Image.new('RGBA',(width,height),color=None)# Creates the frame0 canvis with the same dimensions as the input image
    frame1 = PIL.ImageDraw.Draw(frame0) # 
    frame1.rectangle([(0,0),(width,wide)],fill=rgb)# Draws top box
    frame1.rectangle([(0,0),(wide,height)],fill=rgb)# Draws left box
    frame1.rectangle([(width,height),(0,height-wide)],fill=rgb)# Draws bottom box
    frame1.rectangle([(width,height),(width-wide,0)],fill=rgb)# Draws right box
    frame1.rectangle([(wide,wide),(width-wide,height-wide)],fill=rgb)# Draws clear area
    dwide = 2*wide # Creates the dwide variable set to 2* the width of the frame
    qwid, hhght = (width/4,height/2) # 
    ewid0, hhght0 = (width0/8,height0/2) # 
    newground = background.resize((width-dwide,height-dwide)) # Resizes the picture to fit within the frame
    frame0.paste(newground,box=(wide,wide)) # 
    frame0.paste(mask,box=(qwid+ewid0,hhght)) # 
    frame0.show() # Displays frame0
    return frame0 # Returns the frame0 object

def make_images_support(wide, rgb):
    ''' Makes all images in the current directory support 
    images (frames them and imposes the support image on the background)
    
    Takes the arguments 'wide' (an unsigned integer which is used to determine frame thickness)
    and 'rgb' (a 4 element tuple which is an rgb value used to determine frame color)
    
    '''
    directory = os.getcwd() # Uses working directory
    new_directory = os.path.join(directory, 'support_images')# Create a new directory 'support_images'
    try: # Attempts
        os.mkdir(new_directory)# to make a new directory
    except OSError:# unless it throws an oserror
        pass # if the directory already exists, proceed
    # Load all the images
    image_list, file_list = get_images()
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

