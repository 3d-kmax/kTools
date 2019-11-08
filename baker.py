import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm
import os

class baker():

    def __init__(self):
        self.blueColor = [0.32156, 0.52156, 0.65098]
        self.itemToBake = []
        self.initPath()
        self.bakerUi()

    # USER INTERFACE
    def bakerUi(self):
        buttonHeight = 20
        if (mc.window('bakerWindow', q=True, ex=True)): mc.deleteUI('bakerWindow')

        mc.window('bakerWindow', t='Baker', s=False, mnb=False, mxb=False, tlb=True)
        mc.columnLayout('bakerColumnLayout', rowSpacing=1, adj=True)
        mc.rowLayout(numberOfColumns=2, enable=True)
        mc.iconTextStaticLabel(style='iconOnly', label='baker', image=self.iconPath+'/baker.png')
        mc.columnLayout(rowSpacing=1)
        self.setMeshButton = mc.button(label='Prepare mesh', command=self.setMesh, height=buttonHeight, width=110)
        self.snapUvsButton = mc.button(label='Snap Uvs', enable=False, command=self.snapUvs, height=buttonHeight, width=110)

        '''
        mc.frameLayout('dirt', parent='bakerColumnLayout', marginHeight=0, collapsable=False, label='Dirt :')
        self.setDirtRow = mc.rowLayout(numberOfColumns=5, enable=False)
        self.setDirtButton = mc.button(label='Set Dirt', annotation='Import and set dirt shader', command=self.setDirt, height=buttonHeight, width=60)
        mc.iconTextRadioCollection('dirtResolutions')
        self.setDirt512 = mc.iconTextRadioButton(label='512', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setDirtResolution)
        self.setDirt1024 = mc.iconTextRadioButton(label='1024', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setDirtResolution)
        self.setDirt2048 = mc.iconTextRadioButton(label='2048', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setDirtResolution)
        self.setDirt4096 = mc.iconTextRadioButton(label='4096', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setDirtResolution, select=True)
        mc.setParent('..')
        self.bakeDirtButton = mc.button(label='Bake Occlusion', enable=False, command=self.bakeShader, height=buttonHeight)
        mc.setParent('..')
     
        mc.frameLayout('curvature', parent='bakerColumnLayout', marginHeight=0, collapsable=False, label='Curvature :')
        self.setCurvatureRow = mc.rowLayout(numberOfColumns=5, enable=False)
        self.setCurvatureButton = mc.button(label='Set Curv', command=self.setCurvature, height=buttonHeight, width=60)
        mc.iconTextRadioCollection('curvatureResolutions')
        self.setCurv512 = mc.iconTextRadioButton(label='512', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setCurvResolution)
        self.setCurv1024 = mc.iconTextRadioButton(label='1024', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setCurvResolution)
        self.setCurv2048 = mc.iconTextRadioButton(label='2048', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setCurvResolution)
        self.setCurv4096 = mc.iconTextRadioButton(label='4096', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setCurvResolution, select=True)
        mc.setParent('..')
        self.bakeCurvatureButton = mc.button(label='Bake Curvature', enable=False, command=self.bakeShader, height=buttonHeight)
        mc.setParent('..')
        '''
        mc.frameLayout('Dirt', parent='bakerColumnLayout', marginHeight=0, collapsable=False, label='Dirt :')
        self.setDirtRow = mc.rowLayout(numberOfColumns=3, enable=True)
        self.setDirtButton = mc.button(label='SET', annotation='Import and set dirt shader', command=self.setDirt, height=2*buttonHeight, width=2*buttonHeight)
        mc.rowColumnLayout(numberOfColumns=2, enable=True)
        mc.iconTextRadioCollection('dirtResolutions')
        self.setDirt512 = mc.iconTextRadioButton(label='512', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setDirtResolution)
        self.setDirt1024 = mc.iconTextRadioButton(label='1024', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setDirtResolution)
        self.setDirt2048 = mc.iconTextRadioButton(label='2048', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setDirtResolution)
        self.setDirt4096 = mc.iconTextRadioButton(label='4096', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setDirtResolution, select=True)
        mc.setParent('..')
        self.bakeDirtButton = mc.button(label='BAKE', annotation='Bake dirt', enable=False, command=self.bakeShader, height=2*buttonHeight, width=2*buttonHeight)
        mc.setParent('..')
        mc.setParent('..')
        

        mc.frameLayout('Curvature', parent='bakerColumnLayout', marginHeight=0, collapsable=False, label='Curvature :')
        self.setCurvatureRow = mc.rowLayout(numberOfColumns=3, enable=True)
        self.setCurvatureButton = mc.button(label='SET', annotation='Import and set curvature shader', command=self.setCurvature, height=2*buttonHeight, width=2*buttonHeight)
        mc.rowColumnLayout(numberOfColumns=2, enable=True)
        mc.iconTextRadioCollection('curvatureResolutions')
        self.setCurv512 = mc.iconTextRadioButton(label='512', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setCurvResolution)
        self.setCurv1024 = mc.iconTextRadioButton(label='1024', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setCurvResolution)
        self.setCurv2048 = mc.iconTextRadioButton(label='2048', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setCurvResolution)
        self.setCurv4096 = mc.iconTextRadioButton(label='4096', style='textOnly', height=buttonHeight, width=30, enable=False, onCommand=self.setCurvResolution, select=True)
        mc.setParent('..')
        self.bakeCurvatureButton = mc.button(label='BAKE', annotation='Bake curvature', enable=False, command=self.bakeShader, height=2*buttonHeight, width=2*buttonHeight)
        mc.setParent('..')
        mc.setParent('..')

        self.openFolderButton = mc.button(label='Open Folder', annotation='Open explorer to bake folder', enable=True, command=self.openFolder, height=buttonHeight)
        self.cleanRefButton = mc.button(label='Reset', annotation='Clean Scene and Reset Tool', enable=False, command=self.cleanScene, height=buttonHeight)

        mc.window('bakerWindow', edit=True, wh=(150, 12*buttonHeight))
        mc.showWindow('bakerWindow')

    # INIT PATH/FOLDER
    def initPath(self):
        projectFileName = mc.file(query=True, list=True)
        print ">> file name : ", projectFileName[0]
        if projectFileName[0] == '//man_server/projets/manoir-magique/man_maya/untitled':
            self.bakeFolder = 'E:/bake'
        else:
            self.bakeFolder = projectFileName[0].split('/')
            # print BakeFolder[9]
            del self.bakeFolder[-1]
            self.bakeFolder[6] = "sourceimages"
            self.bakeFolder[10] = "surf"
            self.elementName = self.bakeFolder[9]
            self.bakeFolder = '/'.join(self.bakeFolder)
            self.bakeFolder = self.bakeFolder + "/bake"
        print ">> bake folder : ", self.bakeFolder

        self.iconPath = 'E:/kTools/icons'

    # COMBINE + SMOOTH MESH&UVs
    def setMesh(self, *args):

        itemsToCombine = mc.ls(sl=True)
        print len(itemsToCombine)

        if itemsToCombine == []:
            print ">> Selectionnez les meshs a combiner et a smoother !"

        else:
            if len(itemsToCombine) == 1:
                itemToSmooth = mc.duplicate(itemsToCombine)
                mc.parent(itemToSmooth, world=True)
                # mc.select(newItem, add=1)
                mc.polySmooth(itemToSmooth, method=0, subdivisionType=2, divisions=2, osdVertBoundary=1,
                              osdFvarBoundary=1, osdFvarPropagateCorners=1, osdSmoothTriangles=0,
                              osdCreaseMethod=0, constructionHistory=0)

            if len(itemsToCombine) > 1:
                # mc.select(clear=1)
                for item in itemsToCombine:
                    mc.delete(item, constructionHistory=True)
                    newItem = mc.duplicate(item)
                    # mc.delete(newItem, constructionHistory=True)
                    mc.select(newItem, add=1)

                itemToSmooth = mc.polyUnite(mc.ls(sl=True), constructionHistory=0)

                mc.polySmooth(itemToSmooth, method=0, subdivisionType=2, divisions=2, osdVertBoundary=1,
                              osdFvarBoundary=1, osdFvarPropagateCorners=1, osdSmoothTriangles=0,
                              osdCreaseMethod=0, constructionHistory=0)
                # mc.rename(self.itemToSmooth, elementName)
                # itemToBake = mc.select(itemToSmooth)

            groupToBake = mc.group(name="itemToBake", empty=True)
            mc.parent(itemToSmooth, "itemToBake")

            mc.hide("geo")
            mc.button(self.snapUvsButton, enable=True, edit=True)
            mc.rowLayout(self.setDirtRow, enable=True, edit=True)
            # mc.button(self.setDirtButton, enable=True, edit=True)
            mc.rowLayout(self.setCurvatureRow, enable=True, edit=True)
            # mc.button(self.setCurvatureButton, enable=True, edit=True)
            # self.itemToBake = itemToSmooth
            mc.button(self.cleanRefButton, enable=True, edit=True)
            mc.select(itemToSmooth)

    # SNAPSHOT UVs
    def snapUvs(self, *args):
        itemsToSnap = mc.ls(sl=True)
        #split os.path.splitext
        if itemsToSnap != []:
            valBase = 1

            if not os.path.exists(self.bakeFolder):
                os.makedirs(self.bakeFolder)

            from os import listdir
            from os.path import isfile, join

            onlyfiles = [f for f in listdir(self.bakeFolder) if isfile(join(self.bakeFolder, f))]
            countFile = len(onlyfiles)
            valBase = valBase + countFile
            fileName = "uvs_" + str(self.elementName) + "_v" + str(valBase)
            filePathName = self.bakeFolder + "/" + fileName + '.png'
            # print ">> : ", fileName
            mc.uvSnapshot(overwrite=True, fileFormat="png", name=filePathName, antiAliased=True, xResolution=4096, yResolution=4096)

        else:
            print ">> Selectionnez le mesh avec les uvs a snaper !"

    # IMPORT DIRT SHADER
    def setDirt(self, *args):

        itemToBake = mc.ls(sl=True)

        if itemToBake != []:
            valBase = 1
            dirtShader = mc.ls("dirtRN")
            if dirtShader != []:
                refFile = mc.referenceQuery(dirtShader, filename=True)
                print "Dirt shader already ok !"
            else:
                mc.file("//man_server/projets/manoir-magique/man_misc/Maxime/shaders/bake_dirt_01.ma", r=1, type="mayaAscii",
                        ignoreVersion=1, mergeNamespacesOnClash=1, namespace="dirt", options="v=0;", pr=1)

            if mc.ls("dirt:sh_bake_dirtSG") == [] :
                mc.sets(renderable=1, noSurfaceShader=1, name="dirt:sh_bake_dirtSG")
            mc.defaultNavigation(connectToExisting=True, source="dirt:sh_bake_dirt", destination="dirt:sh_bake_dirtSG")

            mc.sets(itemToBake, edit=True, forceElement="dirt:sh_bake_dirtSG")
            # curv_bidimensional - rotation - unit_4k_v1
            mc.setAttr("dirt:pxr_bake_texture_dirt.filename", self.bakeFolder + "/dirt_" + self.elementName + "_01.tif", type="string")
            # print mc.getAttr("dirt:pxr_bake_texture_dirt.filename")

            mc.button(self.bakeDirtButton, enable=True, edit=True)
            mc.iconTextRadioButton(self.setDirt512 , enable=True, edit=True)
            mc.iconTextRadioButton(self.setDirt1024, enable=True, edit=True)
            mc.iconTextRadioButton(self.setDirt2048, enable=True, edit=True)
            mc.iconTextRadioButton(self.setDirt4096, enable=True, edit=True)
            mc.button(self.bakeCurvatureButton, enable=False, edit=True)
            mc.iconTextRadioButton(self.setCurv512, enable=False, edit=True)
            mc.iconTextRadioButton(self.setCurv1024, enable=False, edit=True)
            mc.iconTextRadioButton(self.setCurv2048, enable=False, edit=True)
            mc.iconTextRadioButton(self.setCurv4096, enable=False, edit=True)
            mc.select(itemToBake)

        else:
            print ">> Selectionnez le mesh a baker !"

    # SET DIRT RESOLUTION
    def setDirtResolution(self, *args):
        if mc.iconTextRadioButton(self.setDirt512, select=True, q=True):
            mc.setAttr("dirt:pxr_bake_texture_dirt.resolutionX", 512)
            mc.setAttr("dirt:pxr_bake_texture_dirt.resolutionY", 512)
        if mc.iconTextRadioButton(self.setDirt1024, select=True, q=True):
            mc.setAttr("dirt:pxr_bake_texture_dirt.resolutionX", 1024)
            mc.setAttr("dirt:pxr_bake_texture_dirt.resolutionY", 1024)
        if mc.iconTextRadioButton(self.setDirt2048, select=True, q=True):
            mc.setAttr("dirt:pxr_bake_texture_dirt.resolutionX", 2048)
            mc.setAttr("dirt:pxr_bake_texture_dirt.resolutionY", 2048)
        if mc.iconTextRadioButton(self.setDirt4096, select=True, q=True):
            mc.setAttr("dirt:pxr_bake_texture_dirt.resolutionX", 4096)
            mc.setAttr("dirt:pxr_bake_texture_dirt.resolutionY", 4096)

    # IMPORT CURVATURE SHADER
    def setCurvature(self, *args):
        itemToBake = mc.ls(sl=True)
        if itemToBake != []:
            valBase = 1
            curvatureShader = mc.ls("curvatureRN")
            if curvatureShader != []:
                refFile = mc.referenceQuery(curvatureShader, filename=True)
                print "Curvature shader already ok !"
            else:
                mc.file("//man_server/projets/manoir-magique/man_misc/Maxime/shaders/bake_curvature_01.ma", r=1,
                        type="mayaAscii",
                        ignoreVersion=1, mergeNamespacesOnClash=1, namespace="curvature", options="v=0;", pr=1)

            if mc.ls("curvature:sh_bake_curvatureSG") == []:
                mc.sets(renderable=1, noSurfaceShader=1, name="curvature:sh_bake_curvatureSG")
            mc.defaultNavigation(connectToExisting=True, source="curvature:sh_bake_curvature", destination="curvature:sh_bake_curvatureSG")

            mc.sets(itemToBake, edit=True, forceElement="curvature:sh_bake_curvatureSG")
            mc.setAttr("curvature:pxr_bake_texture_curvature.filename", self.bakeFolder + "/curv_" + self.elementName + "_01.tif", type="string")
            # print mc.getAttr("curvature:pxr_bake_texture_curvature.filename")

            mc.button(self.bakeCurvatureButton, enable=True, edit=True)
            mc.iconTextRadioButton(self.setCurv512, enable=True, edit=True)
            mc.iconTextRadioButton(self.setCurv1024, enable=True, edit=True)
            mc.iconTextRadioButton(self.setCurv2048, enable=True, edit=True)
            mc.iconTextRadioButton(self.setCurv4096, enable=True, edit=True)
            mc.button(self.bakeDirtButton, enable=False, edit=True)
            mc.iconTextRadioButton(self.setDirt512, enable=False, edit=True)
            mc.iconTextRadioButton(self.setDirt1024, enable=False, edit=True)
            mc.iconTextRadioButton(self.setDirt2048, enable=False, edit=True)
            mc.iconTextRadioButton(self.setDirt4096, enable=False, edit=True)
            mc.select(itemToBake)

        else:
            print ">> Selectionnez le mesh a baker !"

    # SET CURVATURE RESOLUTION
    def setCurvResolution(self, *args):
        if mc.iconTextRadioButton(self.setCurv512, select=True, q=True):
            mc.setAttr("curvature:pxr_bake_texture_curvature.resolutionX", 512)
            mc.setAttr("curvature:pxr_bake_texture_curvature.resolutionY", 512)
        if mc.iconTextRadioButton(self.setCurv1024, select=True, q=True):
            mc.setAttr("curvature:pxr_bake_texture_curvature.resolutionX", 1024)
            mc.setAttr("curvature:pxr_bake_texture_curvature.resolutionY", 1024)
        if mc.iconTextRadioButton(self.setCurv2048, select=True, q=True):
            mc.setAttr("curvature:pxr_bake_texture_curvature.resolutionX", 2048)
            mc.setAttr("curvature:pxr_bake_texture_curvature.resolutionY", 2048)
        if mc.iconTextRadioButton(self.setCurv4096, select=True, q=True):
            mc.setAttr("curvature:pxr_bake_texture_curvature.resolutionX", 4096)
            mc.setAttr("curvature:pxr_bake_texture_curvature.resolutionY", 4096)

    # LAUNCH BAKE TEXTURE
    def bakeShader(self, *args):
        # mc.hide("geo")
        pm.mel.setCurrentRenderer("renderman")
        pm.mel.rmanBakeStartCmd()

    # OPEN FOLDER
    def openFolder(self, *args):
        import subprocess
        pathWindow = self.bakeFolder.replace('/', '\\')
        print pathWindow
        subprocess.call("explorer "+pathWindow, shell=True)

    # CLEAN SCENE
    def cleanScene(self, *args):

        mc.showHidden("geo")
        mc.delete("itemToBake")

        dirtShader = mc.ls("dirtRN")
        if dirtShader != []:
            refFile = mc.referenceQuery(dirtShader, filename=True)
            mc.file(refFile, removeReference=True)

        curvatureShader = mc.ls("curvatureRN")
        if curvatureShader != []:
            refFile = mc.referenceQuery(curvatureShader, filename=True)
            mc.file(refFile, removeReference=True)

        print ">> Bake shaders & mesh to bake were removed !"

        mc.select("geo")
        self.bakerUi
        #baker()

baker()