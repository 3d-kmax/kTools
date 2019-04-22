import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import os

path = "E:/kTools/icons/"
wscName = "kTool"
winName = "kToolWindow"

class KTool():

    def __init__(self):
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

        if (cmds.window('kToolWindow_ui', q=True, ex=True)): cmds.deleteUI('kToolWindow_ui')
        cmds.window('kToolWindow_ui', t=u'kTool', s=False, tb=True, tlb=True, wh=(186, 1100))
        cmds.columnLayout('columnLayout1_ui', h=1000, adj=True)

        cmds.frameLayout('selectionLayout_ui', cll=True, l=u'Common Selection Options')
        cmds.columnLayout('columnLayout2_ui')
        cmds.rowColumnLayout(nc=2)
        cmds.iconTextButton(w=44, vis=True, i=u'E:\kTools\icons/aselect.png')
        cmds.rowColumnLayout(nc=3, cs=[[2, 1], [3, 1]])
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=32, ebg=False, i=u'E:\kTools\icons/objectnex.png', mw=0, mh=0, sl=True)
        cmds.iconTextRadioButton(w=44, h=32, ebg=False, l=u'Multi', st=u'textOnly', mw=0, mh=0)
        cmds.iconTextRadioButton(w=44, h=32, i=u'E:\kTools\icons/uvnex.png', mw=0, mh=0)
        cmds.iconTextRadioButton(w=44, h=32, i=u'E:\kTools\icons/vertexnex.png', mw=0, mh=0)
        cmds.iconTextRadioButton(w=44, h=32, i=u'E:\kTools\icons/edgesnex.png', mw=0, mh=0)
        cmds.iconTextRadioButton(w=44, h=32, i=u'E:\kTools\icons/facesnex.png', mw=0, mh=0)
        cmds.rowColumnLayout(p='columnLayout2_ui', nc=4, cs=[[2, 1], [3, 1], [4, 1]])
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, l=u'Marquee', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont', sl=True)
        cmds.iconTextRadioButton(w=44, h=22, l=u'Drag', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, l=u'Tweak', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
        cmds.iconTextCheckBox(w=44, h=22, l=u'Cam B', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.rowColumnLayout('rowColumnLayout4_ui', p='columnLayout2_ui', nc=2, cw=[[1, 20], [2, 160]])
        cmds.iconTextStaticLabel(w=20, h=20, i=u'E:\kTools\icons/transform.png', mw=0, mh=0)
        cmds.textField()
        cmds.iconTextStaticLabel(w=20, h=20, i=u'E:\kTools\icons/shape.png', mw=0, mh=0)
        cmds.textField(ed=False)
        cmds.iconTextStaticLabel(w=20, h=20, i=u'E:\kTools\icons/constructionHistory.png', mw=0, mh=0)
        cmds.optionMenu()
        cmds.iconTextStaticLabel(p='rowColumnLayout4_ui', w=20, h=20, i=u'E:\kTools\icons/quickRename.png', mw=0, mh=0)
        cmds.textField(p='rowColumnLayout4_ui')

        cmds.frameLayout('transformLayout_ui', p='columnLayout1_ui', cll=True, l=u'Transform')
        cmds.columnLayout('columnLayout3_ui')
        cmds.channelBox('channelBox1_ui', w=180, h=192, # preventOverride=False,
                                                        # attributeEditorMode=False,
                                                        # containerAtTop=False,
                                                        precision=3,
                                                        fixedAttrList=("translateX", "translateY", "translateZ", "rotateX",
                                                                       "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ",
                                                                       'visibility'))
        cmds.gridLayout(nr=5, nc=4, cw=45, ch=44)
        cmds.iconTextButton(w=44, h=44, ebg=True, i=u'E:\kTools\icons/deleteHistory.png')
        cmds.iconTextButton(w=44, h=44, ebg=True, i=u'E:\kTools\icons/centerPivot.png')
        cmds.iconTextButton(en=False, w=44, h=44, ebg=True, i=u'E:\kTools\icons/deleteHistory.png', l=u'//', st=u'textOnly')
        cmds.iconTextButton(en=False, w=44, h=44, ebg=True, i=u'E:\kTools\icons/deleteHistory.png', l=u'//', st=u'textOnly')
        cmds.iconTextButton(w=44, h=44, ebg=True, i=u'E:\kTools\icons/resetTransform.png')
        cmds.iconTextButton(w=44, h=44, ebg=True, i=u'E:\kTools\icons/matchTransform.png')
        cmds.iconTextButton(w=44, h=44, ebg=True, i=u'E:\kTools\icons/freezeTransform.png')
        cmds.iconTextButton(w=44, h=44, ebg=True, i=u'E:\kTools\icons/unfreeze.png')
        cmds.gridLayout(p='columnLayout3_ui', nr=4, nc=4, cw=45, ch=22)
        cmds.iconTextButton(w=44, l=u'R.T', st=u'textOnly')
        cmds.iconTextButton(w=44, h=22, l=u'M.T', st=u'textOnly')
        cmds.iconTextButton(w=44, h=22, l=u'F.T', st=u'textOnly')
        cmds.iconTextButton(en=False, w=44, h=22, l=u'//', st=u'textOnly')
        cmds.iconTextButton(w=44, h=22, l=u'R.R', st=u'textOnly')
        cmds.iconTextButton(w=44, h=22, l=u'M.R', st=u'textOnly')
        cmds.iconTextButton(w=44, h=22, l=u'F.R', st=u'textOnly')
        cmds.iconTextCheckBox(w=44, h=22, i=u'E:\kTools\icons/snapToggle.png', mw=0, mh=0)
        cmds.iconTextButton(w=44, h=22, l=u'R.S', st=u'textOnly')
        cmds.iconTextButton(w=44, h=22, l=u'M.S', st=u'textOnly')
        cmds.iconTextButton(w=44, h=22, l=u'F.S', st=u'textOnly')
        cmds.iconTextButton(en=False, w=44, h=22, l=u'//', st=u'textOnly')

        cmds.frameLayout('displayLayout_ui', p='columnLayout1_ui', cll=True, l=u'Display')

        cmds.frameLayout('toolLayout_ui', p='columnLayout1_ui', cll=True, l=u'Tool Settings')
        cmds.columnLayout('columnLayout6_ui')
        cmds.rowColumnLayout(nc=4, cs=[[2, 1], [3, 1], [4, 1]])
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Object', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'World', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Comp.', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Parent', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Normal', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Gimbal', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(en=False, w=44, h=22, ebg=True, l=u'//', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Custom', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.separator(p='columnLayout6_ui', h=1, st=u'none')
        cmds.rowColumnLayout(p='columnLayout6_ui', nc=4, cs=[[2, 1], [3, 1], [4, 1]])
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Default', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Object', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Manip', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Selection', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.separator(p='columnLayout6_ui', h=1, st=u'none')
        cmds.rowColumnLayout(p='columnLayout6_ui', en=False, vis=True, nc=4, cs=[[2, 1], [3, 1], [4, 1]])
        cmds.text(w=44, h=22, l=u'Snap :', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Relative', st=u'textOnly', fn=u'tinyBoldLabelFont', sl=True)
        cmds.iconTextRadioButton(w=44, h=22, ebg=True, l=u'Absolute', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.floatField(w=44, h=22, pre=3)
        cmds.separator(p='columnLayout6_ui', h=1, st=u'none')
        cmds.rowColumnLayout(p='columnLayout6_ui', nc=4, cs=[[2, 1], [3, 1], [4, 1]])
        cmds.iconTextCheckBox(w=44, h=22, ebg=True, l=u'Tweak', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextCheckBox(w=44, h=22, ebg=True, l=u'Pr.UVs', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextCheckBox(w=44, h=22, ebg=True, l=u'Pr.Child', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextCheckBox(w=44, h=22, ebg=True, l=u'Free Rot.', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextCheckBox(w=44, h=22, ebg=True, l=u'No Neg.S', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextCheckBox(w=44, h=22, ebg=True, l=u'Smt.Dup', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextCheckBox(w=44, h=22, ebg=True, l=u'Smt.Ext', st=u'textOnly', fn=u'tinyBoldLabelFont')

        cmds.frameLayout('softLayout_ui', p='columnLayout1_ui', cll=True, l=u'Soft')
        cmds.columnLayout('columnLayout5_ui')
        cmds.rowColumnLayout('rowColumnLayout9_ui', h=46, nc=3, cs=[[2, 1], [3, 1]])
        cmds.iconTextCheckBox(w=44, h=44, i=u'E:\kTools\icons/offsetCurve.png', l=u'Soft', st=u'iconAndTextVertical', mw=0,
                              mh=0, fn=u'tinyBoldLabelFont')
        cmds.gridLayout(nr=2, nc=2, cw=44, ch=22)
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, l=u'Surface', st=u'textOnly', fn=u'tinyBoldLabelFont', sl=True)
        cmds.iconTextRadioButton(w=44, h=22, l=u'Volume', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, l=u'Object', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, l=u'Global', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.gridLayout(p='rowColumnLayout9_ui', nc=1, cw=44, ch=22)
        cmds.floatField(w=44, pre=3)
        cmds.iconTextCheckBox(w=44, l=u'Color', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.rowColumnLayout(p='columnLayout5_ui', en=True, nc=4, cs=[[2, 1], [3, 1], [4, 1]])
        cmds.iconTextButton(w=44, h=22, ebg=True, l=u'Reset', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, i=u'E:\kTools\icons/softPresetA.png', l=u'Curv1', st=u'iconOnly',
                                 fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, i=u'E:\kTools\icons/softPresetB.png', l=u'Curv2', st=u'iconOnly',
                                 fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, i=u'E:\kTools\icons/softPresetC.png', l=u'Curv3', st=u'iconOnly',
                                 fn=u'tinyBoldLabelFont')

        cmds.frameLayout('symLayout_ui', p='columnLayout1_ui', cll=True, l=u'Symmetry')
        cmds.columnLayout('columnLayout4_ui')
        cmds.rowColumnLayout(h=46, nc=2)
        cmds.iconTextCheckBox(w=44, h=44, i=u'E:\kTools\icons/polyMirrorCut.png', l=u'Sym', st=u'iconAndTextVertical', mw=0,
                              mh=0, fn=u'tinyBoldLabelFont')
        cmds.rowColumnLayout(nc=3, cs=[[2, 1], [3, 1]])
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, l=u'Object', st=u'textOnly', fn=u'tinyBoldLabelFont', sl=True)
        cmds.iconTextRadioButton(w=44, h=22, l=u'World', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, l=u'Topo', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, l=u'X', st=u'textOnly', fn=u'tinyBoldLabelFont', sl=True)
        cmds.iconTextRadioButton(w=44, h=22, l=u'Y', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, l=u'Z', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.rowColumnLayout(p='columnLayout4_ui', en=True, nc=4, cs=[[2, 1], [3, 1], [4, 1]])
        cmds.iconTextButton(w=44, h=22, ebg=True, l=u'Reset', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
        cmds.iconTextCheckBox(w=44, h=22, l=u'P.Seam', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
        cmds.iconTextCheckBox(w=44, h=22, l=u'Partial', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
        cmds.floatField(w=44, h=22, pre=3)

        cmds.frameLayout('stepLayout_ui', p='columnLayout1_ui', cll=True, l=u'Step Snap')
        cmds.columnLayout('columnLayout7_ui')
        cmds.rowColumnLayout(h=46, nc=2)
        cmds.iconTextCheckBox(w=44, h=44, i=u'E:\kTools\icons/snapPixel.png', l=u'Snap', st=u'iconAndTextVertical', mw=0,
                              mh=0, fn=u'tinyBoldLabelFont')
        cmds.rowColumnLayout(nc=3, cs=[[2, 1], [3, 1]])
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, l=u'Relative', st=u'textOnly', fn=u'tinyBoldLabelFont', sl=True)
        cmds.iconTextRadioButton(w=44, h=22, l=u'Absolute', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.floatField(w=44, pre=3)
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, l=u'Edge', st=u'textOnly', fn=u'tinyBoldLabelFont', sl=True)
        cmds.iconTextRadioButton(w=44, h=22, l=u'Surface', st=u'textOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextButton(w=44, h=22, l=u'Normals', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
        cmds.rowColumnLayout(p='columnLayout7_ui', en=True, nc=4, cs=[[2, 1], [3, 1], [4, 1]])
        cmds.iconTextButton(w=44, h=22, ebg=True, l=u'Reset', st=u'textOnly', mw=0, mh=0, fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(w=44, h=22, i=u'E:\kTools\icons/snapGrid.png', st=u'iconOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, i=u'E:\kTools\icons/snapCurve.png', st=u'iconOnly', fn=u'tinyBoldLabelFont')
        cmds.iconTextRadioButton(w=44, h=22, i=u'E:\kTools\icons/snapPoint.png', l=u'', st=u'iconOnly',
                                 fn=u'tinyBoldLabelFont')
        cmds.showWindow('kToolWindow_ui')

    def initScriptJobs(self):
        self.scriptJobIds.append(mc.scriptJob(event=("SelectModeChanged", catchJobException(self.actuTypeSelection))))
        self.scriptJobIds.append(mc.scriptJob(event=("SelectTypeChanged", catchJobException(self.actuTypeSelection))))
        self.scriptJobIds.append(mc.scriptJob(event=("SelectionChanged", catchJobException(self.actuSelection))))
        self.scriptJobIds.append(mc.scriptJob(event=("ToolChanged", catchJobException(self.actuToolSettings))))
        self.scriptJobIds.append(mc.scriptJob(event=("ModelPanelSetFocus", catchJobException(self.testJob))))
        self.scriptJobIds.append(mc.scriptJob(event=("modelEditorChanged", catchJobException(self.initDisplay))))

def catchJobException(func):
    def doIt(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception, e:
            pm.displayError('< {0}.{1} > {2}.'.format(func.__module__, func.__name__, str(e)))
            return
        return ret

    return doIt

KTool().buildUI()
