# kMax Shelf Top tools
# Maxime Terray : kMax
# Remerciements a Sebastien Courtois et a Stephane Hoarau. Cyber Group Studios 
# 04/04/7/2015
# Version 0.2
# Bar top pour Maya 2014
# Regroupant tous les outils et windows utiles

import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import os
#import time
from time import localtime, strftime


class kShelfBar():
    def __init__(self):
        
        scaleIcon = 28
        scaleSeparator = 18

        self.initPath()

        windowName = "kShelfTop"
        toolName = "toolShelfTop"

        if mc.window(windowName, q=True, exists=True):
            mc.deleteUI(windowName)

        if mc.toolBar(toolName, q=True, exists=True):
            mc.deleteUI(toolName)

        myWindow = mc.window(windowName)

        mc.rowColumnLayout(numberOfRows = 1, rowHeight=(1, scaleIcon))

        self.bt_kMaxToolBar = mc.iconTextButton(image1=self.target + "kMaxTool32.png",
                                                highlightImage=self.target + "kMaxTool32b.png",
                                                annotation="Launch kMaxTools",
                                                command=self.kMaxTool,
                                                width=scaleIcon)

        self.bt_kMaxToolBar2 = mc.iconTextButton(image1=self.target + "kMaxTool32.png",
                                                 highlightImage=self.target + "kMaxTool32b.png",
                                                 annotation="Launch kMaxTools",
                                                 command=self.kMaxUi2,
                                                 width=scaleIcon)

        self.bt_sepHor1 = mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_kMod = mc.iconTextButton(image1=self.target + "kMaxMod32.png",
                                         highlightImage=self.target + "kMaxMod32.png",
                                         annotation="Launch kMod Left bar",
                                         command=self.kMod,
                                         width=scaleIcon)

        self.bt_kMaxShelfTop = mc.iconTextButton(image1=self.target + "kMaxShelfTop32.png",
                                                 highlightImage=self.target + "kMaxShelfTop32.png",
                                                 annotation="Launch kMaxShelfTop",
                                                 command=self.kMaxShelfTop,
                                                 width=scaleIcon)

        self.bt_outlinerView = mc.iconTextButton(image1=self.target + "outliner.png",
                                                 highlightImage=self.target + "outliner.png",
                                                 annotation="Outliner/Persp",
                                                 command=self.kmOutlinerView,
                                                 width=scaleIcon)

        self.bt_singlePerspView = mc.iconTextButton(image1=self.target + "singlePerspLayout2016_32.png",
                                                    highlightImage=self.target + "singlePerspLayout2016_32.png",
                                                    annotation="Single Perspective View",
                                                    command=self.kmSinglePerspView,
                                                    width=scaleIcon)

        self.bt_fourView = mc.iconTextButton(image1=self.target + "fourViewLayout2016_32.png",
                                             highlightImage=self.target + "fourViewLayout2016_32.png",
                                             annotation="Four View",
                                             command=self.kmFourView,
                                             width=scaleIcon)

        '''
        self.bt_sepHor2 = mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_scriptView = mc.iconTextButton(image1=self.target + "scriptEdPersp32.png",
                                highlightImage=self.target + "scriptEdPersp32b.png",
                                annotation="Script/Persp",
                                command=self.kmScriptView,
                                width=scaleIcon)

        self.bt_textureView = mc.iconTextButton(image1=self.target + "perspTexture32.png",
                                highlightImage=self.target + "perspTexture32b.png",
                                annotation="Texture/Persp",
                                command=self.kmTextureView,
                                width=scaleIcon)

        self.bt_basicBrowser = mc.iconTextButton(image1=self.target + "common_basicBrowser.png",
                                                 highlightImage=self.target + "common_basicBrowser.png",
                                                 annotation="Basic Browser",
                                                 command=self.kmBasicBrowser,
                                                 width=scaleIcon)

        self.bt_batcher = mc.iconTextButton(image1=self.target + "common_batcher.png",
                                            highlightImage=self.target + "common_batcher.png",
                                            annotation="Batcher",
                                            command=self.kmBatcher,
                                            width=scaleIcon)

        self.bt_qualityCheck = mc.iconTextButton(image1=self.target + "common_qualityCheck.png",
                                                 highlightImage=self.target + "common_qualityCheck.png",
                                                 annotation="Quality Check",
                                                 command=self.kmQualityCheck,
                                                 width=scaleIcon)
        
        self.bt_initScene = mc.iconTextButton(image1=self.target + "initScene.png",
                                              highlightImage=self.target + "initScene.png",
                                              annotation="Init Scene",
                                              command=self.kmInitScene,
                                              width=scaleIcon)
        '''


        mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_new = mc.iconTextButton(image1=self.target + "tt_new.png",
                                        highlightImage=self.target + "tt_new_b.png",
                                        annotation="Create a New Scene",
                                        command=self.kmNew,
                                        width=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_open = mc.iconTextButton(image1=self.target + "tt_open_b.png",
                                         highlightImage=self.target + "tt_open.png",
                                         annotation="Open a Scene",
                                         command=self.kmOpen,
                                         width=scaleIcon)

        self.bt_save = mc.iconTextButton(image1=self.target + "tt_save2_b.png",
                                         highlightImage=self.target + "tt_save2.png",
                                         annotation="Save the current Scene",
                                         command=self.kmSave,
                                         width=scaleIcon)

        self.bt_saveAs = mc.iconTextButton(image1=self.target + "tt_saveAs2_b.png",
                                           highlightImage=self.target + "tt_saveAs2.png",
                                           annotation="Save the current scene under a new name or export all",
                                           command=self.kmSaveAs,
                                           width=scaleIcon)

        self.bt_exportProps = mc.iconTextButton(image1=self.target + "exportSelb.png",
                                              highlightImage=self.target + "exportSel.png",
                                              annotation="Export Prop",
                                              command=self.kmExportProps,
                                              width=scaleIcon)

        self.bt_checkPublishable = mc.iconTextButton(image1=self.target + "tt_checkPublish_b.png",
                                                 highlightImage=self.target + "tt_checkPublish.png",
                                                 annotation="Check Publishability",
                                                 command=self.kmCheckPublishable,
                                                 width=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_classicOpen = mc.iconTextButton(image1=self.target + "open32.png",
                                         highlightImage=self.target + "open32.png",
                                         annotation="Open a Scene",
                                         command=self.kmClassicOpenScene,
                                         width=scaleIcon)

        self.bt_classicSave = mc.iconTextButton(image1=self.target + "save.png",
                                         highlightImage=self.target + "save.png",
                                         annotation="Save the current Scene",
                                         command=self.kmClassicSave,
                                         width=scaleIcon)

        self.bt_savePlus = mc.iconTextButton(image1=self.target + "save+.png",
                                             highlightImage=self.target + "save+.png",
                                             annotation="Incrementale Save",
                                             command=self.kmSavePlus,
                                             width=scaleIcon)

        self.bt_classicSaveAs = mc.iconTextButton(image1=self.target + "saveAs.png",
                                           highlightImage=self.target + "saveAs.png",
                                           annotation="Save the current scene under a new name or export all",
                                           command=self.kmClassicSaveAs,
                                           width=scaleIcon)

        self.bt_import = mc.iconTextButton(image1=self.target + "import.png",
                                           highlightImage=self.target + "import.png",
                                           annotation="Import file",
                                           command=self.kmImport,
                                           width=scaleIcon)

        self.bt_export = mc.iconTextButton(image1=self.target + "export.png",
                                           highlightImage=self.target + "export.png",
                                           annotation="Export entire scene into one file",
                                           command=self.kmExport,
                                           width=scaleIcon)

        self.bt_exportSel = mc.iconTextButton(image1=self.target + "exportSel.png",
                                              highlightImage=self.target + "exportSel.png",
                                              annotation="Export Selection...",
                                              command=self.kmExportSel,
                                              width=scaleIcon)

        self.bt_referenceEditor = mc.iconTextButton(image1=self.target + "reference32.png",
                                                    highlightImage=self.target + "reference32.png",
                                                    annotation="Reference Editor",
                                                    command=self.kmReferenceEditor,
                                                    width=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_outliner = mc.iconTextButton(image1=self.target + "outliner32.png",
                                             highlightImage=self.target + "outliner32.png",
                                             annotation="Outliner",
                                             command=self.kmOutliner,
                                             width=scaleIcon)

        self.bt_nodeEditor = mc.iconTextButton(image1=self.target + "nodeEditor.png",
                                               highlightImage=self.target + "nodeEditor.png",
                                               annotation="Node Editor",
                                               command=self.kmNodeEditor,
                                               width=scaleIcon)

        self.bt_hyperShade = mc.iconTextButton(image1=self.target + "hyperShade.png",
                                               highlightImage=self.target + "hyperShade.png",
                                               annotation="Hypershade",
                                               command=self.kmHyperShade,
                                               width=scaleIcon)

        self.bt_textureEditor = mc.iconTextButton(image1=self.target + "uvEditor.png",
                                                  highlightImage=self.target + "uvEditor.png",
                                                  annotation="UV Texture Editor",
                                                  command=self.kmUVTextureEditor,
                                                  width=scaleIcon)

        self.bt_nameSpaceEditor = mc.iconTextButton(image1=self.target + "nameSpace32.png",
                                                    highlightImage=self.target + "nameSpace32b.png",
                                                    annotation="Namespace Editor",
                                                    command=self.kmNameSpaceEditor,
                                                    width=scaleIcon)

        self.bt_relationshipEditor = mc.iconTextButton(image1=self.target + "relation32.png",
                                                       highlightImage=self.target + "relation32b.png",
                                                       annotation="Relation Ship Editor",
                                                       command=self.kmRelationShipEditor,
                                                       width=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_colorPicker = mc.iconTextButton(image1=self.target + "colorPicker32.png",
                                                highlightImage=self.target + "colorPicker32b.png",
                                                annotation="Color Shader Picker",
                                                command=self.kmColorPicker,
                                                width=scaleIcon)
                                        
        self.bt_randomizer = mc.iconTextButton(image1=self.target + "kRandomizer32.png",
                                               highlightImage=self.target + "kRandomizer32.png",
                                               annotation="Randomizer",
                                               command=self.kmRandomizer,
                                               width=scaleIcon)
       
        self.bt_replacer = mc.iconTextButton(image1=self.target+"kReplacer32.png",
                                             highlightImage=self.target+"kReplacer32.png",
                                             annotation="kReplacer",
                                             command=self.kmReplacer,
                                             width=scaleIcon)

        '''
        self.bt_kitBuilder = mc.iconTextButton(image1=self.target + "scatter32.png",
                                               highlightImage=self.target + "scatter32b.png",
                                               annotation="Scattering",
                                               command=self.kitBuilder,
                                               width=scaleIcon)
                                               '''

        self.bt_frRenamer = mc.iconTextButton(image1=self.target + "text-32.png",
                                              highlightImage=self.target + "text-32.png",
                                              annotation="FrRenamer",
                                              command=self.frRenamer,
                                              width=scaleIcon)

        self.bt_setSmooth = mc.iconTextButton(image1=self.target + "smoothSetTool.png",
                                              highlightImage=self.target + "smoothSetTool.png",
                                              command=self.kmSetSmoothGroupTool, width=scaleIcon)

        self.bt_clean = mc.iconTextButton(image1=self.target + "kCleaner.png",
                                          highlightImage=self.target + "kCleaner.png",
                                          annotation="Cleaner tool",
                                          command=self.kmCleanTool,
                                          width=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)
                                    
        self.bt_switchDisplayPoly = mc.iconTextButton(image1=self.target+"switchAllPoly32.png",
                                                      highlightImage=self.target+"switchAllPoly32.png",
                                                      annotation="Switch display ALL/POLY",
                                                      command=self.kmSwitchDisplayPoly,
                                                      width=scaleIcon)

        self.bt_switchBallPreview = mc.iconTextButton(image1=self.target+"globe_2.png",
                                                      highlightImage=self.target+"globe_2.png",
                                                      annotation="Switch renderThumbnailUpdate",
                                                      command=self.kmSwitchBallPreview,
                                                      width=scaleIcon)

        self.bt_unlockAllAtt = mc.iconTextButton(image1=self.target+"unlock.png",
                                                 highlightImage=self.target+"unlock.png",
                                                 annotation="Unlock all attributs",
                                                 command=self.kmUnlockAllAtt,
                                                 width=scaleIcon)

        ## SPACER
        self.bt_empty = mc.iconTextButton(image1=self.target + "empty.png", width=280, enable=0)

        self.bt_preferences = mc.iconTextButton(image1=self.target + "settings.png",
                                                highlightImage=self.target + "settings.png",
                                                annotation="Preferences",
                                                command=self.kmSetting,
                                                width=scaleIcon)

        self.bt_hotkeys = mc.iconTextButton(image1=self.target + "hotkey.png",
                                            highlightImage=self.target + "hotkey.png",
                                            annotation="Hotkeys Editor",
                                            command=self.kmHotKey,
                                            width=scaleIcon)

        self.bt_plugins = mc.iconTextButton(image1=self.target + "plugin.png",
                                            highlightImage=self.target + "plugin.png",
                                            annotation="Plug-ins Manager",
                                            command=self.kmPlugIn,
                                            width=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_modelingToolKit = mc.iconTextButton(image1=self.target + "modelToolKit.png",
                                                    highlightImage=self.target + "modelToolKit.png",
                                                    annotation="Modeling Tool Kit",
                                                    command=self.kmModelingToolKit,
                                                    width=scaleIcon)

        self.bt_attributeEditor = mc.iconTextButton(image1=self.target + "attributes.png",
                                                    highlightImage=self.target + "attributes.png",
                                                    annotation="Edit the attributes of the selected object",
                                                    command=self.kmAttributeEditor,
                                                    width=scaleIcon)

        self.bt_toolSettings = mc.iconTextButton(image1=self.target + "toolSettings.png",
                                                 highlightImage=self.target + "toolSettings.png",
                                                 annotation="Edit settings for current tool",
                                                 command=self.kmToolSettings,
                                                 width=scaleIcon)

        self.bt_channelBoxLayerEditor = mc.iconTextButton(image1=self.target + "channelLayers.png",
                                                          # selectionImage=self.target + "channel32b.png",
                                                          highlightImage=self.target + "channelLayers.png",
                                                          annotation="Channel Box / Layer Editor",
                                                          command=self.kmChannelBox,
                                                          width=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_clock = mc.iconTextButton(image1=self.target + "clock32.png",
                                          highlightImage=self.target + "clock32b.png",
                                          annotation="Actualise clock",
                                          command=self.kmClock,
                                          width=scaleIcon)

        self.bt_h01 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
        self.bt_h02 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
        self.bt_clockSeparator = mc.iconTextButton(image1=self.target + "digitSeparator.png", width=10, enable=0)
        self.bt_m01 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
        self.bt_m02 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)

        mc.iconTextButton(image1=self.target + "separateHor.png",
                                            disabledImage=self.target + "separateHor.png",
                                            width=scaleSeparator,
                                            enable=0)

        self.bt_reduce = mc.iconTextButton(image1=self.target + "minimize32.png",
                                           highlightImage=self.target + "minimize32.png",
                                           annotation="Minimize Maya",
                                           command=self.kmMinimizeMaya,
                                           width=scaleIcon)
                                   
        self.bt_toggleInterfaceLines = mc.iconTextButton(image1=self.target + "toggleLines32.png",
                                                         highlightImage=self.target + "toggleLines32.png",
                                                         annotation="Toggle interface Lines",
                                                         command=self.kmToggleInterfaceLines,
                                                         width=scaleIcon)

        self.bt_toggleToolBars = mc.iconTextButton(image1=self.target + "toggleInterface32.png",
                                                   highlightImage=self.target + "toggleInterface32.png",
                                                   annotation="Toggle interface Tools Bars",
                                                   command=self.kmToggleToolBars,
                                                   width=scaleIcon)

        self.bt_close = mc.iconTextButton(image1=self.target + "close32.png",
                                          highlightImage=self.target + "close32.png",
                                          annotation="Quit Maya",
                                          command=self.kmCloseMaya,
                                          width=scaleIcon)

        allowedAreas = ['top', 'bottom']
        myTool = mc.toolBar(toolName, area='top', content=myWindow, allowedArea=allowedAreas)
        self.kmClock()

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


    def kMaxTool(self):
        import kmaxUi_main
        reload(kmaxUi_main)
        kmaxUi_main.launchUi()

    def kMaxUi2(self):
        import kMaxUi2
        reload(kMaxUi2)

    def kMod(self):
        import kMod
        reload(kMod)

    def kMaxShelfTop(self):
        import kShelfTop
        reload(kShelfTop)

    def kmNew(self):
        pm.mel.NewScene()

    def kmInitScene(self):
        from mayaShotgun import pathShotgun
        from mayaPipeline import assetPipe
        assetType = pathShotgun.fieldFromPath(mc.file(query=True, sceneName=True), 'sg_asset_type')
        assetPipe.createAssetDialog(namespace=':', assetType=assetType)

        #old
        #import kmrt.sceneInit
        #kmrt.sceneInit.sceneInit('setMod')

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
        pm.mel.ToggleAttributeEditor()
        
    def kmToolSettings(self):
        # pm.mel.ToolSettingsWindow()
        # imageOne = mc.iconTextButton(self.bt_toolSettings, image1=1, q=True)
        # if imageOne == self.target + "toolSettings32.png":
        #     mc.iconTextButton(self.bt_toolSettings, image1=self.target + "toolSettings32b.png", highlightImage=self.target + "toolSettings32.png", e=True)
        # else:
        #     mc.iconTextButton(self.bt_toolSettings, image1=self.target + "toolSettings32.png", highlightImage=self.target + "toolSettings32b.png", e=True)
        pm.mel.ToggleToolSettings()

    def kmChannelBox(self, *args):
        # imageOne = mc.iconTextButton(self.bt_channelBoxLayerEditor, image1=1, q=True)
        # if imageOne == self.target + "channel32.png":
        #     mc.iconTextButton(self.bt_channelBoxLayerEditor, image1=self.target + "channel32b.png", highlightImage=self.target + "channel32.png", e=True)
        # else:
        #     mc.iconTextButton(self.bt_channelBoxLayerEditor, image1=self.target + "channel32.png", highlightImage=self.target + "channel32b.png", e=True)
        pm.mel.ToggleChannelsLayers()

    def kmSinglePerspView(self):
        pm.mel.setNamedPanelLayout("Single Perspective View")

    def kmFourView(self):
        pm.mel.setNamedPanelLayout("Four View")

    def kmOutlinerView(self):
        # pm.mel.ToggleOutliner()
        pm.mel.setNamedPanelLayout("Persp/Outliner")

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
        reload (kReplacer)

    def kitBuilder(self):
        import mayaTools.assetKitBuilder.main
        import mayaTools.assetKitBuilder.core

        mayaTools.assetKitBuilder.main.load()

    def frRenamer(self):
        import renamer.renamer as renamer
        reload( renamer )

        class_renamer = renamer.Renamer()
        class_renamer.UI()

    def kmSetSmoothGroupTool(self):
        #import setSmoothGroupTool
        #reload(setSmoothGroupTool)
        import kSmoothSetTool
        reload(kSmoothSetTool)

    def kmCleanTool(self):
        import kCleaner

        reload(kCleaner)
        #clean.kmCleaner()
        
    def kmSwitchDisplayPoly(self):    
        allModelPanel = mc.getPanel(type='modelPanel')
        if allModelPanel:
            for modelPanelName in allModelPanel:
                print ">> " , mc.modelEditor(modelPanelName, nCloths=1, q=1)
                if mc.modelEditor(modelPanelName, nCloths=1, q=1):
                    mc.modelEditor(modelPanelName, allObjects=0, e=1)
                    mc.modelEditor(modelPanelName, polymeshes=1, e=1)
                else:
                    mc.modelEditor(modelPanelName, allObjects=1, e=1)
    
    def kmSwitchBallPreview(self):
        renderBall =  mc.renderThumbnailUpdate(q=True)
        if renderBall :
            mc.renderThumbnailUpdate(False)
            print ">> Render Thumbnail OFF"
        else :
            mc.renderThumbnailUpdate(True)
            print ">> Render Thumbnail ON"\

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

    '''
    def kmUnfreeze(selfself):
        # unfreeze transform PYMEL
        import pymel.core as pm

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

    '''  mikros      
    def kmBasicBrowser(self):
        from mayaOverrides import tk_command_utils
        from mayaCore.ui import BusyCursor
        with BusyCursor():
            basic_browser_callback = tk_command_utils.get_tk_command('basicBrowser')
            basic_browser_callback()
    
    def kmBatcher(self):
        import batcher.templateBatcherGUI
        reload(batcher.templateBatcherGUI)
        try : 
            batcherTemplate.close()
        except :
            pass
        batcherTemplate = batcher.templateBatcherGUI.BatcherTemplate()
        batcherTemplate.show()
        batcherTemplate.autoSetCategoryAndTemplate()

    def kmQualityCheck(sel):
        # import qualityCheck
        # qualityCheck.load()

        from qualityCheck import gui2
        gui2.launch()
    '''
    def kmClassicOpenScene(self):
        pm.mel.OpenSceneClassic()

    def kmClassicSave(self):
        pm.mel.SaveSceneClassic()

    def kmClassicSaveAs(self):
        pm.mel.SaveSceneAsClassic()

    def kmCheckPublishable(self):
        pm.mel.CheckPublishable()

    def kmClock(self):
        heure = strftime("%H:%M:%S", localtime())
        print heure
        mc.iconTextButton(self.bt_h01, edit=True, image1=self.target + "digit" + heure[0] + ".png")
        mc.iconTextButton(self.bt_h02, edit=True, image1=self.target + "digit" + heure[1] + ".png")
        mc.iconTextButton(self.bt_m01, edit=True, image1=self.target + "digit" + heure[3] + ".png")
        mc.iconTextButton(self.bt_m02, edit=True, image1=self.target + "digit" + heure[4] + ".png")

    def kmMinimizeMaya(self):
        mc.minimizeApp()

    def kmToggleInterfaceLines(self):
        pm.mel.toggleShelfTabs() # shelf Tab
        pm.mel.ToggleMainMenubar() # main menu bar
        pm.mel.ToggleModelEditorBars() # model editor bar
        pm.mel.TogglePanelMenubar() # panel menu bar

    def kmToggleToolBars(self):
        gMainWindow = pm.mel.eval('$tmpVar=$gMainWindow')

        if mc.toolBar("MayaWindow|toolBar1", visible=True, q=True):

            mc.toolBar("MayaWindow|toolBar1", visible=False, e=True) # status line
            mc.toolBar("MayaWindow|toolBar2", visible=False, e=True) # shelf
            # mc.toolBar("MayaWindow|toolBar3", visible=False, e=True) # help line
            # mc.toolBar("MayaWindow|toolBar4", visible=False, e=True) # command line
            mc.toolBar("MayaWindow|toolBar5", visible=False, e=True) # range slider
            mc.toolBar("MayaWindow|toolBar6", visible=False, e=True) # time slider
            mc.toolBar("MayaWindow|toolBar7", visible=False, e=True) # tool box
            mc.window(gMainWindow, titleBar=False, e=True)
            #self.kmToggleInterfaceLines()

        else:
            mc.toolBar("MayaWindow|toolBar1", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar2", visible=True, e=True)
            #mc.toolBar("MayaWindow|toolBar4", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar5", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar6", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar7", visible=True, e=True)
            mc.window(gMainWindow, titleBar=True, e=True)

    def kmCloseMaya(self):
        mc.quit()


kShelfBar()
