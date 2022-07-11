from pickletools import uint8
import cv2 as cv
import numpy as np
import pyautogui
from PIL import ImageGrab, Image, ImageTk
import time
import requests
import pygame
import keyboard
import mouse
import pyWinhook
import autopy
from win32api import GetSystemMetrics
import tkinter as tk
from bs4 import BeautifulSoup
import sys
import threading
pygame.init()

needle_img = cv.imread('needle.png',0)
#cv.imshow("text",needle_img)
sys.setrecursionlimit(10000)
needle_w = needle_img.shape[1]
needle_h = needle_img.shape[0]

def get_mouse_posn(event):
    global topy, topx

    topx, topy = event.x, event.y

def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty

    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)


def selectArea():
    pass
def showBox():
    img = ImageGrab.grab(bbox=(topx,topy,botx,boty))
    img.show()

def matchConfidence():
    img = ImageGrab.grab(bbox=(60,305,1900,1025))
    img.convert('RGBA')
    img_np = np.array(img)
    img_np = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)
    
    result = cv.matchTemplate(img_np, needle_img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print('Best match confidence:  %s' % max_val)


def play():
    if not keyboard.is_pressed('q'):
        img = ImageGrab.grab(bbox=(topx,topy,botx,boty))
        img.convert('RGBA')
        img_np = np.array(img)
        img_np = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)
        

        result = cv.matchTemplate(img_np, needle_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        top_left = max_loc[0]
        if(max_val >=0.65):
        #Move mouse to the position
            mouse.move(top_left+60,385)
        thread = threading.Thread(target=play)
        thread.start()


WIDTH, HEIGHT = 900, 900
topx, topy, botx, boty = 0, 0, 0, 0
rect_id = None  
window = tk.Tk()
window.title("Select Area")
window.geometry('%sx%s' % (WIDTH, HEIGHT))
window.configure(background='grey')

imgPy = pyautogui.screenshot()
img = ImageTk.PhotoImage(imgPy)
canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                   borderwidth=0, highlightthickness=0)
canvas.pack(expand=True)
canvas.img = img  
canvas.create_image(0, 0, image=img, anchor=tk.NW)

# Select Rectangle
rect_id = canvas.create_rectangle(topx, topy, topx, topy,
                                  dash=(2,2), fill='', outline='white')

canvas.bind('<Button-1>', get_mouse_posn)
canvas.bind('<B1-Motion>', update_sel_rect)

window.mainloop()
#showBox()
play()
