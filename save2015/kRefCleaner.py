# kMaxRefCleaner
# Maxime Terray : kMax
# 01/11/2016
# Version 0.1
# Cleaner de References Edits

'''
# Remove all edits
refList = mc.ls("*RN")
for ref in refList:
    nodes = cmds.referenceQuery( ref, editNodes=True )
    attr_types = cmds.referenceQuery( ref, editAttrs=True )
    for node in nodes:
        for attr_type in attr_types:
            for edit_command in ['addAttr', 'connectAttr', 'deleteAttr', 'disconnectAttr', 'parent', 'setAttr', 'lock', 'unlock']:
                cmds.referenceEdit( node+'.'+attr_type, failedEdits=True, successfulEdits=True, removeEdits=True, editCommand=edit_command)
'''

import maya.cmds as mc
import pymel.core as pm
from functools import partial

class kRefCleaner():

    def __init__(self):
        self.refCleanerUI()
        #self.actuUIsize()
              
        a = 1
        b = a - .95 / 2
        g = 0.165
        gg = .27
        self.red = (a, b, b)
        self.green = (b, a, b)
        self.blue = (b, b * 1.5, a)
        self.grey = (g, g, g)
        self.grey2 = (gg,gg,gg)
 
    def refCleanerUI(self):
        windowName = "kRefCleaner"
        
        selectionList = mc.ls(sl=True)
        selectionLong = len(selectionList)
        
        refList = pm.listReferences()
        self.refNumber = len(refList)
        for ref in refList:
            print mc.referenceQuery(ref, referenceNode=True )
        
        if mc.window(windowName, q=True, exists=True):
            mc.deleteUI(windowName)
    
        self.myWindow = mc.window(windowName, toolbox=True, titleBar=True, minimizeButton=False, maximizeButton=False, sizeable=False)#, resizeToFitChildren=True)
        mc.window(self.myWindow, width=210, height=500, edit=True)   
        
        self.fullColumn = mc.columnLayout()
        #mc.rowColumnLayout(numberOfColumns=2)#, columnWidth3=(200, 600, 200))
        
        #column 1
        mc.frameLayout(label="References :", collapsable=False, collapse=False, labelVisible=1, borderVisible=False, borderStyle="out", marginHeight=2, marginWidth=2)
        #, width=500, collapseCommand=partial(self.actuUIsize, -64), expandCommand=partial(self.actuUIsize, 64)     
        mc.paneLayout(width=210, height=210)
        self.refListScroll =  mc.textScrollList(numberOfRows=20, allowMultiSelection=True)
        if refList:
            for ref in refList:
                mc.textScrollList(self.refListScroll, append=mc.referenceQuery(ref, referenceNode=True ), e=True)
            mc.textScrollList(self.refListScroll, selectIndexedItem=1, e=True)
        else:
            print ">> No Ref in the scene"
        mc.setParent( '..' )
        mc.rowLayout( numberOfColumns=3)
        mc.button(label="All", width=40, height=20, command=self.selAllRef)
        mc.button(label="None", width=40, height=20, command=self.selNoneRef)        
        mc.button(label="Open", width=40, height=20)#, command=self.selNoneRef)
        mc.setParent( '..' )
        mc.setParent( '..' )
        
        '''#column 2        
        mc.textScrollList(self.reListScroll, selectItem=1, q=True)
        mc.frameLayout(label="List Edits :", collapsable=False, collapse=False, labelVisible=1, borderVisible=False)
        
        self.editListScroll =  mc.textScrollList( width=400)  
        mc.setParent( '..' ) 
        '''
        
        #column 3
        # 'addAttr', 'connectAttr', 'deleteAttr', 'disconnectAttr', 'parent', 'setAttr', 'lock', 'unlock'     
        mc.frameLayout(label="What do you want to clean :", collapsable=False, collapse=False, labelVisible=1, borderVisible=False, borderStyle="out", marginHeight=2, marginWidth=2)
        mc.columnLayout( adjustableColumn=True )        
        self.successfulEditsBTN = mc.checkBox( label='successfulEdits' , value=0)
        self.failedEditsBTN = mc.checkBox( label='failedEdits', value=1)
        mc.separator(style="in")
        self.setAttrBTN = mc.checkBox( label='setAttr', value=1)
        self.addAttrBTN = mc.checkBox( label='addAttr', value=1)
        self.connectAttrBTN = mc.checkBox( label='connectAttr', value=0)
        self.deleteAttrBTN = mc.checkBox( label='deleteAttr', value=0)
        self.disconnectAttrBTN = mc.checkBox( label='disconnectAttr', value=0)
        mc.separator(style="in")        
        self.parentBTN = mc.checkBox( label='parent', value=0)
        mc.separator(style="in")     
        self.lockBTN = mc.checkBox( label='lock', value=0)
        self.unlockBTN = mc.checkBox( label='unlock', value=0)
        
        mc.rowLayout( numberOfColumns=3)
        mc.button(label="All", width=40, height=20, command=self.selAllEdit)
        mc.button(label="None", width=40, height=20, command=self.selNoneEdit)
        mc.button(label="Default", width=40, height=20, command=self.selDefaultEdit)
        mc.setParent( '..' )        
        
        cleanBtn = mc.button(label="Clean Ref Edit", width=210, height=30, command=self.kRefClean)
        mc.setParent( '..' )
        
        mc.setParent( '..' )
        
        mc.showWindow(self.myWindow)
                
    '''def actuUIsize(self, sizeH=0, *args):
        windowsHeight = mc.window(self.myWindow, height=True, q=True) + sizeH
        mc.window(self.myWindow, height=windowsHeight, width=217, edit=True)'''
    
    def selAllRef(self, * args):
        print self.refNumber
        mc.textScrollList(self.refListScroll, deselectAll=1, e=True)
        for a in range(1, self.refNumber+1):
            mc.textScrollList(self.refListScroll, selectIndexedItem=a, e=True)
     
    def selNoneRef(self, * args):
        mc.textScrollList(self.refListScroll, deselectAll=1, e=True)
    
    def selAllEdit(self, *args):    
        mc.checkBox(self.successfulEditsBTN, value=1, e=1)
        mc.checkBox(self.failedEditsBTN, value=1, e=1)
        mc.checkBox(self.setAttrBTN, value=1, e=1)
        mc.checkBox(self.addAttrBTN, value=1, e=1)
        mc.checkBox(self.connectAttrBTN, value=1, e=1)
        mc.checkBox(self.deleteAttrBTN, value=1, e=1)
        mc.checkBox(self.disconnectAttrBTN, value=1, e=1)
        mc.checkBox(self.parentBTN, value=1, e=1)
        mc.checkBox(self.lockBTN, value=1, e=1)
        mc.checkBox(self.unlockBTN, value=1, e=1)
   
    def selNoneEdit(self, *args):
        mc.checkBox(self.successfulEditsBTN, value=0, e=1)
        mc.checkBox(self.failedEditsBTN, value=0, e=1)
        mc.checkBox(self.setAttrBTN, value=0, e=1)
        mc.checkBox(self.addAttrBTN, value=0, e=1)
        mc.checkBox(self.connectAttrBTN, value=0, e=1)
        mc.checkBox(self.deleteAttrBTN, value=0, e=1)
        mc.checkBox(self.disconnectAttrBTN, value=0, e=1)
        mc.checkBox(self.parentBTN, value=0, e=1)
        mc.checkBox(self.lockBTN, value=0, e=1)
        mc.checkBox(self.unlockBTN, value=0, e=1)
        
    def selDefaultEdit(self, *args):
        mc.checkBox(self.successfulEditsBTN, value=0, e=1)
        mc.checkBox(self.failedEditsBTN, value=1, e=1)
        mc.checkBox(self.setAttrBTN, value=1, e=1)
        mc.checkBox(self.addAttrBTN, value=1, e=1)
        mc.checkBox(self.connectAttrBTN, value=0, e=1)
        mc.checkBox(self.deleteAttrBTN, value=0, e=1)
        mc.checkBox(self.disconnectAttrBTN, value=0, e=1)
        mc.checkBox(self.parentBTN, value=0, e=1)
        mc.checkBox(self.lockBTN, value=0, e=1)
        mc.checkBox(self.unlockBTN, value=0, e=1)
    
    def kRefClean(self, *args):
        editCommandList = []
        if mc.checkBox(self.setAttrBTN, value=1, q=1):
            editCommandList.append("setAttr")
        if mc.checkBox(self.addAttrBTN, value=1, q=1):
            editCommandList.append("addAttr")
        if mc.checkBox(self.connectAttrBTN, value=1, q=1):
           editCommandList.append("connectAttr")
        if mc.checkBox(self.deleteAttrBTN, value=1, q=1):
            editCommandList.append("deleteAttr")
        if mc.checkBox(self.disconnectAttrBTN, value=1, q=1):
            editCommandList.append("disconnectAttr")            
        if mc.checkBox(self.parentBTN, value=1, q=1):
            editCommandList.append("parent")
        if mc.checkBox(self.lockBTN, value=1, q=1):
            editCommandList.append("lock")    
        if mc.checkBox(self.unlockBTN, value=1, q=1):
            editCommandList.append("unlock")             
        print editCommandList
        
        refListSelect = mc.textScrollList(self.refListScroll, selectItem=1, q=True)
        print refListSelect       
        
        for ref in refListSelect:
            nodes = mc.referenceQuery( ref, editNodes=True )
            attrTypes = mc.referenceQuery( ref, editAttrs=True )
            for node in nodes:
                for attrType in attrTypes:
                    for commandd in editCommandList:
                        mc.referenceEdit( node+'.'+attrType,  
                                                failedEdits=mc.checkBox(self.failedEditsBTN, value=1, q=1),
                                                successfulEdits=mc.checkBox(self.successfulEditsBTN, value=1, q=1),
                                                removeEdits=True, editCommand=commandd)
        
        print ">> Ref Edit Clean !!"           
        
        '''
        for ref in refList:
        nodes = cmds.referenceQuery( ref, editNodes=True )
        attr_types = cmds.referenceQuery( ref, editAttrs=True )
        for node in nodes:
            for attr_type in attr_types:
                for edit_command in ['addAttr', 'connectAttr', 'deleteAttr', 'disconnectAttr', 'parent', 'setAttr', 'lock', 'unlock']:
                    cmds.referenceEdit( node+'.'+attr_type, failedEdits=True, successfulEdits=True, removeEdits=True, editCommand=edit_command)'''

kRefCleaner()