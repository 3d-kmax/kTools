# --- smooth sets UI
"""adds or removes objects from smooth sets"""

import maya.cmds as mc

# --- settings

smoothSetBodyName = 'smooth'
partitionName = 'prt_smooth'
layerPrefix = 'lyr'
sep = '_'
optSmoothPreview = True
optSmoothRender = True
optSmooth = False
optLayer = True
optPart = False

# --- functions: sets

def smoothSetName(value):
    return smoothSetBodyName + str(value)

def smoothSetList():
    return filter(lambda x: x.rpartition(':')[-1].startswith(smoothSetBodyName) and x.rpartition(':')[-1][len(smoothSetBodyName):].isdigit(), mc.ls(set=True))

def createSmoothSet(value):
    if not smoothSetName(value) in smoothSetList():
        mc.select(cl=True)
        mc.sets(n='smooth'+str(value))

# --- functions: partition

def createPartition():
    if partitionName not in mc.ls(type='partition'):
        mc.partition(n=partitionName)

def addToPartition(smoothSet):
    if mc.objExists(partitionName):
        setsInPrtLs = mc.partition(partitionName, q=True)
        if not setsInPrtLs:
             mc.partition(smoothSet, add=partitionName)
        else:
            if smoothSet in setsInPrtLs:
                print '# %s already in partition: %s' %(smoothSet, partitionName)
            else:
                if len(setsInPrtLs) == 1:
                    geoInPrtLs = mc.sets(setsInPrtLs[0], q=True)
                else:
                    geoInPrtLs = mc.sets(union=setsInPrtLs)
                for geo in mc.sets(smoothSet, q=True) or []:
                    if geo in geoInPrtLs:
                        setLs = mc.listConnections(geo, s=False, d=True, type='objectSet') or []
                        mc.warning('Could not add %s to the partition because %s belongs to more than one set: %s' %(smoothSet, geo, setLs))
                    else:
                        mc.partition(smoothSet, add=partitionName)

# --- functions: layers

def dispLayerName(value):
    return sep.join([layerPrefix, smoothSetName(value)])

def dispLayerList():
    return filter(lambda x: x.startswith(layerPrefix+sep+smoothSetBodyName) and x[len(layerPrefix+sep+smoothSetBodyName):].isdigit(), mc.ls(typ='displayLayer'))

def createDisplayer(value):
    if not dispLayerName(value) in dispLayerList():
        mc.createDisplayLayer(empty=True, n=dispLayerName(value))

# --- functions: selection

def filterSelection(selection=mc.ls(sl=True, l=True), source='scene'):
    """returns a filtered list of geometry transforms only from selection
    source variable may be 'scene' or 'set' depending of the source of selection"""
    result = []
    if not selection and source == 'scene':
        mc.error('Nothing is selected !')
    else:
        for sel in selection or []:
            if mc.nodeType(sel) == 'transform' and filter(lambda x: mc.nodeType(x) == 'mesh', mc.listRelatives(sel, s=True, f=True) or []):
                result.append(sel)
    return result

# --- functions: options

def optWhichNeedLoop():
    """returns a dict wich specifies if a obj level and/or shape level loop is needed,
    depending of options"""
    result = {'loopInObj':False, 'loopInShape':False}
    shapeOptLs = [smstUI_optSmPw_mI, smstUI_optSmRnd_mI]
    objOptLs = [smstUI_optSmView_mI]
    for mi in shapeOptLs:
        if mc.menuItem(mi, q=True, cb=True):
            result['loopInShape'] = True
            result['loopInObj'] = True
    if not result['loopInObj']:
         for mi in objOptLs:
            if mc.menuItem(mi, q=True, cb=True):
                result['loopInObj'] = True
    return result
        
# --- functions: buttons

def getSmoothLvl(*args):
    if mc.iconTextRadioButton(smstUI_smoothLvl0, select=True, q=True):
        return 0
    if mc.iconTextRadioButton(smstUI_smoothLvl1, select=True, q=True):
        return 1
    if mc.iconTextRadioButton(smstUI_smoothLvl2, select=True, q=True):
        return 2

