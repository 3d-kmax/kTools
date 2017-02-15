# kRandomizer
# Maxime Terray : kMax
# 04/04/7/2015
# Version 0.1
# Randomizer pour Maya 2014


import maya.cmds as mc
import random
from functools import partial


class kRandomizer():
    def __init__(self):

        a = 1
        b = a - .95 / 2
        g = 0.165
        gg = .27
        self.red = (a, b, b)
        self.green = (b, a, b)
        self.blue = (b, b * 1.5, a)
        self.grey = (g, g, g)
        self.grey2 = (gg,gg,gg)

        self.stateMoveUniform = 0
        self.stateRotateUniform = 0
        self.stateScaleUniform = 0

        self.kmRandomizerUI()

    def kmRandomizerUI(self):
        windowName = "kRandomizer"
        if mc.window(windowName, q=True, exists=True):
            mc.deleteUI(windowName)
        hi = 20

        randWindow = mc.window(windowName, resizeToFitChildren=True, sizeable=False, toolbox=True, titleBar=True,
                               minimizeButton=False, maximizeButton=False)

        mc.frameLayout(labelVisible=0, borderVisible=False, marginHeight=0, marginWidth=0)

        mc.rowLayout(numberOfColumns=5)

        # POSITION
        mc.frameLayout(label='Position :', labelVisible=0,  marginHeight=4, marginWidth=4)

        mc.rowColumnLayout("Position", numberOfColumns=2, columnSpacing=[(1, 4), (2, 4)], rowSpacing=[(1, 2)],
                           width=110, height=80, columnWidth=[(1, 50), (2, 50)])
        mc.text("Min :")
        mc.text("Max :")
        self.posXMin = mc.textField(text=0, backgroundColor=self.red)
        self.posXMax = mc.textField(text=0, backgroundColor=self.red)
        self.posYMin = mc.textField(text=0, backgroundColor=self.green)
        self.posYMax = mc.textField(text=0, backgroundColor=self.green)
        self.posZMin = mc.textField(text=0, backgroundColor=self.blue)
        self.posZMax = mc.textField(text=0, backgroundColor=self.blue)
        mc.setParent('..')

        mc.columnLayout()
        mc.radioCollection()
        self.rbRelativeTranslate = mc.radioButton(label='Relative')
        self.rbAbsoluteTranslate = mc.radioButton(label='Absolute', select=True)
        mc.separator(h=hi, style='none')
        mc.button(label="Position", width=110, command=self.kmRandomizePostion)
        mc.setParent('..')

        mc.setParent('..')

        # ROTATION
        mc.frameLayout(label='Rotation :', labelVisible=0,  marginHeight=4, marginWidth=4)

        mc.rowColumnLayout("Rotation", numberOfColumns=2, columnSpacing=[(1, 4), (2, 4)], rowSpacing=[(1, 2)],
                           width=110, height=80, columnWidth=[(1, 50), (2, 50)])
        mc.text("Min :")
        mc.text("Max :")
        self.rotXMin = mc.textField(text=0, backgroundColor=self.red)
        self.rotXMax = mc.textField(text=0, backgroundColor=self.red)
        self.rotYMin = mc.textField(text=0, backgroundColor=self.green)
        self.rotYMax = mc.textField(text=0, backgroundColor=self.green)
        self.rotZMin = mc.textField(text=0, backgroundColor=self.blue)
        self.rotZMax = mc.textField(text=0, backgroundColor=self.blue)
        mc.setParent('..')

        mc.columnLayout()
        mc.radioCollection()
        self.rbRelativeRotate = mc.radioButton(label='Relative')
        self.rbAbsoluteRotate = mc.radioButton(label='Absolute', select=True)
        mc.separator(h=hi, style='none')
        mc.button(label="Rotation", width=110, command=self.kmRandomizeRotation)
        mc.setParent('..')

        mc.setParent('..')

        # SCALE
        mc.frameLayout(label='Scale :', labelVisible=0,  marginHeight=4, marginWidth=4)

        mc.rowColumnLayout("Scale", numberOfColumns=2, columnSpacing=[(1, 4), (2, 4)], rowSpacing=[(1, 2)], width=110,
                           height=80, columnWidth=[(1, 50), (2, 50)])
        mc.text("Min :")
        mc.text("Max :")
        self.scaleXMin = mc.textField(text=1, backgroundColor=self.red)
        self.scaleXMax = mc.textField(text=1, backgroundColor=self.red)
        self.scaleYMin = mc.textField(text=1, backgroundColor=self.green)
        self.scaleYMax = mc.textField(text=1, backgroundColor=self.green)
        self.scaleZMin = mc.textField(text=1, backgroundColor=self.blue)
        self.scaleZMax = mc.textField(text=1, backgroundColor=self.blue)
        mc.setParent('..')

        mc.columnLayout()
        mc.radioCollection()
        self.rbRelativeScale = mc.radioButton(label='Relative')
        self.rbAbsoluteScale = mc.radioButton(label='Absolute', select=True)
        self.cbScaleUniform = mc.checkBox(label='Uniform', height=20, onCommand=self.kmScaleUniformOn,
                                          offCommand=self.kmScaleUniformOff)
        mc.button(label="Scale", width=110, command=self.kmRandomizeScale)
        mc.setParent('..')

        mc.setParent('..')

        # RANDOMIZE SPECIAL
        mc.frameLayout(label='One Axe :', labelVisible=0,  marginHeight=4, marginWidth=4)

        mc.rowColumnLayout("One axe", numberOfColumns=2, columnSpacing=[(1, 4), (2, 4)], rowSpacing=[(1, 2)], width=110,
                           columnWidth=[(1, 50), (2, 50)])
        mc.text("Min :")
        mc.text("Max :")
        self.kmin = mc.textField(text=0)
        self.kmax = mc.textField(text=0)

        mc.setParent('..')

        mc.rowLayout(numberOfColumns=2)

        mc.columnLayout(width=55)
        self.cbAxeX = mc.checkBox(label='Axe X', value=False, changeCommand=self.goX)
        self.cbAxeY = mc.checkBox(label='Axe Y', value=False, changeCommand=self.goY)
        self.cbAxeZ = mc.checkBox(label='Axe Z', value=False, changeCommand=self.goZ)
        mc.setParent('..')

        mc.columnLayout(width=55)
        mc.radioCollection()
        self.rbMove = mc.radioButton(label='Move', select=True, onCommand=self.goMove)
        self.rbRotate = mc.radioButton(label='Rotate', onCommand=self.goRotate)
        self.rbScale = mc.radioButton(label='Scale', onCommand=self.goScale)
        mc.setParent('..')

        mc.setParent('..')

        mc.columnLayout()
        mc.radioCollection()
        self.rbRelative = mc.radioButton(label='Relative')
        self.rbAbsolute = mc.radioButton(label='Absolute', select=True)
        mc.button(label="Special", width=110, command=self.kmRandomizeSpecial)
        mc.setParent('..')

        mc.setParent('..')

        #mc.setParent( '..' )

        mc.showWindow(windowName)

    '''
    def randomizeValue(self, xMin, xMax, yMin, yMax, zMin, zMax):

        xMin = float(mc.textField(self.			,q=True, text=True))
        yMin = float(mc.textField(self.			,q=True, text=True))
        zMin = float(mc.textField(self.			,q=True, text=True))
        xMax = float(mc.textField(self.			,q=True, text=True))
        yMax = float(mc.textField(self.			,q=True, text=True))
        zMax = float(mc.textField(self.			,q=True, text=True))
    '''

    def goX(self, *arg):
        if mc.checkBox(self.cbAxeX, query=True, value=True):
            mc.checkBox(self.cbAxeX, edit=True, backgroundColor=self.red)
        else:
            mc.checkBox(self.cbAxeX, edit=True, backgroundColor=self.grey2)

    def goY(self, *arg):
        if mc.checkBox(self.cbAxeY, query=True, value=True):
            mc.checkBox(self.cbAxeY, edit=True, backgroundColor=self.green)
        else:
            mc.checkBox(self.cbAxeY, edit=True, backgroundColor=self.grey2)

    def goZ(self, *arg):
        if mc.checkBox(self.cbAxeZ, query=True, value=True):
            mc.checkBox(self.cbAxeZ, edit=True, backgroundColor=self.blue)
        else:
            mc.checkBox(self.cbAxeZ, edit=True, backgroundColor=self.grey2)

    def goMove(self, *args):
        mc.radioButton(self.rbAbsolute, edit=True, select=True)

    def goRotate(self, *args):
        mc.radioButton(self.rbRelative, edit=True, select=True)

    def goScale(self, *args):
        mc.radioButton(self.rbAbsolute, edit=True, select=True)

    def randValue(self):
        valueMin = float(mc.textField(self.kmin, query=True, text=True))
        valueMax = float(mc.textField(self.kmax, query=True, text=True))
        return random.uniform(valueMin, valueMax)

    def kmRandomizeSpecial(self, *args):

        selectionList = mc.ls(selection=True, type="transform")
        if selectionList:
            if mc.radioButton(self.rbRelative, query=True, select=True):
                stateR = 1
            else:
                stateR = 0

            if mc.radioButton(self.rbMove, query=True, select=True):
                for obj in selectionList:
                    # value = self.randValue(float(mc.textField(self.kmin, query=True, text=True)), float(mc.textField(self.kmax, query=True, text=True)))
                    if mc.checkBox(self.cbAxeX, query=True, value=True):
                        mc.move(self.randValue(), obj, relative=stateR, moveX=1)
                        # mc.xform(obj, relative=stateR, translation=(value,0,0))
                    if mc.checkBox(self.cbAxeY, query=True, value=True):
                        mc.move(self.randValue(), obj, relative=stateR, moveY=1)
                        # mc.xform(obj, relative=stateR, translation=(0,value,0))
                    if mc.checkBox(self.cbAxeZ, query=True, value=True):
                        mc.move(self.randValue(), obj, relative=stateR, moveZ=1)
                        # mc.xform(obj, relative=stateR, translation=(0,0,value))

            if mc.radioButton(self.rbRotate, query=True, select=True):
                for obj in selectionList:
                    if mc.checkBox(self.cbAxeX, query=True, value=True):
                        mc.rotate(self.randValue(), obj, relative=stateR, objectSpace=True, rotateX=1)
                        # mc.xform(obj, relative=stateR, rotation=(self.randValue(),0,0))
                    if mc.checkBox(self.cbAxeY, query=True, value=True):
                        mc.rotate(self.randValue(), obj, relative=stateR, objectSpace=True, rotateY=1)
                        # mc.xform(obj, relative=stateR, rotation=(0,self.randValue(),0))
                    if mc.checkBox(self.cbAxeZ, query=True, value=True):
                        mc.rotate(self.randValue(), obj, relative=stateR, objectSpace=True, rotateZ=1)
                        # mc.xform(obj, relative=stateR, rotation=(0,0,self.randValue()))

            if mc.radioButton(self.rbScale, query=True, select=True):
                for obj in selectionList:
                    if mc.checkBox(self.cbAxeX, query=True, value=True):
                        mc.scale(self.randValue(), obj, relative=stateR, scaleX=1)
                        # mc.xform(obj, relative=stateR, scale=(self.randValue(), 1, 1))
                    if mc.checkBox(self.cbAxeY, query=True, value=True):
                        mc.scale(self.randValue(), obj, relative=stateR, scaleY=1)
                        # mc.xform(obj, relative=stateR, scale=(1, self.randValue(), 1))
                    if mc.checkBox(self.cbAxeZ, query=True, value=True):
                        mc.scale(self.randValue(), obj, relative=stateR, scaleZ=1)
                        # mc.xform(obj, relative=stateR, scale=(1, 1, self.randValue()))

        else:
            print ">> No selection"

    def kmScaleUniformOn(self, *args):
        mc.textField(self.scaleXMin, edit=True, backgroundColor=self.grey)
        mc.textField(self.scaleXMax, edit=True, backgroundColor=self.grey)

        mc.textField(self.scaleYMin, edit=True, enable=False)
        mc.textField(self.scaleYMax, edit=True, enable=False)
        mc.textField(self.scaleZMin, edit=True, enable=False)
        mc.textField(self.scaleZMax, edit=True, enable=False)
        self.stateScaleUniform = 1

    def kmScaleUniformOff(self, *args):
        mc.textField(self.scaleXMin, edit=True, backgroundColor=self.red)
        mc.textField(self.scaleXMax, edit=True, backgroundColor=self.red)

        mc.textField(self.scaleYMin, edit=True, enable=True, backgroundColor=self.green)
        mc.textField(self.scaleYMax, edit=True, enable=True, backgroundColor=self.green)
        mc.textField(self.scaleZMin, edit=True, enable=True, backgroundColor=self.blue)
        mc.textField(self.scaleZMax, edit=True, enable=True, backgroundColor=self.blue)
        self.stateScaleUniform = 0

    def kmRandomizePostion(self, *args):
        selectionList = mc.ls(selection=True, type="transform")
        # print selectionList
        valueXMin = float(mc.textField(self.posXMin, q=True, text=True))
        valueYMin = float(mc.textField(self.posYMin, q=True, text=True))
        valueZMin = float(mc.textField(self.posZMin, q=True, text=True))
        valueXMax = float(mc.textField(self.posXMax, q=True, text=True))
        valueYMax = float(mc.textField(self.posYMax, q=True, text=True))
        valueZMax = float(mc.textField(self.posZMax, q=True, text=True))

        if mc.radioButton(self.rbRelativeTranslate, query=True, select=True):
            stateMove = 1
        else:
            stateMove = 0

        if selectionList:
            for obj in selectionList:
                x = random.uniform(valueXMin, valueXMax)
                y = random.uniform(valueYMin, valueYMax)
                z = random.uniform(valueZMin, valueZMax)
                mc.xform(obj, relative=stateMove, translation=(x, y, z))  # objectSpace=True)
            print ">> Translate Randomized !"
        else:
            print ">> No selection"

    def kmRandomizeRotation(self, *args):
        selectionList = mc.ls(selection=True, type="transform")

        valueXMin = float(mc.textField(self.rotXMin, q=True, text=True))
        valueYMin = float(mc.textField(self.rotYMin, q=True, text=True))
        valueZMin = float(mc.textField(self.rotZMin, q=True, text=True))
        valueXMax = float(mc.textField(self.rotXMax, q=True, text=True))
        valueYMax = float(mc.textField(self.rotYMax, q=True, text=True))
        valueZMax = float(mc.textField(self.rotZMax, q=True, text=True))

        if mc.radioButton(self.rbRelativeRotate, query=True, select=True):
            stateRotate = 1
        else:
            stateRotate = 0

        if selectionList:
            for obj in selectionList:
                x = random.uniform(valueXMin, valueXMax)
                y = random.uniform(valueYMin, valueYMax)
                z = random.uniform(valueZMin, valueZMax)
                mc.xform(obj, relative=stateRotate, rotation=(x, y, z))
            print ">> Rotation Randomized !"
        else:
            print ">> No selection"

    def kmRandomizeScale(self, *args):
        selectionList = mc.ls(selection=True, type="transform")

        valueXMin = float(mc.textField(self.scaleXMin, q=True, text=True))
        valueYMin = float(mc.textField(self.scaleYMin, q=True, text=True))
        valueZMin = float(mc.textField(self.scaleZMin, q=True, text=True))
        valueXMax = float(mc.textField(self.scaleXMax, q=True, text=True))
        valueYMax = float(mc.textField(self.scaleYMax, q=True, text=True))
        valueZMax = float(mc.textField(self.scaleZMax, q=True, text=True))

        if mc.radioButton(self.rbRelativeScale, query=True, select=True):
            stateScale = 1
        else:
            stateScale = 0

        if selectionList:
            if self.stateScaleUniform:
                for obj in selectionList:
                    randValue = random.uniform(valueXMin, valueXMax)
                    x, y, z = (randValue, randValue, randValue)
                    mc.xform(obj, relative=stateScale, scale=(x, y, z))
            else:
                for obj in selectionList:
                    x = random.uniform(valueXMin, valueXMax)
                    y = random.uniform(valueYMin, valueYMax)
                    z = random.uniform(valueZMin, valueZMax)
                    mc.xform(obj, relative=stateScale, scale=(x, y, z))
            print ">> Scale Randomized !"
        else:
            print ">> No selection"


kRandomizer()