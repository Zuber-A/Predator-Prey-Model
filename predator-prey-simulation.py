import turtle
import random

class World:
    def __init__(self, mx, my):
        self.maxX = mx
        self.maxY = my
        self.thingList = []
        self.grid = []
        self.bearCount = 0
        self.deerCount = 0
        self.fishCount = 0
        self.plantCount = 0

        for arow in range(self.maxY):
            row = []
            for acol in range(self.maxX):
                row.append(None)
            self.grid.append(row)

        self.wturtle = turtle.Turtle()
        self.wscreen = turtle.Screen()
        self.wscreen.setworldcoordinates(0, 0, self.maxX - 1, self.maxY - 1)
        self.wscreen.addshape("Bear.gif")
        self.wscreen.addshape("Fish.gif")
        self.wscreen.addshape("Plant.gif")
        self.wscreen.addshape("Deer.gif")
        self.wturtle.hideturtle()

    def draw(self):
        self.wscreen.tracer(0)
        self.wturtle.forward(self.maxX - 1)
        self.wturtle.left(90)
        self.wturtle.forward(self.maxY - 1)
        self.wturtle.left(90)
        self.wturtle.forward(self.maxX - 1)
        self.wturtle.left(90)
        self.wturtle.forward(self.maxY - 1)
        self.wturtle.left(90)
        for i in range(self.maxY - 1):
            self.wturtle.forward(self.maxX - 1)
            self.wturtle.backward(self.maxX - 1)
            self.wturtle.left(90)
            self.wturtle.forward(1)
            self.wturtle.right(90)
        self.wturtle.forward(1)
        self.wturtle.right(90)
        for i in range(self.maxX - 2):
            self.wturtle.forward(self.maxY - 1)
            self.wturtle.backward(self.maxY - 1)
            self.wturtle.left(90)
            self.wturtle.forward(1)
            self.wturtle.right(90)
        self.wscreen.tracer(1)

    def freezeWorld(self):
        self.wscreen.exitonclick()

    def addThing(self, athing, x, y):
        athing.setX(x)
        athing.setY(y)
        self.grid[y][x] = athing
        athing.setWorld(self)
        self.thingList.append(athing)
        athing.appear()

    def delThing(self, athing):
        athing.hide()
        self.grid[athing.getY()][athing.getX()] = None
        self.thingList.remove(athing)

    def moveThing(self, oldx, oldy, newx, newy):
        self.grid[newy][newx] = self.grid[oldy][oldx]
        self.grid[oldy][oldx] = None

    def getMaxX(self):
        return self.maxX

    def getMaxY(self):
        return self.maxY

    def liveALittle(self):
        if self.thingList != []:
            athing = random.randrange(len(self.thingList))
            randomthing = self.thingList[athing]
            randomthing.liveALittle()

    def emptyLocation(self, x, y):
        if self.grid[y][x] == None:
            return True
        else:
            return False

    def lookAtLocation(self, x, y):
        return self.grid[y][x]

