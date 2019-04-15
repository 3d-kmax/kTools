import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import os

iconSize = 32
path = "E:/kTools/icons/"


class kMod():
    def __init__(self):
        print ">> __init__"
        self.workspaceControlName = "superWorkspace"
        if mc.workspaceControl(self.workspaceControlName, exists=True):
            mc.deleteUI(self.workspaceControlName, control=True)

    def createUI(self):
        print ">> createUI"
        allButtons = [("bt_kMaxToolBar", "kMaxTool32.png", "kMaxTool32b.png", "Launch kMaxTools"),
                      ("bt_kMod", "kMaxMod32.png", "kMaxMod32.png", "Launch kMod Left bar")]
        mc.rowColumnLayout(numberOfRows=1, rowHeight=(1, iconSize))
        for btnName, btnImg, btnHighImg, btnAnno in allButtons:
            mc.iconTextButton(style='iconOnly', image1=path + btnImg, highlightImage=path + btnHighImg,
                              annotation=btnAnno, width=iconSize)

    def build(self):
        print ">> build"
        mc.workspaceControl(self.workspaceControlName, uiScript="kMod().createUI()", retain=False, floating=True)
        mc.workspaceControl(self.workspaceControlName, edit=True, initialHeight=iconSize,
                            dockToControl=("Shelf", "top"))


kMod().build()