def addToSmoothSet(*arg):
    selection = filterSelection(mc.ls(sl=True, l=True), 'scene')
    #value = mc.intSliderGrp(smstUI_smoothLvl_intSG, q=True, value=True)
    value = getSmoothLvl()
    if selection:
        
        # --- set
        remFromAll()
        createSmoothSet(value)
        inSet = mc.sets(smoothSetName(value), q=True) or []
        mc.sets(selection, add=smoothSetName(value))
        result = list(set([sel.rpartition('|')[-1] for sel in selection]) - set(inSet))
        print '# %s added to %s' %(result, smoothSetName(value))
        """
        # --- partition
        createPartition()
        addToPartition(smoothSetName(value))
        """
        # --- options
        options = optWhichNeedLoop()
        if options['loopInObj']:
            for obj in result:
                if mc.menuItem(smstUI_optSmView_mI, q=True, cb=True):
                    mc.displaySmoothness(obj, polygonObject=3)            
                if options['loopInShape']:               
                    for shape in mc.listRelatives(obj, s=True, f=True):
                        if mc.menuItem(smstUI_optSmPw_mI, q=True, cb=True):
                            mc.setAttr(shape+'.smoothLevel', value)
                        if mc.menuItem(smstUI_optSmRnd_mI, q=True, cb=True):
                            mc.setAttr(shape+'.renderSmoothLevel', value)            
        
        # --- layer
        if mc.menuItem(smstUI_optDispLay_mI, q=True, cb=True):
            createDisplayer(value)
            mc.editDisplayLayerMembers(dispLayerName(value), result, noRecurse=True)
            
    else:
        mc.error('Wrong node type in selection ! Please select geometry transforms only')

def remFromSmoothSet(*arg):
    #selection = filterSelection(mc.ls(sl=True, l=True), 'scene')
    selection = mc.ls(sl=True, l=True)
    #value = mc.intSliderGrp(smstUI_smoothLvl_intSG, q=True, value=True)
    value = getSmoothLvl()
    if selection:
        inSet = mc.sets(smoothSetName(value), q=True) or []
        mc.sets(selection, rm=smoothSetName(value))
        print '# %s removed from %s' %(list(set([sel.rpartition('|')[-1] for sel in selection])&set(inSet)), smoothSetName(value))
    else:
        mc.error('Wrong node type in selection ! Please select geometry transforms only')

def remFromAll(*arg):
    #selection = filterSelection(mc.ls(sl=True, l=True), 'scene')
    selection = mc.ls(sl=True, l=True)
    if selection:
        for smoothSet in smoothSetList():
            inSet = mc.sets(smoothSet, q=True) or []
            mc.sets(selection, rm=smoothSet)
            result = list(set([sel.rpartition('|')[-1] for sel in selection]) & set(inSet))
            if result != []:
                print '# %s removed from %s' %(result, smoothSet)
    else:
        mc.error('Wrong node type in selection ! Please select geometry transforms only')

# --- functions: menus

def smoothAll(*arg):
    for smoothSet in filter(lambda x: ':' not in x, smoothSetList()) or []:
        value = int(smoothSet[len(smoothSetBodyName):])
        for obj in filterSelection(mc.sets(smoothSet, q=True),'set'): # or []
            mc.displaySmoothness(obj, polygonObject=3)
            for shape in mc.listRelatives(obj, s=True, f=True):
                mc.setAttr(shape+'.smoothLevel', value)
                if mc.menuItem(smstUI_optSmRnd_mI, q=True, cb=True):
                    mc.setAttr(shape+'.renderSmoothLevel', value)

