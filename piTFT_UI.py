import pygame,pigame
from pygame.locals import *
import os
from time import sleep
import time
import RPi.GPIO as GPIO



#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#touchscreen setup
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY', '')


#Helper functions
def basic_background():
    lcd.fill(WHITE)
    pygame.draw.rect(lcd, YELLOW, (0,0,8,25))
    pygame.draw.rect(lcd, RED, (0,65,8,25))
    pygame.draw.rect(lcd, BLUE, (0,128,8,25))
    pygame.draw.rect(lcd, GREEN, (0,190,8,25))
    pygame.draw.rect(lcd, BLACK, (40,40,240,160), 2)
    pygame.draw.rect(lcd, BLACK, (290,210,30,30), 2)
    text_surface = font_text.render('Quit', True, BLACK)
    text_rect = text_surface.get_rect(center = (305, 225))
    lcd.blit(text_surface, text_rect)

drawing_coords = []

def current_drawing():
    for i in range(1, len(drawing_coords)):
        pygame.draw.line(lcd, current_color, (320-drawing_coords[i-1][0], 240-drawing_coords[i-1][1]), (320-drawing_coords[i][0], 240-drawing_coords[i][1]), 2)

#pygame setup
pygame.init()
pitft = pigame.PiTft()
lcd = pygame.display.set_mode((320,240))
font_text = pygame.font.Font(None, 20)
basic_background()
pygame.display.update()

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def red_mood(channel):
    print("Red mood being sent")

def blue_mood(channel):
    print("Blue mood being sent")

def green_mood(channel):
    print("Green mood being sent")

def yellow_mood(channel):
    print("Yellow mood being sent")

GPIO.add_event_detect(27, GPIO.FALLING, callback=yellow_mood)
GPIO.add_event_detect(23, GPIO.FALLING, callback=red_mood)
GPIO.add_event_detect(22, GPIO.FALLING, callback=blue_mood)
GPIO.add_event_detect(17, GPIO.FALLING, callback=green_mood)

code_run = True
drawing = False
current_color = BLACK

while code_run:
    pitft.update()
    for event in pygame.event.get():
        if(event.type == MOUSEBUTTONDOWN):
            x,y = pygame.mouse.get_pos()
            basic_background()

            if (x > 40 and x < 280 and y > 40 and y < 200):
                drawing = True
            elif (x < 30 and y < 30):
                pygame.quit()
                code_run = False
        elif(event.type == MOUSEBUTTONUP):
            drawing = False
    if drawing:
        x,y = pygame.mouse.get_pos()

        if (x > 40 and x < 280 and y > 40 and y < 200):
            drawing_coords.append((x,y))
            basic_background()
            current_drawing()
            pygame.display.flip()

del(pitft)
pygame.quit()
GPIO.cleanup()
