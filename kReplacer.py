# kMax replacer
# Maxime Terray : kMax
# 03/04/7/2016
# Version 0.1
# Replacer

import maya.cmds as mc
from functools import partial

class kReplacer():

    def __init__(self):
        self.replacerUI()
        self.actuUIsize()
        self.targetCount()
        
        a = 1
        b = a - .95 / 2
        g = 0.165
        gg = .27
        self.red = (a, b, b)
        self.green = (b, a, b)
        self.blue = (b, b * 1.5, a)
        self.grey = (g, g, g)
        self.grey2 = (gg,gg,gg)
        
    def replacerUI(self):
        windowName = "kReplacer"

        if mc.window(windowName, q=True, exists=True):
            mc.deleteUI(windowName)
    
        self.myWindow = mc.window(windowName, toolbox=True, titleBar=True, minimizeButton=False, maximizeButton=False, sizeable=False)#, resizeToFitChildren=True)
        self.fullColumn = mc.columnLayout()

        selectionList = mc.ls(sl=True)
        selectionLong = len(selectionList)

        mc.frameLayout(label="New object :", labelVisible=1, borderVisible=False, borderStyle="out", marginHeight=2, marginWidth=2)
        
        self.newSelObj = mc.textField(text="New object", enable=True, editable=False, backgroundColor=[.2,.2,.2], height=24, width=94 )
        if selectionList:
            mc.textField(self.newSelObj, text = selectionList[-1], e=True)
        else:
            mc.textField(self.newSelObj, text = "No selection", e=True)
        newBtn = mc.button(label="Select new object", width=210, height=30, command=self.getNewSel)
                
        mc.setParent( '..' )
        
        self.newObjsOptionsLayout = mc.frameLayout(label="News objects options :", collapsable=True, collapse=False, labelVisible=1, borderVisible=False, borderStyle="out", marginHeight=2, marginWidth=2, width=216, collapseCommand=partial(self.actuUIsize, -64), expandCommand=partial(self.actuUIsize, 64))
        mc.radioCollection("Hierarchies options")
        mc.columnLayout(rowSpacing=0)
        self.parentOption = mc.radioButton(label='Parent / On hierarchy', select=True)
        self.worldOption = mc.radioButton(label='World / At scene root')
        mc.rowLayout(numberOfColumns=2)
        self.newGroupOption = mc.radioButton(label='New group :')
        self.nameGroupNewTextField = mc.textField(text="NewObjects", width=122)
        mc.setParent( '..' )
        mc.setParent( '..' )
        mc.setParent( '..' )
        
        self.obj2rplPanel = mc.frameLayout(label="Objects to replace :", labelVisible=1, borderVisible=False, borderStyle="out", marginHeight=2, marginWidth=2)
        mc.paneLayout(height=216, width=210)
        self.objToReplace = mc.textScrollList(numberOfRows=20, allowMultiSelection=True)
        if selectionList:
            for item in selectionList[0:-1]:
                mc.textScrollList(self.objToReplace, append=item, e=True)
                mc.frameLayout(self.obj2rplPanel, label="Objects to replace : " + str(self.targetCount()), e=True)
        else:
            print ">> No selection"
        mc.setParent( '..' )
        mc.rowLayout(numberOfColumns=5)
        mc.button(label="Target", width=112, height=30, command=self.setSelTarget)
        mc.button(label="+", width=30, height=30, command=self.addSelTarget)
        mc.button(label="-", width=30, height=30, command=self.delSelTarget)
        #mc.button(label="Select", width=55, height=30, command=self.selTarget)
        mc.button(label="R", width=30, height=30, command=self.rstSelTarget)
        mc.setParent( '..' )
        mc.setParent( '..' )

        self.targetsOptionsLayout = mc.frameLayout(label="Targets options :", collapsable=True, collapse=False, labelVisible=1, borderVisible=False, borderStyle="out", marginHeight=2, marginWidth=2, width=216, collapseCommand=partial(self.actuUIsize, -66), expandCommand=partial(self.actuUIsize, 66))
        mc.rowLayout(numberOfColumns=3, columnWidth=[(1, 86), (2, 60), (3, 60)])
        mc.radioCollection("Targets options")
        mc.radioButton(label='Dont touch !', select=True)
        self.hideOption = mc.radioButton(label='Hide')
        self.deleteOption = mc.radioButton(label='Delete', onCommand=self.deleteTargetOn, offCommand=self.deleteTargetOff)
        mc.setParent( '..' )
        mc.rowLayout(numberOfColumns=2)
        self.newGroupTargetOption = mc.radioButton(label='New group :')
        self.nameGroupTargetTextField = mc.textField(text="Targets", width=122)
        mc.setParent( '..' )
        mc.setParent( '..' )
        mc.setParent( '..' )
        
        self.offsetsLayout = mc.frameLayout(label="Offsets :", collapsable=True, collapse=False, labelVisible=1, borderVisible=False, borderStyle="out", marginHeight=2, marginWidth=2, width=216, collapseCommand=partial(self.actuUIsize, -52), expandCommand=partial(self.actuUIsize, 52))
        mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 56), (2, 51), (3, 51), (4, 51)], columnAlign=(1, "right"))
        mc.text("Translate :")
        self.offTx = mc.floatField(precision=3)
        self.offTy = mc.floatField(precision=3)
        self.offTz = mc.floatField(precision=3)
        mc.text("Rotate :")
        self.offRx = mc.floatField(precision=3)
        self.offRy = mc.floatField(precision=3)
        self.offRz = mc.floatField(precision=3)
        mc.rowLayout(numberOfColumns=2)
        mc.button(label="R", width=18, height=18, command=self.rstOff)        
        mc.text("Scale :")
        mc.setParent( '..' )
        self.offSx = mc.floatField(value=1, precision=3)
        self.offSy = mc.floatField(value=1, precision=3)
        self.offSz = mc.floatField(value=1, precision=3)
        mc.setParent( '..' )
        mc.setParent( '..' )        
        
        mc.frameLayout(label="Replace", labelVisible=0, borderVisible=False, borderStyle="out", marginHeight=1, marginWidth=1)
        mc.columnLayout()
        replaceBtn = mc.button(label="Replace", width=210, height=30, command=self.kReplace)#, backgroundColor=[ .404, .553, .698])
        self.selTargets = mc.button(label="Select Targets", width=210, height=20, enable=0, command=self.selTarget)
        self.selNewObjects = mc.button(label="Select New Objects", width=210, height=20, enable=0, command=self.selNew)
        mc.setParent( '..' )
        mc.setParent( '..' )
        '''
        self.fictif = mc.frameLayout(label="fictif :")
        mc.setParent( '..' )'''
        
        mc.setParent( '..' )

        mc.showWindow(self.myWindow)
        print "window :" + str(mc.window(self.myWindow, height=True, q=True))
        print "new :"  + str(mc.frameLayout(self.newObjsOptionsLayout, height=True, q=True))
        print "offset :"  + str(mc.frameLayout(self.offsetsLayout, height=True, q=True))
        print "targets :"  + str(mc.frameLayout(self.targetsOptionsLayout, height=True, q=True))
       #print "fictif :" + str(mc.frameLayout(self.fictif, height=True, q=True))
        
    def actuUIsizeOld(self):
        #heightFrame = mc.columnLayout(self.fullColumn, height=True, q=True)
        heightWindow = mc.window(self.myWindow, height=True, q=True)
        childList = mc.columnLayout(self.fullColumn, childArray=True, q=True)
        #mc.frameLayout(self.fullFrame, height=True, q=True)
        self.size=0
        print "\n >> Sizes des elements de la window :"
        for item in childList:
            self.nameItem = mc.frameLayout(item, label=True, q=True)
            self.sizeItem = mc.frameLayout(item, height=True, q=True)
            self.size += self.sizeItem
            #self.size += eval("mc.frameLayout(item, height=True, q=True)")
            #mc.frameLayout(item, height=self.sizeItem, edit=True)
            print self.nameItem, mc.frameLayout(item, height=True, q=True)
        #mc.columnLayout(self.fullColumn, height=self.size, edit=True)
        #mc.frameLayout(self.fullFrame, height=self.size, edit=True)
        mc.window(self.myWindow, height=self.size, edit=True)
        
        print "\nWindow size       : ", mc.window(self.myWindow, height=heightWindow, q=True)
        #print "FullFrame size    : ", mc.frameLayout(self.fullFrame, height=True, q=True)
        #print "ColumnFull size   : ", mc.columnLayout(self.fullColumn, height=True, q=True)
        print "FrameLayouts size : ", self.size
                
    def actuUIsize(self, sizeH=0, *args):
        '''stateTargetsOptions = mc.frameLayout(self.targetsOptionsLayout, collapse=True, q=True)
        stateOffsets = mc.frameLayout(self.offsetsLayout, collapse=True, q=True)
        stateNewObjOptions = mc.frameLayout(self.newObjsOptionsLayout, collapse=True, q=True)'''
        
        windowsHeight = mc.window(self.myWindow, height=True, q=True) + sizeH
        mc.window(self.myWindow, height=windowsHeight, width=217, edit=True)

        
        """if not stateOptions and not stateOffsets:
            mc.window(self.myWindow, height=582, edit=True)
        if  not stateOptions and stateOffsets:
            mc.window(self.myWindow, height=514, edit=True)
        if stateOptions and not stateOffsets:
            mc.window(self.myWindow, height=516, edit=True)
        if stateOptions and stateOffsets:
            mc.window(self.myWindow, height=448, edit=True)"""
    
    def deleteTargetOn(self, *args):
        mc.radioButton(self.deleteOption, backgroundColor=[1,1-.95 / 2,1-.95 / 2], edit=True)
    
    def deleteTargetOff(self, *args):
        mc.radioButton(self.deleteOption, backgroundColor=[.27, .27, .27], edit=True)
        #mc.radioButton(self.deleteOption, enableBackground=0, edit=True)

    def getNewSel(self, *args):
        selectionNew = mc.ls(sl=True)
        #print selectionNew
        if selectionNew:
            mc.textField(self.newSelObj, text = str(selectionNew[0]), e=True)
        else:
            print ">> No selection"
        
        mc.button(self.selTargets, enable=False, edit=True)
        mc.button(self.selNewObjects, enable=False, edit=True)

    def importNew(self, *args):
        singleFilter = "All Files (*.*)"
        self.myfile = mc.fileDialog2(fileFilter=singleFilter, dialogStyle=2, fileMode=1)
        test = str(self.myfile)
        print ">> " + test
        name = test.split("/")[-1]
        mc.textField(self.newImportObj, text=name[0:-2], e=True)
        mc.file(self.myfile, reference=True)
    
    def targetCount(self):
        if mc.textScrollList(self.objToReplace, numberOfItems=True, q=True) == 0:
            mc.frameLayout(self.obj2rplPanel, label="Objects to replace : 0", e=True)
        else:
            numTarget = mc.textScrollList(self.objToReplace, numberOfItems=True, q=True)
            mc.frameLayout(self.obj2rplPanel, label="Objects to replace : " + str(numTarget), e=True)

    def addSelTarget(self, *args):
        selectionList = mc.ls(sl=True)
        targetList = mc.textScrollList(self.objToReplace, allItems=True, q=True)
        if selectionList:
            for item in selectionList:
                if targetList:
                    if item not in targetList:
                        mc.textScrollList(self.objToReplace, append=item, e=True)
                else:
                    mc.textScrollList(self.objToReplace, append=item, e=True)
        else:
            print ">> No selection"
        self.targetCount()
        
        mc.button(self.selTargets, enable=False, edit=True)
        mc.button(self.selNewObjects, enable=False, edit=True)

    def delSelTarget(self, *args):
        targetList = mc.textScrollList(self.objToReplace, selectItem=True, q=True)
        if targetList:
            mc.textScrollList(self.objToReplace, removeItem=targetList, e=True)
        else:
            print ">> No selection"
        self.targetCount()

    def rstSelTarget(self, *args):     
        mc.textScrollList(self.objToReplace, removeAll=True, e=True)
        self.targetCount()
        
        mc.button(self.selTargets, enable=False, edit=True)
        mc.button(self.selNewObjects, enable=False, edit=True)

    def setSelTarget(self, *args):
        selectionList = mc.ls(sl=True)
        #selectionLong = len(selectionList)
        #print selectionList
        mc.textScrollList(self.objToReplace, removeAll=True, e=True)
        if selectionList:
            for item in selectionList:
                mc.textScrollList(self.objToReplace, append=item, e=True)
            self.targetCount()
        else:
            print ">> No selection"
        #self.targetCount()
        
        mc.button(self.selTargets, enable=False, edit=True)
        mc.button(self.selNewObjects, enable=False, edit=True)
        
    def rstOff(self, *args):
        mc.floatField(self.offTx, value=0, e=True)
        mc.floatField(self.offTy, value=0, e=True)
        mc.floatField(self.offTz, value=0, e=True)
        
        mc.floatField(self.offRx, value=0, e=True)
        mc.floatField(self.offRy, value=0, e=True)
        mc.floatField(self.offRz, value=0, e=True)
        
        mc.floatField(self.offSx, value=1, e=True)
        mc.floatField(self.offSy, value=1, e=True)
        mc.floatField(self.offSz, value=1, e=True)
        
    def getOffsets(self, *args):
        self.newTranslationX = float(self.newTranslation[0]) + mc.floatField(self.offTx, value=True, q=True)
        self.newTranslationY = float(self.newTranslation[1]) + mc.floatField(self.offTy, value=True, q=True)
        self.newTranslationZ = float(self.newTranslation[2]) + mc.floatField(self.offTz, value=True, q=True)
        self.newRotationX = float(self.newRotation[0]) + mc.floatField(self.offRx, value=True, q=True)
        self.newRotationY = float(self.newRotation[1]) + mc.floatField(self.offRy, value=True, q=True)
        self.newRotationZ = float(self.newRotation[2]) + mc.floatField(self.offRz, value=True, q=True)
        self.newScaleX = float(self.newScale[0])  * mc.floatField(self.offSx, value=True, q=True)
        self.newScaleY = float(self.newScale[1])  * mc.floatField(self.offSy, value=True, q=True)
        self.newScaleZ = float(self.newScale[2])  * mc.floatField(self.offSz, value=True, q=True)
        
        self.newTranslation = (self.newTranslationX, self.newTranslationY, self.newTranslationZ)
        self.newRotation = (self.newRotationX, self.newRotationY, self.newRotationZ)
        self.newScale = (self.newScaleX, self.newScaleY, self.newScaleZ)
                
    def kReplace(self, *args):
        targetList = mc.textScrollList(self.objToReplace, allItems=True, q=True)
        nameObjSource = mc.textField(self.newSelObj, text=True, q=True)
        objSource = mc.ls(nameObjSource)
        self.newObjList = []
        
        for self.target in targetList:
            self.getNewCoord()
            
            if not mc.frameLayout(self.offsetsLayout, collapse=True, q=True):
                self.getOffsets()        
 
            #self.newObj = mc.duplicate(objSource, renameChildren=True, upstreamNodes=True, returnRootsOnly=True)            
            if mc.radioButton(self.parentOption, query=True, select=True):
                self.newObj = mc.duplicate(objSource, renameChildren=True, upstreamNodes=True, returnRootsOnly=True)
                #self.newObj = mc.instance(objSource) #, renameChildren=True, upstreamNodes=True, returnRootsOnly=True)
                parent = mc.listRelatives(self.target, parent=True)
                mc.parent(self.newObj, parent)
            
            if mc.radioButton(self.worldOption, query=True, select=True):
                self.newObj = mc.duplicate(objSource, renameChildren=True, upstreamNodes=True, returnRootsOnly=True)
                
            if mc.radioButton(self.newGroupOption, query=True, select=True):
                self.newObj = mc.duplicate(objSource, renameChildren=True, upstreamNodes=True, returnRootsOnly=True)
                nameGroup = mc.textField(self.nameGroupNewTextField, text=True, q=True)
                if not mc.objExists(nameGroup):
                    newGroup = mc.group(name=nameGroup, empty=True)
                mc.parent(self.newObj, nameGroup)
                
            if mc.radioButton(self.hideOption, query=True, select=True):
                mc.setAttr(self.target + ".visibility", 0)
                
            if mc.radioButton(self.deleteOption, query=True, select=True):
                mc.delete(self.target)
            
            if mc.radioButton(self.newGroupTargetOption, query=True, select=True):
                nameGroupTarget = mc.textField(self.nameGroupTargetTextField, text=True, q=True)
                if not mc.objExists(nameGroupTarget):
                    newGroup = mc.group(name=nameGroupTarget, empty=True)
                mc.parent(self.target, nameGroupTarget)
            
            self.newObjList += self.newObj
            self.setNewCoord()
            
        mc.button(self.selTargets, enable=True, edit=True)
        mc.button(self.selNewObjects, enable=True, edit=True)
        self.selNew()
        #mc.select(self.newObjList)
    
    def getNewCoord(self, *args):
        self.newTranslation = mc.xform(self.target, q=True, translation=True, worldSpace=True)
        self.newRotation = mc.xform(self.target, q=True, rotation=True, worldSpace=True)
        self.newScale = mc.xform(self.target, q=True, relative=True, scale=True)
    
    def setNewCoord(self, *args):
        mc.xform(self.newObj, p=True, translation=self.newTranslation, worldSpace=True)
        mc.xform(self.newObj, p=True, rotation=self.newRotation, worldSpace=True)
        mc.xform(self.newObj, p=True, scale=self.newScale)

    def selTarget(self, *args):
        targetList = mc.textScrollList(self.objToReplace, allItems=True, q=True)
        if targetList :
            mc.select(targetList)    

    def selNew(self,*args):
        mc.select(self.newObjList)

kReplacer()