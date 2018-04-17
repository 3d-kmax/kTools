import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import os



# self.target = "/homes/mte/maya/2016/scripts/kTools/icons/"
path_brut = os.path.realpath(__file__)
print ">> path brut : ", path_brut
path_norm = os.path.normpath(path_brut)  # os.path.normcase()
print ">> path norm : ", path_norm
path_clean = path_norm.replace("\\", "/")
print ">> path clean : ", path_clean
path_list = path_clean.split('/')[:-1]
print ">> path split : ", path_list
#path_list.extend(['icons'])
target = ''
for item in path_list:
    target += item + '/'
print ">> : ", target
print ">> : ", target[0:-1]
target = target[0:-1]

widthWin = 64+140+8#+20
heightWin = 1000
heightBtn = 20
windowName = "kMaxUi2"

if mc.window(windowName, q=True, exists=True):
    mc.deleteUI(windowName)

kMaxUi2Window = mc.window(windowName, height=heightWin, width=widthWin, toolbox=True, titleBar=True, minimizeButton=False, maximizeButton=False, sizeable=False)#, resizeToFitChildren=True)
mc.window(windowName, width=widthWin, height=heightWin, edit=True)
mc.scrollLayout( 'scrollLayout', childResizable=True ) # to delete
mc.columnLayout( adjustableColumn=True, width=widthWin)#-4)

# Common Selection Options
mc.frameLayout( label='Common Selection Options', collapse=False, collapsable=True)

mc.columnLayout()
mc.rowLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 150)])
#mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 66), (2, 66), (3, 66), (4, 66)])#, columnAlign4=["center","center","center","center"], columnAttach4=["both","both","both","both"], rowAttach=[(1, "both", 0), (1, "both", 0), (1, "both", 0), (1, "both", 0)])
#mc.rowLayout(numberOfColumns=2, columnWidth=[(1, 66), (2, 198)])
mc.iconTextStaticLabel( style='iconOnly', image=target+"/icons/moveTool.png", height=2*heightBtn)

mc.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 50), (2, 50), (3, 50)])
mc.iconTextRadioCollection("Selection Type")
mc.iconTextRadioButton(label='Object', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='Multi', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='UV', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='Vertex', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='Edge', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='Face', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.setParent( '..' )

mc.setParent( '..' )

mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 50), (2, 50), (3, 50), (4, 50)])#, columnAlign4=["center","center","center","center"], columnAttach4=["both","both","both","both"], rowAttach=[(1, "both", 0), (1, "both", 0), (1, "both", 0), (1, "both", 0)])
mc.iconTextRadioCollection("Selection mode")
mc.iconTextRadioButton(label='Marquee', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", select=True, height=heightBtn)
mc.iconTextRadioButton(label='Drag', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='Tweak', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextCheckBox(label='Cam Based', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.setParent( '..' )
#mc.setParent( '..' )

mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 24), (2,180)], columnAlign=[(1, "right"),(2, "right")])
mc.iconTextStaticLabel( style='iconOnly', image=target+"/icons/transform.png", height=heightBtn)
#mc.text(label="Transform  : ", font="tinyBoldLabelFont")
mc.textField()
mc.iconTextStaticLabel( style='iconOnly', image=target+"/icons/shape.png", height=heightBtn)
#mc.text(label="Shape  : ", font="tinyBoldLabelFont")
mc.textField()
mc.iconTextStaticLabel( style='iconOnly', image=target+"/icons/constructionHistory.png", height=heightBtn)
#mc.text(label="History  : ", font="tinyBoldLabelFont")
mc.textField()
mc.iconTextStaticLabel( style='iconOnly', image=target+"/icons/quickRename.png", height=heightBtn)
#mc.text(label="Sel. by name  : ", font="tinyBoldLabelFont")
mc.textField()
mc.setParent( '..' )

mc.setParent( '..' )
mc.setParent( '..' )

# Display
mc.frameLayout( label='Display', collapse=False, collapsable=True)
mc.columnLayout()

