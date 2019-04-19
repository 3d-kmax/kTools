import maya.cmds as mc

path = "E:/kTools/icons/"
wscName = "kTool"
winName = "kToolWindow"

def buildUI():
    if mc.window(winName, q=True, ex=True): 
        mc.deleteUI(winName)
    if mc.windowPref(winName, ex=1): 
        mc.windowPref(winName, r=1)
    if mc.workspaceControl(wscName, query=True, exists=True): 
        mc.deleteUI(wscName, control=True)

    mc.window(winName, t=u'kTools', s=False, tb=True, tlb=True, tbm=True, wh=(185, 800))
    mc.columnLayout('columnLayout1_ui', adj=True)

    mc.frameLayout('frameLayout1_ui', cll=True, l=u'Common Selection Options')
    mc.columnLayout('columnLayout2_ui')
    mc.rowColumnLayout('rowColumnLayout2_ui', h=60, nc=2)
    mc.iconTextButton('iconTextButton1_ui', w=44, h=60, i=path + "aselect.png")
    mc.rowColumnLayout('rowColumnLayout1_ui', h=60, nc=3, cs=[[2, 1], [3, 1]])
    mc.iconTextRadioCollection('iconTextRadioCollection1_ui')
    mc.iconTextRadioButton('iconTextRadioButton1_ui', w=44, h=30, i=path + 'objectnex.png', mw=0, mh=0,sl=True)
    mc.iconTextRadioButton('iconTextRadioButton2_ui', w=44, h=30, l=u'Multi', st=u'textOnly', mw=0, mh=0)
    mc.iconTextRadioButton('iconTextRadioButton3_ui', w=44, h=30, i=path + 'uvnex.png', mw=0, mh=0)
    mc.iconTextRadioButton('iconTextRadioButton4_ui', w=44, h=30, i=path + 'vertexnex.png', mw=0, mh=0)
    mc.iconTextRadioButton('iconTextRadioButton5_ui', w=44, h=30, i=path + 'edgesnex.png', mw=0, mh=0)
    mc.iconTextRadioButton('iconTextRadioButton6_ui', w=44, h=30, i=path + 'facesnex.png', mw=0, mh=0)
    mc.rowColumnLayout('rowColumnLayout3_ui', p='columnLayout2_ui', nc=4, cs=[[2, 1], [3, 1], [4, 1]])
    mc.iconTextRadioCollection('iconTextRadioCollection2_ui')
    mc.iconTextRadioButton('iconTextRadioButton8_ui', w=44, h=20, l=u'Marquee', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont', sl=True)
    mc.iconTextRadioButton('iconTextRadioButton7_ui', w=44, h=20, l=u'Drag', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
    mc.iconTextRadioButton('iconTextRadioButton9_ui', w=44, h=20, l=u'Tweak', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
    mc.iconTextRadioButton('iconTextRadioButton10_ui', w=44, h=20, l=u'Cam B', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
    mc.rowColumnLayout('rowColumnLayout4_ui', p='columnLayout2_ui', nc=2, cw=[[1, 20], [2, 160]])
    mc.iconTextStaticLabel('iconTextStaticLabel1_ui', w=20, h=20, i=path + 'transform.png', mw=0, mh=0)
    mc.textField('textField1_ui')
    mc.iconTextStaticLabel('iconTextStaticLabel2_ui', w=20, h=20, i=path + 'shape.png', mw=0, mh=0)
    mc.textField('textField2_ui', ed=False)
    mc.iconTextStaticLabel('iconTextStaticLabel3_ui', w=20, h=20, i=path + 'constructionHistory.png', mw=0, mh=0)
    mc.textField('textField3_ui')
    mc.iconTextStaticLabel('iconTextStaticLabel4_ui', w=20, h=20, i=path + 'quickRename.png', mw=0, mh=0)
    mc.textField('textField4_ui')

    mc.frameLayout('frameLayout2_ui', p='columnLayout1_ui', cll=True, l=u'Display')

    mc.frameLayout('frameLayout3_ui', p='columnLayout1_ui', cll=True, l=u'Transform')
    mc.columnLayout('columnLayout3_ui', adj=True)
    mc.channelBox('channelBox1_ui', h=192, preventOverride=False, attributeEditorMode=False, precision=3, containerAtTop=False, fixedAttrList = ("translateX","translateY","translateZ","rotateX","rotateY","rotateZ","scaleX","scaleY","scaleZ","visibility"))
    mc.rowColumnLayout('rowColumnLayout5_ui', nc=4, cs=[[2, 1], [3, 1], [4, 1]])
    mc.iconTextButton('iconTextButton2_ui', w=44, h=44, i=path + 'deleteHistory.png', mw=0, mh=0)
    mc.iconTextButton('iconTextButton3_ui', w=44, h=44, i=path + 'centerPivot.png', mw=0, mh=0)
    mc.iconTextButton('iconTextButton4_ui', en=False, w=44, h=44, i=path + 'deleteHistory.png', l=u'//', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton5_ui', en=False, w=44, h=44, i=path + 'deleteHistory.png', l=u'//',  st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton6_ui', w=44, h=44, i=path + 'resetTransform.png', mw=0, mh=0)
    mc.iconTextButton('iconTextButton7_ui', w=44, h=44, i=path + 'matchTransform.png', mw=0, mh=0)
    mc.iconTextButton('iconTextButton8_ui', w=44, h=44, i=path + 'freezeTransform.png', mw=0, mh=0)
    mc.iconTextButton('iconTextButton9_ui', w=44, h=44, i=path + 'unfreeze.png', mw=0, mh=0)
    mc.iconTextButton('iconTextButton10_ui', w=44, h=22, l=u'R.T', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton11_ui', w=44, h=22, l=u'M.T', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton12_ui', w=44, h=22, l=u'F.T', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton13_ui', en=False, w=44, h=22, l=u'//', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton14_ui', w=44, h=22, l=u'R.R', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton15_ui', w=44, h=22, l=u'M.R', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton16_ui', w=44, h=22, l=u'F.R', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton17_ui', w=44, h=22, l=u'Live', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton18_ui', w=44, h=22, l=u'R.S', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton19_ui', w=44, h=22, l=u'M.S', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton20_ui', w=44, h=22, l=u'F.S', st=u'textOnly', mw=0, mh=0)
    mc.iconTextButton('iconTextButton21_ui', en=False, w=44, h=22, l=u'//', st=u'textOnly', mw=0, mh=0)

    mc.frameLayout('frameLayout4_ui', p='columnLayout1_ui', cll=True, l=u'Tool Settings')

    mc.frameLayout('frameLayout5_ui', p='columnLayout1_ui', cll=True, l=u'Soft')

    mc.frameLayout('frameLayout6_ui', p='columnLayout1_ui', cll=True, l=u'Symmetry')

    mc.frameLayout('frameLayout7_ui', p='columnLayout1_ui', cll=True, l=u'Step')


    #mc.showWindow(winName, parent=myWsc)
    mc.window(winName, parent=myWsc)

    mc.workspaceControl(myWsc, uiScript="buildUI()", floating=False, retain=False, tabToControl=('AttributeEditor', -1))


buildUI()
