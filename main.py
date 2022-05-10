from pynput.mouse import Listener



def get_corners_pos():
    corners = (None, None)

    def on_click(x, y, button, pressed):
        if pressed:
            print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

    with Lister(on_click=on_click) as listener:
        listener.join()
        
        

if __name__ == '__main__':
    get_corner_pos()
    



