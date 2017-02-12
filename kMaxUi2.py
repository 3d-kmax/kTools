import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import os

path_list = os.path.realpath(__file__).split('\\')[:-2]
path_list.extend(['kTools'])
target = ''
for item in path_list:
    target += item + '/'

widthWin = 64+200+8
heightWin = 1000
windowName = "kMaxUi2"

if mc.window(windowName, q=True, exists=True):
    mc.deleteUI(windowName)

kMaxUi2Window = mc.window(windowName, height=heightWin, width=widthWin, toolbox=True, titleBar=True, minimizeButton=False, maximizeButton=False, sizeable=False)#, resizeToFitChildren=True)
mc.window(windowName, width=widthWin, height=heightWin, edit=True)
mc.scrollLayout( 'scrollLayout', childResizable=True ) # to delete
mc.columnLayout( adjustableColumn=True, width=widthWin-4)

# Common Selection Options
mc.frameLayout( label='Common Selection Options', collapse=False, collapsable=True)
mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 66), (2, 198)], columnAlign=[(1, "right"),(2, "right")])
mc.text(label="Transform  : ", font="tinyBoldLabelFont")
mc.textField()
mc.text(label="Shape  : ", font="tinyBoldLabelFont")
mc.textField()
mc.text(label="History  : ", font="tinyBoldLabelFont")
mc.textField()
mc.text(label="Sel. by name  : ", font="tinyBoldLabelFont")
mc.textField()
#mc.setParent( '..' )
mc.columnLayout(columnAttach=("both", 1), adjustableColumn=False, columnWidth=66)
mc.iconTextRadioCollection("Selection mode")
mc.iconTextRadioButton(label='Marquee', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", select=True, height=20)
mc.iconTextRadioButton(label='Drag', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='Tweak', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.setParent( '..' )
mc.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 66), (2, 66), (3, 66)])
mc.iconTextRadioCollection("Selection Type")
mc.iconTextRadioButton(label='Object', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='Multi', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='UV', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='Vertex', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='Edge', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='Face', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20) 
mc.iconTextCheckBox(label='Cam Based', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.setParent( '..' )
mc.setParent( '..' )
mc.setParent( '..' )

# Display
mc.frameLayout( label='Display', collapse=False, collapsable=True)
mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 66), (2, 66), (3, 66), (4,66)])
mc.iconTextCheckBox(label='HUD', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='GRID', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='BGColor', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='HIST', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='Near', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='Far', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, enable=False, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Border', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='XRAY', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='DF MT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='DF LT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Wire', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='HLT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='BFC', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='2SL', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, enable=False, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='ISO', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='ACTU', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='AUTO', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20, marginWidth=0, marginHeight=0)
mc.rowLayout(numberOfColumns=2, columnWidth2=[33, 33], columnAlign2=["center","center"], columnAttach2=["both", "both"], height=20)
mc.iconTextButton(label='+', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='-', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20, marginWidth=0, marginHeight=0)
mc.setParent( '..' )
mc.setParent( '..' )
mc.setParent( '..' )

# Transform
mc.frameLayout( label='Transform', collapse=False, collapsable=True)
mc.columnLayout()
#192 370
mc.channelBox('Channel Box', height=192, preventOverride=False, attributeEditorMode=False, containerAtTop=False, precision=3, fixedAttrList = ("translateX","translateY","translateZ","rotateX","rotateY","rotateZ","scaleX","scaleY","scaleZ","visibility"))
mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 66), (2, 66), (3, 66), (4,66)])
mc.iconTextButton(label='DEL HIST', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='CP', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='CPG', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='NGONES', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)

