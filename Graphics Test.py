'''
Vidur Modgil
Oregon Trail Graphics Test
AP World History
Mrs. Fitzpatrick
'''

# Preprossescor Directives
import turtle
import os

def prompt(category, prompt):
    action = turtle.textinput(category, prompt)
    return action

def main():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Graphical Elements/Background Map.png')
    tr = turtle.Turtle()
    wn = turtle.Screen()
    wn.bgpic(filename)
    tr.penup()
    tr.goto(x=-350, y=100)
    wn.mainloop()

if __name__ == '__main__':
    main()