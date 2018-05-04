import maya.cmds as mc
from functools import partial
import pymel.core as pm
import maya.mel as mel
import os

class kSmoothSetTool():

    def __init__(self):
        self.initPath()
        self.smoothSetToolUI()
        self.smoothSetBodyName = 'smooth'

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
        print "Target >> :", self.target

    def smoothSetToolUI(self):
        windowName = "smoothSetTool"

        if mc.window(windowName, q=True, exists=True):
            mc.deleteUI(windowName)

        self.myWindow = mc.window(windowName, toolbox=True, titleBar=True, minimizeButton=False, maximizeButton=False,
                                  sizeable=False)  # , resizeToFitChildren=True,
        mc.window(self.myWindow, width=160, height=80, edit=True)


        mc.frameLayout(label="Smooth set :", labelVisible=0, borderVisible=0, marginHeight=2,
                       marginWidth=2)  # borderStyle="out",

        mc.columnLayout(rowSpacing=2)

        mc.rowLayout(numberOfColumns=3, columnWidth=[(1, 54), (2, 54), (3, 54)])
        smstUI_smoothLvl_set = mc.iconTextRadioCollection("Smooth level")
        self.smstUI_smoothLvl0 = mc.iconTextRadioButton(l="0 ", style='iconAndTextHorizontal',
                                                   image=self.target + "polyCube2016.png",
                                                   selectionImage=self.target + "polyCube2016b.png")
        self.smstUI_smoothLvl1 = mc.iconTextRadioButton(l="1 ", style='iconAndTextHorizontal',
                                                   image=self.target + "kSphere32.png",
                                                   selectionImage=self.target + "kSphere32b.png")
        self.smstUI_smoothLvl2 = mc.iconTextRadioButton(l="2 ", style='iconAndTextHorizontal',
                                                   image=self.target + "polySphere2016.png",
                                                   selectionImage=self.target + "polySphere2016b.png")
        mc.setParent('..')
        mc.setParent('..')

        mc.rowLayout(numberOfColumns=3)
        smstUI_add_b = mc.button(l='+', c=self.addToSmoothSet, height=30, width=30)
        smstUI_rm_b = mc.button(l='-', c=self.remFromSmoothSet, height=30, width=30)
        smstUI_rmAll_b = mc.button(l='Remove From All', c=self.remFromAll, height=30, width=100)
        mc.setParent('..')
        # mc.setParent('..')

        mc.frameLayout(label="Apply rdr smooth attr", labelVisible=0, borderVisible=0, marginHeight=2,marginWidth=2)
        self.bt_applyRdrSmoothAttr = mc.button(l='Apply rdr smooth attr', c=self.kApplyRdrSmoothAttr, height=30, width=160)
        mc.setParent('..')

        mc.showWindow(self.myWindow)

    def addToSmoothSet(self, *arg):
        selection = self.filterSelection(mc.ls(sl=True, l=True), 'scene')
        # value = mc.intSliderGrp(smstUI_smoothLvl_intSG, q=True, value=True)
        value = self.getSmoothLvl()
        if selection:

            # --- set
            self.remFromAll()
            self.createSmoothSet(value)
            inSet = mc.sets(self.smoothSetName(value), q=True) or []
            mc.sets(selection, add=self.smoothSetName(value))
            result = list(set([sel.rpartition('|')[-1] for sel in selection]) - set(inSet))
            print '# %s added to %s' % (result, self.smoothSetName(value))
            """
            # --- partition
            createPartition()
            addToPartition(smoothSetName(value))
            """

            '''
            '# --- options
            options = self.optWhichNeedLoop()
            if options['loopInObj']:
                for obj in result:
                    if mc.menuItem(smstUI_optSmView_mI, q=True, cb=True):
                        mc.displaySmoothness(obj, polygonObject=3)
                    if options['loopInShape']:
                        for shape in mc.listRelatives(obj, s=True, f=True):
                            if mc.menuItem(smstUI_optSmPw_mI, q=True, cb=True):
                                mc.setAttr(shape + '.smoothLevel', value)
                            if mc.menuItem(smstUI_optSmRnd_mI, q=True, cb=True):
                                mc.setAttr(shape + '.renderSmoothLevel', value)

            # --- layer
            if mc.menuItem(smstUI_optDispLay_mI, q=True, cb=True):
                createDisplayer(value)
                mc.editDisplayLayerMembers(dispLayerName(value), result, noRecurse=True)
            '''
        else:
            mc.error('Wrong node type in selection ! Please select geometry transforms only')

    def remFromSmoothSet(self, *arg):
        # selection = filterSelection(mc.ls(sl=True, l=True), 'scene')
        selection = mc.ls(sl=True, l=True)
        # value = mc.intSliderGrp(smstUI_smoothLvl_intSG, q=True, value=True)
        value = self.getSmoothLvl()
        if selection:
            inSet = mc.sets(self.smoothSetName(value), q=True) or []
            mc.sets(selection, rm=self.smoothSetName(value))
            print '# %s removed from %s' % (
            list(set([sel.rpartition('|')[-1] for sel in selection]) & set(inSet)), self.smoothSetName(value))
        else:
            mc.error('Wrong node type in selection ! Please select geometry transforms only')

    def remFromAll(self, *arg):
        # selection = filterSelection(mc.ls(sl=True, l=True), 'scene')
        selection = mc.ls(sl=True, l=True)
        if selection:
            for smoothSet in self.smoothSetList():
                inSet = mc.sets(smoothSet, q=True) or []
                mc.sets(selection, rm=smoothSet)
                result = list(set([sel.rpartition('|')[-1] for sel in selection]) & set(inSet))
                if result != []:
                    print '# %s removed from %s' % (result, smoothSet)
        else:
            mc.error('Wrong node type in selection ! Please select geometry transforms only')

    def filterSelection(self, selection=mc.ls(sl=True, l=True), source='scene'):
        """returns a filtered list of geometry transforms only from selection
        source variable may be 'scene' or 'set' depending of the source of selection"""
        result = []
        if not selection and source == 'scene':
            mc.error('Nothing is selected !')
        else:
            for sel in selection or []:
                if mc.nodeType(sel) == 'transform' and filter(lambda x: mc.nodeType(x) == 'mesh',
                                                              mc.listRelatives(sel, s=True, f=True) or []):
                    result.append(sel)
        return result

    def getSmoothLvl(self, *args):
        if mc.iconTextRadioButton(self.smstUI_smoothLvl0, select=True, q=True):
            return 0
        if mc.iconTextRadioButton(self.smstUI_smoothLvl1, select=True, q=True):
            return 1
        if mc.iconTextRadioButton(self.smstUI_smoothLvl2, select=True, q=True):
            return 2

    def smoothSetName(self, value):
        return self.smoothSetBodyName + str(value)

    def smoothSetList(self):
        return filter(lambda x: x.rpartition(':')[-1].startswith(self.smoothSetBodyName) and x.rpartition(':')[-1][len(
            self.smoothSetBodyName):].isdigit(), mc.ls(set=True))

    def createSmoothSet(self, value):
        if not self.smoothSetName(value) in self.smoothSetList():
            mc.select(cl=True)
            mc.sets(n='smooth' + str(value))

    def kApplyRdrSmoothAttr(self, *args):
        print "hello"
        # add smooth to mesh
        smooth1 = []
        smooth2 = []
        if mc.objExists('smooth1') and mc.sets('smooth1', q=True) is not None :
            smooth1 = mc.sets('smooth1', q=True)
        if mc.objExists('smooth2') and mc.sets('smooth2', q=True) is not None :
            smooth2 = mc.sets('smooth2', q=True)
        selectionList = smooth1 + smooth2
        for item in selectionList:
            childrenShape_l = mc.listRelatives(item, ad=True, type='shape', f=True)
            for shape in childrenShape_l:
                if mc.objExists(shape + '.rman__torattr___subdivScheme') != True:
                    mel.eval('rmanAddAttr ' + shape + ' rman__torattr___subdivScheme ""')
                if mc.objExists(shape + '.rman__torattr___subdivFacevaryingInterp') != True:
                    mel.eval('rmanAddAttr ' + shape + ' rman__torattr___subdivFacevaryingInterp""')

kSmoothSetTool()