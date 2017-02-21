# TEAMTO

# UI :

self.bt_selNgones = mc.iconTextButton(image1=self.target + "selNgones.png",
                                      highlightImage=self.target + "selNgones.png",
                                      annotation="Select nGones", command=self.kmSelNgones, width=scaleIcon)

self.bt_convertUItoPY = mc.iconTextButton(image1=self.target + "convertUI32.png",
                                          highlightImage=self.target + "convertUI32b.png",
                                          annotation="Convert .ui file in .py file",
                                          command=self.kmConvertUI, width=scaleIcon)

self.bt_ttRig3 = mc.iconTextButton(image1=self.target + "ttRig3.png", highlightImage=self.target + "ttRig3.png",
                                   annotation="Launch ttRig3", command=self.ttRig3, width=scaleIcon)

self.bt_checkPublish = mc.iconTextButton(image1=self.target + "checkPublish.png",
                                         highlightImage=self.target + "checkPublish.png",
                                         annotation="Check Publishability", command=self.checkPublish, width=scaleIcon)

self.bt_light = mc.iconTextButton(image1=self.target + "sun32.png", highlightImage=self.target + "sun32.png",
                                  annotation="Create/Delete LightConfig for Viewport", command=self.kmLightTheSun,
                                  width=scaleIcon)

self.bt_setSmooth = mc.iconTextButton(image1=self.target + "smoothSetTool.png",
                                      highlightImage=self.target + "smoothSetTool.png",
                                      command=self.kmSetSmoothGroupTool, width=scaleIcon)

self.bt_propsBankManager = mc.iconTextButton(image1=self.target + "propsManager32.png",
                                             highlightImage=self.target + "propsManager32.png",
                                             annotation="props bank manager", command=self.kmPropsManager,
                                             width=scaleIcon)

self.bt_mainpackManager = mc.iconTextButton(image1=self.target + "mainPackTool32.png",
                                            highlightImage=self.target + "mainPackTool32.png",
                                            annotation="mainpack manager", command=self.kmMainpackManager,
                                            width=scaleIcon)

self.bt_scatter = mc.iconTextButton(image1=self.target + "scatter32.png", highlightImage=self.target + "scatter32b.png",
                                    annotation="Scattering", command=self.icPolyScatter, width=scaleIcon)

self.bt_freezeScale = mc.iconTextButton(image1=self.target + "freezeT.png", highlightImage=self.target + "freezeT.png",
                                        annotation="Freeze Scale", command=self.kmFreezeScale, width=scaleIcon)

self.bt_deleteHistory = mc.iconTextButton(image1=self.target + "delete_history.png",
                                          highlightImage=self.target + "delete_history.png",
                                          annotation="Delete construction history", command=self.kmDeleteHistory,
                                          width=scaleIcon)

self.bt_centerPivot = mc.iconTextButton(image1=self.target + "center.png", highlightImage=self.target + "center.png",
                                        annotation="Center Pivot", command=self.kmCenterPivot, width=scaleIcon)

self.bt_textureFileManager = mc.iconTextButton(image1=self.target + "textMan32.png", annotation="UV Texture Editor",
                                               command=self.kmTextureFileManager, width=scaleIcon)

# DEF :

def kmSetSmoothGroupTool(self):
    import setSmoothGroupTool
    reload(setSmoothGroupTool)

def kmPropsManager(self):
    pm.mel.ava_assetBankManager()

def kmMainpackManager(self):
    pm.mel.ava_mainpack_manager()

def kmSelNgones(self):
    mel.eval('polyCleanupArgList 3 { "0","2","1","0","1","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" };')

def kmLightTheSun(self):
    sel = mc.ls('groupLightPrev')
    if not sel:
        mc.ambientLight(n='ambiantLightPrev', intensity=2.5)
        mc.spotLight(n='spotLightPrev', intensity=0.6, coneAngle=120)
        mc.setAttr('spotLightPrevShape.emitSpecular', 0)
        mc.setAttr('spotLightPrev.rotateX', -90)
        mc.setAttr('spotLightPrev.translateY', 300)
        # mc.setAttr( 'spotLightPrev.scale', 200, 200, 200, type="double3")
        mc.group('ambiantLightPrev', 'spotLightPrev', n='groupLightPrev')
        allModelPanel = mc.getPanel(type='modelPanel')
        if allModelPanel:
            for modelPanelName in allModelPanel:
                mc.modelEditor(modelPanelName, e=True, displayLights="all", shadows=True)
    else:
        mc.delete(sel)
        allModelPanel = mc.getPanel(type='modelPanel')
        if allModelPanel:
            for modelPanelName in allModelPanel:
                mc.modelEditor(modelPanelName, e=True, displayLights="default", shadows=False)

def kmTextureFileManager(self):
    pm.mel.FileTextureManager()

def ttRig3(self):
    pm.mel.ttRig3()

def checkPublish(self):
    pm.mel.CheckPublishable()

def icPolyScatter(self):
    pm.mel.icPolyScatter()

def kmFreezeScale(self):
    mc.makeIdentity(a=1, t=0, r=0, s=1, n=1, pn=1)

def kmDeleteHistory(self):
    mc.delete(constructionHistory=True)

def kmCenterPivot(self):
    pm.mel.CenterPivot()