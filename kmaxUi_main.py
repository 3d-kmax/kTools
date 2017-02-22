# kMax Tool Bar
# Maxime Terray : kMax
# Remerciements a Sebastien Courtois et a Stephane Hoarau. Cyber Group Studios 
# 20/07/2014
# Version 0.1
# Panneau lateral pour Maya 2013
# Regroupant le Tool Settings, le Channel Box, et l'Attribut Editor.

import shiboken
from PySide import QtCore, QtGui

Qt = QtCore.Qt

import maya.OpenMayaUI as mui
import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import os

import kmaxUi
reload(kmaxUi)

import kMod
import kShelfTop
#mc.shelfTabLayout("MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout", selectTab="TTmod", e=True)


def wrapinstance(ptr, base=None):
    """
	Utility to convert a pointer to a Qt class instance (PySide/PyQt compatible)

	:param ptr: Pointer to QObject in memory
	:type ptr: long or Swig instance
	
	:param base: (Optional) Base class to wrap with (Defaults to QObject, which should handle anything)
	:type base: QtGui.QWidget
	
	:return: QWidget or subclass instance
	:rtype: QtGui.QWidget
	"""
    if ptr is None:
        return None
    ptr = long(ptr)  # Ensure type
    if globals().has_key('shiboken'):
        if base is None:
            qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
            metaObj = qObj.metaObject()
            cls = metaObj.className()
            superCls = metaObj.superClass().className()
            if hasattr(QtGui, cls):
                base = getattr(QtGui, cls)
            elif hasattr(QtGui, superCls):
                base = getattr(QtGui, superCls)
            else:
                base = QtGui.QWidget
        return shiboken.wrapInstance(long(ptr), base)
    elif globals().has_key('sip'):
        base = QtCore.QObject
        return sip.wrapinstance(long(ptr), base)
    else:
        return None


def getMayaWindow():
    return wrapinstance(mui.MQtUtil.mainWindow())


def controlToPySide(sMayaUiName):
    ptr = mui.MQtUtil.findControl(sMayaUiName)
    if ptr is not None:
        return wrapinstance(ptr)


def layoutToPySide(sMayaUiName):
    ptr = mui.MQtUtil.findLayout(sMayaUiName)
    if ptr is not None:
        return wrapinstance(ptr)


def windowToPySide(sMayaUiName):
    ptr = mui.MQtUtil.findWindow(sMayaUiName)
    if ptr is not None:
        return wrapinstance(ptr)


