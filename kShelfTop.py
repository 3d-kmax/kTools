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
        
        scaleIcon = 30
        scaleSeparator = 18
        path_list = os.path.realpath(__file__).split('\\')[:-2]
        path_list.extend(['scripts', 'kTools', 'icons'])
        self.target = ''
        for item in path_list:
            self.target += item + '/'

        windowName = "kShelfTop"
        toolName = "toolShelfTop"

        if mc.window(windowName, q=True, exists=True):
            mc.deleteUI(windowName)

        if mc.toolBar(toolName, q=True, exists=True):
            mc.deleteUI(toolName)

        myWindow = mc.window(windowName)

        mc.rowColumnLayout(numberOfRows = 1, rowHeight=(1, scaleIcon))

        self.bt_kMaxToolBar = mc.iconTextButton(image1=self.target + "kMaxTool32.png", highlightImage=self.target + "kMaxTool32b.png",
                                        annotation="Launch kMaxTools", command=self.kMaxTool, width=scaleIcon)

        self.bt_sepHor1 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_kMod = mc.iconTextButton(image1=self.target + "kMaxMod32.png", highlightImage=self.target + "kMaxMod32b.png",
                                    annotation="Launch kMod Left bar", command=self.kMod, width=scaleIcon)

        self.bt_kMaxShelfTop = mc.iconTextButton(image1=self.target + "kMaxShelfTop32.png",
                                         highlightImage=self.target + "kMaxShelfTop32b.png",
                                         annotation="Launch kMaxShelfTop", command=self.kMaxShelfTop, width=scaleIcon)

        self.bt_sepHor7 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_basicBrowser = mc.iconTextButton(image1=self.target + "common_basicBrowser.png", highlightImage=self.target + "common_basicBrowser.png",
                                  annotation="Basic Browser", command=self.kmBasicBrowser, width=scaleIcon)
	
        self.bt_batcher = mc.iconTextButton(image1=self.target + "common_batcher.png", highlightImage=self.target + "common_batcher.png",
                                  annotation="Batcher", command=self.kmBatcher, width=scaleIcon)

        self.bt_qualityCheck = mc.iconTextButton(image1=self.target + "common_qualityCheck.png", highlightImage=self.target + "common_qualityCheck.png",
                                  annotation="Quality Check", command=self.kmQualityCheck, width=scaleIcon)      
        
        self.bt_sepHor1 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_initScene = mc.iconTextButton(image1=self.target + "new32.png", highlightImage=self.target + "new32b.png",
                                annotation="Init Scene", command=self.kmInitScene, width=scaleIcon)

        self.bt_new = mc.iconTextButton(image1=self.target + "new32.png", highlightImage=self.target + "new32b.png",
                                annotation="Create a New Scene", command=self.kmNew, width=scaleIcon)

        self.bt_open = mc.iconTextButton(image1=self.target + "open32.png", highlightImage=self.target + "open32b.png",
                                 annotation="Open a Scene", command=self.kmOpen, width=scaleIcon)

        self.bt_sepHor1 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_save = mc.iconTextButton(image1=self.target + "save32.png", highlightImage=self.target + "save32b.png",
                                 annotation="Save the current Scene", command=self.kmSave, width=scaleIcon)

        self.bt_savePlus = mc.iconTextButton(image1=self.target + "save+32.png", highlightImage=self.target + "save+32b.png",
                                     annotation="Incrementale Save", command=self.kmSavePlus, width=scaleIcon)

        self.bt_saveAs = mc.iconTextButton(image1=self.target + "saveAs32.png", highlightImage=self.target + "saveAs32b.png",
                                   annotation="Save the current scene under a new name or export all",
                                   command=self.kmSaveAs, width=scaleIcon)

        self.bt_sepHor52 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_import = mc.iconTextButton(image1=self.target + "import32.png", highlightImage=self.target + "import32b.png",
                                   annotation="Import file", command=self.kmImport, width=scaleIcon)

        self.bt_export = mc.iconTextButton(image1=self.target + "export32.png", highlightImage=self.target + "export32b.png",
                                   annotation="Export entire scene (including contents of all references) into one file",
                                   command=self.kmExport, width=scaleIcon)

        self.bt_exportSel = mc.iconTextButton(image1=self.target + "exportSel32.png", highlightImage=self.target + "exportSel32b.png",
                                      annotation="Export Selection...", command=self.kmExportSel, width=scaleIcon)

        self.bt_sepHor52 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_referenceEditor = mc.iconTextButton(image1=self.target + "reference32.png",
                                            highlightImage=self.target + "reference32b.png", annotation="Reference Editor",
                                            command=self.kmReferenceEditor, width=scaleIcon)

        self.bt_sepHor1 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_outliner = mc.iconTextButton(image1=self.target + "outliner32.png", highlightImage=self.target + "outliner32b.png",
                                     annotation="Outliner", command=self.kmOutliner, width=scaleIcon)

        self.bt_hyperShade = mc.iconTextButton(image1=self.target + "hyperShade32.png", highlightImage=self.target + "hyperShade32b.png",
                                       annotation="Hypershade", command=self.kmHyperShade, width=scaleIcon)
		
        self.bt_nodeEditor = mc.iconTextButton(image1=self.target + "hyperShade32.png", highlightImage=self.target + "hyperShade32b.png",
                                       annotation="Node Editor", command=self.kmNodeEditor, width=scaleIcon)


        self.bt_textureEditor = mc.iconTextButton(image1=self.target + "texture32.png", highlightImage=self.target + "texture32b.png",
                                          annotation="UV Texture Editor", command=self.kmUVTextureEditor, width=scaleIcon)
                                    
        '''
        self.bt_textureFileManager = mc.iconTextButton(image1=self.target+"textMan32.png", annotation="UV Texture Editor", 
                                            command=self.kmTextureFileManager, width=scaleIcon)
        '''

        self.bt_nameSpaceEditor = mc.iconTextButton(image1=self.target + "nameSpace32.png",
                                            highlightImage=self.target + "nameSpace32b.png", annotation="Namespace Editor",
                                            command=self.kmNameSpaceEditor, width=scaleIcon)

        self.bt_relationshipEditor = mc.iconTextButton(image1=self.target + "relation32.png",
                                               highlightImage=self.target + "relation32b.png",
                                               annotation="Relation Ship Editor", command=self.kmRelationShipEditor, width=scaleIcon)

        self.bt_sepHor3 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)


        '''
        self.bt_sepHor4 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)
                                     
        self.bt_freezeScale = mc.iconTextButton(image1=self.target+"freezeT.png", highlightImage=self.target+"freezeT.png",
                                    annotation="Freeze Scale", command=self.kmFreezeScale, width=scaleIcon)

        self.bt_deleteHistory = mc.iconTextButton(image1=self.target+"delete_history.png", highlightImage=self.target+"delete_history.png",
                                    annotation="Delete construction history", command=self.kmDeleteHistory, width=scaleIcon)
                                    
        self.bt_centerPivot = mc.iconTextButton(image1=self.target+"center.png", highlightImage=self.target+"center.png",
                                    annotation="Center Pivot", command=self.kmCenterPivot, width=scaleIcon)                          
        '''

        self.bt_outlinerView = mc.iconTextButton(image1=self.target + "perspOutliner32.png",
                                 highlightImage=self.target + "perspOutliner32b.png", annotation="Outliner/Persp",
                                 command=self.kmOutlinerView, width=scaleIcon)

        self.bt_singlePerspView = mc.iconTextButton(image1=self.target + "singlePersp32.png",
                                highlightImage=self.target + "singlePersp32b.png",
                                annotation="Single Perspective View", command=self.kmSinglePerspView, width=scaleIcon)

        self.bt_fourView = mc.iconTextButton(image1=self.target + "fourView32.png", highlightImage=self.target + "fourView32b.png",
                                annotation="Four View", command=self.kmFourView, width=scaleIcon)

        self.bt_scriptView = mc.iconTextButton(image1=self.target + "scriptEdPersp32.png",
                                highlightImage=self.target + "scriptEdPersp32b.png", annotation="Script/Persp",
                                command=self.kmScriptView, width=scaleIcon)

        '''
        self.bt_textureView = mc.iconTextButton(image1=self.target + "perspTexture32.png",
                                highlightImage=self.target + "perspTexture32b.png", annotation="Texture/Persp",
                                command=self.kmTextureView, width=scaleIcon)
        '''

        self.bt_sepHor5 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                width=scaleSeparator, enable=0)

        self.bt_colorPicker = mc.iconTextButton(image1=self.target + "colorPicker32.png",
                                highlightImage=self.target + "colorPicker32b.png", annotation="Color Shader Picker",
                                command=self.kmColorPicker, width=scaleIcon)
                                
        
                                        
        self.bt_randomizer = mc.iconTextButton(image1=self.target + "kRandomizer32.png", highlightImage=self.target + "kRandomizer32.png",
                                       annotation="Randomizer", command=self.kmRandomizer, width=scaleIcon)
       
        self.bt_replacer = mc.iconTextButton(image1=self.target+"kReplacer32.png", highlightImage=self.target+"kReplacer32.png",
                                        annotation="kReplacer", command=self.kmReplacer, width=scaleIcon)
       
        self.bt_scatter = mc.iconTextButton(image1=self.target + "scatter32.png", highlightImage=self.target + "scatter32b.png",
                                    annotation="Scattering", command=self.icPolyScatter, width=scaleIcon)

        self.bt_kitBuilder = mc.iconTextButton(image1=self.target + "scatter32.png", highlightImage=self.target + "scatter32b.png",
                                    annotation="Scattering", command=self.kitBuilder, width=scaleIcon)

        ''' TEAM TO
        self.bt_setSmooth = mc.iconTextButton(image1=self.target + "smoothSetTool.png",
                                highlightImage=self.target + "smoothSetTool.png",
                                command=self.kmSetSmoothGroupTool, width=scaleIcon)
                                
        self.bt_propsBankManager = mc.iconTextButton(image1=self.target+"propsManager32.png", highlightImage=self.target+"propsManager32.png",
                                    annotation="props bank manager", command=self.kmPropsManager, width=scaleIcon)
                                    
        self.bt_mainpackManager = mc.iconTextButton(image1=self.target+"mainPackTool32.png", highlightImage=self.target+"mainPackTool32.png",
                                    annotation="mainpack manager", command=self.kmMainpackManager, width=scaleIcon)
        '''
                                    
        self.bt_frRenamer = mc.iconTextButton(image1=self.target + "text-32.png", highlightImage=self.target + "text-32.png",
                                      annotation="FrRenamer", command=self.frRenamer, width=scaleIcon)
                                      
        self.bt_ngones = mc.iconTextButton(image1=self.target+"selNgones32.png", highlightImage=self.target+"selNgones32.png",
                                        annotation="Isolate objects with ngones, and create a Set" , command=self.kmExeNgones, width=scaleIcon)
                                       
        '''
        self.bt_selNgones = mc.iconTextButton(image1=self.target+"selNgones.png", highlightImage=self.target+"selNgones.png",
                                        annotation="Select nGones", command=self.kmSelNgones, width=scaleIcon)
                                                
        self.bt_convertUItoPY = mc.iconTextButton(image1=self.target + "convertUI32.png", highlightImage=self.target + "convertUI32b.png",
                                          annotation="Convert .ui file in .py file",
                                          command=self.kmConvertUI, width=scaleIcon)
                                          
		self.bt_ttRig3 = mc.iconTextButton(image1=self.target+"ttRig3.png", highlightImage=self.target+"ttRig3.png",
                                    annotation="Launch ttRig3", command=self.ttRig3, width=scaleIcon)
        
		self.bt_checkPublish = mc.iconTextButton(image1=self.target+"checkPublish.png", highlightImage=self.target+"checkPublish.png",
                                    annotation="Check Publishability", command=self.checkPublish, width=scaleIcon)        
        
        self.bt_light = mc.iconTextButton(image1=self.target+"sun32.png", highlightImage=self.target+"sun32.png",
                                    annotation="Create/Delete LightConfig for Viewport" , command=self.kmLightTheSun, width=scaleIcon)
        '''

        self.bt_clean = mc.iconTextButton(image1=self.target + "kCleaner.png", highlightImage=self.target + "kCleaner.png",
                                  annotation="Cleaner tool",
                                  command=self.kmCleanTool, width=scaleIcon)

        self.bt_sepHor5 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)
                                    
        self.bt_switchDisplayPoly = mc.iconTextButton(image1=self.target+"switchAllPoly32.png", highlightImage=self.target+"switchAllPoly32.png",
                                    annotation="Switch display ALL/POLY", command=self.kmSwitchDisplayPoly, width=scaleIcon)

        self.bt_switchBallPreview = mc.iconTextButton(image1=self.target+"globe_2.png", highlightImage=self.target+"globe_2.png",
                                    annotation="Switch renderThumbnailUpdate", command=self.kmSwitchBallPreview, width=scaleIcon)    
                                    
            
        self.bt_empty = mc.iconTextButton(image1=self.target + "empty.png", width=160, enable=0)

        self.bt_preferences = mc.iconTextButton(image1=self.target + "settings32.png", highlightImage=self.target + "settings32b.png",
                                        annotation="Preferences", command=self.kmSetting, width=scaleIcon)

        self.bt_hotkeys = mc.iconTextButton(image1=self.target + "hotkey32.png", highlightImage=self.target + "hotkey32b.png",
                                    annotation="Hotkeys Editor", command=self.kmHotKey, width=scaleIcon)

        self.bt_plugins = mc.iconTextButton(image1=self.target + "plug32.png", highlightImage=self.target + "plug32b.png",
                                    annotation="Plug-ins Manager", command=self.kmPlugIn, width=scaleIcon)

        self.bt_sepHor2 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_attributeEditor = mc.iconTextButton(image1=self.target + "attribute32.png",
                                            highlightImage=self.target + "attribute32b.png",
                                            annotation="Edit the attributes of the selected object",
                                            command=self.kmAttributeEditor, width=scaleIcon)

        self.bt_toolSettings = mc.iconTextButton(image1=self.target + "toolSettings32.png",
                                         highlightImage=self.target + "toolSettings32b.png",
                                         annotation="Edit settings for current tool", command=self.kmToolSettings, width=scaleIcon)

        self.bt_channelBoxLayerEditor = mc.iconTextButton(image1=self.target + "channel32.png", #selectionImage=self.target + "channel32b.png",
                                                  highlightImage=self.target + "channel32b.png",
                                                  annotation="Channel Box / Layer Editor", command=self.kmChannelBox, width=scaleIcon)
        #self.bt_sceneManager = mc.shelfButton(image1=self.target + "stella32.png", highlightImage=self.target + "stella32b.png",
        #                                 annotation="Scene manager", command=self.cubeSceneManager)

        self.bt_sepHor7 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_clock = mc.iconTextButton(image1=self.target + "clock32.png", highlightImage=self.target + "clock32b.png",
                                  annotation="Actualise clock", command=self.kmClock, width=scaleIcon)

        self.bt_h01 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
        self.bt_h02 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
        self.bt_clockSeparator = mc.iconTextButton(image1=self.target + "digitSeparator.png", width=10, enable=0)
        self.bt_m01 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)
        self.bt_m02 = mc.iconTextButton(image1=self.target + "digit8.png", width=22, enable=0)

        self.bt_sepHor8 = mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                                    width=scaleSeparator, enable=0)

        self.bt_reduce = mc.iconTextButton(image1=self.target + "minimize32.png", highlightImage=self.target + "minimize32b.png",
                                   annotation="Minimize Maya", command=self.kmMinimizeMaya, width=scaleIcon)
                                   
        self.bt_toggleInterfaceLines = mc.iconTextButton(image1=self.target + "toggleLines32.png",
                                                 highlightImage=self.target + "toggleLines32b.png",
                                                 annotation="Toggle interface Lines",
                                                 command=self.kmToggleInterfaceLines, width=scaleIcon)

        self.bt_toggleToolBars = mc.iconTextButton(image1=self.target + "toggleInterface32.png",
                                           highlightImage=self.target + "toggleInterface32b.png",
                                           annotation="Toggle interface Tools Bars", command=self.kmToggleToolBars, width=scaleIcon)

        self.bt_close = mc.iconTextButton(image1=self.target + "close32.png", highlightImage=self.target + "close32b.png",
                                  annotation="Quit Maya", command=self.kmCloseMaya, width=scaleIcon)

        allowedAreas = ['top', 'bottom']
        myTool = mc.toolBar(toolName, area='top', content=myWindow, allowedArea=allowedAreas)
        self.kmClock()

    def kMaxTool(self):
        import kmaxUi_main
        reload(kmaxUi_main)
        kmaxUi_main.launchUi()

    def kMod(self):
        import kMod
        reload(kMod)

    def kMaxShelfTop(self):
        import kShelfTop
        reload(kShelfTop)

    def kmNew(self):
        pm.mel.NewScene()

    def kmInitScene(self):
        import kmrt.sceneInit
        kmrt.sceneInit.sceneInit('setMod')

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
        
    '''
    def kmTextureFileManager(self):
        pm.mel.FileTextureManager()
    '''

    def kmNameSpaceEditor(self):
        pm.mel.NamespaceEditor()

    def kmRelationShipEditor(self):
        pm.mel.SetEditor()

    def kmAttributeEditor(self):
        #pm.mel.AttributeEditor()
        imageOne = mc.iconTextButton(self.bt_attributeEditor, image1=1, q=True)
        
        if imageOne == self.target + "attribute32.png":
            mc.iconTextButton(self.bt_attributeEditor, image1=self.target + "attribute32b.png", highlightImage=self.target + "attribute32.png", e=True)
        else:
            mc.iconTextButton(self.bt_attributeEditor, image1=self.target + "attribute32.png", highlightImage=self.target + "attribute32b.png", e=True)
        
        
        pm.mel.ToggleAttributeEditor()
        
    def kmToolSettings(self):
        #pm.mel.ToolSettingsWindow()
        imageOne = mc.iconTextButton(self.bt_toolSettings, image1=1, q=True)
        if imageOne == self.target + "toolSettings32.png":
            mc.iconTextButton(self.bt_toolSettings, image1=self.target + "toolSettings32b.png", highlightImage=self.target + "toolSettings32.png", e=True)
        else:
            mc.iconTextButton(self.bt_toolSettings, image1=self.target + "toolSettings32.png", highlightImage=self.target + "toolSettings32b.png", e=True)
        
        pm.mel.ToggleToolSettings()

    def kmChannelBox(self, *args):   
        imageOne = mc.iconTextButton(self.bt_channelBoxLayerEditor, image1=1, q=True)
        
        if imageOne == self.target + "channel32.png":
            mc.iconTextButton(self.bt_channelBoxLayerEditor, image1=self.target + "channel32b.png", highlightImage=self.target + "channel32.png", e=True)
        else:
            mc.iconTextButton(self.bt_channelBoxLayerEditor, image1=self.target + "channel32.png", highlightImage=self.target + "channel32b.png", e=True)
        
        pm.mel.ToggleChannelsLayers()     
    
    '''
    def kmFreezeScale(self):
        mc.makeIdentity(a=1, t=0, r=0, s=1, n=1, pn=1) 

    def kmDeleteHistory(self):
        mc.delete(constructionHistory=True)
    
    def kmCenterPivot(self):
        pm.mel.CenterPivot()
    '''
    
    def kmSinglePerspView(self):
        pm.mel.setNamedPanelLayout("Single Perspective View")

    def kmFourView(self):
        pm.mel.setNamedPanelLayout("Four View")

    def kmOutlinerView(self):
        pm.mel.setNamedPanelLayout("Persp/Outliner")

    def kmScriptView(self):
        pm.mel.setNamedPanelLayout("Script/View")

    '''
    def kmTextureView(self):
        pm.mel.setNamedPanelLayout("Persp/UV Texture Editor")
    '''
        
    def kmColorPicker(self):
        import kColorizer
        reload(kColorizer)
                
    def kmRandomizer(self):
        import kRandomizer
        reload(kRandomizer)
    
    def kmReplacer(self):
        import kReplacer
        reload (kReplacer)
        
    def icPolyScatter(self):
        pm.mel.icPolyScatter()

    def kitBuilder(self):
        import mayaTools.assetKitBuilder.main
        import mayaTools.assetKitBuilder.core

        mayaTools.assetKitBuilder.main.load()

    ''' TEAMTO
     
    def kmSetSmoothGroupTool(self):
        import setSmoothGroupTool
        reload(setSmoothGroupTool)
    
    def kmPropsManager(self):
        pm.mel.ava_assetBankManager()
        
    def kmMainpackManager(self):
        pm.mel.ava_mainpack_manager()
        
    def kmSelNgones(self):
        mel.eval('polyCleanupArgList 3 { "0","2","1","0","1","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" };')
    '''

    def frRenamer(self):
        import renamer.renamer as renamer
        reload( renamer )

        class_renamer= renamer.Renamer()
        class_renamer.UI()

    def kmExeNgones(self):
        mel.eval('polyCleanupArgList 3 { "0","2","1","0","1","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" };')
        mel.eval('toggleSelMode;')
        #km.toggleIsolateObject()
        allModelPanel = mc.getPanel(type='modelPanel')
        if allModelPanel:
            for modelPanelName in allModelPanel:
                state = mc.isolateSelect(modelPanelName, query=True, state=True)
                if state == 0:
                    if mc.selectMode(q=True, object=True):
                        pm.mel.enableIsolateSelect(modelPanelName, 1)
                    else:
                        mc.selectMode(object=True)
                        pm.mel.enableIsolateSelect(modelPanelName, 1)
                        mc.selectMode(component=True)
                    print ">> Isolate : ON."
                else:
                    pm.mel.enableIsolateSelect(modelPanelName, 0)
                    print ">> Isolate : OFF."
        mc.sets(name="ObjWithNGones")
        
        
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
        renderBall = mc.renderThumbnailUpdate(q=True)
        if renderBall :
            mc.renderThumbnailUpdate(False)
            print ">> Render Thumbnail OFF"
        else :
            mc.renderThumbnailUpdate(True)
            print ">> Render Thumbnail ON"
                
    '''
    def kmLightTheSun(self):
        sel = mc.ls('groupLightPrev')
        if not sel :
            mc.ambientLight(n='ambiantLightPrev', intensity=2.5)
            mc.spotLight(n='spotLightPrev', intensity=0.6, coneAngle=120)
            mc.setAttr( 'spotLightPrevShape.emitSpecular', 0)
            mc.setAttr( 'spotLightPrev.rotateX', -90 )
            mc.setAttr( 'spotLightPrev.translateY', 300)
            #mc.setAttr( 'spotLightPrev.scale', 200, 200, 200, type="double3")
            mc.group( 'ambiantLightPrev', 'spotLightPrev', n='groupLightPrev' )
            allModelPanel = mc.getPanel(type='modelPanel')
            if allModelPanel:
                for modelPanelName in allModelPanel:
                    mc.modelEditor(modelPanelName, e=True, displayLights="all", shadows=True)
        else :
            mc.delete(sel)
            allModelPanel = mc.getPanel(type='modelPanel')
            if allModelPanel:
                for modelPanelName in allModelPanel:
                    mc.modelEditor(modelPanelName, e=True, displayLights="default", shadows=False)
    
    def ttRig3(self):
        pm.mel.ttRig3()
    
    def checkPublish(self):
        pm.mel.CheckPublishable()
    
    def kmConvertUI(self):
        # transform UI to PY
        import pysideuic

        pysideuic.compileUiDir(r'C:\Users\m.terray\Documents\maya\2014-x64\scripts')
    def cubeSceneManager(self):
        pm.mel.cubeSceneManager()
    '''
        
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
        import qualityCheck
        qualityCheck.load()

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
        pm.mel.toggleShelfTabs()
        pm.mel.ToggleMainMenubar()
        pm.mel.ToggleModelEditorBars()
        pm.mel.TogglePanelMenubar()

    def kmToggleToolBars(self):
        gMainWindow = pm.mel.eval('$tmpVar=$gMainWindow')

        if mc.toolBar("MayaWindow|toolBar1", visible=True, q=True):

            mc.toolBar("MayaWindow|toolBar1", visible=False, e=True)
            mc.toolBar("MayaWindow|toolBar2", visible=False, e=True)
            mc.toolBar("MayaWindow|toolBar4", visible=False, e=True)
            mc.toolBar("MayaWindow|toolBar5", visible=False, e=True)
            mc.toolBar("MayaWindow|toolBar6", visible=False, e=True)
            mc.toolBar("MayaWindow|toolBar7", visible=False, e=True)
            mc.window(gMainWindow, titleBar=False, e=True)

        else:
            mc.toolBar("MayaWindow|toolBar1", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar2", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar4", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar5", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar6", visible=True, e=True)
            mc.toolBar("MayaWindow|toolBar7", visible=True, e=True)
            mc.window(gMainWindow, titleBar=True, e=True)

    def kmCloseMaya(self):
        mc.quit()


kShelfBar()
