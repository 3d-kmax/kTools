import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import os

def catchJobException(func):
    def doIt(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception, e:
            pm.displayError('< {0}.{1} > {2}.'.format(func.__module__, func.__name__, str(e)))
            return
        return ret

    return doIt

class KTool():

# INITIALISATION :
# initialisation des variables et des etats des boutons de kmaxToolBar en fonction de celles de maya

    def __init__(self):
        self.wscName = "kToolWorkspace"
        self.winName = "kToolWindow"
        self.toolBarName = "kToolBar"
        self.selectColor = [0.32156, 0.52156, 0.65098]

        self.initPath()

        self.buildUI()

        self.scriptJobIds = []
        self.initScriptJobs()

        self.actuSelection()
        self.actuTypeSelection()
        self.actuToolSettings()
        self.initSelectStyle()

# build UI
    def buildUI(self):
        if mc.window(self.winName, query=True, exists=True):
            mc.deleteUI(self.winName)
        if mc.windowPref(self.winName, exists=1):
            mc.windowPref(self.winName, r=1)
        if mc.toolBar(self.toolBarName, query=True, exists=True):
            mc.deleteUI(self.toolBarName)
        '''
        if mc.workspaceControl(wscName, query=True, exists=True):
            mc.deleteUI(wscName, control=True)
        '''

        mc.window(self.winName, title='kTool', sizeable=False, widthHeight=(186, 1100))
        mc.columnLayout('columnLayout1', height=1100, adjustableColumn=True)


# build UI : Frame 'Common Selection Options'
        mc.frameLayout('selection_Layout', parent='columnLayout1', collapsable=True, label='Common Selection Options')
        mc.columnLayout('columnLayout2')
        mc.rowColumnLayout(numberOfColumns=2)
        self.lb_tool = mc.iconTextStaticLabel(width=44, visible=True, image=self.path + 'selectTool.png')
        mc.rowColumnLayout(numberOfColumns=3, columnSpacing=[[2, 1], [3, 1]])
        mc.iconTextRadioCollection()
        self.bt_selObj = mc.iconTextRadioButton(width=44, height=32, enableBackground=False, image=self.path + 'objectnex.png', select=True, onCommand=self.selObject)
        self.bt_selMulti = mc.iconTextRadioButton(width=44, height=32, enableBackground=False, label='Multi',  style='textOnly', onCommand=self.selMulti)
        self.bt_selUv = mc.iconTextRadioButton(width=44, height=32, image=self.path + 'uvnex.png', onCommand=self.selUv)
        self.bt_selVert = mc.iconTextRadioButton(width=44, height=32, image=self.path + 'vertexnex.png', onCommand=self.selVertex)
        self.bt_selEdge = mc.iconTextRadioButton(width=44, height=32, image=self.path + 'edgesnex.png', onCommand=self.selEdge)
        self.bt_selFace = mc.iconTextRadioButton(width=44, height=32, image=self.path + 'facesnex.png', onCommand=self.selFace)
        mc.rowColumnLayout(parent='columnLayout2', numberOfColumns=4, columnSpacing=[[2, 1], [3, 1], [4, 1]])
        mc.iconTextRadioCollection()
        self.bt_marqueeSelStyle = mc.iconTextRadioButton(width=44, height=22, label='Marquee',  style='textOnly', font='tinyBoldLabelFont', select=True)
        self.bt_dragSelStyle = mc.iconTextRadioButton(width=44, height=22, label='Drag',  style='textOnly', font='tinyBoldLabelFont')
        self.bt_tweakSelStyle = mc.iconTextRadioButton(width=44, height=22, label='Tweak',  style='textOnly', font='tinyBoldLabelFont')
        self.bt_camSwitch = mc.iconTextCheckBox(width=44, height=22, label='Cam B',  style='textOnly', font='tinyBoldLabelFont')
        mc.rowColumnLayout('rowColumnLayout4', parent='columnLayout2', numberOfColumns=2, columnWidth=[[1, 20], [2, 160]])
        mc.iconTextStaticLabel(width=20, height=20, image=self.path + 'transform.png')
        self.tf_transformName = mc.textField(enterCommand=self.renameTransform)
        mc.iconTextStaticLabel(width=20, height=20, image=self.path + 'shape.png')
        self.tf_shapeName = mc.textField(editable=False)
        mc.iconTextStaticLabel(width=20, height=20, image=self.path + 'constructionHistory.png')
        self.om_history = mc.optionMenu(changeCommand=self.openAttributEditor, alwaysCallChangeCommand=True, maxVisibleItems=10)
        mc.iconTextStaticLabel(width=20, height=20, image=self.path + 'quickRename.png')
        self.tf_selByName = mc.textField(placeholderText='select by name', enterCommand=self.selectByName)


# build UI : Frame 'Transform'
        mc.frameLayout('transform_Layout', parent='columnLayout1', collapsable=True, label='Transform')
        mc.columnLayout('columnLayout3')
        mc.channelBox('channelBox1', width=180, height=192, # preventOverride=False,
                                    # attributeEditorMode=False,
                                    # containerAtToparent=False,
                                    precision=3,
                                    fixedAttrList=("translateX", "translateY", "translateZ", "rotateX", "rotateY",
                                                   "rotateZ", "scaleX", "scaleY", "scaleZ", 'visibility'))
        mc.gridLayout(numberOfRows=5, numberOfColumns=4, cellWidth=45, cellHeight=44)
        mc.iconTextButton(width=44, height=44, enableBackground=True, image=self.path + 'deleteHistory.png')
        mc.iconTextButton(width=44, height=44, enableBackground=True, image=self.path + 'centerPivot.png')
        mc.iconTextButton(enable=False, width=44, height=44, enableBackground=True, image=self.path + 'deleteHistory.png', label='//',  style='textOnly')
        mc.iconTextButton(enable=False, width=44, height=44, enableBackground=True, image=self.path + 'deleteHistory.png', label='//',  style='textOnly')
        mc.iconTextButton(width=44, height=44, enableBackground=True, image=self.path + 'resetTransform.png')
        mc.iconTextButton(width=44, height=44, enableBackground=True, image=self.path + 'matchTransform.png')
        mc.iconTextButton(width=44, height=44, enableBackground=True, image=self.path + 'freezeTransform.png')
        mc.iconTextButton(width=44, height=44, enableBackground=True, image=self.path + 'unfreeze.png')
        mc.gridLayout(parent='columnLayout3', numberOfRows=4, numberOfColumns=4, cellWidth=45, cellHeight=22)
        mc.iconTextButton(width=44, label='R.T',  style='textOnly')
        mc.iconTextButton(width=44, height=22, label='M.T',  style='textOnly')
        mc.iconTextButton(width=44, height=22, label='F.T',  style='textOnly')
        mc.iconTextButton(enable=False, width=44, height=22, label='//',  style='textOnly')
        mc.iconTextButton(width=44, height=22, label='R.R',  style='textOnly')
        mc.iconTextButton(width=44, height=22, label='M.R',  style='textOnly')
        mc.iconTextButton(width=44, height=22, label='F.R',  style='textOnly')
        mc.iconTextCheckBox(width=44, height=22, image=self.path + 'snapToggle.png')
        mc.iconTextButton(width=44, height=22, label='R.S',  style='textOnly')
        mc.iconTextButton(width=44, height=22, label='M.S',  style='textOnly')
        mc.iconTextButton(width=44, height=22, label='F.S',  style='textOnly')
        mc.iconTextButton(enable=False, width=44, height=22, label='//',  style='textOnly')


# build UI : Frame 'Display'
        mc.frameLayout('display_Layout', parent='columnLayout1', collapsable=True, label='Display')


# build UI : Frame 'Tool Settings'
        self.fl_tool = mc.frameLayout('tool_Layout', parent='columnLayout1', collapsable=True, label='Tool Settings')
        mc.columnLayout('columnLayout6')
        mc.rowColumnLayout(numberOfColumns=4, columnSpacing=[[2, 1], [3, 1], [4, 1]])
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Object',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='World',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Comp.',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Parent',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Normal',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Gimbal',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(enable=False, width=44, height=22, enableBackground=True, label='//',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Custom',  style='textOnly', font='tinyBoldLabelFont')
        mc.separator(parent='columnLayout6', height=1,  style='none')
        mc.rowColumnLayout(parent='columnLayout6', numberOfColumns=4, columnSpacing=[[2, 1], [3, 1], [4, 1]])
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Default',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Object',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Manip',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Selection',  style='textOnly', font='tinyBoldLabelFont')
        mc.separator(parent='columnLayout6', height=1,  style='none')
        mc.rowColumnLayout(parent='columnLayout6', enable=False, visible=True, numberOfColumns=4, columnSpacing=[[2, 1], [3, 1], [4, 1]])
        mc.text(width=44, height=22, label='Snap :', font='tinyBoldLabelFont')
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Relative',  style='textOnly', font='tinyBoldLabelFont' , select=True)
        mc.iconTextRadioButton(width=44, height=22, enableBackground=True, label='Absolute',  style='textOnly', font='tinyBoldLabelFont')
        mc.floatField(width=44, height=22, precision=3)
        mc.separator(parent='columnLayout6', height=1,  style='none')
        mc.rowColumnLayout(parent='columnLayout6', numberOfColumns=4, columnSpacing=[[2, 1], [3, 1], [4, 1]])
        mc.iconTextCheckBox(width=44, height=22, enableBackground=True, label='Tweak',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextCheckBox(width=44, height=22, enableBackground=True, label='Pr.UVs',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextCheckBox(width=44, height=22, enableBackground=True, label='Pr.Child',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextCheckBox(width=44, height=22, enableBackground=True, label='Free Rot.',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextCheckBox(width=44, height=22, enableBackground=True, label='No Neg.S',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextCheckBox(width=44, height=22, enableBackground=True, label='Smt.Dup',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextCheckBox(width=44, height=22, enableBackground=True, label='Smt.Ext',  style='textOnly', font='tinyBoldLabelFont')


# build UI : Frame 'Soft'
        mc.frameLayout('soft_Layout', parent='columnLayout1', collapsable=True, label='Soft')
        mc.columnLayout('columnLayout5')
        mc.rowColumnLayout('rowColumnLayout9', height=46, numberOfColumns=3, columnSpacing=[[2, 1], [3, 1]])
        mc.iconTextCheckBox(width=44, height=44, image=self.path + 'offsetCurve.png', label='Soft',  style='iconAndTextVertical', font='tinyBoldLabelFont')
        mc.gridLayout(numberOfRows=2, numberOfColumns=2, cellWidth=44, cellHeight=22)
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, label='Surface',  style='textOnly', font='tinyBoldLabelFont' , select=True)
        mc.iconTextRadioButton(width=44, height=22, label='Volume',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, label='Object',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, label='Global',  style='textOnly', font='tinyBoldLabelFont')
        mc.gridLayout(parent='rowColumnLayout9', numberOfColumns=1, cellWidth=44, cellHeight=22)
        mc.floatField(width=44, precision=3)
        mc.iconTextCheckBox(width=44, label='Color',  style='textOnly', font='tinyBoldLabelFont')
        mc.rowColumnLayout(parent='columnLayout5', enable=True, numberOfColumns=4, columnSpacing=[[2, 1], [3, 1], [4, 1]])
        mc.iconTextButton(width=44, height=22, enableBackground=True, label='Reset',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, image=self.path + 'softPresetA.png',  style='iconOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, image=self.path + 'softPresetB.png',  style='iconOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, image=self.path + 'softPresetC.png',  style='iconOnly', font='tinyBoldLabelFont')


# build UI : Frame 'Symmetry'
        mc.frameLayout('sym_Layout', parent='columnLayout1', collapsable=True, label='Symmetry')
        mc.columnLayout('columnLayout4')
        mc.rowColumnLayout(height=46, numberOfColumns=2)
        mc.iconTextCheckBox(width=44, height=44, image=self.path + 'polyMirrorCut.png', label='Sym',  style='iconAndTextVertical', font='tinyBoldLabelFont')
        mc.rowColumnLayout(numberOfColumns=3, columnSpacing=[[2, 1], [3, 1]])
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, label='Object',  style='textOnly', font='tinyBoldLabelFont', select=True)
        mc.iconTextRadioButton(width=44, height=22, label='World',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, label='Topo',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, label='X',  style='textOnly', font='tinyBoldLabelFont', select=True)
        mc.iconTextRadioButton(width=44, height=22, label='Y',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, label='Z',  style='textOnly', font='tinyBoldLabelFont')
        mc.rowColumnLayout(parent='columnLayout4', enable=True, numberOfColumns=4, columnSpacing=[[2, 1], [3, 1], [4, 1]])
        mc.iconTextButton(width=44, height=22, enableBackground=True, label='Reset',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextCheckBox(width=44, height=22, label='P.Seam',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextCheckBox(width=44, height=22, label='Partial',  style='textOnly', font='tinyBoldLabelFont')
        mc.floatField(width=44, height=22, precision=3)


# build UI : Frame 'Step Snap'
        mc.frameLayout('step_Layout', parent='columnLayout1', collapsable=True, label='Step Snap')
        mc.columnLayout('columnLayout7')
        mc.rowColumnLayout(height=46, numberOfColumns=2)
        mc.iconTextCheckBox(width=44, height=44, image=self.path + 'snapPixel.png', label='Snap',  style='iconAndTextVertical', font='tinyBoldLabelFont')
        mc.rowColumnLayout(numberOfColumns=3, columnSpacing=[[2, 1], [3, 1]])
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, label='Relative',  style='textOnly', font='tinyBoldLabelFont' , select=True)
        mc.iconTextRadioButton(width=44, height=22, label='Absolute',  style='textOnly', font='tinyBoldLabelFont')
        mc.floatField(width=44, precision=3)
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, label='Edge',  style='textOnly', font='tinyBoldLabelFont' , select=True)
        mc.iconTextRadioButton(width=44, height=22, label='Surface',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextButton(width=44, height=22, label='Normals',  style='textOnly', font='tinyBoldLabelFont')
        mc.rowColumnLayout(parent='columnLayout7', enable=True, numberOfColumns=4, columnSpacing=[[2, 1], [3, 1], [4, 1]])
        mc.iconTextButton(width=44, height=22, enableBackground=True, label='Reset',  style='textOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioCollection()
        mc.iconTextRadioButton(width=44, height=22, image=self.path + 'snapGrid.png', style='iconOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, image=self.path + 'snapCurve.png', style='iconOnly', font='tinyBoldLabelFont')
        mc.iconTextRadioButton(width=44, height=22, image=self.path + 'snapPoint.png', style='iconOnly', font='tinyBoldLabelFont')

        # mc.showWindow(self.winName)
        # gMainWindow = pm.mel.eval('$tmpVar=$gMainWindow')
        allowedAreas = ['left', 'right']
        mc.toolBar(self.toolBarName, area='right', content=self.winName, allowedArea=allowedAreas) # , parent=gMainWindow)


# DEFINITION DES FONCTIONS D'INITIALISATION :

    def initPath(self):
        # self.path = "/homes/mte/maya/2016/scripts/kTools/icons/"
        # self.path = "E:/kTools/icons/"
        path_brut = os.path.realpath(__file__)
        path_norm = os.path.normpath(path_brut)  # os.path.normcase()
        path_clean = path_norm.replace("\\", "/")
        path_list = path_clean.split('/')[:-1]
        path_list.extend(['icons'])
        self.path = ''
        for item in path_list:
            self.path += item + '/'
        # print ">> :", self.path

    def isAutoAddNewObjsEnabled(self):
        iJob = pm.mel.eval('$temp = $isolateSelectAutoAddScriptJob')
        print "JOB ID >> :", iJob
        return mc.scriptJob(ex=iJob)

    def setIconTool(self, toolType):
        mc.iconTextStaticLabel(self.lb_tool, edit=True, image=self.path + toolType + '.png')

    def initSelectStyle(self):
        if mc.selectPref(q=True, paintSelect=True):
            mc.iconTextRadioButton(self.bt_dragSelStyle, edit=True,select=True)
            if mc.selectPref(q=True, paintSelectWithDepth=True):
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=True)
            else:
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=False)
        else:
            mc.iconTextRadioButton(self.bt_marqueeSelStyle, edit=True, select=True)
            if mc.selectPref(q=True, useDepth=True):
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=True)
            else:
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=False)

    def initScriptJobs(self):
        self.scriptJobIds.append(mc.scriptJob(parent=self.winName, event=("SelectModeChanged", catchJobException(self.actuTypeSelection))))
        self.scriptJobIds.append(mc.scriptJob(parent=self.winName, event=("SelectTypeChanged", catchJobException(self.actuTypeSelection))))
        self.scriptJobIds.append(mc.scriptJob(parent=self.winName, event=("SelectionChanged", catchJobException(self.actuSelection))))
        self.scriptJobIds.append(mc.scriptJob(parent=self.winName, event=("ToolChanged", catchJobException(self.actuToolSettings))))
        # self.scriptJobIds.append(mc.scriptJob(parent=self.winName,event=("ModelPanelSetFocus", catchJobException(self.testJob))))
        # self.scriptJobIds.append(mc.scriptJob(parent=self.winName,event=("modelEditorChanged", catchJobException(self.initDisplay))))

    def actuToolSettings(self):
        ctx = mc.currentCtx()
        ctxType = mc.contextInfo(ctx, c=True)
        # if self.wg_moveSettings.isVisible() or self.wg_rotateSettings.isVisible() or self.wg_scaleSettings.isVisible() or self.wg_nullSettings.isVisible():
        if ctxType == "manipMove":
            self.setIconTool("manipMove")
            mc.frameLayout(self.fl_tool, edit=True, label="Move Settings")
            # self.wg_rotateSettings.setVisible(False)
            # self.wg_scaleSettings.setVisible(False)
            # self.wg_nullSettings.setVisible(False)
            # self.wg_moveSettings.setVisible(True)
            # self.initMoveSettings()
        if ctxType == "manipRotate":
            self.setIconTool("manipRotate")
            mc.frameLayout(self.fl_tool, edit=True, label="Rotate Settings")
            # self.wg_moveSettings.setVisible(False)
            # self.wg_scaleSettings.setVisible(False)
            # self.wg_nullSettings.setVisible(False)
            # self.wg_rotateSettings.setVisible(True)
            # self.initRotateSettings()
        if ctxType == "manipScale":
            self.setIconTool("manipScale")
            mc.frameLayout(self.fl_tool, edit=True, label="Scale Settings")
            # self.wg_moveSettings.setVisible(False)
            # self.wg_rotateSettings.setVisible(False)
            # self.wg_nullSettings.setVisible(False)
            # self.wg_scaleSettings.setVisible(True)
            # self.initScaleSettings()
        if ctxType == "selectTool":
            self.setIconTool("selectTool")
            mc.frameLayout(self.fl_tool, edit=True, label="Tool Settings")
            # self.wg_moveSettings.setVisible(False)
            # self.wg_rotateSettings.setVisible(False)
            # self.wg_scaleSettings.setVisible(False)
            # self.wg_nullSettings.setVisible(True)

    def actuTypeSelection(self):
        if mc.selectMode(q=True, object=True):
            mc.iconTextRadioButton(self.bt_selObj, edit=True, select=True)
            mc.iconTextRadioButton(self.bt_selVert, edit=True, enableBackground=False)
            mc.iconTextRadioButton(self.bt_selEdge, edit=True, enableBackground=False)
            mc.iconTextRadioButton(self.bt_selFace, edit=True, enableBackground=False)
            mc.iconTextRadioButton(self.bt_selUv, edit=True, enableBackground=False)
            mc.iconTextRadioButton(self.bt_selMulti, edit=True, enableBackground=False)

        else:
            if mc.selectType(q=True, vertex=True):
                mc.iconTextRadioButton(self.bt_selObj, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selVert, edit=True, select=True)
                mc.iconTextRadioButton(self.bt_selEdge, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selFace, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selUv, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selMulti, edit=True, enableBackground=False)

            if mc.selectType(q=True, edge=True):
                mc.iconTextRadioButton(self.bt_selObj, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selVert, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selEdge, edit=True, select=True)
                mc.iconTextRadioButton(self.bt_selFace, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selUv, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selMulti, edit=True, enableBackground=False)

            if mc.selectType(q=True, facet=True):
                mc.iconTextRadioButton(self.bt_selObj, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selVert, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selEdge, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selFace, edit=True, select=True)
                mc.iconTextRadioButton(self.bt_selUv, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selMulti, edit=True, enableBackground=False)

            if mc.selectType(q=True, meshComponents=True):
                mc.iconTextRadioButton(self.bt_selObj, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selVert, edit=True, backgroundColor=self.selectColor)
                mc.iconTextRadioButton(self.bt_selEdge, edit=True, backgroundColor=self.selectColor)
                mc.iconTextRadioButton(self.bt_selFace, edit=True, backgroundColor=self.selectColor)
                mc.iconTextRadioButton(self.bt_selUv, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selMulti, edit=True, select=True)

            if mc.selectType(q=True, polymeshUV=True):
                mc.iconTextRadioButton(self.bt_selObj, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selVert, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selEdge, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selFace, edit=True, enableBackground=False)
                mc.iconTextRadioButton(self.bt_selUv, edit=True, select=True)
                mc.iconTextRadioButton(self.bt_selMulti, edit=True, enableBackground=False)

    def actuSelection(self):
        # self.initVisibility()
        # self.initDoubleSide()
        # self.initVisPivot()

        histNum = mc.optionMenu(self.om_history, query=True, numberOfItems=True) + 1
        print ">>>  : ", histNum
        mc.textField(self.tf_transformName, edit=True, text='')
        mc.textField(self.tf_shapeName, edit=True, text='')
        for n in range(1, histNum):
            itemName = "hist_" + str(n)
            mc.deleteUI(itemName, menuItem=True)
            print ">>> : ", itemName, " deleted !!"

        selectionList = mc.ls(selection=True, o=True)
        if selectionList:
            print selectionList[-1]
            history = mc.listHistory(selectionList, interestLevel=2)
            histNum = len(history)
            mc.textField(self.tf_transformName, edit=True, text=selectionList[-1])
            mc.textField(self.tf_shapeName, edit=True, text=history[0])
            mc.optionMenu(self.om_history, edit=True, numberOfItems=histNum)
            for n in range(1, histNum):
                selec = history[n]
                itemName = "hist_" + str(n)
                mc.menuItem(itemName, parent=self.om_history, label=selec)
        else:
            print "pas de selection"

    def openAttributEditor(self, histItem):
        pm.mel.showEditor(histItem)

    def closeEvent(self, event):
        print ">> Bye bye !"
        try:
            if self.scriptJobIds:
                for jobId in self.scriptJobIds:
                    mc.scriptJob(kill=jobId)
                    print ">> Job {0} killed".format(jobId)
        finally:
            return QtGui.QWidget.closeEvent(self, event)


# FONCTIONS APPELE PAR LES BOUTONS DE LA "KMAX TOOL BAR"

# COMMON SELECTION OPTIONS

# DEFINITION DES FONCTIONS D'INTERACTIONS :

# 'Common Selection Options'
    def renameTransform(self, txt):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            mc.rename(selectionList[-1], txt)
            print ">> Object New Name : " + txt
        else:
            print ">> You need a selection"
        self.actuSelection()

    def selectByName(self, txt):
        mc.select(txt)

    def selVertex(self, *args):
        mc.selectMode(component=True)
        mc.selectType(vertex=True)

    def selEdge(self, *args):
        mc.selectMode(component=True)
        mc.selectType(edge=True)

    def selFace(self, *args):
        mc.selectMode(component=True)
        mc.selectType(facet=True)

    def selObject(self, *args):
        mc.selectMode(object=True)

    def selMulti(self, *args):
        mc.selectMode(component=True)
        mc.selectType(meshComponents=True)

    def selUv(self, *args):
        mc.selectMode(component=True)
        mc.selectType(polymeshUV=True)