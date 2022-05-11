from pynput.mouse import Listener
import webcolors
import numpy as np
import math
import pyautogui
import cv2 as cv



def get_corners_pos():
    print("Click on the top left and bottom right corner to calibrate the game ... ")
    corners = [None, None]
    def on_click(x, y, button, pressed):
        if pressed:
            if corners[0]:
                corners[1] = (x, y)
                return False
            else:
                corners[0] = (x, y)

    with Listener(on_click=on_click) as listener:
        listener.join()
    
    return corners


def get_contours(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, threshold = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    return contours[1:]

def get_count():
    pass 


def get_shape(img):
    contours = get_contours(img)
    
    count = [0, 0, 0] # oval, losange, squiggle

    contours = sorted(contours, key=cv.contourArea)
    contours.reverse()
    
    img_c = img.shape[0] / 2
    img_width = img.shape[1]
    good_contours = []
    # Only keep contours where the y center is close to the image center
    for cnt in contours:
        m = cv.moments(cnt)
        try:
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])
        except:
            continue
        
        good_area = (img_width * 0.1, img_c - img.shape[0] * 0.2) 
        w = img_width - img_width * 0.2
        h = img.shape[0] * 0.4
    

        if cx >= good_area[0] and cx <= good_area[0] + w:
            if cy >= good_area[1] and cy <= good_area[1] + h:
                good_contours.append(cnt)
    
    if good_contours:
        principal_shapes = [good_contours[0]]
        for i in range(1, len(good_contours)):
            prev_cnt = cv.contourArea(good_contours[i - 1])
            cnt = cv.contourArea(good_contours[i])
            if math.isclose(prev_cnt, cnt, abs_tol= 0.5):
                principal_shapes.append(good_contours[i])
            else:
                break

        return principal_shapes

    return good_contours

    if count[0] >= max(count):
        return 'oval'
    elif count[1] >= max(count):
        return 'losange'
    elif count[2] >= max(count):
        return 'squiggle'
    else:
        return len(contours)


def get_color(img):
    def get_closest_color(requested_color):
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name

        return min_colors[min(min_colors.keys())]

    colors = np.unique(img.reshape(-1, img.shape[2]), axis=0)

    count = [0, 0, 0] # green, red, purple
    for color in colors:
        try:
           color = webcolors.rgb_to_name(color)
        except:
           color = get_closest_color(color)
        
        if 'green' in color:
            count[0] += 1
        elif 'blue' in color:
            count[1] += 1
        elif 'magenta' in color:
            count[2] += 1

    if count[0] >= max(count):
        return 'green'
    elif count[1] >= max(count):
        return 'red'
    elif count[2] >= max(count):
        return 'purple'

    return 'no idea'


def get_filling():
    pass


def extract_characteristics(img):
    return {"color": get_color(img), "shape": get_shape(img)}


def read_board(img):
    
    cols, rows = 3, 4

    sq_w = img.shape[1] / cols
    sq_h = img.shape[0] / rows
    for i in range(3):
        for j in range(4):
            tl = (i * sq_w, j * sq_h)
            x = int(tl[0])
            y = int(tl[1])
            w = int(sq_w)
            h = int(sq_h)
    
            characteristics = extract_characteristics(img[y:y + h, x: x + w])
            
            # Print color on the screen
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(img, characteristics['color'], (x, y + h ), font, 0.5,(0,0,0), 1, cv.LINE_AA)
            cv.putText(img, str(len(characteristics['shape'])), (x, y + 20), font, 0.5,(0,0,0), 1, cv.LINE_AA)


    return img

if __name__ == '__main__':
    corners = get_corners_pos()
    tl = corners[0]
    br = corners[1]
    w = br[0] - tl[0]
    h = br[1] - tl[1]

    while True:
        img = pyautogui.screenshot(region=(tl[0], tl[1], w, h))
        img = np.array(img)[:, :, ::-1].copy()
        
        img = read_board(img)

        cv.imshow('Current Board', img)

        cv.waitKey(0)
        cv.destroyAllWindows()
        


    
    




