import pygame,pigame
from pygame.locals import *
import os
from time import sleep
import time
import RPi.GPIO as GPIO
import socket 
import threading
import queue



GPIO.setmode(GPIO.BCM)

#TCP 
HOST = "127.0.0.1"
PORT =  5001
message_queue = queue.Queue()
shutdown_event = threading.Event()

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (128,0,128)
ERASER = (232,187,180)

#touchscreen setup
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY', '')

#TCP Thread
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind((HOST, PORT))
    server.listen(5)
    server.settimeout(1.0)
    
    print("TCP server listening...")
    

    with server:
        while not shutdown_event.is_set():
            try:
                conn, addr = server.accept()
            except socket.timeout:
                continue
            
            with conn:
                conn.settimeout(1.0)
                
                with conn.makefile('r', encoding='utf-8') as file:
                    message = file.readline().strip()

                    if message:
                        print("Recieved:",message)
                        message_queue.put(message)
    


server_thread = threading.Thread(target=tcp_server, daemon=True)
server_thread.start()

#Helper functions
def basic_background():
    lcd.fill(WHITE)
    #Mood buttons
    pygame.draw.rect(lcd, YELLOW, (0,0,8,25))
    pygame.draw.rect(lcd, RED, (0,65,8,25))
    pygame.draw.rect(lcd, BLUE, (0,128,8,25))
    pygame.draw.rect(lcd, GREEN, (0,190,8,25))
    #Boxes
    pygame.draw.rect(lcd, BLACK, (40,40,240,160), 2)
    pygame.draw.rect(lcd, BLACK, (290,210,30,30), 2)
    pygame.draw.rect(lcd, BLACK, (130, 210, 60, 20), 2)
    pygame.draw.rect(lcd, BLACK, (130, 10, 60, 20), 2)
    #Color select
    pygame.draw.circle(lcd, BLACK, (300, 25), 11, 0)
    pygame.draw.circle(lcd, RED, (300, 55), 11, 0)
    pygame.draw.circle(lcd, BLUE, (300, 85), 11, 0)
    pygame.draw.circle(lcd, GREEN, (300, 115), 11, 0)
    pygame.draw.circle(lcd, PURPLE, (300, 145), 11, 0)
    pygame.draw.circle(lcd, ERASER, (300, 185), 15, 0)
    #Width select
    pygame.draw.circle(lcd, BLACK, (240, 15), 11, 2)
    pygame.draw.circle(lcd, BLACK, (240, 15), 2, 0)
    pygame.draw.circle(lcd, BLACK, (270, 15), 11, 2)
    pygame.draw.circle(lcd, BLACK, (270, 15), 5, 0)
    #Text
    text_surface = eraser_text.render('Eraser', True, BLACK)
    text_rect = text_surface.get_rect(center = (300, 185))
    lcd.blit(text_surface, text_rect)
    text_surface = font_text.render('Quit', True, BLACK)
    text_rect = text_surface.get_rect(center = (305, 225))
    lcd.blit(text_surface, text_rect)
    text_surface = font_text.render('Send', True, BLACK)
    text_rect = text_surface.get_rect(center = (160, 220))
    lcd.blit(text_surface, text_rect)
    text_surface = font_text.render('Clear', True, BLACK)
    text_rect = text_surface.get_rect(center = (160, 20))
    lcd.blit(text_surface, text_rect)

def selected_color_highlight(color, width):
    if color == BLACK: y_val = 25
    elif color == RED: y_val = 55
    elif color == BLUE: y_val = 85
    elif color == GREEN: y_val = 115
    elif color == PURPLE: y_val = 145
    elif color == WHITE:
        y_val = 185
        pygame.draw.circle(lcd, BLACK, (300, y_val), 15, 3)
        return
    pygame.draw.circle(lcd, BLACK, (300, y_val), 11, 3)
    if width == 2:
        pygame.draw.circle(lcd, BLACK, (240, 15), 13, 2)
    elif width == 4:
        pygame.draw.circle(lcd, BLACK, (270,15), 13, 2)

