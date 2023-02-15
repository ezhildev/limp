import math, pygame, pytmx

def load_font(file, size):
    return pygame.font.Font(file, size)

def load_img(file):
    return pygame.image.load(file);

def load_sound(file):
    return pygame.mixer.Sound(file)

def load_surface(size):
    return pygame.surface.Surface(size) 

def load_map(file):
    return pytmx.load_pygame(file)

def save_game(data, file):
    '''save the data(dictionary type) in file '''
    if type(data) != dict: raise TypeError('only dictionary type data is allowed for save')
    f = open(file, 'w')
    f.write(str(data))
    f.close()

def read_game(file):
    '''if that file is exist then it reaturn the data as a dict format
        or it will return None
    '''
    try:
        f = open(file, 'r')
        data = eval(f.read())
    except:
        f = open(file, 'a')
        data = None
    finally:
        f.close()
    return data

def image_at(spritesheet, rectangle) -> pygame.Surface:
    '''This is used to extract the image from the spritesheet'''
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(spritesheet, (0, 0), rect)
    return image

def lerp(start, end, value) -> float:
    '''Linear interpolation'''
    difference = end - start
    if difference > value:
        return start + value
    if difference < -value:
        return start - value
    return end

def fade_in(screen, value) -> None:
    '''this used to increase a alpha value'''
    alpha = lerp(screen.get_alpha(), 255, value)
    screen.set_alpha(alpha)

def fade_out(screen, value) -> None:
    '''this used to decrease a alpha value'''
    alpha = lerp(screen.get_alpha(), 0, value)
    screen.set_alpha(alpha)

def collision_list(rect:pygame.Rect, rect_list) -> list:
    '''this will return a list of collided rects'''
    collided_rects = []
    for r in rect_list:
        if rect.colliderect(r):
            collided_rects.append(r)
    return collided_rects

# this algorithm obtained from here -> https://bit.ly/3CfwfmR. some steps are modified for my convenient
def collide_circle(rect,   # rectangle info
              center_x, center_y, radius):  # circle info
    """ Detect collision between a rectangle and circle. """
    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rect.right < cleft or rect.left > cright or rect.bottom < ctop or rect.top > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rect.left, rect.right):
        for y in (rect.top, rect.bottom):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rect.left <= center_x <= rect.right and rect.top <= center_y <= rect.bottom:
        return True  # overlaid

    return False  # no collision detected

