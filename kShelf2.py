import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm
import os
from time import localtime, strftime


class KShelf():
    def __init__(self):
        path = "E:/kTools/icons/"
        iconSize = 28
        separatorSize = 12
        wscName = "kSh"

        self.initPath()

        windowName = "kShelf2Window"
        self.toolName = "kShelf2"

        if mc.window(windowName, q=True, exists=True):
            mc.deleteUI(windowName)

        if mc.toolBar(self.toolName, q=True, exists=True):
            mc.deleteUI(self.toolName)

        myWindow = mc.window(windowName)

        allButtons = [("bt_kMaxToolBar", "kMaxTool32.png", "kMaxTool32b.png", "Launch kMaxTools", self.kMaxTool),
                      #("bt_kMaxToolBar2", "kMaxTool32.png", "kMaxTool32b.png", "Launch kMaxTools", self.kMaxUi2),
                      ("bt_separator_00", "separateHor.png", "separateHor.png", "", ""),
                      ("bt_kMod", "kMaxMod32.png", "kMaxMod32.png", "Launch kMod Left bar", self.kMod),
                      ("bt_kMaxShelfTop", "kMaxShelfTop32.png", "kMaxShelfTop32.png", "Launch kMaxShelfTop", self.kMaxShelfTop),
                      ("bt_outlinerView", "outliner.png", "outliner.png", "Outliner/Persp", self.kmOutlinerView),
                      ("bt_singlePerspView", "singlePerspLayout2016_32.png", "singlePerspLayout2016_32.png", "Single Perspective View", self.kmSinglePerspView),
                      ("bt_fourView", "fourViewLayout2016_32.png", "fourViewLayout2016_32.png", "Four View", self.kmFourView),
                      ("bt_separator_01", "separateHor.png", "separateHor.png", "", ""),
                      ("bt_new", "new.png", "new.png", "Create a New Scene", self.kmNew),
                      ("bt_classicOpen", "open.png", "open.png", "Open a Scene", self.kmClassicOpenScene),
                      ("bt_classicSave", "save.png", "save.png", "Save the current Scene", self.kmClassicSave),
                      ("bt_savePlus", "save+.png", "save+.png", "Incrementale Save", self.kmSavePlus),
                      ("bt_classicSaveAs", "saveAs.png", "saveAs.png", "Save the current scene under a new name or export all", self.kmClassicSaveAs),
                      ("bt_import", "import.png", "import.png", "Import file", self.kmImport),
                      ("bt_export", "export.png", "export.png", "Export entire scene into one file", self.kmExport),
                      ("bt_exportSel", "exportSel.png", "exportSel.png", "Export Selection...", self.kmExportSel),
                      ("bt_referenceEditor", "reference.png", "reference.png", "Reference Editor", self.kmReferenceEditor),
                      ("bt_separator_02", "separateHor.png", "separateHor.png",  "", ""),
                      ("bt_open", "teamtTo.png", "teamtTo.png", "Open a Scene", self.kmOpen),
                      ("bt_save", "tt_save2_b.png", "tt_save2_b.png", "Save the current Scene", self.kmSave),
                      ("bt_saveAs", "tt_saveAs2_b.png", "tt_saveAs2_b.png", "Save the current scene under a new name or export all", self.kmSaveAs),
                      ("bt_exportProps", "exportSelb.png", "exportSelb.png", "Export Prop", self.kmExportProps),
                      ("bt_checkPublishable", "tt_checkPublish_b.png", "tt_checkPublish_b.png", "Check Publishability", self.kmCheckPublishable),
                      ("bt_compareGeom", "compareGeom.png", "compareGeom.png", "Compare OLD with NEW", self.kmCompareGeom),
                      ("bt_hardwareShader", "hardwareShader.png", "hardwareShader.png", "Apply hardwareShader on pxr shader", self.kmHardwareShader),
                      ("bt_buildPresScene", "buildPres.png", "buildPres.png", "build presentation scene", self.buildPresentationScene),
                      ("bt_launchPresScene", "launchPres.png", "launchPres.png", "launch presentation scene", self.launchPresentationRender),
                      #("bt_separator_03", "separateHor.png", "separateHor.png",  "", ""),
                      ("bt_separator_04", "separateHor.png", "separateHor.png",  "", ""),
                      ("bt_outliner", "outliner32.png", "outliner32.png", "Outliner", self.kmOutliner),
                      ("bt_nameSpaceEditor", "nameSpaceEditor.png", "nameSpaceEditor.png", "Namespace Editor", self.kmNameSpaceEditor),
                      ("bt_nodeEditor", "nodeEditor.png", "nodeEditor.png", "Node Editor", self.kmNodeEditor),
                      ("bt_hyperShade", "hyperShade.png", "hyperShade.png", "Hypershade", self.kmHyperShade),
                      ("bt_textureEditor", "uvTextureEditor.png", "uvTextureEditor.png", "UV Texture Editor", self.kmUVTextureEditor),
                      ("bt_uvSnapshot", "uvSnapshot.png", "uvSnapshot.png", "UV Snapshot", self.uvSnapshot),
                      ("bt_relationshipEditor", "relation32.png", "relation32b.png", "Relation Ship Editor", self.kmRelationShipEditor),
                      ("bt_separator_05", "separateHor.png", "separateHor.png",  "", ""),
                      ("bt_colorPicker", "colorPicker.png", "colorPicker.png", "Color Shader Picker", self.kmColorPicker),
                      ("bt_randomizer", "kRandomizer32.png", "kRandomizer32.png", "Randomizer", self.kmRandomizer),
                      ("bt_replacer", "kReplacer32.png", "kReplacer32.png", "kReplacer", self.kmReplacer),
                      ("bt_frRenamer", "text-32.png", "text-32.png", "FrRenamer", self.frRenamer),
                      ("bt_setSmooth", "smoothSetTool.png", "smoothSetTool.png", "Set smooth tool", self.kmSetSmoothGroupTool),
                      ("bt_separator_06", "separateHor.png", "separateHor.png", "", ""),
                      ("bt_switchDisplayPoly", "switchAllPoly32.png", "switchAllPoly32.png", "Switch display ALL/POLY", self.kmSwitchDisplayPoly),
                      ("bt_switchLighting", "lighting.png", "lighting.png", "Switch Lighting", self.kmSwitchLighting),
                      ("bt_switchBallPreview", "globe_2.png", "globe_2.png", "Switch renderThumbnailUpdate", self.kmSwitchBallPreview),
                      ("bt_unlockAllAtt", "unlock.png", "unlock.png", "Unlock all attributs", self.kmUnlockAllAtt),
                      ("bt_deleteUnAutorisedNodes", "delUnusedNode32.png", "delUnusedNode32.png", "Delete all unautorised nodes", self.delUnautorisedNodes),
                      ("bt_cleanRmanRdrOptions", "cleanRmanRdrOpions.png", "cleanRmanRdrOpions.png", "clean renderman render options", self.cleanRdrmanRdrOptions),
                      ("bt_clean", "kCleaner.png", "kCleaner.png", "Cleaner tool", self.kmCleanTool),
                      ("bt_spacer", "empty.png", "empty.png", "", ""),
                      ("bt_uiDesigner", "uid.png", "uid.png", "UI Designer", self.kmUiDesigner),
                      ("bt_connectPC", "connectPC.png", "connectPC.png", "Connect Maya to PyCharm", self.kmConnectPC),
                      ("bt_preferences", "settings.png", "settings.png", "Preferences", self.kmSetting),
                      ("bt_hotkeys", "hotkey.png", "hotkey.png", "Hotkeys Editor", self.kmHotKey),
                      ("bt_plugins", "plugin.png", "plugin.png", "Plug-ins Manager", self.kmPlugIn),
                      ("bt_separator_07", "separateHor.png", "separateHor.png",  "", ""),
                      ("bt_attributeEditor", "attributes.png", "attributes.png", "Attribute Editor", self.kmAttributeEditor),
                      ("bt_channelBox", "channelBox.png", "channelBox.png", "Channel Box", self.kmChannelBox),
                      ("bt_modelingToolKit", "modelToolkit.png", "modelToolkit.png", "Modeling Tool Kit", self.kmModelingToolKit),
                      ("bt_toolSettings", "toolSettings.png", "toolSettings.png", "Tool Settings", self.kmToolSettings),
                      ("bt_layerEditor", "layerEditor.png", "layerEditor.png", "Layer Editor", self.kmLayerEditor),
                      ("bt_separator_08", "separateHor.png", "separateHor.png", "", ""),
                      # ("bt_clock", "clock32.png", "clock32b.png", "Actualise clock", self.kmClock),
                      # ("bt_h01", "digit8.png", "digit8.png", "", ""),
                      # ("bt_h02", "digit8.png", "digit8.png", "", ""),
                      # ("bt_clockSeparator", "digitSeparator.png",  "digitSeparator.png", "", ""),
                      # ("bt_m01", "digit8.png", "digit8.png", "", ""),
                      # ("bt_m02", "digit8.png", "digit8.png", "", ""),
                      # ("bt_separator", "separateHor.png", "separateHor.png", "", ""),
                      ("bt_reduce", "minimize32.png", "minimize32.png", "Minimize Maya", self.kmMinimizeMaya),
                      ("bt_toggleInterfaceLines", "toggleLines32.png", "toggleLines32.png", "Toggle interface Lines", self.kmToggleInterfaceLines),
                      ("bt_toggleToolBars", "toggleInterface32.png", "toggleInterface32.png", "Toggle interface Tools Bars", self.kmToggleToolBars),
                      ("bt_close", "close32.png", "close32.png", "Quit Maya", self.kmCloseMaya)
                      ]

        mc.rowColumnLayout(numberOfRows = 1, rowHeight=(1, iconSize))

        for btnName, imgFileName, imgHltFileName, btnAnnotation, btnCommand in allButtons:
            '''
            if btnName == "bt_h01":
                self.bt_h01 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
            if btnName == "bt_h02":
                self.bt_h02 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
            if btnName == "bt_m01":
                self.bt_m01 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
            if btnName == "bt_m02":
                self.bt_m02 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
            if imgFileName == "digitSeparator.png":
                mc.iconTextButton(btnName, edit=True,
                                            width=10,
                                            enable=0)
            '''

            if imgFileName != "digit8.png" :
                btnName = mc.iconTextButton(image1=self.target + imgFileName,
                                            highlightImage=self.target + imgHltFileName,
                                            annotation=btnAnnotation,
                                            command=btnCommand,
                                            width=iconSize)

            if imgFileName == "separateHor.png":
                mc.iconTextButton(btnName, edit=True,
                                            width=separatorSize,
                                            enable=0)

            if imgFileName == "empty.png":
                mc.iconTextButton(btnName, edit=True,
                                            width=200,
                                            enable=0)

        allowedAreas = ['top', 'bottom']
        mc.toolBar(self.toolName, area='top', content=myWindow, allowedArea=allowedAreas)

        # self.kmClock()

    def initPath(self):
        # self.target = "/homes/mte/maya/2016/scripts/kTools/icons/"
        path_brut = os.path.realpath(__file__)
        path_norm = os.path.normpath(path_brut)  # os.path.normcase()
        path_clean = path_norm.replace("\\", "/")
        path_list = path_clean.split('/')[:-1]
        path_list.extend(['icons'])
        self.target = ''
        for item in path_list:
            self.target += item + '/'
        # print ">> :", self.target

    def kMaxTool(self):
        import kTool
        reload(kTool)
        kTool.KTool()

    def kMaxUi2(self):
        import kMaxUi2
        reload(kMaxUi2)

    def kMod(self):
        import kMod2
        reload(kMod2)

    def kMaxShelfTop(self):
        import kShelf2
        reload(kShelf2)

    def kmNew(self):
        pm.mel.NewScene()

    def kmOpen(self):
        pm.mel.OpenScene()

    def kmSave(self):
        pm.mel.SaveScene()

    def kmSavePlus(self):
        pm.mel.IncrementAndSave()

    def kmSaveAs(self):
        pm.mel.SaveSceneAs()

    def kmImport(self):
        pm.mel.Import()

    def kmExport(self):
        pm.mel.Export()

    def kmExportSel(self):
        pm.mel.ExportSelection()

    def kmExportProps(self):
        pm.mel.tak_ExportProp()

    def kmConnectPC(self):
        # connection maya / pycharm
        if not mc.commandPort(':4434', q=True):
            mc.commandPort(n=':4434')

    def kmSetting(self):
        pm.mel.PreferencesWindow()

    def kmHotKey(self):
        pm.mel.HotkeyPreferencesWindow()

    def kmPlugIn(self):
        pm.mel.PluginManager()

    def kmOutliner(self):
        # Create a new regular outliner in its own window
        mc.window(title="Outliner", toolbox=True)
        mc.frameLayout(labelVisible=False, width=300, height=500)
        panel = mc.outlinerPanel()
        outliner = mc.outlinerPanel(panel, query=True, outlinerEditor=True)
        mc.outlinerEditor(outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList',
                          showShapes=False, showReferenceNodes=False, showReferenceMembers=False, showAttributes=False,
                          showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True,
                          ignoreDagHierarchy=False, expandConnections=False, showNamespace=True, showCompounds=True,
                          showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False,
                          doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True,
                          setFilter='defaultSetFilter')
        mc.showWindow()

    def kmReferenceEditor(self):
        pm.mel.ReferenceEditor()

    def kmHyperShade(self):
        pm.mel.HypershadeWindow()

    def kmNodeEditor(self):
        pm.mel.NodeEditorWindow()

    def kmUVTextureEditor(self):
        pm.mel.TextureViewWindow()

    def kmNameSpaceEditor(self):
        pm.mel.NamespaceEditor()

    def kmRelationShipEditor(self):
        pm.mel.SetEditor()

    def kmModelingToolKit(self):
        pm.mel.ToggleModelingToolkit()

    def kmAttributeEditor(self):
        # imageOne = mc.iconTextButton(self.bt_attributeEditor, image1=1, q=True)
        #         if imageOne == self.target + "attribute32.png":
        #     mc.iconTextButton(self.bt_attributeEditor, image1=self.target + "attribute32b.png", highlightImage=self.target + "attribute32.png", e=True)
        # else:
        #     mc.iconTextButton(self.bt_attributeEditor, image1=self.target + "attribute32.png", highlightImage=self.target + "attribute32b.png", e=True)

        # mc.iconTextButton(bt_attributeEditor, backgroundColor=(103, 141, 178))
        pm.mel.ToggleAttributeEditor()

    def kmToolSettings(self):
        pm.mel.ToggleToolSettings()

    def kmLayerEditor(self, *args):
        pm.mel.ToggleLayerBar()

    def kmChannelBox(self, *args):
        pm.mel.ToggleChannelBox()

    def kmSinglePerspView(self):
        pm.mel.setNamedPanelLayout("Single Perspective View")

    def kmFourView(self):
        pm.mel.setNamedPanelLayout("Four View")

    def kmOutlinerView(self):
        pm.mel.ToggleOutliner()
        # pm.mel.setNamedPanelLayout("Persp/Outliner")

    def kmScriptView(self):
        pm.mel.setNamedPanelLayout("Script/View")

    def kmColorPicker(self):
        import kColorizer
        reload(kColorizer)

    def kmRandomizer(self):
        import kRandomizer
        reload(kRandomizer)

    def kmReplacer(self):
        import kReplacer
        reload(kReplacer)

    def frRenamer(self):
        import renamer.renamer as renamer
        reload(renamer)

        class_renamer = renamer.Renamer()
        class_renamer.UI()

    def kmSetSmoothGroupTool(self):
        # import setSmoothGroupTool
        # reload(setSmoothGroupTool)
        import kSmoothSetTool
        reload(kSmoothSetTool)

    def kmCleanTool(self):
        import kCleaner

        reload(kCleaner)
        # clean.kmCleaner()

    def kmUiDesigner(self):
        # import sys
        # sys.path.append('e:\\sdd_UIDesigner_new\\scripts\\')
        # import sdd_UIDNew
        # reload(sdd_UIDNew)
        from sdd_UIDNew import UIDesigner
        execfile('E:\\sdd_UIDesigner_new\\scripts\\sdd_UIDNew.py')
        UIDesigner('E:\\sdd_UIDesigner_new\\scripts\\').show()

    def kmSwitchDisplayPoly(self):
        allModelPanel = mc.getPanel(type='modelPanel')
        if allModelPanel:
            for modelPanelName in allModelPanel:
                print ">> ", mc.modelEditor(modelPanelName, nCloths=1, q=1)
                if mc.modelEditor(modelPanelName, nCloths=1, q=1):
                    mc.modelEditor(modelPanelName, allObjects=0, e=1)
                    mc.modelEditor(modelPanelName, polymeshes=1, e=1)
                else:
                    mc.modelEditor(modelPanelName, allObjects=1, e=1)

    def kmSwitchLighting(self):
        item = mc.ls("*:c_lighting_work")
        if item != []:
            if mc.referenceQuery(item, isNodeReferenced=True):
                refFile = mc.referenceQuery(item, filename=True)
                mc.file(refFile, removeReference=True)
        else:
            mc.file(
                "//tak_server/projets/take-it-easy-mike/tak_maya/scenes/lights/for_work/lighting_shading_work/lighting_shading_work_v000.ma",
                r=1, type="mayaAscii", ignoreVersion=1, mergeNamespacesOnClash=1, namespace="", options="v=0;", pr=1)

    def kmSwitchBallPreview(self):
        renderBall = mc.renderThumbnailUpdate(q=True)
        if renderBall:
            mc.renderThumbnailUpdate(False)
            print ">> Render Thumbnail OFF"
        else:
            mc.renderThumbnailUpdate(True)
            print ">> Render Thumbnail ON"

    def kmUnlockAllAtt(self):
        selectionList = mc.ls(selection=True, l=True)
        if selectionList:
            lock_l = mc.listRelatives(selectionList, ad=True, type='transform', f=True)
            lock_l = sorted(lock_l, key=lambda s: s.count('|'), reverse=False)

            transformAttr_l = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.shearXY', '.shearXZ',
                               '.shearYZ', '.rotateAxisX', '.rotateAxisY', '.rotateAxisZ', '.visibility']
            # transform_global_l = ['.translate', '.rotate', '.scale', '.shear']

            for obj in lock_l:
                obj_sn = obj.split('|')[-1:][0]
                if mc.nodeType(obj) == 'transform' and ':' not in obj:
                    if obj_sn.startswith('c_') != True:
                        for attr in transformAttr_l:
                            mc.setAttr(obj + attr, lock=False)
                        print obj + " >> All Attributs unlock !"

    def delUnautorisedNodes(self):
        mentalrayNodes = ("mentalrayItemsList", "mentalrayGlobals")
        turtleNodes = ("TurtleBakeLayerManager", "TurtleDefaultBakeLayer", "TurtleRenderOptions", "TurtleUIOptions")
        ilrNodes = ("ilrBakeLayer", "ilrOptionsNode", "ilrBakeLayerManager", "ilrUIOptionsNode")
        otherNodes = ("poseInterpolatorManager", "shapeEditorManager", "ProductionRapidHair", "ProductionRapidFur",
                      "Preview", "PreviewMotionblur", "poseInterpolatorManager", "ProductionRapidMotion",
                      "PreviewFinalGather", "Draft", "poseInterpolatorManager2", "poseInterpolatorManager1",
                      "ProductionMotionblur", "DraftMotionBlur", "PreviewGlobalIllum", "PreviewRapidMotion",
                      "PreviewCaustics", "PreviewImrRayTracyOn", "shapeEditorManager1", "shapeEditorManager2",
                      "miContourPreset", "PreviewImrRayTracyOff", "ProductionFineTrace", "Production",
                      "DraftRapidMotion", "miDefaultOptions", "miDefaultOptions1", "miDefaultFramebuffer",
                      "hyperShadePrimaryNodeEditorSavedTabsInfo",)
        allNodes = mentalrayNodes + turtleNodes + ilrNodes + otherNodes
        plop = 0
        for node in allNodes:
            if mc.ls(node) != []:
                mc.lockNode(node, lock=False)
                mc.select(node)
                mc.delete()
                plop += 1
                print ">> : ", node, "deleted !"
            else:
                print ">> : ", node, "not in this scene !"
        print ">> : ", plop, " node(s) deleted ! "

    def cleanRdrmanRdrOptions(self):
        a = ""
        mc.setAttr("defaultRenderGlobals.preMel", a, type="string")
        mc.setAttr("defaultRenderGlobals.postMel", a, type="string")
        mc.setAttr("defaultRenderGlobals.preRenderLayerMel", a, type="string")
        mc.setAttr("defaultRenderGlobals.postRenderLayerMel", a, type="string")
        mc.setAttr("defaultRenderGlobals.preRenderMel", a, type="string")
        mc.setAttr("defaultRenderGlobals.postRenderMel", a, type="string")

    def kmClassicOpenScene(self):
        pm.mel.OpenSceneClassic()

    def kmClassicSave(self):
        pm.mel.SaveSceneClassic()

    def kmClassicSaveAs(self):
        pm.mel.SaveSceneAsClassic()

    def kmCheckPublishable(self):
        pm.mel.CheckPublishable()

    def kmCompareGeom(self):
        # from tak.maya.compare_geom import compareGeom
        pm.mel.compareGeom()

    def kmHardwareShader(self):
        if mc.ls("GEO"):
            if not mc.listAttr("GEO", string="rmb_texture_display"):
                mc.addAttr("GEO", longName="rmb_texture_display", attributeType="bool", keyable=True, defaultValue=True)
        from tak.maya.hardware_shaders import setHardwareShaders
        setHardwareShaders()

    def buildPresentationScene(self):
        pm.mel.tak_buildPresentationScene()

    def launchPresentationRender(self):
        pm.mel.tak_launchPresentationRender()

    def uvSnapshot(self):
        valBase = 1

        projectFileName = mc.file(query=True, list=True)
        UVFolder = projectFileName[0].split('/')
        del UVFolder[-1]
        UVFolder[6] = "sourceimages"
        print ">> : ", UVFolder[9]
        propsName = UVFolder[9]
        UVFolder = '/'.join(UVFolder)
        UVFolder = UVFolder + "/uv"

        if not os.path.exists(UVFolder):
            os.makedirs(UVFolder)

        from os import listdir
        from os.path import isfile, join

        onlyfiles = [f for f in listdir(UVFolder) if isfile(join(UVFolder, f))]
        countFile = len(onlyfiles)
        print ">> : ", countFile + valBase

        valBase = valBase + countFile

        # fileName = "UV_%s" % valBase
        fileName = "uv_" + str(propsName) + "_v" + str(valBase)
        filePathName = UVFolder + "/" + fileName + '.png'
        print ">> : ", fileName
        mc.uvSnapshot(o=True, ff="png", n=filePathName, xr=4096, yr=4096)

    '''
    def kmClock(self):
        heure = strftime("%H:%M:%S", localtime())
        print heure
        mc.iconTextButton(self.bt_h01, edit=True, image1=self.target + "digit" + heure[0] + ".png")
        mc.iconTextButton(self.bt_h02, edit=True, image1=self.target + "digit" + heure[1] + ".png")
        mc.iconTextButton(self.bt_m01, edit=True, image1=self.target + "digit" + heure[3] + ".png")
        mc.iconTextButton(self.bt_m02, edit=True, image1=self.target + "digit" + heure[4] + ".png")
    '''

    def kmMinimizeMaya(self):
        mc.minimizeApp()

    def kmToggleInterfaceLines(self):
        # pm.mel.toggleShelfTabs()  # shelf Tab
        # pm.mel.ToggleMainMenubar()  # main menu bar
        pm.mel.ToggleModelEditorBars()  # model editor bar
        pm.mel.TogglePanelMenubar()  # panel menu bar

    def kmToggleToolBars(self):
        ''' 2015
        gMainWindow = pm.mel.eval('$tmpVar=$gMainWindow')

        if mc.toolBar("MayaWindow|toolBar1", visible=True, q=True):

            mc.toolBar("MayaWindow|toolBar1", visible=False, e=True)  # status line
            mc.toolBar("MayaWindow|toolBar2", visible=False, e=True)  # shelf
            # mc.toolBar("MayaWindow|toolBar3", visible=False, e=True) # help line
            # mc.toolBar("MayaWindow|toolBar4", visible=False, e=True) # command line
            mc.toolBar("MayaWindow|toolBar5", visible=False, e=True)  # range slider
            mc.toolBar("MayaWindow|toolBar6", visible=False, e=True)  # time slider
            mc.toolBar("MayaWindow|toolBar7", visible=False, e=True)  # tool box
            mc.window(gMainWindow, titleBar=False, e=True)
            # self.kmToggleInterfaceLines()
        else:
            mc.toolBar("MayaWindow|toolBar1", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar2", visible=True, e=True)
            # mc.toolBar("MayaWindow|toolBar4", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar5", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar6", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar7", visible=True, e=True)
            mc.window(gMainWindow, titleBar=True, e=True)
        '''
        gMainWindow = pm.mel.eval('$tmpVar=$gMainWindow')

        if mc.workspaceControl("StatusLine", query=True, visible=True):
            mc.workspaceControl("StatusLine", edit=True, visible=False)
            mc.workspaceControl("Shelf", edit=True, visible=False)
            # mc.workspaceControl("Help Line", edit=True, visible=False)
            # mc.workspaceControl("Command Line", edit=True, visible=False)
            mc.workspaceControl("RangeSlider", edit=True, visible=False)
            mc.workspaceControl("TimeSlider", edit=True, visible=False)
            mc.workspaceControl("ToolBox", edit=True, visible=False)
            # KShelf()
            # kMod.KMod()
            mc.window(gMainWindow, titleBar=False, e=True)
        else:
            mc.workspaceControl("StatusLine", edit=True, visible=True)
            mc.workspaceControl("Shelf", edit=True, visible=True)
            mc.workspaceControl("HelpLine", edit=True, visible=True)
            mc.workspaceControl("CommandLine", edit=True, visible=True)
            mc.workspaceControl("RangeSlider", edit=True, visible=True)
            mc.workspaceControl("TimeSlider", edit=True, visible=True)
            mc.workspaceControl("ToolBox", edit=True, visible=True)
            # mc.deleteUI(self.toolName)
            # kMod.KMod().mc.deleteUI(self.toolName)
            mc.window(gMainWindow, titleBar=True, e=True)

    def kmCloseMaya(self):
        mc.quit()


KShelf()