def notification(message):
    pygame.draw.rect(lcd, BLACK, (10,10,300,50), 3)
    notif_message = f"Message Recieved: {message}"
    text_surface = font_text.render(notif_message, True, BLACK)
    text_rect = text_surface.get_rect(center = (160, 35))
    lcd.blit(text_surface, text_rect)


current_color = BLACK
current_width = 2
current_line = []
drawing_lines = []
drawing_color = []
drawing_width = []

def current_drawing():
    for index, line in enumerate(drawing_lines):
        for i in range(1, len(line)):
            pygame.draw.line(lcd, drawing_color[index], (320-line[i-1][0], 240-line[i-1][1]), (320-line[i][0], 240-line[i][1]),drawing_width[index])
    for i in range(1, len(current_line)):
        pygame.draw.line(lcd, current_color, (320-current_line[i-1][0], 240-current_line[i-1][1]),(320-current_line[i][0], 240-current_line[i][1]),current_width)


#pygame setup
pygame.init()
pitft = pigame.PiTft()
lcd = pygame.display.set_mode((320,240))
font_text = pygame.font.Font(None, 15)
eraser_text = pygame.font.Font(None, 13)
basic_background()
selected_color_highlight(current_color, current_width)
pygame.display.update()

#GPIO setup
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
active_notification = False
notification_message = ""

while code_run:
    #ANIMATION
    pitft.update()
    for event in pygame.event.get():
        if(event.type == MOUSEBUTTONDOWN):
            x,y = pygame.mouse.get_pos()
            basic_background()

            #DRAWING
            if (x > 40 and x < 280 and y > 40 and y < 200):
                drawing = True
                current_line = [(x,y)]
            #QUIT
            elif (x < 30 and y < 30):
                code_run = False
            #COLOR OPTIONS
            elif (x < 30 and y > 200 and y < 230):
                current_color = BLACK
            elif (x < 30 and y > 175 and y < 185):
                current_color = RED
            elif (x < 30 and y > 140 and y < 170):
                current_color = BLUE
            elif (x < 30 and y > 110 and y < 140):
                current_color = GREEN
            elif (x < 30 and y > 80 and y < 110):
                current_color = PURPLE
            elif (x < 30 and y > 40 and y < 70):
                current_color = WHITE
                current_width = 10
            #SIZE OPTIONS
            elif (x > 65 and x < 95 and y > 225):
                current_width = 2
            elif (x > 35 and x < 65 and y > 225):
                current_width = 4
            #CLEAR
            elif (x > 130 and x < 190 and y > 210 and y < 230):
                current_line = []
                drawing_lines = []
                drawing_color = []
                drawing_width = []
            if (len(drawing_width) != 0):
                if drawing_width[-1] == 10:
                    current_width = drawing_width[-2]
        elif(event.type == MOUSEBUTTONUP):
            if drawing:
                drawing = False
                drawing_lines.append(current_line)
                drawing_color.append(current_color)
                drawing_width.append(current_width)
                current_line = []
    if drawing:
        x,y = pygame.mouse.get_pos()

        if (x > 40 and x < 280 and y > 40 and y < 200):
            current_line.append((x,y))
    basic_background()
    selected_color_highlight(current_color, current_width)
    current_drawing()
    if active_notification:
        notification(notification_message)
    pygame.display.flip() 

    #MOOD DETECT
    while not message_queue.empty():
        message = message_queue.get_nowait()
        active_notification = True
        if message == "hello":
            notification_message = "Hello"
        elif message == "love":
            notification_message = "I love you"
        elif message == "miss":
            notification_message = "I miss you"
        elif message == "proud":
            notification_message = "I'm proud of you"

shutdown_event.set()
server_thread.join(timeout=2)
del(pitft)
pygame.quit()
GPIO.remove_event_detect(27)
GPIO.remove_event_detect(23)
GPIO.remove_event_detect(22)
GPIO.remove_event_detect(17)
GPIO.cleanup()