mc.iconTextCheckBox(label='VIS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='Normals', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='DoubleS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='PIVOT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)

mc.iconTextButton(label='RT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='RR', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='RS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='RESET', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)

mc.iconTextButton(label='MT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='MR', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='MR',  style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='MATCH', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)

mc.iconTextButton(label='FT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='FT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='FS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='FREEZE', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)

mc.iconTextButton(label='UFT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='UFR', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='UFS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.iconTextButton(label='UNFREEZE', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=20)
mc.setParent( '..' )

mc.setParent( '..' )
mc.setParent( '..' )

# Tools
mc.frameLayout( label='Tools', collapse=False, collapsable=True)
mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 66), (2, 66), (3, 66), (4,66)])
mc.iconTextRadioCollection("Orientation")
mc.iconTextRadioButton(label='OBJECT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, select=True)
mc.iconTextRadioButton(label='WORLD', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='COMP.', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='PARENT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='NORMAL', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, enable=False, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, enable=False, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, enable=False, marginWidth=0, marginHeight=0)

mc.iconTextRadioCollection("Pivot")
mc.iconTextRadioButton(label='DEFAULT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, select=True)
mc.iconTextRadioButton(label='OBJECT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='MANIP', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='SELECT.', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png",  height=20)

mc.iconTextCheckBox(label='STEP', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextButton(label='Relative', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.rowLayout(numberOfColumns=2, columnWidth2=[32,30], columnAlign2=["center","center"], columnAttach2=["both","both"], height=20)
mc.floatField(editable=True, minValue=0, value=1, precision=2)
mc.iconTextRadioCollection("Discrete")
mc.iconTextRadioButton(label='1', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.setParent( '..' )
mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=20)
mc.iconTextRadioButton(label='5', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='45', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.setParent( '..' )

#mc.iconTextRadioCollection("Snap")
mc.rowLayout(numberOfColumns=3, columnWidth3=[20,20,20], columnAlign3=["center","center","center"], columnAttach3=["both","both","both"], height=20)
mc.iconTextCheckBox(label='1', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='2', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='3', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.setParent( '..' )
mc.rowLayout(numberOfColumns=3, columnWidth3=[20,20,20], columnAlign3=["center","center","center"], columnAttach3=["both","both","both"], height=20)
mc.iconTextCheckBox(label='4', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='5', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='6', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.setParent( '..' )

mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, enable=False, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, enable=False, marginWidth=0, marginHeight=0)

mc.iconTextCheckBox(label='TWEAK', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='SMART', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='Pres. Chlid', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextCheckBox(label='Pres. UVs', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)

mc.iconTextButton(label='Relative', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.floatField(editable=True, minValue=0, value=1, precision=2)
mc.floatField(editable=True, minValue=0, value=1, precision=2)
mc.floatField(editable=True, minValue=0, value=1, precision=2)
mc.setParent( '..' )
mc.setParent( '..' )

# Soft Selection
mc.frameLayout( label='Soft Selection', collapse=False, collapsable=True)
mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 66), (2, 66), (3, 66), (4,66)])
mc.iconTextCheckBox(label='SOFT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.floatField(editable=True, minValue=0, value=1, precision=3)
mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=20)
mc.iconTextRadioCollection("Soft Curve")
mc.iconTextRadioButton(label='curv1', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, select=True)
mc.iconTextRadioButton(label='curv2', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.setParent( '..' )
mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=20)
mc.iconTextRadioButton(label='curv3', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='curv4', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.setParent( '..' )
mc.iconTextRadioCollection("Falloff Mode")
mc.iconTextRadioButton(label='Surface', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, select=True)
mc.iconTextRadioButton(label='Volume', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='Object', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='Global', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.setParent( '..' )
mc.setParent( '..' )

# Symmetry Settings
mc.frameLayout( label='Symmetry Settings', collapse=False, collapsable=True)
mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 66), (2, 66), (3, 66), (4,66)])
mc.iconTextCheckBox(label='SYM', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.floatField(editable=True, minValue=0, value=1, precision=3)

mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, enable=False, marginWidth=0, marginHeight=0)

mc.rowLayout(numberOfColumns=3, columnWidth3=[20,20,20], columnAlign3=["center","center","center"], columnAttach3=["both","both","both"], height=20)
mc.iconTextRadioCollection("Symmetry axes")
mc.iconTextRadioButton(label='X', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextRadioButton(label='Y', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.iconTextRadioButton(label='Z', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=20)
mc.setParent( '..' )

mc.iconTextRadioCollection("Symmetry Mode")
mc.iconTextRadioButton(label='Object', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, select=True)
mc.iconTextRadioButton(label='World', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextRadioButton(label='Topology', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)

mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20, enable=False, marginWidth=0, marginHeight=0)

mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=20)
mc.iconTextButton(label='+X', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextButton(label='-X', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.setParent( '..' )
mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=20)
mc.iconTextButton(label='+Y', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextButton(label='-Y', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.setParent( '..' )
mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=20)
mc.iconTextButton(label='+Z', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.iconTextButton(label='-Z', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=20)
mc.setParent( '..' )

mc.setParent( '..' )
mc.setParent( '..' )

mc.showWindow()