mc.rowColumnLayout(numberOfColumns=10, columnWidth=[(1, 20), (2, 20), (3, 20), (4,20), (5, 20), (6, 20), (7, 20), (8,20), (9, 20), (10, 20)])#, (11, 22), (12,22)])
mc.iconTextCheckBox(label='HUD', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/hud.png", highlightImage=target+"/icons/hud.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='GRID', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/grid.png", highlightImage=target+"/icons/grid.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='HLT', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/highlightSelect.png", highlightImage=target+"/icons/highlightSelect.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='MeshBorder', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/wireframe.png", highlightImage=target+"/icons/wireframe.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='uvBorder', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/uvBorder.png", highlightImage=target+"/icons/uvBorder.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='HypershadePreview', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/hyperShadeIcon.png", highlightImage=target+"/icons/hyperShadeIcon.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Msh', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/shape.png", highlightImage=target+"/icons/shape.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Def', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/lattice.png", highlightImage=target+"/icons/lattice.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Loc', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/locator.png", highlightImage=target+"/icons/locator.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='GPU', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, marginWidth=0, marginHeight=0)

mc.iconTextCheckBox(label='Wire', style='iconOnly', font="tinyBoldLabelFont", image=target + "/icons/wireframe.png",
                    highlightImage=target + "/icons/wireframe.png", selectionImage=target + "/btn/imageEnable.png",
                    selectionHighlightImage=target + "/btn/imageHighlight.png", height=heightBtn, marginWidth=0,
                    marginHeight=0)
mc.iconTextCheckBox(label='Shaded', style='iconOnly', font="tinyBoldLabelFont", image=target + "/icons/shaded.png",
                    highlightImage=target + "/icons/shaded.png", selectionImage=target + "/btn/imageEnable.png",
                    selectionHighlightImage=target + "/btn/imageHighlight.png", height=heightBtn, marginWidth=0,
                    marginHeight=0)
mc.iconTextCheckBox(label='DefaultMat', style='iconOnly', font="tinyBoldLabelFont",
                    image=target + "/icons/useDefaultMaterial.png",
                    highlightImage=target + "/icons/useDefaultMaterial.png",
                    selectionImage=target + "/btn/imageEnable.png",
                    selectionHighlightImage=target + "/btn/imageHighlight.png", height=heightBtn, marginWidth=0,
                    marginHeight=0)
mc.iconTextCheckBox(label='ShadedWire', style='iconOnly', font="tinyBoldLabelFont",
                    image=target + "/icons/wireframeOnShaded.png",
                    highlightImage=target + "/icons/wireframeOnShaded.png",
                    selectionImage=target + "/btn/imageEnable.png",
                    selectionHighlightImage=target + "/btn/imageHighlight.png", height=heightBtn, marginWidth=0,
                    marginHeight=0)
mc.iconTextCheckBox(label='Textured', style='iconOnly', font="tinyBoldLabelFont", image=target + "/icons/textured.png",
                    highlightImage=target + "/icons/textured.png", selectionImage=target + "/btn/imageEnable.png",
                    selectionHighlightImage=target + "/btn/imageHighlight.png", height=heightBtn, marginWidth=0,
                    marginHeight=0)
mc.iconTextCheckBox(label='XRAY', style='iconOnly', font="tinyBoldLabelFont", image=target + "/icons/xray.png",
                    highlightImage=target + "/icons/xray.png", selectionImage=target + "/btn/imageEnable.png",
                    selectionHighlightImage=target + "/btn/imageHighlight.png", height=heightBtn, marginWidth=0,
                    marginHeight=0)
mc.iconTextCheckBox(label='BFC', style='iconAndTextCentered', font="tinyBoldLabelFont",
                    image=target + "/btn/imageActif.png", highlightImage=target + "/btn/imageHighlight.png",
                    selectionImage=target + "/btn/imageEnable.png",
                    selectionHighlightImage=target + "/btn/imageHighlight.png", height=heightBtn, marginWidth=0,
                    marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont",
                    image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png",
                    selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png",
                    height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont",
                    image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png",
                    selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png",
                    height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont",
                    image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png",
                    selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png",
                    height=heightBtn, marginWidth=0, marginHeight=0)

mc.iconTextCheckBox(label='DefaultLight', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/light.png", highlightImage=target+"/icons/light.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='All', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/icons/light.png", highlightImage=target+"/icons/light.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Flat', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='No', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='2SL', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont",
                    image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png",
                    selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png",
                    height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Shadows', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/shadows.png", highlightImage=target+"/icons/shadows.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Occlusion', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/occlusion.png", highlightImage=target+"/icons/occlusion.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='AntiAliasing', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/multiSamplingAntiAliasing.png", highlightImage=target+"/icons/multiSamplingAntiAliasing.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='BG', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn, marginWidth=0, marginHeight=0)

#mc.setParent( '..' )

#mc.rowColumnLayout(numberOfColumns=5, columnWidth=[(1,66), (2,66), (3,66), (4,33), (5,33)])#, columnAlign5=["center","center","center","center","center"], columnAttach5=["both", "both", "both", "both", "both"], height=heightBtn)
mc.iconTextCheckBox(label='ISO', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/isolateSelected.png", highlightImage=target+"/icons/isolateSelected.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='ACTU', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/actualize.png", highlightImage=target+"/icons/actualize.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='AUTO', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/autoRefresh.png", highlightImage=target+"/icons/autoRefresh.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='+', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='-', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn, marginWidth=0, marginHeight=0)

mc.iconTextCheckBox(label='Cam', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/camera.png", highlightImage=target+"/icons/camera.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Set', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/cameraSetting.png", highlightImage=target+"/icons/cameraSetting.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextCheckBox(label='Lock', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/cameraLock.png", highlightImage=target+"/icons/cameraLock.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='Near', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='Far', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn, marginWidth=0, marginHeight=0)

mc.setParent( '..' )

mc.setParent( '..' )
mc.setParent( '..' )

#mc.iconTextCheckBox(label='HIST', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/constructionHistory.png", highlightImage=target+"/icons/constructionHistory.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn, marginWidth=0, marginHeight=0)

# Transform
mc.frameLayout( label='Transform', collapse=False, collapsable=True)
mc.columnLayout()
#192 370
mc.channelBox('Channel Box', height=192, width=210, preventOverride=False, attributeEditorMode=False, containerAtTop=False, precision=3, fixedAttrList = ("translateX","translateY","translateZ","rotateX","rotateY","rotateZ","scaleX","scaleY","scaleZ","visibility"))
mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 50), (2, 50), (3, 50), (4,50)])
mc.iconTextButton(label='DEL HIST', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='CP', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='CPG', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='NGONES', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)

