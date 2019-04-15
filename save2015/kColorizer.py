# kMax colorShaderPicker
# Maxime Terray : kMax
# 21/04/7/2015
# Version 0.1
# Color Shader Picker pour Maya 2014

import maya.cmds as mc
from functools import partial
import pymel.core as pm

import os

class kColorizer():

    def __init__(self):
        self.initPath()
        self.pickColor = 0
        self.colorizerUI()
        self.actuUIsize()
        #self.shaderType = self.initShaderType()

    def colorizerUI(self):

        '''
        path_list = os.path.realpath(__file__).split('/')[:-1]
        path_list.extend(['icons'])
        target = ""
        for item in path_list:
            target += item + '/'
            '''

        allButtons = [("blueShader32.png", 0.63, 0.66, 0.70, "blue"),
                      ("greenShader32.png", 0.63, 0.70, 0.63, "green"),
                      ("yellowShader32.png", 0.70, 0.70, 0.63, "yellow"),
                      ("orangeShader32.png", 0.70, 0.64, 0.63, "orange"),
                      ("redShader32.png", 0.70, 0.63, 0.63, "red"),
                      ("purpleShader32.png", 0.67, 0.63, 0.70, "purple"),
                      ("brownShader32.png", 0.70, 0.66, 0.63, "brown"),
                      ("lightGrayShader32.png", 0.8, 0.8, 0.8, "white"),
                      ("blackShader32.png", 0.25, 0.25, 0.25, "black")]

        self.nbBtn = len(allButtons)
        self.widthWin = self.nbBtn * 38 + 46
        
        windowName = "kColorizer"

        if mc.window(windowName, q=True, exists=True):
            mc.deleteUI(windowName)

        self.myWindow = mc.window(windowName, toolbox=True, titleBar=True, minimizeButton=False, maximizeButton=False, sizeable=False)#, resizeToFitChildren=True,
        mc.window(self.myWindow, width=self.widthWin -2, height=60, edit=True)
       
        mc.columnLayout()
        
        mc.rowLayout(numberOfColumns = self.nbBtn+2)
        #self.shaderType = self.initShaderType()
        for btn in allButtons:
            #print ">> color : " + str(btn[4])
            #annotationBtn = self.setBtnAnnotation(str(btn[4]))
            #print ">> annotation : " + annotationBtn
            self.btnName = mc.iconTextButton(image=self.target + btn[0], command=partial(self.applyShaderColor, R=btn[1], G=btn[2], B=btn[3], name=btn[4]))
        mc.iconTextButton(image=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png", width=9, enable=0)
        mc.iconTextButton(image=self.target + "pipette32.png", annotation="Pick Color to Apply on Selection", command=self.kPipette)
        mc.setParent( '..' )
        
        self.optionsLayout = mc.frameLayout(label="Options :", labelVisible=False, borderVisible=False, collapsable=True, collapse=False, marginHeight=2, marginWidth=2, width=self.widthWin, collapseCommand=self.actuUIsize, expandCommand=self.actuUIsize)#borderStyle="out",
        
        mc.rowLayout(numberOfColumns=3)
        
        mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 90), (2, 79), (3, 79), (4, 79)], columnAlign=[(1, "right"),(2, "right"),(3, "right"),(4, "right")])
        self.radioC = mc.radioCollection()
        self.rdrManBtn =  mc.radioButton(label='RenderMan', annotation="renderMan", onCommand=self.initShaderType, enable=True, select=False)
        self.lambertBtn = mc.radioButton(label='Lambert', annotation="lambert", onCommand=self.initShaderType, select=True)
        self.phongBtn = mc.radioButton(label='Phong', annotation="phong", onCommand=self.initShaderType)
        self.blinnBtn = mc.radioButton(label='Blinn', annotation="blinn", onCommand=self.initShaderType)
        mc.text(label="Prefix : ")
        self.shPrefix = mc.textField(text="sh_", enable=True, editable=True, height=20, width=50 )
        mc.text(label="Suffix : ")
        self.shSuffix = mc.textField(text="", enable=True, editable=True, height=20, width=50 )
        mc.setParent( '..' )
        
        mc.iconTextButton(image=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png", width=9, enable=0)
        self.selUnknowNodesBtn = mc.iconTextButton(style='iconOnly', image=self.target + "delUnusedNode32.png", command=self.delUnknowNodes)
        mc.setParent( '..' )
        
        mc.setParent( '..' )                 
        
        mc.setParent( '..' )

        mc.showWindow(self.myWindow)

    def initPath(self):
        # self.target = "/homes/mte/maya/2016/scripts/kTools/icons/"
        path_brut = os.path.realpath(__file__)
        print ">> path brut : ", path_brut
        path_norm = os.path.normpath(path_brut)  # os.path.normcase()
        print ">> path norm : ", path_norm
        path_clean = path_norm.replace("\\", "/")
        print ">> path clean : ", path_clean
        path_list = path_clean.split('/')[:-1]
        print ">> path split : ", path_list
        path_list.extend(['icons'])
        self.target = ''
        for item in path_list:
            self.target += item + '/'
        print ">> :", self.target

    def setBtnAnnotation(self, btnColor="Color"):
        shaderType = self.initShaderType()
        shaderAnnotation = "Apply " + btnColor + " " + shaderType + " color"
        return shaderAnnotation
        
    def actuUIsize(self):
        stateOptions = mc.frameLayout( self.optionsLayout, collapse=True, q=True)
        mc.window(self.myWindow, width=self.widthWin, edit=True)
        if not stateOptions:
            mc.window(self.myWindow, height=84, edit=True) #108
        else:
            mc.window(self.myWindow, height=38, edit=True)    #60
    
    def initShaderType(self, *args):
        if mc.radioButton(self.lambertBtn, select=True, q=True):
            self.shaderType = "lambert"            
        if mc.radioButton(self.phongBtn, select=True, q=True):
            self.shaderType = "phong"
        if mc.radioButton(self.blinnBtn, select=True, q=True):
            self.shaderType = "blinn"
        if mc.radioButton(self.rdrManBtn, select=True, q=True):
            self.shaderType = "RMSGPSurface"
        
        print ">> Shader selection :", self.shaderType
        return self.shaderType
    
    def applyShaderColor(self, name, R=0.5, G=0.5, B=0.5, *args):  
        shPrefix = mc.textField(self.shPrefix, text=True, q=True)
        shSuffix= mc.textField(self.shSuffix, text=True, q=True)
        shType = self.initShaderType()
        print ">> " + shPrefix + shType + shSuffix
        shaderName = shPrefix + name + "_" + shType + shSuffix
        shadingGroupName = shaderName + 'SG'
        selectionList = mc.ls(selection=True, type="transform")

        if selectionList:
            if not mc.objExists(shaderName):
                mc.shadingNode(self.shaderType, asShader=True, name=shaderName)
                if self.shaderType == "RMSGPSurface":
                    mc.setAttr(shaderName + ".surfaceColor", R, G, B, type="double3")
                    mc.setAttr(shaderName + ".specularGain", 0)
                    mc.setAttr(shaderName + ".specularFeatures", 0)
                else:
                    mc.setAttr(shaderName + ".color", R, G, B, type="double3")
                mc.sets(renderable=True, empty=1, noSurfaceShader=True, name=shadingGroupName)
                mc.defaultNavigation(source=shaderName, destination=shadingGroupName, connectToExisting=1)
            for obj in selectionList:
                mc.sets(obj, forceElement=shadingGroupName, e=1)
            mc.select(selectionList)
        else:
            print ">> No selection"

    def kPipette(self):
        shPrefix = mc.textField(self.shPrefix, text=True, q=True)
        shSuffix= mc.textField(self.shSuffix, text=True, q=True)
        shType = self.initShaderType()
        self.pickColor += 1
        colorName = shPrefix + "Picker" + shType + str(self.pickColor) + shSuffix
        selectionList = mc.ls(selection=True, type="transform")
        if selectionList:
            mc.colorEditor(mini=False)
            kColor = mc.colorEditor(query=True, rgb=True)
            self.applyShaderColor(name=colorName, R=kColor[0], G=kColor[1], B=kColor[2])
        else:
            print ">> No selection"
    
    def delUnknowNodes(self, *args):
        pm.mel.hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")
        
kColorizer()

'''
nomShader="Mon_Shader"
nomShadingGroup=nomShader+'SG'
# Cree un shader
cmds.shadingNode("lambert",asShader=True, name=nomShader)
# Cree un shading group
cmds.sets(renderable=True,empty=1,noSurfaceShader=True,name=nomShadingGroup)
# Connecte le shading au shading group
cmds.defaultNavigation(source=nomShader,destination=nomShadingGroup,connectToExisting=1)
# Remplace le shader
cmds.sets(objet,forceElement=nomShadingGroup,edit=1)
'''
