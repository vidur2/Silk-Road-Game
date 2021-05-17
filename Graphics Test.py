'''
Vidur Modgil
Oregon Trail Graphics Test
AP World History
Mrs. Fitzpatrick
'''

# Preprossescor Directives
import turtle
import os
import time

def main():
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'Graphical Elements/Background Map.png')
        tr = turtle.Turtle()
        wn = turtle.Screen()
        wn.bgpic(filename)
        tr.penup()
        tr.goto(x=-350, y=100)
        tr.pendown()
        tr.goto(x=-230, y=0)
        tr.goto(x=-180, y=10)
        tr.goto(x=-150, y=20)
        tr.goto(x=-50, y=100)
        tr.goto(200, 100)
        tr.goto(250, -80)
        wn.mainloop()
        print('Done!')
    except:
        print('Done!')
if __name__ == '__main__':
    main()