mc.iconTextCheckBox(label='VIS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextCheckBox(label='Normals', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextCheckBox(label='DoubleS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextCheckBox(label='PIVOT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)

mc.iconTextButton(label='RT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='RR', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='RS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='RESET', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)

mc.iconTextButton(label='MT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='MR', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='MR',  style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='MATCH', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)

mc.iconTextButton(label='FT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='FT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='FS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='FREEZE', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)

mc.iconTextButton(label='UFT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='UFR', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='UFS', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.iconTextButton(label='UNFREEZE', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", height=heightBtn)
mc.setParent( '..' )

mc.setParent( '..' )
mc.setParent( '..' )

# Tools
mc.frameLayout( label='Tools', collapse=False, collapsable=True)
mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 50), (2, 50), (3, 50), (4,50)])
mc.iconTextRadioCollection("Orientation")
mc.iconTextRadioButton(label='OBJECT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, select=True)
mc.iconTextRadioButton(label='WORLD', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='COMP.', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='PARENT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='NORMAL', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, enable=False, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, enable=False, marginWidth=0, marginHeight=0)
mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, enable=False, marginWidth=0, marginHeight=0)

mc.iconTextRadioCollection("Pivot")
mc.iconTextRadioButton(label='DEFAULT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, select=True)
mc.iconTextRadioButton(label='OBJECT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='MANIP', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='SELECT.', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png",  height=heightBtn)

mc.iconTextCheckBox(label='STEP', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextButton(label='Relative', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.rowLayout(numberOfColumns=2, columnWidth2=[24,24], columnAlign2=["center","center"], columnAttach2=["both","both"], height=heightBtn)
mc.floatField(editable=True, minValue=0, value=1, precision=2)
mc.iconTextRadioCollection("Discrete")
mc.iconTextRadioButton(label='1', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.setParent( '..' )
mc.rowLayout(numberOfColumns=2, columnWidth2=[24,24], columnAlign2=["center","center"], columnAttach2=["both","both"], height=heightBtn)
mc.iconTextRadioButton(label='5', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='45', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.setParent( '..' )

#mc.iconTextRadioCollection("Snap")

mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 150), (2, 50)])

mc.rowLayout(numberOfColumns=6, columnWidth6=[24,24,24,24,24,24], columnAlign6=["center","center","center","center","center","center"], columnAttach6=["both","both","both","both","both","both"], height=heightBtn)
mc.iconTextCheckBox(label='1', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/snapGrid.png", highlightImage=target+"/icons/snapGrid.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextCheckBox(label='2', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/snapCurve.png", highlightImage=target+"/icons/snapCurve.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
# mc.setParent( '..' )
# mc.rowLayout(numberOfColumns=2, columnWidth2=[24,24], columnAlign2=["center","center"], columnAttach2=["both","both"], height=heightBtn)
mc.iconTextCheckBox(label='3', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/snapPoint.png", highlightImage=target+"/icons/snapPoint.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextCheckBox(label='4', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/snapMeshCenter.png", highlightImage=target+"/icons/snapMeshCenter.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
# mc.setParent( '..' )
# mc.rowLayout(numberOfColumns=2, columnWidth2=[24,24], columnAlign2=["center","center"], columnAttach2=["both","both"], height=heightBtn)
mc.iconTextCheckBox(label='5', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/snapPlane.png", highlightImage=target+"/icons/snapPlane.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextCheckBox(label='6', style='iconOnly', font="tinyBoldLabelFont", image=target+"/icons/snapToggle.png", highlightImage=target+"/icons/snapToggle.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.setParent( '..' )
mc.textField()

mc.setParent( '..' )


# mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, enable=False, marginWidth=0, marginHeight=0)
# mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, enable=False, marginWidth=0, marginHeight=0)

mc.iconTextCheckBox(label='TWEAK', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextCheckBox(label='SMART', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextCheckBox(label='Pres. Chlid', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextCheckBox(label='Pres. UVs', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)

mc.iconTextButton(label='Relative', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.floatField(editable=True, minValue=0, value=1, precision=2)
mc.floatField(editable=True, minValue=0, value=1, precision=2)
mc.floatField(editable=True, minValue=0, value=1, precision=2)
mc.setParent( '..' )
mc.setParent( '..' )

# Soft Selection
mc.frameLayout( label='Soft Selection', collapse=False, collapsable=True)
mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 50), (2, 50), (3, 50), (4,50)])
mc.iconTextCheckBox(label='SOFT', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.floatField(editable=True, minValue=0, value=1, precision=3)
mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=heightBtn)
mc.iconTextRadioCollection("Soft Curve")
mc.iconTextRadioButton(label='curv1', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, select=True)
mc.iconTextRadioButton(label='curv2', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.setParent( '..' )
mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=heightBtn)
mc.iconTextRadioButton(label='curv3', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='curv4', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.setParent( '..' )
mc.iconTextRadioCollection("Falloff Mode")
mc.iconTextRadioButton(label='Surface', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, select=True)
mc.iconTextRadioButton(label='Volume', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='Object', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='Global', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.setParent( '..' )
mc.setParent( '..' )

# Symmetry Settings
mc.frameLayout( label='Symmetry Settings', collapse=False, collapsable=True)
mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 50), (2, 50), (3, 50), (4,50)])
mc.iconTextCheckBox(label='SYM', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.floatField(editable=True, minValue=0, value=1, precision=3)

# mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, enable=False, marginWidth=0, marginHeight=0)

mc.rowLayout(numberOfColumns=3, columnWidth3=[20,20,20], columnAlign3=["center","center","center"], columnAttach3=["both","both","both"], height=heightBtn)
mc.iconTextRadioCollection("Symmetry axes")
mc.iconTextRadioButton(label='X', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextRadioButton(label='Y', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.iconTextRadioButton(label='Z', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", selectionHighlightImage=target+"/btn/imageHighlight.png", height=heightBtn)
mc.setParent( '..' )

mc.iconTextRadioCollection("Symmetry Mode")
mc.iconTextRadioButton(label='Object', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, select=True)
mc.iconTextRadioButton(label='World', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextRadioButton(label='Topology', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)

mc.iconTextButton(label='//', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn, enable=False, marginWidth=0, marginHeight=0)

mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=heightBtn)
mc.iconTextButton(label='+X', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextButton(label='-X', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.setParent( '..' )
mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=heightBtn)
mc.iconTextButton(label='+Y', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextButton(label='-Y', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.setParent( '..' )
mc.rowLayout(numberOfColumns=2, columnWidth2=[30,32], columnAlign2=["center","center"], columnAttach2=["both","both"], height=heightBtn)
mc.iconTextButton(label='+Z', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.iconTextButton(label='-Z', style='iconAndTextCentered', font="tinyBoldLabelFont", image=target+"/btn/imageActif.png", highlightImage=target+"/btn/imageHighlight.png", selectionImage=target+"/btn/imageEnable.png", disabledImage=target+"/btn/imageActif.png", height=heightBtn)
mc.setParent( '..' )

mc.setParent( '..' )
mc.setParent( '..' )

mc.showWindow()