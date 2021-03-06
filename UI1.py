import pygame
from pygame import font
from  deep1 import prediction
from PIL import Image, ImageGrab
import numpy as np

# pre defined colors, pen radius and font color
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
draw_on = False
last_pos = (0, 0)
color = (255, 128, 0)
radius = 4
font_size = 500

#image size
width = 400
height = 400

# initializing screen
screen = pygame.display.set_mode((width, height))
screen.fill(white)
pygame.font.init()
pygame.display.set_caption("MLP Digits:Please Right Click to Clear Entry")

def crope(orginal):
    cropped = pygame.Surface((width-5, height-5))
    cropped.blit(orginal, (0, 0), (0, 0, width-5, height-5))
    return cropped


def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)

def text_objects(text, myfont):
    textSurface = myfont.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',14)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (150,350)
    screen.blit(TextSurf, TextRect)

    pygame.display.update()
	
try:
    while True:
        # get all events
        e = pygame.event.wait()

        # clear screen after right click
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button == 3):
            screen.fill(white)

        # quit
        if e.type == pygame.QUIT:
            raise StopIteration

        # start drawing after left click
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button != 3):
            color = black
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True

        # stop drawing after releasing left click
        if e.type == pygame.MOUSEBUTTONUP and e.button != 3:
            draw_on = False
            #change directory to desired place to save input image
            fname = r"C:\Users\erick\.conda\envs\Deep Learn Hello World\Test Image\img_test1.png" 
            img = crope(screen)
            pygame.image.save(img, fname)
            img1 = Image.open(fname)
            img2 = img1.resize((28,28))
            img3 = np.invert(img2.convert('L')).ravel()
            output_img = prediction(img3)
            Predict = "Prediction for test image: " + str(np.squeeze(output_img))
            message_display(Predict)
        # start drawing line on screen if draw is true
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)
            last_pos = e.pos

        pygame.display.flip()

	
except StopIteration:
    pass
pygame.quit()