def conformSmoothSets(*arg):
    
    memberLs = []
    moreThanOneSetLs = []
    groupLs = []
    shapeLs = []
    
    # --- merge smooth sets
    mergeSmoothSetWithNamespace()
    
    smoothSetLs = filter(lambda x: ':' not in x, smoothSetList())
    if smoothSetLs:
        for smoothSet in smoothSetLs:
            memberLs = list(set(memberLs) | set(mc.sets(smoothSet, q=True) or []))
        if memberLs:
            for member in memberLs:
                # --- check if object is a geometry transform
                if mc.nodeType(member) == 'transform' and filter(lambda x: mc.nodeType(x) == 'mesh', mc.listRelatives(member, s=True, f=True) or []):
                    if len(set(mc.listConnections(member, s=True, d=True, type='objectSet')) & set(smoothSetLs)) > 1:
                        moreThanOneSetLs.append(member)
                else:
                    # --- group
                    if mc.nodeType(member) == 'transform' and not mc.listRelatives(member, s=True, f=True):
                        if mc.listRelatives(member, c=True):
                            groupLs.append(member)
                        else:
                            smoothSetLs = list(set(mc.listConnections(member, s=True, d=True, type='objectSet')) & set(smoothSetLs))
                            for smoothSet in smoothSetLs:
                                mc.sets(member, rm=smoothSet)
                                print '# %s removed from %s' %(member, smoothSet)
                    # --- shape
                    elif mc.nodeType(member) == 'mesh':
                        shapeLs.append(member)
                    # --- else
                    else:
                        smoothSetLs = list(set(mc.listConnections(member, s=True, d=True, type='objectSet')) & set(smoothSetLs))
                        for smoothSet in smoothSetLs:
                            mc.sets(member, rm=smoothSet)
                            print '# %s removed from %s' %(member, smoothSet)
        else:
            mc.warning('Smooth sets are empty')
    else:
        mc.error('No smooth set to conform found !')        
    
    # --- delete empty sets
    for smoothSet in smoothSetLs:
        if not mc.sets(smoothSet, q=True):
            mc.delete(smoothSet)
            print '# %s was empty and has been deleted' %smoothSet
     
    print 'More than one set:'
    print moreThanOneSetLs
    print 'Groups'
    print groupLs
    print 'Shapes'
    print shapeLs

def mergeSmoothSetWithNamespace(*arg):
    """creates or adds to local smooth sets objects from imported smooth sets of the same value"""
    nsSetLs = filter(lambda x: ':' in x, mc.ls(set=True))
    nsSmoothSetLs = filter(lambda x: x.rpartition(':')[-1].startswith(smoothSetBodyName) and x.rpartition(':')[-1][len(smoothSetBodyName):].isdigit(), nsSetLs)
    if nsSmoothSetLs:
        for smoothSet in nsSmoothSetLs:
            value = smoothSet.rpartition(':')[-1][len(smoothSetBodyName):]
            createSmoothSet(value)
            result = mc.sets(smoothSetName(value), sub=smoothSet)
            if result: 
                mc.sets(result, rm=smoothSet)
                print '# %s removed from %s' %(result, smoothSet)
                mc.sets(result, add=smoothSetName(value))
                print '# %s added to %s' %(result, smoothSetName(value))
            else:
                print '# %s: Merge not needed' %smoothSet
    else:
        mc.warning('No smooth sets with namespace found !')

def createSmoothPartition(*arg):
    """creates a smooth partition and adds smooth sets to it"""
    createPartition()
    for smoothSet in smoothSetList():
        addToPartition(smoothSet)

def createLayerFromSmoothSets(*arg):
    smoothSetLs = smoothSetList()
    smoothSetLs.sort(reverse=True)
    for smoothSet in smoothSetLs:
        memberLs = mc.sets(smoothSet, q=True)
        if memberLs:
            value = smoothSet[len(smoothSetBodyName):]
            createDisplayer(value)
            mc.editDisplayLayerMembers(dispLayerName(value), memberLs, noRecurse=True)

def removeSmoothLayers(*arg):
    for layer in dispLayerList():
        mc.delete(layer)

# --- UI: build main UI

#def setSmoothGroupToolUI():
if mc.window('smstUI', q=True, exists=True):
    mc.deleteUI('smstUI')
smoothSetUI = mc.window('smstUI', t='Smooth Sets UI', mb=True, toolbox=True, titleBar=True, minimizeButton=False, maximizeButton=False, sizeable=False)
mc.window( smoothSetUI, edit=True, height=80, width=160)

mc.menu(l='Tools')
mc.menuItem(l='Smooth all from smooth sets', c=smoothAll)
mc.menuItem(d=True)
mc.menuItem(l='Conform smooth sets', c=conformSmoothSets)
mc.menuItem(l='Merge smooth sets with namespace', c=mergeSmoothSetWithNamespace)
mc.menuItem(l='Create smooth partition', c=createSmoothPartition)

mc.menu(l='Layers')
mc.menuItem(l='Create layers from smooth sets', c=createLayerFromSmoothSets)
mc.menuItem(l='Remove smooth set layers', c=removeSmoothLayers)