def catchJobException(func):
    def doIt(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception, e:
            pm.displayError('< {0}.{1} > {2}.'.format(func.__module__, func.__name__, str(e)))
            return
        return ret

    return doIt


def isAutoAddNewObjsEnabled():
	iJob = pm.mel.eval("$temp = $isolateSelectAutoAddScriptJob") #2106
	#print iJob
    #iJob = pm.mel.eval("$temp = $autoAddNewObjJobNum") #2015
	return mc.scriptJob(ex=iJob)


# isolate selection pour le raccourci clavier				enableIsolateSelect modelPanel4 true; 		isolateSelect -state 1 modelPanel4;
def toggleIsolateObject():
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
                # self.bt_isolateSel.setStyleSheet("background-color: "+self.selectColor+";\n"
                # "selection-background-color: rgb(150, 150, 150);\n")
                print ">> Isolate : ON."
            else:
                pm.mel.enableIsolateSelect(modelPanelName, 0)
                # self.bt_isolateSel.setStyleSheet("background-color: "+self.unSelectColor+";\n"			
                # "selection-background-color: "+self.selectColor+";\n")
                print ">> Isolate : OFF."


class KmaxWin(QtGui.QWidget, kmaxUi.Ui_kmaxToolBar):
    '''
    Mon outil custom de ouf

    :param QtGui.QWidget: QWidget import
    :type QtGui.QWidget:
    :param kmaxUi.Ui_kmaxToolBar: Ui_kmaxToolBar import
    :type kmaxUi.Ui_kmaxToolBar:
    '''

    def __init__(self, parent=None):

        # INITIALISATION :
        # initialisation des variables et des etats des boutons de kmaxToolBar en fonction de celles de maya		
        super(KmaxWin, self).__init__(parent)

        self.debugMode = 0

        self.scriptJobIds = []
        self.allModelPanel = []
        self.toggleTweak = 0

        self.HUDState = 0

        self.nearValue = 0
        self.farValue = 0
        self.makeLiveState = 0

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        # self.selectColor = "rgb(50, 110, 180)"		# BLEU good : "rgb(50, 100, 150)"
        self.selectColor = "rgb(103, 141, 178)"  # Maya BLEU
        self.unSelectColor = "rgb(100, 100, 100)"  # GRIS FONCE
        self.textColor = "rgb(150, 150, 150)"  # GRIS CLAIR
        self.titleColor = "rgb(42, 42, 42)"

        self.initLink()
        self.initScriptJobs()

        self.initVisibility()
        self.initVisPivot()
        self.initDoubleSide()
        self.initNoHistory()
        self.initToggleBorderEdge()

        self.initInterface()
        self.initIcon()
        self.initDisplay()

        self.initMoveSettings()
        self.initRotateSettings()
        self.initScaleSettings()

        self.initSoftSelec()
        self.initSoftValue()
        self.softPresetA()
        self.softVolume()

        self.initSymModelling()
        self.initSymTolerance()

        self.actuToolSettings()
        self.initToggleTweak()
        self.initToolsSettings()
        self.initSelectStyle()
        self.initChannelBox()
        self.initNearClip()
        self.initFarClip()
        self.initHUD()
        self.initDiscrete()

        self.actuSelection()
        self.actuTypeSelection()
        self.actuToolSettings()

    def initIcon(self):
        # user = "m.terray"
        # mayaVersion = "2014-x64"
        # target = "C:/Users/"+user+"/Documents/maya/"+mayaVersion+"/prefs/icons/"

        path_list = os.path.realpath(__file__).split('/')[:-1]
        path_list.extend(['icons'])
        target = ''
        for item in path_list:
            target += item + '/'
        print target

        self.iconLockOn = QtGui.QIcon()
        self.iconLockOn.addPixmap(QtGui.QPixmap(target + "lock_closed_b.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        bt_locks = (self.bt_commonLock, self.bt_displayLock, self.bt_transformLock, self.bt_toolLock, self.bt_softLock)
        for lock in bt_locks:
            lock.setIcon(self.iconLockOn)

        self.iconLockOff = QtGui.QIcon()
        self.iconLockOff.addPixmap(QtGui.QPixmap(target + "lock_open_b.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.presetSoftA = QtGui.QIcon()
        # self.presetSoftA.setIconSize(QtCore.QSize(32, 32))
        self.presetSoftA.addPixmap(QtGui.QPixmap(target + "softPresetA3220.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.presetSoftA.addPixmap(QtGui.QPixmap(target+"softPresetA_w.png"), QtGui.QIcon.Normal, QtGui.QIcon.On) ##OK !
        self.bt_softPresetA.setIcon(self.presetSoftA)

        self.presetSoftB = QtGui.QIcon()
        self.presetSoftB.addPixmap(QtGui.QPixmap(target + "softPresetB3220.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_softPresetB.setIcon(self.presetSoftB)

        self.presetSoftC = QtGui.QIcon()
        self.presetSoftC.addPixmap(QtGui.QPixmap(target + "softPresetC3220.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_softPresetC.setIcon(self.presetSoftC)

    # LIENS entre boutons et fonctions/methodes
    def initLink(self):

        self.bt_commonSelectionOptions.clicked.connect(self.commonSelOpt)
        self.bt_displayMenu.clicked.connect(self.dispMenu)
        self.bt_transformMenu.clicked.connect(self.transMenu)
        self.bt_toolSettings.clicked.connect(self.toolsSettings)
        self.bt_softSelectionMenu.clicked.connect(self.softSymSelectionMenu)

        self.bt_commonLock.clicked.connect(self.commonLock)
        self.bt_displayLock.clicked.connect(self.displayLock)
        self.bt_transformLock.clicked.connect(self.transformLock)
        self.bt_toolLock.clicked.connect(self.toolLock)
        self.bt_softLock.clicked.connect(self.softLock)

        # common selection options
        self.le_transformName.returnPressed.connect(self.renameTransform)

        self.bt_selVert.clicked.connect(self.selVertex)
        self.bt_selEdge.clicked.connect(self.selEdge)
        self.bt_selFace.clicked.connect(self.selFace)
        self.bt_selObj.clicked.connect(self.selObject)
        self.bt_selMulti.clicked.connect(self.selMulti)

        self.le_select.returnPressed.connect(self.selectByName)

        self.cb_history.activated[str].connect(self.openAttributEditor)
        # self.bt_color.clicked.connect(self.setUIcolor)

        self.bt_selectionStyle.clicked.connect(self.selectionStyleSwitch)
        self.bt_camSwitch.clicked.connect(self.camSwitch)

        # display menu
        self.bt_hudInfos.clicked.connect(self.HUDswitch)
        self.bt_toggleGrid.clicked.connect(self.toggleGrid)
        self.bt_backgroundColor.clicked.connect(self.setBackgroundColor)
        self.bt_setChecker.clicked.connect(self.setChecker)

        self.bt_nearClip.clicked.connect(self.setNearClip)
        self.bt_farClip.clicked.connect(self.setFarClip)

        self.bt_xrayMat.clicked.connect(self.useXrayMat)
        self.bt_defaultMat.clicked.connect(self.useDefaultMat)
        self.bt_defaultLight.clicked.connect(self.useDefaultLight)
        self.bt_wireframe.clicked.connect(self.wireOnShaded)

        self.bt_selHighlight.clicked.connect(self.selHighlight)
        self.bt_backFaceCulling.clicked.connect(self.backFaceCulling)
        self.bt_twoSideLight.clicked.connect(self.twoSideLight)
        self.bt_toggleBorderEdge.clicked.connect(self.tglBorderEdges)

        self.bt_isolateSel.clicked.connect(self.isolateSelection)
        self.bt_isolateActu.clicked.connect(self.actuIso)
        self.bt_autoAddIsolate.clicked.connect(self.autoAddIsolate)
        self.bt_addToIsolate.clicked.connect(self.addToIsolate)
        self.bt_removeToIsolate.clicked.connect(self.removeToIsolate)

        # transform menu
        self.bt_resetTranslation.clicked.connect(self.resetTranslation)
        self.bt_resetRotation.clicked.connect(self.resetRotation)
        self.bt_resetScaling.clicked.connect(self.resetScaling)
        self.bt_resetAllTransform.clicked.connect(self.resetAllTransform)

        self.bt_freezeTranslation.clicked.connect(self.freezeTranslate)
        self.bt_freezeRotation.clicked.connect(self.freezeRotate)
        self.bt_freezeScale.clicked.connect(self.freezeScale)
        self.bt_freezeAllTransform.clicked.connect(self.freezeAllTransform)

        self.bt_deleteHistory.clicked.connect(self.deleteHistory)
        self.bt_selNgones.clicked.connect(self.selNgones)
        self.bt_toggleNormals.clicked.connect(self.tglDisplayNormals)
        self.bt_noHistory.clicked.connect(self.noHistory)
        self.bt_centerPivot.clicked.connect(self.centerPivot)

        self.bt_alignX.clicked.connect(self.alignX)
        self.bt_alignY.clicked.connect(self.alignY)
        self.bt_alignZ.clicked.connect(self.alignZ)
        self.bt_makeLive.clicked.connect(self.makeLiveMesh)

        self.bt_visibility.clicked.connect(self.visibility)
        self.bt_visPivot.clicked.connect(self.visPivot)
        self.bt_doubleSide.clicked.connect(self.doubleSide)

        self.bt_matchAll.clicked.connect(self.matchAllTransforms)
        self.bt_matchTranslate.clicked.connect(self.matchTranslate)
        self.bt_matchRotate.clicked.connect(self.matchRotate)
        self.bt_matchScale.clicked.connect(self.matchScale)
        # self.bt_matchPivot.clicked.connect(self.matchPivot)

        # soft selection tool
        self.bt_softSelection.toggled.connect(self.softSelection)
        self.le_softValue.returnPressed.connect(self.softValue)
        self.bt_softVolume.clicked.connect(self.softVolume)
        self.bt_softGlobal.clicked.connect(self.softGlobal)
        self.bt_softSurface.clicked.connect(self.softSurface)
        self.bt_softObject.clicked.connect(self.softObject)
        self.bt_softPresetA.clicked.connect(self.softPresetA)
        self.bt_softPresetB.clicked.connect(self.softPresetB)
        self.bt_softPresetC.clicked.connect(self.softPresetC)
        self.bt_resetSoft.clicked.connect(self.softReset)

        # symmetric	tool
        self.bt_symMod.toggled.connect(self.symmetricModelling)
        self.le_symTolerance.returnPressed.connect(self.symTolerance)
        self.bt_symSwitch.clicked.connect(self.symSwitch)
        self.bt_symX.clicked.connect(self.symX)
        self.bt_symY.clicked.connect(self.symY)
        self.bt_symZ.clicked.connect(self.symZ)
        self.bt_resetSym.clicked.connect(self.symReset)

        # mirror
        self.bt_mirrorNegX.clicked.connect(self.mirrorNegX)
        self.bt_mirrorPosX.clicked.connect(self.mirrorPosX)
        self.bt_mirrorNegY.clicked.connect(self.mirrorNegY)
        self.bt_mirrorPosY.clicked.connect(self.mirrorPosY)
        self.bt_mirrorNegZ.clicked.connect(self.mirrorNegZ)
        self.bt_mirrorPosZ.clicked.connect(self.mirrorPosZ)

        # Panneau d'options pour le move
        self.bt_objectMove.clicked.connect(self.objectMove)
        self.bt_localMove.clicked.connect(self.localMove)
        self.bt_worldMove.clicked.connect(self.worldMove)
        self.bt_normalMove.clicked.connect(self.normalMove)
        self.bt_tweak.toggled.connect(self.tweakMod)
        self.bt_discreteMove.toggled.connect(self.discreteMove)
        for s in ("05", "45"):  # "10", "25", "45"):
            btn = getattr(self, "bt_m" + s)
            btn.clicked.connect(self.setMoveStep)
        # self.bt_m05.clicked.connect(self.setMoveStep)
        # self.bt_m10.clicked.connect(self.setMoveStep)...
        self.sb_discreteMoveValue.valueChanged.connect(self.setDiscreteMoveValue)
        self.bt_resetMove.clicked.connect(self.resetMove)

        # Panneau d'options pour le rotate
        self.bt_localRotate.clicked.connect(self.localRotate)
        self.bt_worldRotate.clicked.connect(self.worldRotate)
        self.bt_gimbalRotate.clicked.connect(self.gimbalRotate)
        self.bt_defaultPivotRotate.clicked.connect(self.defautPivotRotate)
        self.bt_objectPivotRotate.clicked.connect(self.objectPivotRotate)
        self.bt_manipPivotRotate.clicked.connect(self.manipPivotRotate)
        self.bt_discreteRotate.toggled.connect(self.discreteRotate)
        for s in ("05", "45"):  # "10", "25", "45"):
            btn = getattr(self, "bt_r" + s)
            btn.clicked.connect(self.setRotateStep)
        self.sb_discreteRotateValue.valueChanged.connect(self.setDiscreteRotateValue)
        self.bt_resetRotate.clicked.connect(self.resetRotate)

        # Panneau d'options pour le scale
        self.bt_objectScale.clicked.connect(self.objectScale)
        self.bt_localScale.clicked.connect(self.localScale)
        self.bt_worldScale.clicked.connect(self.worldScale)
        self.bt_normalScale.clicked.connect(self.normalScale)
        self.bt_defaultPivotScale.clicked.connect(self.defautPivotScale)
        self.bt_objectPivotScale.clicked.connect(self.objectPivotScale)
        self.bt_manipPivotScale.clicked.connect(self.manipPivotScale)
        self.bt_discreteScale.toggled.connect(self.discreteScale)
        for s in ("05", "45"):  # "10", "25", "45"):
            btn = getattr(self, "bt_s" + s)
            btn.clicked.connect(self.setScaleStep)
        self.sb_discreteScaleValue.valueChanged.connect(self.setDiscreteScaleValue)
        self.bt_resetScale.clicked.connect(self.resetScale)

    # DEFINITION DES FONCTIONS D'INITIALISATION :	

    def initNearClip(self):
        nrClipPlane = mc.viewClipPlane("perspShape", q=True, nearClipPlane=True)

    def initFarClip(self):
        frClipPlane = mc.viewClipPlane("perspShape", q=True, farClipPlane=True)

    def initHUD(self):
        # hidding or remove all HUD elements
        self.HUDList = ['HUDObjDetBackfaces',
                        'HUDObjDetSmoothness',
                        'HUDObjDetInstance',
                        'HUDObjDetDispLayer',
                        'HUDObjDetDistFromCam',
                        'HUDObjDetNumSelObjs',
                        'HUDPolyCountVerts',
                        'HUDPolyCountEdges',
                        'HUDPolyCountFaces',
                        'HUDPolyCountTriangles',
                        'HUDPolyCountUVs']
        for HUDName in self.HUDList:
            if mc.headsUpDisplay(HUDName, q=True, visible=True):
                mc.headsUpDisplay(HUDName, edit=True, visible=False)

        mc.headsUpDisplay('HUDvertex', rem=True)
        mc.headsUpDisplay('HUDedges', rem=True)
        mc.headsUpDisplay('HUDfaces', rem=True)

        # show HUD with just modeling selection information (obj, vertex, edges, face)
        self.HUDswitch()
        self.bt_hudInfos.setChecked(True)
        self.HUDState = 1

    def initSelectStyle(self):
        self.bt_selectionStyle.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                       "selection-background-color: rgb(150, 150, 150);\n")
        if mc.selectPref(q=True, paintSelect=True):
            self.bt_selectionStyle.setText("Drag")
            if mc.selectPref(q=True, paintSelectWithDepth=True):
                self.bt_camSwitch.setChecked(True)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")
            else:
                self.bt_camSwitch.setChecked(False)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
        else:
            self.bt_selectionStyle.setText("Marquee")
            if mc.selectPref(q=True, useDepth=True):
                self.bt_camSwitch.setChecked(True)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")
            else:
                self.bt_camSwitch.setChecked(False)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")

    def initVisibility(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            selectionList = mc.ls(selection=True, type='transform')
            stateVIS = mc.getAttr(selectionList[-1] + ".visibility")
            self.bt_visibility.setChecked(stateVIS)
            if stateVIS:
                self.bt_visibility.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                           "selection-background-color: rgb(150, 150, 150);\n")
            else:
                self.bt_visibility.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                             "selection-background-color: " + self.selectColor + ";\n")

    def initVisPivot(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            selectionList = mc.ls(selection=True, type='transform')
            stateVisPivot = mc.getAttr(selectionList[-1] + ".displayRotatePivot")
            self.bt_visPivot.setChecked(stateVisPivot)
            if stateVisPivot:
                self.bt_visPivot.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                         "selection-background-color: rgb(150, 150, 150);\n")
            else:
                self.bt_visPivot.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")

    def initDoubleSide(self):
        # selectionList = mc.ls( selection=True, type='mesh' )
        # print ">> bouton doubleside OFF"
        '''startSelection = mc.ls(selection=True)#, type="transform")
        if startSelection:
            selShapes = mc.listRelatives(startSelection, shapes=True)
            if selShapes:
                selLocShapes = mc.ls(type='locator')
                if selLocShapes:
                    for obj in selLocShapes:
                        selShapes.remove(obj)
                selectionList = mc.listRelatives(selShapes, p=True)

                if selectionList:
                    stateDF = mc.getAttr(selectionList[-1]+".doubleSided")
                    self.bt_doubleSide.setChecked(stateDF)
                    if stateDF:
                        self.bt_doubleSide.setStyleSheet("background-color: "+self.selectColor+";\n"
                                                                "selection-background-color: rgb(150, 150, 150);\n")
                    else:
                        self.bt_doubleSide.setStyleSheet("background-color: "+self.unSelectColor+";\n"
                                                            "selection-background-color: "+self.selectColor+";\n")
            else:
                self.bt_doubleSide.setChecked(False)
        else:
        self.bt_doubleSide.setChecked(False)'''

    def initToggleBorderEdge(self):
        stateBorder = mc.polyOptions(displayBorder=True, newPolymesh=True, q=True)[0]
        if stateBorder:  # mc.polyOptions(displayBorder=True, newPolymesh=True, q=True):
            print ">> Border visible"
            self.bt_toggleBorderEdge.setChecked(True)
            self.bt_toggleBorderEdge.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                             "selection-background-color: rgb(150, 150, 150);\n")
        else:
            print ">> Border not visible"
            self.bt_toggleBorderEdge.setChecked(False)
            self.bt_toggleBorderEdge.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                               "selection-background-color: " + self.selectColor + ";\n")

    def initNoHistory(self):
        stateHistory = mc.constructionHistory(q=True, tgl=True)
        if stateHistory:
            self.bt_noHistory.setChecked(True)
            self.bt_noHistory.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                      "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_noHistory.setChecked(False)
            self.bt_noHistory.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")

    def initInterface(self):
        # bt_commonSelectionOptions
        self.bt_commonSelectionOptions.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                              "color: " + self.selectColor + ";\n"  # "border-color: "+self.selectColor+";\n"  # "border-width: 2px;"  # "border-style: solid;"  # "border-color: blue;"  # "border-radius: 11px;"  # "text-align: left;"
                                                                                                                             "font-weight: bold;"
                                                                                                                             "selection-background-color: " + self.selectColor + ";\n")
        self.bt_commonSelectionOptions.setDisabled(True)

        # bt_displayMenu
        self.bt_displayMenu.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                   "color: " + self.selectColor + ";\n"
                                                                                                                  "font-weight: bold;"
                                                                                                                  "selection-background-color: " + self.selectColor + ";\n")
        self.bt_displayMenu.setDisabled(True)

        # bt_transformMenu
        self.bt_transformMenu.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                     "color: " + self.selectColor + ";\n"
                                                                                                                    "font-weight: bold;"
                                                                                                                    "selection-background-color: " + self.selectColor + ";\n")
        self.bt_transformMenu.setDisabled(True)

        # bt_toolSettings
        self.bt_toolSettings.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                    "color: " + self.selectColor + ";\n"
                                                                                                                   "font-weight: bold;"
                                                                                                                   "selection-background-color: " + self.selectColor + ";\n")
        self.bt_toolSettings.setDisabled(True)

        # bt_softSelectionMenu	
        self.bt_softSelectionMenu.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                         "color: " + self.selectColor + ";\n"
                                                                                                                        "font-weight: bold;"
                                                                                                                        "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softSelectionMenu.setDisabled(True)

        # lock
        self.bt_commonLock.setChecked(True)
        self.bt_commonLock.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                  "color: " + self.selectColor + ";\n"
                                                                                                                 "font-weight: bold;"
                                                                                                                 "selection-background-color: " + self.selectColor + ";\n")

        self.bt_displayLock.setChecked(True)
        self.bt_displayLock.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                   "color: " + self.selectColor + ";\n"
                                                                                                                  "font-weight: bold;"
                                                                                                                  "selection-background-color: " + self.selectColor + ";\n")

        self.bt_transformLock.setChecked(True)
        self.bt_transformLock.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                     "color: " + self.selectColor + ";\n"
                                                                                                                    "font-weight: bold;"
                                                                                                                    "selection-background-color: " + self.selectColor + ";\n")

        self.bt_toolLock.setChecked(True)
        self.bt_toolLock.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                "color: " + self.selectColor + ";\n"
                                                                                                               "font-weight: bold;"
                                                                                                               "selection-background-color: " + self.selectColor + ";\n")

        self.bt_softLock.setChecked(True)
        self.bt_softLock.setStyleSheet("background-color: " + self.titleColor + ";\n"
                                                                                "color: " + self.selectColor + ";\n"
                                                                                                               "font-weight: bold;"
                                                                                                               "selection-background-color: " + self.selectColor + ";\n")

    def initDisplay(self):
        print ">> initDisplay"
        # bt_xrayMat
        if mc.modelEditor("modelPanel4", q=True, xray=True):  # probleme a regler : "modelPanel4" !!!		
            self.bt_xrayMat.setChecked(True)
            self.bt_xrayMat.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                    "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_xrayMat.setChecked(False)
            self.bt_xrayMat.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")

        # bt_defaultMat
        if mc.modelEditor("modelPanel4", q=True, useDefaultMaterial=True):  # probleme a regler : "modelPanel4" !!!
            self.bt_defaultMat.setChecked(True)
            self.bt_defaultMat.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                       "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_defaultMat.setChecked(False)
            self.bt_defaultMat.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")

        # bt_defaultLight
        self.bt_defaultLight.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                     "selection-background-color: rgb(150, 150, 150);\n")
        if mc.modelEditor("modelPanel4", q=True,
                          displayLights=True) == "default":  # probleme a regler : "modelPanel4" !!!
            self.bt_defaultLight.setText("DF LT")
        if mc.modelEditor("modelPanel4", q=True, displayLights=True) == "none":
            self.bt_defaultLight.setText("NO LT")

        # bt_wireframe
        if mc.modelEditor("modelPanel4", q=True, wireframeOnShaded=True):  # probleme a regler : "modelPanel4" !!!		
            self.bt_wireframe.setChecked(True)
            self.bt_wireframe.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                      "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_wireframe.setChecked(False)
            self.bt_wireframe.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")

        # bt_selHighlight
        if mc.modelEditor("modelPanel4", q=True, selectionHiliteDisplay=True):  # probleme a regler : "modelPanel4" !!!
            self.bt_selHighlight.setChecked(True)
            self.bt_selHighlight.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                         "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_selHighlight.setChecked(False)
            self.bt_selHighlight.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")

        # bt_backFaceCulling
        if mc.modelEditor("modelPanel4", q=True, backfaceCulling=True):  # probleme a regler : "modelPanel4" !!!
            self.bt_backFaceCulling.setChecked(True)
            self.bt_backFaceCulling.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                            "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_backFaceCulling.setChecked(False)
            self.bt_backFaceCulling.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                              "selection-background-color: " + self.selectColor + ";\n")

        # bt_twoSideLight
        if mc.modelEditor("modelPanel4", q=True, twoSidedLighting=True):  # probleme a regler : "modelPanel4" !!!	
            self.bt_twoSideLight.setChecked(True)
            self.bt_twoSideLight.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                         "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_twoSideLight.setChecked(False)
            self.bt_twoSideLight.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")

        # bt_toggleGrid
        if mc.grid(toggle=True, q=True):
            self.bt_toggleGrid.setChecked(True)
            self.bt_toggleGrid.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                       "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_toggleGrid.setChecked(False)
            self.bt_toggleGrid.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")

        # bt_isolateSel	
        if mc.isolateSelect("modelPanel4", q=True, state=True):  # probleme a regler : "modelPanel4" !!!	
            self.bt_isolateSel.setChecked(True)
            self.bt_isolateSel.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                       "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_isolateSel.setChecked(False)
            self.bt_isolateSel.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")

        # bt_autoAddIsolate												
        if isAutoAddNewObjsEnabled():
            self.bt_autoAddIsolate.setChecked(True)
            self.bt_autoAddIsolate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                           "selection-background-color: rgb(150, 150, 150);\n")
        else:
            self.bt_autoAddIsolate.setChecked(False)
            self.bt_autoAddIsolate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                             "selection-background-color: " + self.selectColor + ";\n")

    def initDiscrete(self):
        self.bt_discreteMove.setChecked(mc.manipMoveContext("Move", q=True, snap=True))
        self.sb_discreteMoveValue.setValue(mc.manipMoveContext("Move", q=True, snapValue=True))

        self.bt_discreteRotate.setChecked(mc.manipRotateContext("Rotate", q=True, snap=True))
        self.sb_discreteRotateValue.setValue(mc.manipRotateContext("Rotate", q=True, snapValue=True))

        self.bt_discreteScale.setChecked(mc.manipScaleContext("Scale", q=True, snap=True))
        self.sb_discreteScaleValue.setValue(mc.manipScaleContext("Scale", q=True, snapValue=True))

    def initSoftSelec(self):
        if mc.softSelect(q=True, softSelectEnabled=True):
            self.bt_softSelection.setChecked(True)
            self.bt_softSelection.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")

    def initSoftValue(self):
        softValue = mc.softSelect(q=True, softSelectDistance=True)
        self.le_softValue.setText(str(softValue))

    def initSymModelling(self):
        if mc.symmetricModelling(q=True, symmetry=True):
            self.bt_symMod.setChecked(True)
            self.bt_symMod.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_symSwitch.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                      "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_symSwitch.setText(str(mc.symmetricModelling(q=True, about=True)).capitalize())

    def initSymTolerance(self):
        symTolerance = mc.symmetricModelling(q=True, tolerance=True)
        self.le_symTolerance.setText(str(symTolerance))

    def initToolsSettings(self):
        self.wg_moveSettings.setVisible(False)
        self.wg_rotateSettings.setVisible(False)
        self.wg_scaleSettings.setVisible(False)
        self.wg_nullSettings.setVisible(True)

    def initMoveSettings(self):
        state = mc.manipMoveContext("Move", q=True, mode=True)
        if state == 0:
            self.bt_objectMove.setChecked(True)
            self.bt_objectMove.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                       "selection-background-color: rgb(150, 150, 150);\n")

            self.bt_worldMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")
            self.bt_localMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")
            self.bt_normalMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
        if state == 1:
            self.bt_localMove.setChecked(True)
            self.bt_localMove.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                      "selection-background-color: rgb(150, 150, 150);\n")

            self.bt_worldMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")
            self.bt_objectMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
            self.bt_normalMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
        if state == 2:
            self.bt_worldMove.setChecked(True)
            self.bt_worldMove.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                      "selection-background-color: rgb(150, 150, 150);\n")

            self.bt_objectMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
            self.bt_localMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")
            self.bt_normalMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
        if state == 3:
            self.bt_normalMove.setChecked(True)
            self.bt_normalMove.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                       "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_worldMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")
            self.bt_localMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")
            self.bt_objectMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")

    def initRotateSettings(self):
        stateA = mc.manipRotateContext("Rotate", q=True, mode=True)
        if stateA == 0:
            self.bt_localRotate.setChecked(True)
            self.bt_localRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                        "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_worldRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
            self.bt_gimbalRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
        if stateA == 1:
            self.bt_worldRotate.setChecked(True)
            self.bt_worldRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                        "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_localRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
            self.bt_gimbalRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
        if stateA == 2:
            self.bt_gimbalRotate.setChecked(True)
            self.bt_gimbalRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                         "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_worldRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
            self.bt_localRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")

        stateB = mc.manipRotateContext("Rotate", q=True, useManipPivot=True)
        stateC = mc.manipRotateContext("Rotate", q=True, useObjectPivot=True)
        stateD = stateB, stateC

        if stateD == (0, 0):
            self.bt_defaultPivotRotate.setChecked(True)
            self.bt_defaultPivotRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                               "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_objectPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                "selection-background-color: " + self.selectColor + ";\n")
            self.bt_manipPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                               "selection-background-color: " + self.selectColor + ";\n")
        if stateD == (0, 1):
            self.bt_objectPivotRotate.setChecked(True)
            self.bt_objectPivotRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                              "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_defaultPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                 "selection-background-color: " + self.selectColor + ";\n")
            self.bt_manipPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                               "selection-background-color: " + self.selectColor + ";\n")
        if stateD == (1, 0):
            self.bt_manipPivotRotate.setChecked(True)
            self.bt_manipPivotRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                             "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_defaultPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                 "selection-background-color: " + self.selectColor + ";\n")
            self.bt_objectPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                "selection-background-color: " + self.selectColor + ";\n")

    def initScaleSettings(self):
        stateA = mc.manipScaleContext("Scale", q=True, mode=True)
        if stateA == 0:
            self.bt_objectScale.setChecked(True)
            self.bt_objectScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                        "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_worldScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
            self.bt_localScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
            self.bt_normalScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
        if stateA == 1:
            self.bt_localScale.setChecked(True)
            self.bt_localScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                       "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_worldScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
            self.bt_objectScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
            self.bt_normalScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
        if stateA == 2:
            self.bt_worldScale.setChecked(True)
            self.bt_worldScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                       "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_objectScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
            self.bt_localScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
            self.bt_normalScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
        if stateA == 3:
            self.bt_normalScale.setChecked(True)
            self.bt_normalScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                        "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_worldScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
            self.bt_localScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
            self.bt_objectScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")

        stateB = mc.manipScaleContext("Scale", q=True, useManipPivot=True)
        stateC = mc.manipScaleContext("Scale", q=True, useObjectPivot=True)
        stateD = stateB, stateC

        if stateD == (0, 0):
            self.bt_defaultPivotScale.setChecked(True)
            self.bt_defaultPivotScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                              "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_objectPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                               "selection-background-color: " + self.selectColor + ";\n")
            self.bt_manipPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                              "selection-background-color: " + self.selectColor + ";\n")

        if stateD == (0, 1):
            self.bt_objectPivotScale.setChecked(True)
            self.bt_objectPivotScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                             "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_defaultPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                "selection-background-color: " + self.selectColor + ";\n")
            self.bt_manipPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                              "selection-background-color: " + self.selectColor + ";\n")

        if stateD == (1, 0):
            self.bt_manipPivotScale.setChecked(True)
            self.bt_manipPivotScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                            "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_objectPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                               "selection-background-color: " + self.selectColor + ";\n")
            self.bt_defaultPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                "selection-background-color: " + self.selectColor + ";\n")

    def initToggleTweak(self):
        mc.STRSTweakModeOff()
        self.bt_tweak.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                "selection-background-color: " + self.selectColor + ";\n")
        self.toggleTweak = 0

    def initChannelBox(self):
        sTmpWin = mc.window("channelBoxTmpWindow")
        mc.formLayout('channelBoxTmpForm')
        sChboxName = mc.channelBox('Channel Box',
                                   attributeEditorMode=False,
                                   containerAtTop=False,
                                   precision=3,
                                   w=self.wg_channelBox.width(),
                                   h=self.wg_channelBox.height(),
                                   # fixedAttrList = ("translateX","translateY","translateZ","rotateX","rotateY","rotateZ","scaleX","scaleY","scaleZ")
        )
        qChbox = controlToPySide(sChboxName)
        self.lt_channelBox.addWidget(qChbox)
        mc.deleteUI(sTmpWin, window=True)

    def initScriptJobs(self):
        self.scriptJobIds.append(mc.scriptJob(event=("SelectModeChanged", catchJobException(self.actuTypeSelection))))
        self.scriptJobIds.append(mc.scriptJob(event=("SelectTypeChanged", catchJobException(self.actuTypeSelection))))
        self.scriptJobIds.append(mc.scriptJob(event=("SelectionChanged", catchJobException(self.actuSelection))))
        self.scriptJobIds.append(mc.scriptJob(event=("ToolChanged", catchJobException(self.actuToolSettings))))
        self.scriptJobIds.append(mc.scriptJob(event=("ModelPanelSetFocus", catchJobException(self.testJob))))
        self.scriptJobIds.append(mc.scriptJob(event=("modelEditorChanged", catchJobException(self.initDisplay))))

    def testJob(self):
        print ">> Panel Actif : " + mc.getPanel(withFocus=True)

    def closeEvent(self, event):
        print ">> Bye bye !"
        try:
            if self.scriptJobIds:
                for jobId in self.scriptJobIds:
                    mc.scriptJob(kill=jobId)
                    print ">> Job {0} killed".format(jobId)
        finally:
            return QtGui.QWidget.closeEvent(self, event)

    # # FONCTIONS APPELE PAR LES BOUTONS DE LA "KMAX TOOL BAR"

    # # bouton pour toggle visibility des panneaux

    def commonSelOpt(self):
        state = self.wg_commonSelectionOptions.isVisible()
        if state:
            self.wg_commonSelectionOptions.setVisible(False)
        else:
            self.wg_commonSelectionOptions.setVisible(True)

    def commonLock(self):
        if self.bt_commonLock.isChecked():
            self.bt_commonSelectionOptions.setDisabled(True)
            self.bt_commonLock.setIcon(self.iconLockOn)
        else:
            self.bt_commonSelectionOptions.setDisabled(False)
            self.bt_commonLock.setIcon(self.iconLockOff)

    def dispMenu(self):
        state = self.wg_displayMenu.isVisible()
        if state:
            self.wg_displayMenu.setVisible(False)
        else:
            self.wg_displayMenu.setVisible(True)

    def displayLock(self):
        if self.bt_displayLock.isChecked():
            self.bt_displayMenu.setDisabled(True)
            self.bt_displayLock.setIcon(self.iconLockOn)
        else:
            self.bt_displayMenu.setDisabled(False)
            self.bt_displayLock.setIcon(self.iconLockOff)

    def transMenu(self):
        state = self.wg_transformMenu.isVisible()
        if state:
            self.wg_transformMenu.setVisible(False)
        else:
            self.wg_transformMenu.setVisible(True)

    def transformLock(self):
        if self.bt_transformLock.isChecked():
            self.bt_transformMenu.setDisabled(True)
            self.bt_transformLock.setIcon(self.iconLockOn)
        else:
            self.bt_transformMenu.setDisabled(False)
            self.bt_transformLock.setIcon(self.iconLockOff)

    def toolsSettings(self):
        ctx = mc.currentCtx()
        ctxType = mc.contextInfo(ctx, c=True)
        if ctxType == "manipMove":
            state = self.wg_moveSettings.isVisible()
            if state:
                self.wg_moveSettings.setVisible(False)
            else:
                self.wg_moveSettings.setVisible(True)
        if ctxType == "manipRotate":
            state = self.wg_rotateSettings.isVisible()
            if state:
                self.wg_rotateSettings.setVisible(False)
            else:
                self.wg_rotateSettings.setVisible(True)
        if ctxType == "manipScale":
            state = self.wg_scaleSettings.isVisible()
            if state:
                self.wg_scaleSettings.setVisible(False)
            else:
                self.wg_scaleSettings.setVisible(True)
        if ctxType == "selectTool":
            state = self.wg_nullSettings.isVisible()
            if state:
                self.wg_nullSettings.setVisible(False)
            else:
                self.wg_nullSettings.setVisible(True)

    def toolLock(self):
        if self.bt_toolLock.isChecked():
            self.bt_toolSettings.setDisabled(True)
            self.bt_toolLock.setIcon(self.iconLockOn)
        else:
            self.bt_toolSettings.setDisabled(False)
            self.bt_toolLock.setIcon(self.iconLockOff)

    def softSymSelectionMenu(self):
        state = self.wg_softSymSettings.isVisible()
        if state:
            self.wg_softSymSettings.setVisible(False)
        else:
            self.wg_softSymSettings.setVisible(True)

    def softLock(self):
        if self.bt_softLock.isChecked():
            self.bt_softSelectionMenu.setDisabled(True)
            self.bt_softLock.setIcon(self.iconLockOn)
        else:
            self.bt_softSelectionMenu.setDisabled(False)
            self.bt_softLock.setIcon(self.iconLockOff)

    # # COMMON SELECTION OPTIONS

    def selectByName(self):
        mc.select(str(self.le_select.text()))

    def selVertex(self):
        mc.selectMode(component=True)
        mc.selectType(vertex=True)

    def selEdge(self):
        mc.selectMode(component=True)
        mc.selectType(edge=True)

    def selFace(self):
        mc.selectMode(component=True)
        mc.selectType(facet=True)

    def selObject(self):
        mc.selectMode(object=True)

    def selMulti(self):
        mc.selectMode(component=True)
        mc.selectType(meshComponents=True)

    def setNearClip(self):
        self.value = ["0.1", "1", "3"]
        if self.nearValue == 3:
            self.nearValue = 0
        self.allCamShape = ("perspShape", "topShape", "frontShape", "sideShape")
        if self.allCamShape:
            for camShape in self.allCamShape:
                self.bt_nearClip.setText("Near " + self.value[self.nearValue])
                mc.setAttr(camShape + ".nearClipPlane", float(self.value[self.nearValue]))
            self.nearValue = self.nearValue + 1


    def setFarClip(self):
        self.value = ["100", "100000"]
        if self.farValue == 2:
            self.farValue = 0
        self.allCamShape = ("perspShape", "topShape", "frontShape", "sideShape")
        if self.allCamShape:
            for camShape in self.allCamShape:
                self.bt_farClip.setText("Far " + self.value[self.farValue])
                mc.setAttr(camShape + ".farClipPlane", float(self.value[self.farValue]))
            self.farValue = self.farValue + 1

    def selectionStyleSwitch(self):
        if mc.selectPref(q=True, paintSelect=True):
            mc.selectPref(paintSelect=0)
            self.bt_selectionStyle.setText("Marquee")
            print ">> Selection mode is MARQUEE."
            if mc.selectPref(q=True, useDepth=True):
                self.bt_camSwitch.setChecked(True)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")
            else:
                self.bt_camSwitch.setChecked(False)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
        else:
            mc.selectPref(paintSelect=1)
            self.bt_selectionStyle.setText("Drag")
            print ">> Selection mode is DRAG."
            if mc.selectPref(q=True, paintSelectWithDepth=True):
                self.bt_camSwitch.setChecked(True)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")
            else:
                self.bt_camSwitch.setChecked(False)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")

    def camSwitch(self):
        if mc.selectPref(q=True, paintSelect=True):
            if mc.selectPref(q=True, paintSelectWithDepth=True):
                mc.selectPref(paintSelectWithDepth=0)
                self.bt_camSwitch.setChecked(False)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
            else:
                mc.selectPref(paintSelectWithDepth=1)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")
        else:
            if mc.selectPref(q=True, useDepth=True):
                mc.selectPref(useDepth=0)
                self.bt_camSwitch.setChecked(False)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
            else:
                mc.selectPref(useDepth=1)
                self.bt_camSwitch.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")

    # # DISPLAY MENU

    def actuSelection(self):
        self.initVisibility()
        self.initDoubleSide()
        self.initVisPivot()

        # print ">> State of visibility and double side updated"

        selectionList = mc.ls(selection=True, o=True)
        if selectionList:
            self.le_transformName.setText(selectionList[-1])

        self.cb_history.clear()

        if selectionList:
            history = mc.listHistory(selectionList, il=2)
            histNum = len(history)
            self.le_shapeName.setText(history[0])
            for n in range(1, histNum):
                # for selec in history:
                selec = history[n]
                # print ">> selec : ", selec
                # print ">> history : ", history[-1]
                self.cb_history.addItem(selec)

    def openAttributEditor(self, text):
        # modifier = self.cb_history.currentText()				# plus besoin grace a : activated[str]	
        print ">> Index Activated : ", text
        pm.mel.showEditor(text)

    # pm.mel.copyAEWindow()									# pour copier l'attribut editor dans un panneau
    # pm.mel.ToggleAttributeEditor()						# masquer l'attribut editor complet pour ne voir plus que le panneau simple

    def showInputs(self):
        selectionList = mc.ls(selection=True, o=True)
        if selectionList:
            history = mc.listHistory(selectionList, interestLevel=2)

    def actuToolSettings(self):
        ctx = mc.currentCtx()
        ctxType = mc.contextInfo(ctx, c=True)
        # self.bt_toolSettings.isEnabled() and
        if self.wg_moveSettings.isVisible() or self.wg_rotateSettings.isVisible() or self.wg_scaleSettings.isVisible() or self.wg_nullSettings.isVisible():
            if ctxType == "manipMove":
                # if self.bt_toolSettings.isEnabled():
                self.wg_rotateSettings.setVisible(False)
                self.wg_scaleSettings.setVisible(False)
                self.wg_nullSettings.setVisible(False)
                self.wg_moveSettings.setVisible(True)
                self.initMoveSettings()
                self.bt_toolSettings.setText("Move Settings")
            if ctxType == "manipRotate":
                self.wg_moveSettings.setVisible(False)
                self.wg_scaleSettings.setVisible(False)
                self.wg_nullSettings.setVisible(False)
                self.wg_rotateSettings.setVisible(True)
                self.initRotateSettings()
                self.bt_toolSettings.setText("Rotate Settings")
            if ctxType == "manipScale":
                self.wg_moveSettings.setVisible(False)
                self.wg_rotateSettings.setVisible(False)
                self.wg_nullSettings.setVisible(False)
                self.wg_scaleSettings.setVisible(True)
                self.initScaleSettings()
                self.bt_toolSettings.setText("Scale Settings")
            if ctxType == "selectTool":
                self.wg_moveSettings.setVisible(False)
                self.wg_rotateSettings.setVisible(False)
                self.wg_scaleSettings.setVisible(False)
                self.wg_nullSettings.setVisible(True)
                self.bt_toolSettings.setText("Tool Settings")

    def actuTypeSelection(self):
        print ">> Le type de selection a change !!"
        if mc.selectMode(q=True, object=True):
            self.bt_selObj.setChecked(True)
            self.bt_selObj.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_selVert.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
            self.bt_selEdge.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
            self.bt_selFace.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
            self.bt_selMulti.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                       "selection-background-color: " + self.selectColor + ";\n")
            print ">> Mode Object"

        else:
            if mc.selectType(q=True, vertex=True):
                self.bt_selVert.setChecked(True)
                self.bt_selVert.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                        "selection-background-color: rgb(150, 150, 150);\n")
                self.bt_selObj.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selEdge.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selFace.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selMulti.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
                print ">> Mode Vertex"

            if mc.selectType(q=True, edge=True):
                self.bt_selEdge.setChecked(True)
                self.bt_selEdge.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                        "selection-background-color: rgb(150, 150, 150);\n")
                self.bt_selObj.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selVert.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selFace.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selMulti.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
                print ">> Mode Edge"

            if mc.selectType(q=True, facet=True):
                self.bt_selFace.setChecked(True)
                self.bt_selFace.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                        "selection-background-color: rgb(150, 150, 150);\n")
                self.bt_selObj.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selEdge.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selVert.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selMulti.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
                print ">> Mode Face"

            if mc.selectType(q=True, meshComponents=True):
                self.bt_selMulti.setChecked(True)
                self.bt_selMulti.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                         "selection-background-color: rgb(150, 150, 150);\n")
                self.bt_selObj.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selEdge.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selVert.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
                self.bt_selFace.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
                print ">> Mode Multi"

                # pour renommer l'object selectionne

    def renameTransform(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            mc.rename(selectionList[-1], str(self.le_transformName.text()))
            print ">> Object New Name : " + self.le_transformName.text()
        else:
            print ">> You need a selection"

    def renameShape(self):  # USELESS !
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            history = mc.listHistory(selectionList)
            print ">> Shape New Name : " + self.le_shapeName.text()
        else:
            print ">> You need a selection"

            # selection highlight: 												modelEditor -e -sel false modelPanel4

    def selHighlight(self):
        self.allModelPanel = mc.getPanel(type='modelPanel')
        if self.allModelPanel:
            for modelPanelName in self.allModelPanel:
                state = mc.modelEditor(modelPanelName, q=True, selectionHiliteDisplay=True)
                if state:
                    mc.modelEditor(modelPanelName, e=True, selectionHiliteDisplay=False)
                    self.bt_selHighlight.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                   "selection-background-color: " + self.selectColor + ";\n")
                    print ">> HighLight Selection is OFF."
                else:
                    mc.modelEditor(modelPanelName, e=True, selectionHiliteDisplay=True)
                    self.bt_selHighlight.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                                 "selection-background-color: rgb(150, 150, 150);\n")
                    print ">> HighLight Selection is ON."

                    # toggle no/default light  :

    def useDefaultLight(self):
        self.allModelPanel = mc.getPanel(type='modelPanel')
        if self.allModelPanel:
            for modelPanelName in self.allModelPanel:
                state = mc.modelEditor(modelPanelName, q=True, displayLights=True)
                if state == "default":
                    mc.modelEditor(modelPanelName, e=True, displayLights="none")
                    self.bt_defaultLight.setText("NO LT")
                    print ">> No Light mode."
                else:
                    mc.modelEditor(modelPanelName, e=True, displayLights="default")
                    self.bt_defaultLight.setText("DF LT")
                    print ">> Default Light mode."

                    # setChecker

    def setChecker(self):
        # selectionList = mc.ls( selection=True, type='transform' )
        # mc.shadingNode("file", asTexture=True)
        print ">> NoIcon map apply on object"

    def twoSideLight(self):
        # two side lighting  //modelEditor -e -twoSidedLighting false modelPanel4
        self.allModelPanel = mc.getPanel(type='modelPanel')
        if self.allModelPanel:
            for modelPanelName in self.allModelPanel:
                state = mc.modelEditor(modelPanelName, q=True, twoSidedLighting=True)
                if state:
                    mc.modelEditor(modelPanelName, e=True, twoSidedLighting=False)
                    self.bt_twoSideLight.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                   "selection-background-color: " + self.selectColor + ";\n")
                    print ">> Two sided Lighted is OFF."
                else:
                    mc.modelEditor(modelPanelName, e=True, twoSidedLighting=True)
                    self.bt_twoSideLight.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                                 "selection-background-color: rgb(150, 150, 150);\n")
                    print ">> Two sided Lighted is ON."

                    # toggle border edge visibility

    def tglBorderEdges(self):
        '''
        Toggle poly edge border visibility
        '''
        selectionList = mc.ls(type='mesh')
        '''if not selectionList:
            print ">> No Selection"
            return'''

        # state = mc.getAttr(selectionList[0] + '.displayBorders')
        stateBorder = mc.polyOptions(displayBorder=True, newPolymesh=True, query=True)[0]
        if not stateBorder:
            for obj in selectionList:
                mc.setAttr(obj + '.displayBorders', True)
            self.bt_toggleBorderEdge.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                             "selection-background-color: rgb(150, 150, 150);\n")
            mc.polyOptions(displayBorder=True, newPolymesh=True)
            print ">> Border Edge is Visible"
        else:
            for obj in selectionList:
                mc.setAttr(obj + '.displayBorders', False)
            self.bt_toggleBorderEdge.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                               "selection-background-color: " + self.selectColor + ";\n")
            mc.polyOptions(displayBorder=False, newPolymesh=True)
            print ">> Border Edge is NOT Visible"

    def backFaceCulling(self):
        # ToggleBackfaceCulling

        self.allModelPanel = mc.getPanel(type='modelPanel')
        if self.allModelPanel:
            for modelPanelName in self.allModelPanel:
                state = mc.modelEditor(modelPanelName, q=True, backfaceCulling=True)
                if state:
                    mc.modelEditor(modelPanelName, e=True, backfaceCulling=False)
                    self.bt_backFaceCulling.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                      "selection-background-color: " + self.selectColor + ";\n")
                    print ">> BackFaceCulling is OFF."
                else:
                    mc.modelEditor(modelPanelName, e=True, backfaceCulling=True)
                    self.bt_backFaceCulling.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                                    "selection-background-color: rgb(150, 150, 150);\n")
                    print ">> BackFaceCulling is ON."

    def toggleGrid(self):
        # toggle grid
        state = mc.grid(toggle=True, q=True)
        if state:
            mc.grid(toggle=0)
            self.bt_toggleGrid.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                         "selection-background-color: " + self.selectColor + ";\n")
            print ">> Grid ON."
        # self.bt_toggleGrid.setText("Grid Off")

        else:
            mc.grid(toggle=1)
            self.bt_toggleGrid.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                       "selection-background-color: rgb(150, 150, 150);\n")
            print ">> Grid OFF."
            # self.bt_toggleGrid.setText("Grid On")

    def setBackgroundColor(self):
        mc.displayRGBColor('background', 0.27, 0.27, 0.27)
        self.bt_backgroundColor.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                        "selection-background-color: rgb(150, 150, 150);\n")
        # self.bt_backgroundColor.setStyleSheet(self.textColor = "rgb(150, 150, 150)"
        # self.bt_backgroundColor.setDisabled(True)
        print ">> Background Color SET TO GREY."

    def HUDswitch(self):
        if self.HUDState == 0:
            mc.ToggleObjectDetails()
            # hide useless information in HUD
            mc.headsUpDisplay('HUDObjDetBackfaces', e=True, s=4, b=0, visible=False)
            mc.headsUpDisplay('HUDObjDetSmoothness', e=True, s=4, b=1, visible=False)
            mc.headsUpDisplay('HUDObjDetInstance', e=True, s=4, b=2, visible=False)
            mc.headsUpDisplay('HUDObjDetDispLayer', e=True, s=4, b=3, visible=False)
            mc.headsUpDisplay('HUDObjDetDistFromCam', e=True, s=4, b=4, visible=False)

            # show modeling selection info in HUD
            mc.headsUpDisplay('HUDObjDetNumSelObjs', e=True, ba='right', da='right', dw=50,
                              visible=True)
            mc.headsUpDisplay('HUDvertex', label='Vertex :', ba='right', da='right', dw=50, s=4, b=6,
                              preset="polyVerts",
                              visible=True)
            mc.headsUpDisplay('HUDedges', label='Edges :', ba='right', da='right', dw=50, s=4, b=7, preset="polyEdges",
                              visible=True)
            mc.headsUpDisplay('HUDfaces', label='Faces :', ba='right', da='right', dw=50, s=4, b=8, preset="polyFaces",
                              visible=True)
            self.bt_hudInfos.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                     "selection-background-color: rgb(150, 150, 150);\n")
            # self.bt_hudInfos.setChecked(True)
            self.HUDState = 1
            print ">> HUD is ON."
        else:
            mc.headsUpDisplay('HUDObjDetNumSelObjs', e=True, visible=False)
            mc.headsUpDisplay('HUDvertex', rem=True)
            mc.headsUpDisplay('HUDedges', rem=True)
            mc.headsUpDisplay('HUDfaces', rem=True)
            self.bt_hudInfos.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                       "selection-background-color: " + self.selectColor + ";\n")
            self.HUDState = 0
            print ">> HUD is OFF."

            # x ray 	: setXrayOption true modelPanel4;

    def useXrayMat(self):
        self.allModelPanel = mc.getPanel(type='modelPanel')
        if self.allModelPanel:
            for modelPanelName in self.allModelPanel:
                state = mc.modelEditor(modelPanelName, q=True, xray=True)
                if state:
                    mc.modelEditor(modelPanelName, e=True, xray=False)
                    self.bt_xrayMat.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                              "selection-background-color: " + self.selectColor + ";\n")
                    print ">> Xray is OFF."
                else:
                    mc.modelEditor(modelPanelName, e=True, xray=True)
                    self.bt_xrayMat.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                            "selection-background-color: rgb(150, 150, 150);\n")
                    print "Xray is ON."

    def wireOnShaded(self):  # setWireframeOnShadedOption true modelPanel4;
        self.allModelPanel = mc.getPanel(type='modelPanel')
        if self.allModelPanel:
            for modelPanelName in self.allModelPanel:
                state = mc.modelEditor(modelPanelName, q=True, wireframeOnShaded=True)
                if state:
                    mc.modelEditor(modelPanelName, e=True, wireframeOnShaded=False)
                    self.bt_wireframe.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                "selection-background-color: " + self.selectColor + ";\n")
                    print ">> Wireframe on shaded is OFF."
                else:
                    mc.modelEditor(modelPanelName, e=True, wireframeOnShaded=True)
                    self.bt_wireframe.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                              "selection-background-color: rgb(150, 150, 150);\n")
                    print ">> Wireframe on shaded is ON."

                    # useDefault material: modelEditor -e -udm true modelPanel4;		modelEditor -e -udm true modelPanel4;

    def useDefaultMat(self):
        self.allModelPanel = mc.getPanel(type='modelPanel')
        if self.allModelPanel:
            for modelPanelName in self.allModelPanel:
                state = mc.modelEditor(modelPanelName, q=True, useDefaultMaterial=True)
                if state:
                    mc.modelEditor(modelPanelName, e=True, useDefaultMaterial=False)
                    self.bt_defaultMat.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                 "selection-background-color: " + self.selectColor + ";\n")
                    print ">> Use default material on all object : OFF."
                else:
                    mc.modelEditor(modelPanelName, e=True, useDefaultMaterial=True)
                    self.bt_defaultMat.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                               "selection-background-color: rgb(150, 150, 150);\n")
                    print ">> Use default material on all object : ON."

    # isolate selection : enableIsolateSelect modelPanel4 true; 		isolateSelect -state 1 modelPanel4;
    def isolateSelection(self):
        self.allModelPanel = mc.getPanel(type='modelPanel')
        if self.allModelPanel:
            for modelPanelName in self.allModelPanel:
                state = mc.isolateSelect(modelPanelName, query=True, state=True)
                if state == 0:
                    if mc.selectMode(q=True, object=True):
                        pm.mel.enableIsolateSelect(modelPanelName, 1)
                    else:
                        mc.selectMode(object=True)
                        pm.mel.enableIsolateSelect(modelPanelName, 1)
                        mc.selectMode(component=True)
                    self.bt_isolateSel.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                               "selection-background-color: rgb(150, 150, 150);\n")
                    print ">> Isolate : ON."
                else:
                    pm.mel.enableIsolateSelect(modelPanelName, 0)
                    self.bt_isolateSel.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                 "selection-background-color: " + self.selectColor + ";\n")
                    print ">> Isolate : OFF."

    def actuIso(self):
        self.isolateSelection()
        self.isolateSelection()
        print "toto"
        
    # autoadd to isolate : isoSelectAutoAddNewObjs modelPanel4 true;
    def autoAddIsolate(self):
        # self.allModelPanel = mc.getPanel(type='modelPanel') # ne fonctionne pas sur tous les panels en meme temps... bug maya
        self.focusPanel = mc.getPanel(withFocus=True)
        #bAutoAdd = setIsolateSelectAutoAdd()
        bAutoAdd = isAutoAddNewObjsEnabled()
        if self.focusPanel:
            if not bAutoAdd:
                pm.mel.isoSelectAutoAddNewObjs(self.focusPanel, True)
                self.bt_autoAddIsolate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                               "selection-background-color: rgb(150, 150, 150);\n")
                print ">> Auto add to isolate : ON."
            else:
                pm.mel.isoSelectAutoAddNewObjs(self.focusPanel, False)
                self.bt_autoAddIsolate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                                 "selection-background-color: " + self.selectColor + ";\n")
                print ">> Auto add to isolate : OFF."

                # add to isolate : addSelectedToEditor modelPanel4; isolateSelect -addSelected modelPanel4;

    def addToIsolate(self):
        self.allModelPanel = mc.getPanel(type='modelPanel')
        for modelPanelName in self.allModelPanel:
            mc.isolateSelect(modelPanelName, addSelected=True)
            print ">> Selection is append to Isolate."

            # remove to isolate : removeSelectedFromEditor modelPanel4; 	isolateSelect -removeSelected modelPanel4;

    def removeToIsolate(self):
        self.allModelPanel = mc.getPanel(type='modelPanel')
        for modelPanelName in self.allModelPanel:
            mc.isolateSelect(modelPanelName, removeSelected=True)
            print ">> Selection is remove to Isolate."

    ## TRANSFORM MENU

    def freezeTranslate(self):
        '''
        Freeze object Translation to (0,0,0)
        '''
        print ">> Translate Freezed"
        mc.makeIdentity(a=1, t=1, r=0, s=0, n=0, pn=1)
        self.actuSelection()  # actualiser les valeurs de transform

    def freezeRotate(self):
        '''
        Freeze object Rotation to (0,0,0)
        '''
        print ">> Rotate Freezed"
        mc.makeIdentity(a=1, t=0, r=1, s=0, n=0, pn=1)
        self.actuSelection()  # actualiser les valeurs de transform

    def freezeScale(self):
        '''
        Freeze object Scale to (0,0,0)
        '''
        print ">> Scale Freezed"
        mc.makeIdentity(a=1, t=0, r=0, s=1, n=0, pn=1)
        self.actuSelection()  # actualiser les valeurs de transform

    def freezeAllTransform(self):
        '''
        Freeze All Transform on selected Objects
        '''
        print ">> All transformations Freezed"
        mc.makeIdentity(a=1, t=1, r=1, s=1, n=1, pn=1)
        # mc.FreezeTransformations()
        # makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;
        self.actuSelection()  # actualiser les valeurs de transform

    def resetTranslation(self):
        '''
        Reset object Translation to the origin (0,0,0)
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        for obj in selectionList:
            mc.xform(obj, absolute=True, t=[0, 0, 0])

    def resetRotation(self):
        '''
        Reset object Rotation to (0,0,0)
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        for obj in selectionList:
            mc.xform(obj, absolute=True, ro=[0, 0, 0])

    def resetScaling(self):
        '''
        Reset object Scaling to (1,1,1)
        '''
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        for obj in selectionList:
            mc.xform(obj, absolute=True, s=[1, 1, 1])

    def resetAllTransform(self):
        """
        Reset All Transform on selected Objects
        """
        selectionList = mc.ls(selection=True, type='transform')
        if not selectionList:
            print ">> No Selection"
        for obj in selectionList:
            mc.xform(obj, absolute=True, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])

    def visibility(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            state = mc.getAttr(selectionList[-1] + ".visibility")
            if state:
                mc.setAttr(selectionList[-1] + ".visibility", 0)
                self.bt_visibility.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                             "selection-background-color: " + self.selectColor + ";\n")
            else:
                mc.setAttr(selectionList[-1] + ".visibility", 1)
                self.bt_visibility.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                           "selection-background-color: rgb(150, 150, 150);\n")
        else:
            '''if self.bt_visibility.setChecked(True):
                self.bt_visibility.setChecked(False)
            else:
                self.bt_visibility.setChecked(True)'''
            print ">> No selection"

    def visPivot(self):
        selectionList = mc.ls(selection=True, type='transform')
        stateScalePivot = mc.getAttr(selectionList[-1] + ".displayScalePivot")
        stateRotatePivot = mc.getAttr(selectionList[-1] + ".displayRotatePivot")
        if stateScalePivot:
            mc.setAttr(selectionList[-1] + ".displayScalePivot", 0)
            mc.setAttr(selectionList[-1] + ".displayRotatePivot", 0)
            self.bt_visPivot.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                       "selection-background-color: " + self.selectColor + ";\n")
        else:
            mc.setAttr(selectionList[-1] + ".displayScalePivot", 1)
            mc.setAttr(selectionList[-1] + ".displayRotatePivot", 1)
            self.bt_visPivot.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                     "selection-background-color: rgb(150, 150, 150);\n")

    def doubleSide(self):
        # selectionList = mc.ls( selection=True, type='mesh' )
        print ">> bouton doubleside OFF"
        '''startSelection = mc.ls(selection=True)#, type="transform")
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
        '''

    def centerPivot(self):
        mc.CenterPivot()
        print ">> Center Pivot"

    def selNgones(self):
        mel.eval(
            'polyCleanupArgList 3 { "0","2","1","0","1","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" };')
        print ">> nGones selected"

    def tglDisplayNormals(self):
        startSelection = mc.ls(selection=True, exactType="transform")
        if startSelection:
            selShapes = mc.listRelatives(startSelection, shapes=True)
            if selShapes:
                #stateNormals = mc.polyOptions(selShapes[-1], displayNormal=True, query=True)[0]
                stateNormals = mc.getAttr(selShapes[-1] + '.displayNormal')
                #print ">> ", startSelection, selShapes[-1], stateNormals

                if stateNormals:
                    for obj in selShapes:
                        mc.polyOptions(obj, displayNormal=False)
                        #mc.setAttr(obj + '.displayNormal', False)
                    msg = ">> Display Normals OFF"
                else:
                    for obj in selShapes:
                        mc.polyOptions(obj, displayNormal=True, facet=True, point=False, sizeNormal=1)
                        #mc.setAttr(obj + '.displayNormal', True)
                    msg = ">> Display Normals ON"
            else:
                msg = ">> No Shape selected"
        else:
            msg = ">> No Selection"

        print msg

    def deleteHistory(self):
        mc.DeleteHistory()
        print ">> History Deleted"

    def noHistory(self):
        history = mc.constructionHistory(q=True, tgl=True)
        if history:
            mc.constructionHistory(tgl=False)
            self.bt_noHistory.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")
            print ">> Without Construction History !!!"
        else:
            mc.constructionHistory(tgl=True)
            self.bt_noHistory.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                      "selection-background-color: rgb(150, 150, 150);\n")
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
                self.bt_makeLive.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
                print ">>", selectionList[-1], "is DEAD"
            else:
                mc.makeLive(selectionList[-1])
                self.makeLiveState = 1
                self.bt_makeLive.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                         "selection-background-color: rgb(150, 150, 150);\n")
                print ">>", selectionList[-1], "is aLIVE"
        else:
            mc.makeLive(none=True)
            self.makeLiveState = 0
            self.bt_makeLive.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                       "selection-background-color: " + self.selectColor + ";\n")
            print ">> No selection // All is DEAD"

    ## MATCH TRANSFORM :

    def matchAllTransforms(self):
        self.matchTranslate()
        self.matchRotate()
        self.matchScale()
        print ">> Match All Transfroms"

    def matchTranslate(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList >= 2:
            newTranslation = mc.xform(selectionList[-1], q=True, translation=True, worldSpace=True)
            for objMacth in selectionList[:-1]:
                mc.xform(objMacth, p=True, translation=newTranslation, worldSpace=True)
        print ">> Match Translate"

    def matchRotate(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList >= 2:
            newRotation = mc.xform(selectionList[-1], q=True, rotation=True, worldSpace=True)
            for objMacth in selectionList[:-1]:
                mc.xform(objMacth, p=True, rotation=newRotation, worldSpace=True)
        print ">> Match Rotate"

    def matchScale(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList >= 2:
            newScale = mc.xform(selectionList[-1], q=True, scale=True)
            for objMacth in selectionList[:-1]:
                mc.xform(objMacth, p=True, scale=newScale)
        print ">> Match Scale"

    def matchPivot(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList >= 2:
            newPivots = mc.xform(selectionList[-1], q=True, scalePivot=True, worldSpace=True)
            for objMacth in selectionList[:-1]:
                mc.xform(objMacth, p=True, translation=newPivots, worldSpace=True)
        print ">> Match Pivot"

    ##SOFT and SYMMETRIC SELECTION PAN :

    def softSelection(self, state):
        self.initSoftValue()
        if state:
            mc.softSelect(softSelectEnabled=1)
            self.bt_softSelection.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")
            print ">> Soft Selection is ON."
        else:
            mc.softSelect(softSelectEnabled=0)
            self.bt_softSelection.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
            print ">> Soft Selection is OFF."
            # "softSelect -e -softSelectEnabled true"

    def softValue(self):
        value = self.le_softValue.text()
        mc.softSelect(softSelectDistance=float(value))

    def softVolume(self):
        mc.softSelect(softSelectFalloff=0)
        self.bt_softVolume.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")

        self.bt_softSurface.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softGlobal.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softObject.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        print ">> Soft selection is on VOLUME."

    # mc.setSoftSelectFalloffMode("Volume")
    # "setSoftSelectFalloffMode( Volume)"

    def softSurface(self):
        mc.softSelect(softSelectFalloff=1)
        self.bt_softSurface.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                    "selection-background-color: rgb(150, 150, 150);\n")

        self.bt_softVolume.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softGlobal.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softObject.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        print ">> Soft selection is on SURFACE."

    # mc.setSoftSelectFalloffMode("Surface")

    def softGlobal(self):
        mc.softSelect(softSelectFalloff=2)
        self.bt_softGlobal.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")

        self.bt_softVolume.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softSurface.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softObject.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        print ">> Soft selection is on GLOBAL."

    # mc.setSoftSelectFalloffMode("Global")

    def softObject(self):
        mc.softSelect(softSelectFalloff=3)
        self.bt_softObject.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")

        self.bt_softVolume.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softSurface.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softGlobal.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        print ">> Soft selection is on OBJECT."

    # mc.setSoftSelectFalloffMode("Object")

    def softPresetA(self):
        mc.softSelect(softSelectCurve=str("1,0,3,0.9,0.3,3,0,1,1"))
        self.bt_softPresetA.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                    "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_softPresetB.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softPresetC.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        print ">> Soft Selection PresetA."

    # softSelect -e -softSelectCurve "1,0.5,2,0,1,2,1,0,2";

    def softPresetB(self):
        mc.softSelect(softSelectCurve=str("1,0,1,0,1,1"))
        self.bt_softPresetB.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                    "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_softPresetA.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softPresetC.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        print ">> Soft Selection PresetB."

    def softPresetC(self):
        mc.softSelect(softSelectCurve=str("1,0,1,0.4,0.15,3,0,1,1"))
        self.bt_softPresetC.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                    "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_softPresetA.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_softPresetB.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        print ">> Soft Selection PresetC."

    def softReset(self):
        mc.softSelect(softSelectReset=1)
        # softSelect -softSelectReset
        self.le_softValue.setText(str(mc.softSelect(q=True, softSelectDistance=True)))
        print ">> Soft Selection is RESET"

    def symmetricModelling(self, state):
        self.initSymTolerance()
        if state:
            mc.symmetricModelling(symmetry=1)
            self.bt_symMod.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")
            self.bt_symSwitch.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                      "selection-background-color: rgb(150, 150, 150);\n")
            print ">> Symmetric moddeling is ON."
        else:
            mc.symmetricModelling(symmetry=0)
            self.bt_symMod.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
            self.bt_symSwitch.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                        "selection-background-color: " + self.selectColor + ";\n")
            print ">> Symmetric moddeling is OFF."
            # "symmetricModelling -e -symmetry"

    def symSwitch(self):
        # symmetricModelling -e -about "object"
        # btn = self.sender()
        # if btn.text() == "world":
        if mc.symmetricModelling(q=True, about=True) == "world":
            # print btn
            mc.symmetricModelling(about="object")
            self.bt_symSwitch.setText("Object")
            print ">> Symmetric moddeling is on OBJECT."
        else:
            # print btn
            mc.symmetricModelling(about="world")
            self.bt_symSwitch.setText("World")
            print ">> Symmetric moddeling is on WORLD."

    def symX(self):
        # symmetricModelling -e -axis "x"
        mc.symmetricModelling(axis="x")
        self.bt_symX.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                             "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_symY.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                               "selection-background-color: " + self.selectColor + ";\n")
        self.bt_symZ.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                               "selection-background-color: " + self.selectColor + ";\n")
        print ">> Symmetric moddeling is on X."

    def symY(self):
        mc.symmetricModelling(axis="y")
        self.bt_symY.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                             "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_symX.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                               "selection-background-color: " + self.selectColor + ";\n")
        self.bt_symZ.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                               "selection-background-color: " + self.selectColor + ";\n")
        print ">> Symmetric moddeling is on Y."

    def symZ(self):
        mc.symmetricModelling(axis="z")
        self.bt_symZ.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                             "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_symX.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                               "selection-background-color: " + self.selectColor + ";\n")
        self.bt_symY.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                               "selection-background-color: " + self.selectColor + ";\n")
        print ">> Symmetric moddeling is on Z."

    def symTolerance(self):
        value = self.le_symTolerance.text()
        mc.symmetricModelling(tolerance=float(value))

    def symReset(self):
        mc.symmetricModelling(reset=1)
        # softSelect -softSelectReset
        self.le_symTolerance.setText(str(mc.symmetricModelling(q=True, tolerance=True)))
        print ">> Symmetric modelling tool is RESET"

    def mirrorNegX(self):  # polyMirrorFace -ws 1  -direction 0 -mergeMode 1 -ch 1;
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polyMirrorFace(obj, worldSpace=True, direction=1, mergeMode=1, mergeThreshold=0.015)

    def mirrorPosX(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polyMirrorFace(obj, worldSpace=True, direction=0, mergeMode=1, mergeThreshold=0.015)

    def mirrorNegY(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polyMirrorFace(obj, worldSpace=True, direction=3, mergeMode=1, mergeThreshold=0.015)

    def mirrorPosY(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polyMirrorFace(obj, worldSpace=True, direction=2, mergeMode=1, mergeThreshold=0.015)

    def mirrorNegZ(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polyMirrorFace(obj, worldSpace=True, direction=5, mergeMode=1, mergeThreshold=0.015)

    def mirrorPosZ(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polyMirrorFace(obj, worldSpace=True, direction=4, mergeMode=1, mergeThreshold=0.015)

                ## MOVE SETTINGS

    def tweakMod(self):  # mc.STRSTweakModeToggle()
        if self.toggleTweak == 1:
            mc.STRSTweakModeToggle()
            self.bt_tweak.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                    "selection-background-color: " + self.selectColor + ";\n")
            self.toggleTweak = 0
            print ">> Tweak mod is OFF"
        else:
            mc.STRSTweakModeToggle()
            self.bt_tweak.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                  "selection-background-color: rgb(150, 150, 150);\n")
            self.toggleTweak = 1
            print ">> Tweak mod is ON"

    def objectMove(self):  # manipMoveContext -e -mode 0 Move
        mc.manipMoveContext("Move", e=True, m=0)
        self.bt_objectMove.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")

        self.bt_worldMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                    "selection-background-color: " + self.selectColor + ";\n")
        self.bt_localMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                    "selection-background-color: " + self.selectColor + ";\n")
        self.bt_normalMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        print ">> Move axis is set to OBJECT"

    def localMove(self):
        mc.manipMoveContext("Move", e=True, m=1)
        self.bt_localMove.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                  "selection-background-color: rgb(150, 150, 150);\n")

        self.bt_worldMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                    "selection-background-color: " + self.selectColor + ";\n")
        self.bt_objectMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_normalMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        print ">> Move axis is set to LOCAL"

    def worldMove(self):
        mc.manipMoveContext("Move", e=True, m=2)
        self.bt_worldMove.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                  "selection-background-color: rgb(150, 150, 150);\n")

        self.bt_objectMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_localMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                    "selection-background-color: " + self.selectColor + ";\n")
        self.bt_normalMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        print ">> Move axis is set to WORLD"

    def normalMove(self):
        mc.manipMoveContext("Move", e=True, m=3)
        self.bt_normalMove.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")

        self.bt_worldMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                    "selection-background-color: " + self.selectColor + ";\n")
        self.bt_localMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                    "selection-background-color: " + self.selectColor + ";\n")
        self.bt_objectMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        print ">> Move axis is set to VERTEX NORMALE"

    def discreteMove(self, state):
        if state:
            mc.manipMoveContext("Move", e=True, snap=True)
            self.bt_discreteMove.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                         "selection-background-color: rgb(150, 150, 150);\n")
            print ">> Discrete Move is ON"
        else:
            mc.manipMoveContext("Move", e=True, snap=False)
            self.bt_discreteMove.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
            print ">> Discrete Move is OFF"

    def setMoveStep(self):
        btn = self.sender()
        mc.manipMoveContext("Move", e=True, snapValue=int(btn.text()))
        self.sb_discreteMoveValue.setValue(int(btn.text()))
        for s in ("05", "45"):  # "10", "25", "45"):
            btnB = getattr(self, "bt_m" + s)
            btnB.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                           "selection-background-color: " + self.selectColor + ";\n")
        btn.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                    "selection-background-color: rgb(150, 150, 150);\n")

    def setDiscreteMoveValue(self, value):
        mc.manipMoveContext("Move", e=True, snapValue=value)
        print ">> Move step is set to : " + str(mc.manipMoveContext("Move", q=True, snapValue=value))

    # def discreteMove10(self):
    # mc.manipMoveContext("Move", e=True, snapValue=10)

    def resetMove(self):
        mc.resetTool("Move")
        self.initDiscrete()
        self.initMoveSettings()
        print ">> Move Tool is RESET"

    ## ROTATE SETTINGS

    def localRotate(self):
        # manipRotateContext -e -mode 0 Rotate
        mc.manipRotateContext("Rotate", e=True, m=0)
        self.bt_localRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                    "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_worldRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_gimbalRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                       "selection-background-color: " + self.selectColor + ";\n")
        print ">> Rotate axis is set to LOCAL"

    def worldRotate(self):
        mc.manipRotateContext("Rotate", e=True, m=1)
        self.bt_worldRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                    "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_localRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_gimbalRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                       "selection-background-color: " + self.selectColor + ";\n")
        print ">> Rotate axis is set to WORLD"

    def gimbalRotate(self):
        mc.manipRotateContext("Rotate", e=True, m=2)
        self.bt_gimbalRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                     "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_worldRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_localRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        print ">> Rotate axis is set to GIMBAL"

    def defautPivotRotate(self):  # manipRotateContext -e -useManipPivot 0 -useObjectPivot 0 Rotate
        mc.manipRotateContext("Rotate", e=True, useManipPivot=0, useObjectPivot=0)
        self.bt_defaultPivotRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                           "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_objectPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
        self.bt_manipPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
        print ">> Rotate pivot is set to DEFAULT"

    def objectPivotRotate(self):
        mc.manipRotateContext("Rotate", e=True, useManipPivot=0, useObjectPivot=1)
        self.bt_objectPivotRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_defaultPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                             "selection-background-color: " + self.selectColor + ";\n")
        self.bt_manipPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
        print ">> Rotate pivot is set to OBJECT"

    def manipPivotRotate(self):
        mc.manipRotateContext("Rotate", e=True, useManipPivot=1, useObjectPivot=0)
        self.bt_manipPivotRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                         "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_defaultPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                             "selection-background-color: " + self.selectColor + ";\n")
        self.bt_objectPivotRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
        print ">> Rotate pivot is set to MANIP"

    def discreteRotate(self, state):
        if state:
            mc.manipRotateContext("Rotate", e=True, snap=True)
            self.bt_discreteRotate.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                           "selection-background-color: rgb(150, 150, 150);\n")
            print ">> Discrete Rotate is ON"
        else:
            mc.manipRotateContext("Rotate", e=True, snap=False)
            self.bt_discreteRotate.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                             "selection-background-color: " + self.selectColor + ";\n")
            print ">> Discrete Rotate is OFF"

    def setRotateStep(self):
        btn = self.sender()
        mc.manipRotateContext("Rotate", e=True, snapValue=int(btn.text()))
        self.sb_discreteRotateValue.setValue(int(btn.text()))
        for s in ("05", "45"):  # "10", "25", "45"):
            btnB = getattr(self, "bt_r" + s)
            btnB.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                           "selection-background-color: " + self.selectColor + ";\n")
        btn.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                    "selection-background-color: rgb(150, 150, 150);\n")

    def setDiscreteRotateValue(self, value):
        mc.manipRotateContext("Rotate", e=True, snapValue=value)
        print ">> Rotate step is set to : " + str(mc.manipRotateContext("Rotate", q=True, snapValue=value))

    def resetRotate(self):
        mc.resetTool("Rotate")
        self.initDiscrete()
        self.initRotateSettings()
        print ">> Rotate Tool is RESET"

    ##SCALE SETTINGS

    def objectScale(self):  # manipScaleContext -e -mode 0 Scale
        mc.manipScaleContext("Scale", e=True, m=0)
        self.bt_objectScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                    "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_worldScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_localScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_normalScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        print ">> Scale axis is set to OBJECT"

    def localScale(self):
        mc.manipScaleContext("Scale", e=True, m=1)
        self.bt_localScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_worldScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_objectScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_normalScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        print ">> Scale axis is set to LOCAL"

    def worldScale(self):
        mc.manipScaleContext("Scale", e=True, m=2)
        self.bt_worldScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                   "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_objectScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        self.bt_localScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_normalScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        print ">> Scale axis is set to WORLD"

    def normalScale(self):
        mc.manipScaleContext("Scale", e=True, m=3)
        self.bt_normalScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                    "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_worldScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_localScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                     "selection-background-color: " + self.selectColor + ";\n")
        self.bt_objectScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                      "selection-background-color: " + self.selectColor + ";\n")
        print ">> Scale axis is set to NORMAL"

    def defautPivotScale(self):
        mc.manipScaleContext("Scale", e=True, useManipPivot=0, useObjectPivot=0)
        self.bt_defaultPivotScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_objectPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
        self.bt_manipPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
        print ">> Scale pivot is set to DEFAULT"

    def objectPivotScale(self):
        mc.manipScaleContext("Scale", e=True, useManipPivot=0, useObjectPivot=1)
        self.bt_objectPivotScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                         "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_defaultPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
        self.bt_manipPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                          "selection-background-color: " + self.selectColor + ";\n")
        print ">> Scale pivot is set to OBJECT"

    def manipPivotScale(self):
        mc.manipScaleContext("Scale", e=True, useManipPivot=1, useObjectPivot=0)
        self.bt_manipPivotScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                        "selection-background-color: rgb(150, 150, 150);\n")
        self.bt_objectPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                           "selection-background-color: " + self.selectColor + ";\n")
        self.bt_defaultPivotScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
        print ">> Scale pivot is set to MANIP"

    def discreteScale(self, state):
        if state:
            mc.manipScaleContext("Scale", e=True, snap=True)
            self.bt_discreteScale.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                                          "selection-background-color: rgb(150, 150, 150);\n")
            print ">> Discrete Scale is ON"
        else:
            mc.manipScaleContext("Scale", e=True, snap=False)
            self.bt_discreteScale.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                                            "selection-background-color: " + self.selectColor + ";\n")
            print ">> Discrete Scale is OFF"

    def setScaleStep(self):
        btn = self.sender()
        mc.manipScaleContext("Scale", e=True, snapValue=int(btn.text()))
        self.sb_discreteScaleValue.setValue(int(btn.text()))
        for s in ("05", "45"):  # "10", "25", "45"):
            btnB = getattr(self, "bt_s" + s)
            btnB.setStyleSheet("background-color: " + self.unSelectColor + ";\n"
                                                                           "selection-background-color: " + self.selectColor + ";\n")
        btn.setStyleSheet("background-color: " + self.selectColor + ";\n"
                                                                    "selection-background-color: rgb(150, 150, 150);\n")

    def setDiscreteScaleValue(self, value):
        mc.manipScaleContext("Scale", e=True, snapValue=value)
        print ">> Scale step is set to : " + str(mc.manipScaleContext("Scale", q=True, snapValue=value))

    def resetScale(self):
        mc.resetTool("Scale")
        self.initDiscrete()
        self.initScaleSettings()
        print ">> Scale Tool is RESET"


def launchUi():
    sDockName = "kMaxToolDock"
    if mc.dockControl(sDockName, q=True, ex=True):
        qDock = controlToPySide(sDockName)
        myUi = qDock.findChild(QtGui.QWidget, "kmaxToolBar")
        myUi.close()
        mc.deleteUI(sDockName)

        print ">> kMax Tool Bar killed !"

    mc.refresh()

    try:
        myWindow = mc.window("kmaxTmpWin")
        mc.columnLayout(parent=myWindow)

        myDock = mc.dockControl(sDockName, label="kMax Tool Bar",
                                area='right',
                                content=myWindow,
                                allowedArea=['right', 'left'],
                                width=270, sizeable=False)

        qDock = controlToPySide(myDock)
        myUi = KmaxWin(qDock)
        # print myUi, myUi.objectName()
        qDock.setWidget(myUi)

        print ">> kMax Tool Bar Launch !"

    finally:
        mc.deleteUI(myWindow)
