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

        self.initVisibility()
        self.actuSelection()
        self.actuTypeSelection()
        self.actuToolSettings()
        self.initSelectStyle()

    # BUILD UI

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


        # build UI : Common Selection Options

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
        self.bt_marqueeSelStyle = mc.iconTextRadioButton(width=44, height=22, label='Marquee',  style='textOnly', font='tinyBoldLabelFont', onCommand=self.selectionStyleSwitch)
        self.bt_dragSelStyle = mc.iconTextRadioButton(width=44, height=22, label='Drag',  style='textOnly', font='tinyBoldLabelFont', onCommand=self.selectionStyleSwitch)
        self.bt_tweakSelStyle = mc.iconTextRadioButton(width=44, height=22, label='Tweak',  style='textOnly', font='tinyBoldLabelFont')
        self.bt_camSwitch = mc.iconTextCheckBox(width=44, height=22, label='Cam B',  style='textOnly', font='tinyBoldLabelFont', changeCommand=self.camSwitch)
        mc.rowColumnLayout('rowColumnLayout4', parent='columnLayout2', numberOfColumns=2, columnWidth=[[1, 20], [2, 160]])
        mc.iconTextStaticLabel(width=20, height=20, image=self.path + 'transform.png')
        self.tf_transformName = mc.textField(enterCommand=self.renameTransform)
        mc.iconTextStaticLabel(width=20, height=20, image=self.path + 'shape.png')
        self.tf_shapeName = mc.textField(editable=False)
        mc.iconTextStaticLabel(width=20, height=20, image=self.path + 'constructionHistory.png')
        self.om_history = mc.optionMenu(changeCommand=self.openAttributEditor, alwaysCallChangeCommand=True, maxVisibleItems=10)
        mc.iconTextStaticLabel(width=20, height=20, image=self.path + 'quickRename.png')
        self.tf_selByName = mc.textField(placeholderText='select by name', enterCommand=self.selectByName)


        # build UI : Transform

        mc.frameLayout('transform_Layout', parent='columnLayout1', collapsable=True, label='Transform')
        mc.columnLayout('columnLayout3')
        mc.channelBox('channelBox1', width=180, height=192, # preventOverride=False,
                                    # attributeEditorMode=False,
                                    # containerAtToparent=False,
                                    precision=3,
                                    fixedAttrList=("translateX", "translateY", "translateZ", "rotateX", "rotateY",
                                                   "rotateZ", "scaleX", "scaleY", "scaleZ", 'visibility'))
        mc.gridLayout(numberOfRows=5, numberOfColumns=4, cellWidth=45, cellHeight=44)
        mc.iconTextButton(width=44, height=44, enableBackground=False, image=self.path + 'deleteHistory.png', command=self.deleteHistory)
        mc.iconTextButton(width=44, height=44, enableBackground=False, image=self.path + 'centerPivot.png', command=self.centerPivot)
        mc.iconTextButton(width=44, height=44, enableBackground=False, label='//',  style='textOnly', enable=False)
        self.bt_visibility = mc.iconTextCheckBox(width=44, height=44, image=self.path + 'visibility.png', changeCommand=self.visibility)
        mc.iconTextButton(width=44, height=44, enableBackground=False, image=self.path + 'resetTransform.png', command=self.resetAllTransform)
        mc.iconTextButton(width=44, height=44, enableBackground=False, image=self.path + 'matchTransform.png', command=self.matchAllTransforms)
        mc.iconTextButton(width=44, height=44, enableBackground=False, image=self.path + 'freezeTransform.png', command=self.freezeAllTransform)
        mc.iconTextButton(width=44, height=44, enableBackground=False, image=self.path + 'unfreeze.png', command=self.unFreeze)
        mc.gridLayout(parent='columnLayout3', numberOfRows=4, numberOfColumns=4, cellWidth=45, cellHeight=22)
        mc.iconTextButton(width=44, height=22, label='R.T', style='textOnly', image=self.path + 'resetSmall.png', command=self.resetTranslation)
        mc.iconTextButton(width=44, height=22, label='M.T', style='textOnly', image=self.path + 'matchSmall.png', command=self.matchTranslate)
        mc.iconTextButton(width=44, height=22, label='F.T', style='textOnly', image=self.path + 'freezeSmall.png', command=self.freezeTranslate)
        mc.iconTextButton(width=44, height=22, label='//',  style='textOnly', enable=False)
        mc.iconTextButton(width=44, height=22, label='R.R', style='textOnly', image=self.path + 'resetSmall.png', command=self.resetRotation)
        mc.iconTextButton(width=44, height=22, label='M.R', style='textOnly', image=self.path + 'matchSmall.png', command=self.matchRotate)
        mc.iconTextButton(width=44, height=22, label='F.R', style='textOnly', image=self.path + 'freezeSmall.png', command=self.freezeRotate)
        mc.iconTextCheckBox(width=44, height=22, image=self.path + 'snapToggle.png')
        mc.iconTextButton(width=44, height=22, label='R.S', style='textOnly', image=self.path + 'resetSmall.png', command=self.resetScaling)
        mc.iconTextButton(width=44, height=22, label='M.S', style='textOnly', image=self.path + 'matchSmall.png', command=self.matchScale)
        mc.iconTextButton(width=44, height=22, label='F.S', style='textOnly', image=self.path + 'freezeSmall.png', command=self.freezeScale)
        mc.iconTextButton(width=44, height=22, label='//',  style='textOnly', enable=False)


        # build UI : Display

        mc.frameLayout('display_Layout', parent='columnLayout1', collapsable=True, label='Display')


        # build UI : Tool Settings

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


        # build UI : Soft selection

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


        # build UI : Symmetry

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


        # build UI : Step Snap

        mc.frameLayout('step_Layout', parent='columnLayout1', collapsable=True, label='Step & Snap')
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
            mc.iconTextRadioButton(self.bt_dragSelStyle, edit=True, select=True)
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

    def initVisibility(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            #selectionList = mc.ls(selection=True, type='transform')
            stateVIS = mc.getAttr(selectionList[-1] + ".visibility")
            if stateVIS:
                mc.iconTextCheckBox(self.bt_visibility, edit=True, value=True)
            else:
                mc.iconTextCheckBox(self.bt_visibility, edit=True, value=False)

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
            mc.iconTextRadioButton(self.bt_tweakSelStyle, edit=True, enable=True)
            # self.wg_rotateSettings.setVisible(False)
            # self.wg_scaleSettings.setVisible(False)
            # self.wg_nullSettings.setVisible(False)
            # self.wg_moveSettings.setVisible(True)
            # self.initMoveSettings()
        if ctxType == "manipRotate":
            self.setIconTool("manipRotate")
            mc.frameLayout(self.fl_tool, edit=True, label="Rotate Settings")
            mc.iconTextRadioButton(self.bt_tweakSelStyle, edit=True, enable=True)
            # self.wg_moveSettings.setVisible(False)
            # self.wg_scaleSettings.setVisible(False)
            # self.wg_nullSettings.setVisible(False)
            # self.wg_rotateSettings.setVisible(True)
            # self.initRotateSettings()
        if ctxType == "manipScale":
            self.setIconTool("manipScale")
            mc.frameLayout(self.fl_tool, edit=True, label="Scale Settings")
            mc.iconTextRadioButton(self.bt_tweakSelStyle, edit=True, enable=True)
            # self.wg_moveSettings.setVisible(False)
            # self.wg_rotateSettings.setVisible(False)
            # self.wg_nullSettings.setVisible(False)
            # self.wg_scaleSettings.setVisible(True)
            # self.initScaleSettings()
        if ctxType == "selectTool":
            self.setIconTool("selectTool")
            mc.frameLayout(self.fl_tool, edit=True, label="Tool Settings")
            mc.iconTextRadioButton(self.bt_tweakSelStyle, edit=True, enable=False)
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
        self.initVisibility()
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
            # print selectionList[-1]
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
            mc.iconTextCheckBox(self.bt_visibility, edit=True, value=False)
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


    # DEFINITION DES FONCTIONS D'INTERACTIONS :

    # Common Selection Options

    def selObject(self, *args):
        mc.selectMode(object=True)

    def selMulti(self, *args):
        mc.selectMode(component=True)
        mc.selectType(meshComponents=True)

    def selUv(self, *args):
        mc.selectMode(component=True)
        mc.selectType(polymeshUV=True)

    def selVertex(self, *args):
        mc.selectMode(component=True)
        mc.selectType(vertex=True)

    def selEdge(self, *args):
        mc.selectMode(component=True)
        mc.selectType(edge=True)

    def selFace(self, *args):
        mc.selectMode(component=True)
        mc.selectType(facet=True)

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

    def selectionStyleSwitch(self, *args):
        if mc.selectPref(query=True, paintSelect=True):
            mc.selectPref(paintSelect=False)
            mc.iconTextRadioButton(self.bt_marqueeSelStyle, edit=True, select=True)
            #self.bt_selectionStyle.setText("Marquee")
            print ">> Selection mode is MARQUEE."
            if mc.selectPref(query=True, useDepth=True):
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=True)
                #self.bt_camSwitch.setChecked(True)
                #self.buttonOn(self.bt_camSwitch)
            else:
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=False)
                #self.bt_camSwitch.setChecked(False)
                #self.buttonOff(self.bt_camSwitch)
        else:
            mc.selectPref(paintSelect=True)
            mc.iconTextRadioButton(self.bt_dragSelStyle, edit=True, select=True)
            #self.bt_selectionStyle.setText("Drag")
            print ">> Selection mode is DRAG."
            if mc.selectPref(query=True, paintSelectWithDepth=True):
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=True)
                #self.bt_camSwitch.setChecked(True)
                #self.buttonOn(self.bt_camSwitch)
            else:
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=False)
                #self.bt_camSwitch.setChecked(False)
                #self.buttonOff(self.bt_camSwitch)

    def camSwitch(self, *args):
        if mc.selectPref(q=True, paintSelect=True):
            if mc.selectPref(q=True, paintSelectWithDepth=True):
                mc.selectPref(paintSelectWithDepth=False)
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=False)
            else:
                mc.selectPref(paintSelectWithDepth=True)
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=True)
        else:
            if mc.selectPref(q=True, useDepth=True):
                mc.selectPref(useDepth=0)
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=False)
            else:
                mc.selectPref(useDepth=1)
                mc.iconTextCheckBox(self.bt_camSwitch, edit=True, value=True)


    # Transform menu :

    def deleteHistory(self):
        mc.DeleteHistory()
        print ">> History Deleted"

    def centerPivot(self):
        mc.CenterPivot()
        print ">> Center Pivot"

    def visibility(self, *args):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            state = mc.getAttr(selectionList[-1] + ".visibility")
            if state:
                mc.setAttr(selectionList[-1] + ".visibility", 0)
                mc.iconTextCheckBox(self.bt_visibility, edit=True, value=False)
            else:
                mc.setAttr(selectionList[-1] + ".visibility", 1)
                mc.iconTextCheckBox(self.bt_visibility, edit=True, value=True)
        else:
            mc.iconTextCheckBox(self.bt_visibility, edit=True, value=False)
            print ">> No selection"


    def resetTranslation(self):
        '''
        Reset object Translation to the origin (0,0,0)
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        else:
            for obj in selectionList:
                mc.xform(obj, absolute=True, t=[0, 0, 0])

    def resetRotation(self):
        '''
        Reset object Rotation to (0,0,0)
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        else:
            for obj in selectionList:
                mc.xform(obj, absolute=True, ro=[0, 0, 0])

    def resetScaling(self):
        '''
        Reset object Scaling to (1,1,1)
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        else:
            for obj in selectionList:
                mc.xform(obj, absolute=True, s=[1, 1, 1])

    def resetAllTransform(self):
        """
        Reset All Transform on selected Objects
        """
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        else:
            for obj in selectionList:
                mc.xform(obj, absolute=True, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])


    def matchTranslate(self):
        selectionList = mc.ls(selection=True, type='transform')
        if len(selectionList) >= 2:
            newTranslation = mc.xform(selectionList[-1], q=True, translation=True, worldSpace=True)
            for objMacth in selectionList[:-1]:
                mc.xform(objMacth, p=True, translation=newTranslation, worldSpace=True)
            print ">> Match Translate"
        else:
            print ">> No good Selection"

    def matchRotate(self):
        selectionList = mc.ls(selection=True, type='transform')
        if len(selectionList) >= 2:
            newRotation = mc.xform(selectionList[-1], q=True, rotation=True, worldSpace=True)
            for objMacth in selectionList[:-1]:
                mc.xform(objMacth, p=True, rotation=newRotation, worldSpace=True)
            print ">> Match Rotate"
        else:
            print ">> No good Selection"

    def matchScale(self):
        selectionList = mc.ls(selection=True, type='transform')
        if len(selectionList) >= 2:
            newScale = mc.xform(selectionList[-1], q=True, scale=True)
            for objMacth in selectionList[:-1]:
                mc.xform(objMacth, p=True, scale=newScale)
            print ">> Match Scale"
        else:
            print ">> No good Selection"

    def matchAllTransforms(self):
        self.matchTranslate()
        self.matchRotate()
        self.matchScale()
        # mc.select(selectionList[0], replace=True)
        print ">> Match All Transfroms"


    def freezeTranslate(self):
        '''
        Freeze object Translation to (0,0,0)
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        else:
            mc.makeIdentity(a=1, t=1, r=0, s=0, n=0, pn=1)
            print ">> Translate Freezed"
        self.actuSelection()  # actualiser les valeurs de transform

    def freezeRotate(self):
        '''
        Freeze object Rotation to (0,0,0)
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        else:
            mc.makeIdentity(a=1, t=0, r=1, s=0, n=0, pn=1)
            print ">> Rotate Freezed"
        self.actuSelection()  # actualiser les valeurs de transform

    def freezeScale(self):
        '''
        Freeze object Scale to (0,0,0)
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        else:
            mc.makeIdentity(a=1, t=0, r=0, s=1, n=0, pn=1)
        print ">> Scale Freezed"
        self.actuSelection()  # actualiser les valeurs de transform

    def freezeAllTransform(self):
        '''
        Freeze All Transform on selected Objects
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        else:
            mc.makeIdentity(a=1, t=1, r=1, s=1, n=1, pn=1)
            print ">> All transformations Freezed"
        self.actuSelection()  # actualiser les valeurs de transform


    def unFreeze(self):
        def cleanupUnfreeze(*args):
            sel = pm.ls(sl=1)

            nodes = pm.ls(args)
            if not nodes:
                nodes = sel
            nodes = pm.ls(nodes, type='transform')
            if not nodes:
                raise RuntimeError()

            for node in nodes:
                _t = node.t.get()
                _rp = node.rp.get()
                _rpt = node.rpt.get()

                _shape = None
                shapes = node.getShapes()
                if shapes:
                    _shape = pm.createNode('transform', p=node)
                    for _sh in shapes:
                        _sh.setParent(_shape, r=1, s=1)
                    _shape.setParent(w=1)

                children = node.getChildren(type='transform')
                for _ch in children:
                    if not (node.t.isSettable() and node.r.isSettable() and node.s.isSettable()):
                        pm.warning('cleanupUnfreeze: "%s" (child of "%s") have locked or connected transformations!' % (
                            str(_ch), str(node)))
                    _ch.setParent(w=1)

                node.rp.set(0, 0, 0)
                node.sp.set(0, 0, 0)
                node.rpt.set(0, 0, 0)
                node.spt.set(0, 0, 0)
                node.t.set(_t + _rp + _rpt)

                for _ch in children:
                    _ch.setParent(node)

                if _shape:
                    _shape.setParent(node)
                    pm.makeIdentity(_shape, a=1)
                    for _sh in shapes:
                        _sh.setParent(node, r=1, s=1)
                    pm.delete(_shape)

            pm.select(sel)

        cleanupUnfreeze()

    '''
    def visPivot(self):
        selectionList = mc.ls(selection=True, type='transform')
        stateScalePivot = mc.getAttr(selectionList[-1] + ".displayScalePivot")
        stateRotatePivot = mc.getAttr(selectionList[-1] + ".displayRotatePivot")
        if stateScalePivot:
            mc.setAttr(selectionList[-1] + ".displayScalePivot", 0)
            mc.setAttr(selectionList[-1] + ".displayRotatePivot", 0)
            self.buttonOff(self.bt_visPivot)
        else:
            mc.setAttr(selectionList[-1] + ".displayScalePivot", 1)
            mc.setAttr(selectionList[-1] + ".displayRotatePivot", 1)
            self.buttonOn(self.bt_visPivot)
            
    def doubleSide(self):
        # selectionList = mc.ls( selection=True, type='mesh' )
        print ">> button doubleside is DISABLE !"
        startSelection = mc.ls(selection=True)#, type="transform")
        selShapes = mc.listRelatives(startSelection, shapes=True)
        selLocShapes = mc.ls(type='locator')
        for obj in selLocShapes:
            selShapes.remove(obj)
        selectionList = mc.listRelatives(selShapes, p=True)

        state = mc.getAttr(selectionList[-1]+".doubleSided")
        if selectionList:
            for obj in selectionList:
                if state:
                    mc.setAttr(obj+".doubleSided", 0)
                    self.bt_doubleSide.setStyleSheet("background-color: "+self.unSelectColor+";\n"
                                                    "selection-background-color: "+self.selectColor+";\n")
                else:
                    mc.setAttr(obj+".doubleSided", 1)
                    self.bt_doubleSide.setStyleSheet("background-color: "+self.selectColor+";\n"
                                                    "selection-background-color: rgb(150, 150, 150);\n")        

    def selNgones(self):
        mel.eval(
            'polyCleanupArgList 3 { "0","2","1","0","1","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" };')
        print ">> nGones selected"

    def tglDisplayNormals(self):
        startSelection = mc.ls(selection=True, exactType="transform")
        if startSelection:
            selShapes = mc.listRelatives(startSelection, shapes=True)
            if selShapes:
                # stateNormals = mc.polyOptions(selShapes[-1], displayNormal=True, query=True)[0]
                stateNormals = mc.getAttr(selShapes[-1] + '.displayNormal')
                # print ">> ", startSelection, selShapes[-1], stateNormals

                if stateNormals:
                    for obj in selShapes:
                        mc.polyOptions(obj, displayNormal=False)
                        # mc.setAttr(obj + '.displayNormal', False)
                    msg = ">> Display Normals OFF"
                else:
                    for obj in selShapes:
                        mc.polyOptions(obj, displayNormal=True, facet=True, point=False, sizeNormal=1)
                        # mc.setAttr(obj + '.displayNormal', True)
                    msg = ">> Display Normals ON"
            else:
                msg = ">> No Shape selected"
        else:
            msg = ">> No Selection"

        print msg

    def noHistory(self):
        history = mc.constructionHistory(q=True, tgl=True)
        if history:
            mc.constructionHistory(tgl=False)
            self.buttonOff(self.bt_noHistory)
            print ">> Without Construction History !!!"
        else:
            mc.constructionHistory(tgl=True)
            self.buttonOn(self.bt_noHistory)
            print ">> With Construction History"
 
    def alignX(self):
        selectionList = mc.ls(selection=True)
        if selectionList:
            mc.scale(0, selectionList, relative=True, objectCenterPivot=True, scaleX=1)
        print ">> Selected components align on X"

    def alignY(self):
        selectionList = mc.ls(selection=True)
        if selectionList:
            mc.scale(0, selectionList, relative=True, objectCenterPivot=True, scaleY=1)
        print ">> Selected components align on Y"

    def alignZ(self):
        selectionList = mc.ls(selection=True)
        if selectionList:
            mc.scale(0, selectionList, relative=True, objectCenterPivot=True, scaleZ=1)
        print ">> Selected components align on Z"

    def makeLiveMesh(self):
        selectionList = mc.ls(selection=True, type='transform')
        # buttonState = self.bt_makeLive.isChecked(q=True)
        if selectionList:
            if self.makeLiveState:
                mc.makeLive(none=True)
                self.makeLiveState = 0
                self.buttonOff(self.bt_makeLive)
                print ">>", selectionList[-1], "is DEAD"
            else:
                mc.makeLive(selectionList[-1])
                self.makeLiveState = 1
                self.buttonOn(self.bt_makeLive)
                print ">>", selectionList[-1], "is aLIVE"
        else:
            mc.makeLive(none=True)
            self.makeLiveState = 0
            self.buttonOff(self.bt_makeLive)
            print ">> No selection // All is DEAD"
    '''