mc.menu(l='Options')
smstUI_optSmPw_mI = mc.menuItem(l='Auto set preview division level', cb=optSmoothPreview)
smstUI_optSmRnd_mI = mc.menuItem(l='Auto set render division level', cb=optSmoothRender)
mc.menuItem(d=True)
smstUI_optSmView_mI = mc.menuItem(l='Auto smooth in viewport', cb=optSmooth)
smstUI_optDispLay_mI = mc.menuItem(l='Auto create layers', cb=optLayer)
smstUI_optDispLay_mI = mc.menuItem(l='Auto create partition', cb=optPart)


#smstUI_win_formL = mc.formLayout()
#smstUI_slider_frameL = mc.frameLayout(labelVisible=0, borderVisible=False, p=smstUI_win_formL)
mc.frameLayout(label="Smooth set :", labelVisible=0, borderVisible=0, marginHeight=2, marginWidth=2) #borderStyle="out",

mc.columnLayout(rowSpacing=2)

mc.rowLayout(numberOfColumns=3, columnWidth=[(1,54), (2,54), (3,54)])
smstUI_smoothLvl_set = mc.iconTextRadioCollection("Smooth level")
smstUI_smoothLvl0 = mc.iconTextRadioButton(l="0 ", style='iconAndTextHorizontal', image="E:/kTools/icons/polyCube2016.png", selectionImage="E:/kTools/icons/polyCube2016b.png")
smstUI_smoothLvl1 = mc.iconTextRadioButton(l="1 ", style='iconAndTextHorizontal', image="E:/kTools/icons/kSphere32.png", selectionImage="E:/kTools/icons/kSphere32b.png")
smstUI_smoothLvl2 = mc.iconTextRadioButton(l="2 ", style='iconAndTextHorizontal', image="E:/kTools/icons/polySphere2016.png", selectionImage="E:/kTools/icons/polySphere2016b.png")
mc.setParent('..')
mc.setParent('..')
'''
smstUI_slider_formL = mc.formLayout()
smstUI_smoothLvl_intSG = mc.intSliderGrp(l='Smooth Level: ', field=True, min=0, max=3, columnWidth=[(1,80), (2,20), (3,60)])
mc.setParent('..')'''

mc.rowLayout(numberOfColumns=3)
#smstUI_buttons_formL = mc.formLayout(nd=3, p=smstUI_win_formL)
smstUI_add_b = mc.button(l='+', c=addToSmoothSet, height=30, width=30)
smstUI_rm_b = mc.button(l='-', c=remFromSmoothSet, height=30, width=30)
smstUI_rmAll_b = mc.button(l='Remove From All', c=remFromAll, height=30,  width=100)
mc.setParent('..')
#mc.setParent('..')

mc.setParent('..')
# --- UI: arrange layout

'''mc.formLayout(smstUI_win_formL, e=True, \
af = ((smstUI_slider_frameL, 'top', 2), \
    (smstUI_slider_frameL, 'left', 0), \
    (smstUI_slider_frameL, 'right', 0), \
    (smstUI_buttons_formL, 'left', 0), \
    (smstUI_buttons_formL, 'right', 0), \
    (smstUI_buttons_formL, 'bottom', 0)))
    
mc.formLayout(smstUI_smstUI_smoothLvl_set, e=True, \
af = ((

mc.formLayout(smstUI_slider_formL, e=True, \
af = ((smstUI_smoothLvl_intSG, 'top', 0), \
    (smstUI_smoothLvl_intSG, 'left', 0), \
    (smstUI_smoothLvl_intSG, 'right', 0), \
    (smstUI_smoothLvl_intSG, 'bottom', 0)))

mc.formLayout(smstUI_buttons_formL, e=True, \
af = ((smstUI_add_b, 'top', 0), \
    (smstUI_add_b, 'left', 0), \
    (smstUI_rm_b, 'top', 0), \
    (smstUI_rmAll_b, 'top', 0), \
    (smstUI_rmAll_b, 'right', 0)), \
ac = ((smstUI_rm_b, 'left', 1, smstUI_add_b), \
    (smstUI_rm_b, 'right', 1, smstUI_rmAll_b)), \
ap = ((smstUI_add_b, 'right', 0, 1), \
    (smstUI_rmAll_b, 'left', 0, 2)))'''

mc.showWindow(smoothSetUI)        
        
#setSmoothGroupToolUI()
#print mc.window('smstUI', q=True, wh=True)