class Plant:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.hideturtle()
        self.turtle.shape("Plant.gif")

        self.xpos = 0
        self.ypos = 0
        self.world = None

        self.breedTick = 0

    def setX(self, newx):
        self.xpos = newx

    def setY(self, newy):
        self.ypos = newy

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def setWorld(self, aworld):
        self.world = aworld

    def appear(self):
        self.turtle.goto(self.xpos, self.ypos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def liveALittle(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        adjplant = 0
        for offset in offsetList:
            newx = self.xpos + offset[0]
            newy = self.ypos + offset[1]
            if 0 <= newx < self.world.getMaxX() and 0 <= newy < self.world.getMaxY():
                if (not self.world.emptyLocation(newx, newy)) and isinstance(self.world.lookAtLocation(newx, newy),
                                                                             Plant):
                    adjplant = adjplant + 1

        if adjplant >= 2:
            self.world.delThing(self)
        else:
            self.breedTick = self.breedTick + 1
            if self.breedTick >= 10:
                self.tryToBreed()


    def tryToBreed(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        while True:
            randomOffset = random.choice(offsetList)
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]
            if (0 <= nextx < self.world.getMaxX() and
                               0 <= nexty < self.world.getMaxY()):
                break

        if self.world.emptyLocation(nextx, nexty):
            childThing = Plant()
            self.world.addThing(childThing, nextx, nexty)
            self.breedTick = 0

class Fish:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.hideturtle()
        self.turtle.shape("Fish.gif")

        self.xpos = 0
        self.ypos = 0
        self.world = None

        self.starveTick = 0
        self.breedTick = 0

    def setX(self, newx):
        self.xpos = newx

    def setY(self, newy):
        self.ypos = newy

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def setWorld(self, aworld):
        self.world = aworld

    def appear(self):
        self.turtle.goto(self.xpos, self.ypos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def move(self, newx, newy):
        self.world.moveThing(self.xpos, self.ypos, newx, newy)
        self.xpos = newx
        self.ypos = newy
        self.turtle.goto(self.xpos, self.ypos)

    def liveALittle(self):
        self.breedTick = self.breedTick + 1
        if self.breedTick >= 10:
            self.tryToBreed()

        self.tryToEat()

        if self.starveTick == 14:
            self.world.delThing(self)
        else:
            self.tryToMove()

    def tryToEat(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        adjprey = []
        for offset in offsetList:
            newx = self.xpos + offset[0]
            newy = self.ypos + offset[1]
            if 0 <= newx < self.world.getMaxX() and 0 <= newy < self.world.getMaxY():
                if (not self.world.emptyLocation(newx, newy)) and isinstance(self.world.lookAtLocation(newx, newy),
                                                                             Plant):
                    adjprey.append(self.world.lookAtLocation(newx, newy))

        if len(adjprey) > 0:
            randomprey = adjprey[random.randrange(len(adjprey))]
            preyx = randomprey.getX()
            preyy = randomprey.getY()

            self.world.delThing(randomprey)
            self.move(preyx, preyy)
            self.starveTick = 0
        else:
            self.starveTick = self.starveTick + 1

    def tryToBreed(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        while True:
            randomOffset = random.choice(offsetList)
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]
            if (0 <= nextx < self.world.getMaxX() and
                               0 <= nexty < self.world.getMaxY()):
                break

        if self.world.emptyLocation(nextx, nexty):
            childThing = Fish()
            self.world.addThing(childThing, nextx, nexty)
            self.breedTick = 0

    def tryToMove(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        while True:
            randomOffset = random.choice(offsetList)
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]
            if (0 <= nextx < self.world.getMaxX() and
                               0 <= nexty < self.world.getMaxY()):
                break

        if self.world.emptyLocation(nextx, nexty):
            self.move(nextx, nexty)

class Deer:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.hideturtle()
        self.turtle.shape("Deer.gif")

        self.xpos = 0
        self.ypos = 0
        self.world = None

        self.starveTick = 0
        self.breedTick = 0

    def setX(self, newx):
        self.xpos = newx

    def setY(self, newy):
        self.ypos = newy

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def setWorld(self, aworld):
        self.world = aworld

    def appear(self):
        self.turtle.goto(self.xpos, self.ypos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def move(self, newx, newy):
        self.world.moveThing(self.xpos, self.ypos, newx, newy)
        self.xpos = newx
        self.ypos = newy
        self.turtle.goto(self.xpos, self.ypos)

    def liveALittle(self):
        self.breedTick = self.breedTick + 1
        if self.breedTick >= 10:
            self.tryToBreed()

        self.tryToEat()

        if self.starveTick == 14:
            self.world.delThing(self)
        else:
            self.tryToMove()

    def tryToEat(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        adjprey = []
        for offset in offsetList:
            newx = self.xpos + offset[0]
            newy = self.ypos + offset[1]
            if 0 <= newx < self.world.getMaxX() and 0 <= newy < self.world.getMaxY():
                if (not self.world.emptyLocation(newx, newy)) and isinstance(self.world.lookAtLocation(newx, newy),
                                                                             Plant):
                    adjprey.append(self.world.lookAtLocation(newx, newy))

        if len(adjprey) > 0:
            randomprey = adjprey[random.randrange(len(adjprey))]
            preyx = randomprey.getX()
            preyy = randomprey.getY()

            self.world.delThing(randomprey)
            self.move(preyx, preyy)
            self.starveTick = 0
        else:
            self.starveTick = self.starveTick + 1

    def tryToBreed(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        while True:
            randomOffset = random.choice(offsetList)
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]
            if (0 <= nextx < self.world.getMaxX() and
                               0 <= nexty < self.world.getMaxY()):
                break

        if self.world.emptyLocation(nextx, nexty):
            childThing = Deer()
            self.world.addThing(childThing, nextx, nexty)
            self.breedTick = 0

    def tryToMove(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        while True:
            randomOffset = random.choice(offsetList)
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]
            if (0 <= nextx < self.world.getMaxX() and
                               0 <= nexty < self.world.getMaxY()):
                break

        if self.world.emptyLocation(nextx, nexty):
            self.move(nextx, nexty)

class Bear:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.hideturtle()
        self.turtle.shape("Bear.gif")

        self.xpos = 0
        self.ypos = 0
        self.world = None

        self.starveTick = 0
        self.breedTick = 0

    def setX(self, newx):
        self.xpos = newx

    def setY(self, newy):
        self.ypos = newy

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def setWorld(self, aworld):
        self.world = aworld

    def appear(self):
        self.turtle.goto(self.xpos, self.ypos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def move(self, newx, newy):
        self.world.moveThing(self.xpos, self.ypos, newx, newy)
        self.xpos = newx
        self.ypos = newy
        self.turtle.goto(self.xpos, self.ypos)

    def liveALittle(self):
        self.breedTick = self.breedTick + 1
        if self.breedTick >= 8:
            self.tryToBreed()

        self.tryToEat()

        if self.starveTick == 10:
            self.world.delThing(self)
        else:
            self.tryToMove()

    def tryToEat(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        adjprey = []
        for offset in offsetList:
            newx = self.xpos + offset[0]
            newy = self.ypos + offset[1]
            if 0 <= newx < self.world.getMaxX() and 0 <= newy < self.world.getMaxY():
                if (not self.world.emptyLocation(newx, newy)) and\
                        isinstance(self.world.lookAtLocation(newx, newy),Fish):
                    adjprey.append(self.world.lookAtLocation(newx, newy))

            if 0 <= newx < self.world.getMaxX() and 0 <= newy < self.world.getMaxY():
                if (not self.world.emptyLocation(newx, newy)) and \
                        isinstance(self.world.lookAtLocation(newx, newy), Deer):
                    adjprey.append(self.world.lookAtLocation(newx, newy))

        if len(adjprey) > 0:
            randomprey = adjprey[random.randrange(len(adjprey))]
            preyx = randomprey.getX()
            preyy = randomprey.getY()

            self.world.delThing(randomprey)
            self.move(preyx, preyy)
            self.starveTick = 0
        else:
            self.starveTick = self.starveTick + 1

    def tryToBreed(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        while True:
            randomOffset = random.choice(offsetList)
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]
            if (0 <= nextx < self.world.getMaxX() and
                               0 <= nexty < self.world.getMaxY()):
                break

        if self.world.emptyLocation(nextx, nexty):
            childThing = Bear()
            self.world.addThing(childThing, nextx, nexty)
            self.breedTick = 0

    def tryToMove(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0), (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        while True:
            randomOffset = random.choice(offsetList)
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]
            if (0 <= nextx < self.world.getMaxX() and
                               0 <= nexty < self.world.getMaxY()):
                break

        if self.world.emptyLocation(nextx, nexty):
            self.move(nextx, nexty)

NUMBER_OF_BEARS = 5
NUMBER_OF_DEER = 9
NUMBER_OF_FISH = 9
NUMBER_OF_PLANTS = 9
WORLD_LIFE_TIME = 5000
WORLD_WIDTH = 50
WORLD_HEIGHT = 25

World.wscreen = turtle.Screen()


def mainSimulation():

    myworld = World(WORLD_WIDTH, WORLD_HEIGHT)
    myworld.draw()

    for i in range(NUMBER_OF_FISH):
        newfish = Fish()
        while True:
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())

            if myworld.emptyLocation(x, y):
                break

        myworld.addThing(newfish, x, y)

    for i in range(NUMBER_OF_PLANTS):
        newplant = Plant()
        while True:
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())

            if myworld.emptyLocation(x, y):
                break

        myworld.addThing(newplant, x, y)

    for i in range(NUMBER_OF_BEARS):
        newbear = Bear()
        while True:
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())

            if myworld.emptyLocation(x, y):
                break

        myworld.addThing(newbear, x, y)

    for i in range(NUMBER_OF_DEER):
        newdeer = Deer()
        while True:
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())

            if myworld.emptyLocation(x, y):
                break

        myworld.addThing(newdeer, x, y)


    for i in range(WORLD_LIFE_TIME):

        World.wscreen.tracer(0)
        myworld.liveALittle()
        World.wscreen.tracer(1)


    myworld.freezeWorld()


mainSimulation()

