## VRAC

import maya.cmds as mc
selectionList = mc.ls(sl=True)
if selectionList:
    for item in selectionList:
        attrLock = mc.listAttr(locked=True)
        print ">> ", item, "Attributs lock : " + str(attrLock)
        if attrLock :
            for attr in attrLock:
                mc.setAttr(item + "." + attr, lock=False)
                print ">> Attributs unlocked : " + str(attr)
                mc.lockNode( item, lock=False )


##              
selectionList= mc.ls(sl=True)
for item in selectionList:
    name = item.split("_")
    mc.group(item, n="grp_" + name[1], world=True)

item= mc.ls(sl=True)
mc.delete( item )

##
item = mc.ls("building_ctrls_grp.visibility")
mc.lockNode( item, lock=True, q=True)

item = mc.ls(sl=True)
mc.lockNode( item, lock=True)

##
aselectionList = mc.ls("*root_*")
selectionList = mc.ls(sl=True)
if selectionList:
    for item in selectionList:
        attrList = cmds.listAttr(item, ud=True)
        for attr in attrList:
            mc.setAttr(item + "." + attr, lock=False)
            mc.deleteAttr(item + "." + attr)
            
selectionList = mc.ls(sl=True)
if selectionList:
    for item in selectionList:
        attrList = cmds.listAttr(item, ud=True)
        for attr in attrList:
            mc.setAttr(item + "." + attr, lock=False)
            mc.deleteAttr(item + "." + attr)
            
# snap selected objects vertically onto mesh "floor"
import pymel.core as pm

lives = pm.ls(live=1)
if lives:
	floor = lives[0]
else:
	floor = pm.ls("floor", transforms=1)[0]

up = (0,1,0)
down = (0,-1,0)

remaining = list()
for o in pm.ls(sl=1):
    src = o.getRotatePivot(space='world')
    intersections = floor.intersect(src, up, space='world')
    if not intersections[0]:
        intersections = floor.intersect(src, down, space='world')
        if not intersections[0]:
            remaining.append(o)
            continue
    dst = intersections[1][0]
    pm.move(o, dst, rotatePivotRelative=True, worldSpace=True)

pm.select(remaining)


## clean / delete  renderman and MI attr 
            
selectionList = mc.ls(sl=True)
for item in selectionList:
    '''allAttr = mc.listAttr(item)
    #print item, ": ", allAttr
    if mc.objExists(item + "Shape" + ".mi*"):
        itemMIAttr = mc.listAttr(item + "Shape", string="mi*")
        print item, ": ", itemMIAttr'''    
    
    if mc.objExists(item + ".arcGenArchiveNameDisplay*"):
        itemArcAttr = str(mc.listAttr(item, string="*arcGenArchiveNameDisplay*")[0])
        mc.deleteAttr( item + "." + itemArcAttr )
    
    if mc.objExists(item + "Shape" + ".miSubdivApprox"):
        itemMIAttr = mc.listAttr(item + "Shape", string="*miSubdivApprox*")[0]
        mc.deleteAttr( item + "Shape." + itemMIAttr )
        
    if mc.objExists(item + "Shape" + ".rs*"):
        itemRSAttr = mc.listAttr(item + "Shape", string="*rs*")[0]
        mc.deleteAttr( item + "Shape." + itemRSAttr )
        
    if mc.objExists(item + "Shape" + ".rman__torattr___subdivScheme"):
        itemRDMAttr = mc.listAttr(item + "Shape", string="*rman__torattr___subdivScheme*")[0]
        mc.deleteAttr( item + "Shape." + itemRDMAttr )        

selectionList = mc.ls(sl=True)
if selectionList:
    for item in selectionList:
        attrList = cmds.listAttr(item + "Shape", ud=True)
        for attr in attrList:
            print attr


selectionList = mc.ls(sl=True)
for item in selectionList:
    if mc.objExists(item + ".currentUVSet"):
        itemArcAttr = str(mc.listAttr(item, string="currentUVSet")[0])
        #mc.deleteAttr( item + "." + itemArcAttr )
        print item, ": ", itemArcAttr
        
# lalalaa
selectionList = mc.ls(sl=True)
if selectionList:
    for item in selectionList:       
        itemRSAttr = mc.listAttr(item + "Shape", string="rs*")
        if itemRSAttr:
            for attr in itemRSAttr :
                try:
                    mc.deleteAttr( item + "Shape." + attr)
                except:
                    print "plop"
                
                
            if mc.objExists(item + "Shape." + attr):
                itemRSAttr = mc.listAttr(item + "Shape", string="*rs*")[0]


selectionList = mc.ls(sl=True)
for item in selectionList:
    shape = mc.listRelatives(item)[0]
    #attrList = item + "Shape.lev"
    #mc.setAttr(item+".lev", 1) 
    #mc.setAttr(item+".lev", lock=False)
    if mc.objExists(shape + ".rman__torattr___subdivScheme"):
        mc.setAttr(shape + ".rman__torattr___subdivScheme", 0)
    else :
        print "pouet"
        #itemRDMAttr = mc.listAttr(item + "Shape", string="*rman__torattr___subdivScheme*")[0]
        #mc.deleteAttr( item + "Shape." + itemRDMAttr )  
    
## clean / delete all attribute renderman\n
import maya.cmds as mc
selectionList = mc.ls(\"*Shape*\")
for item in selectionList:
        if mc.objExists(item + \".rmanCCs\"):
            mc.deleteAttr( item + \".rmanCCs\")
            attributList = mc.listAttr(item, string=\"*rman*\")
            if attributList:        
                for itemAttr in attributList:
                    mc.deleteAttr( item + \".\" + itemAttr )"		

    # Create a new regular outliner in its own window

mc.window(title="Outliner", toolbox=True)
mc.frameLayout( labelVisible=False, width=300, height=500 )
panel = mc.outlinerPanel(tearOff=False)
outliner = mc.outlinerPanel(panel, query=True, outlinerEditor=True)
myOutliner = mc.outlinerEditor( outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList', showShapes=False, showReferenceNodes=False, showReferenceMembers=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showNamespace=True, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, setFilter='defaultSetFilter')


myOutliner = mc.outlinerPanel(tearOff=True, outlinerEditor=False)
print ">> ", myOutliner
print mc.outlinerPanel(myOutliner, parent=True, q=True)        

##
mc.select("c_*")
selectionList = mc.ls(sl=True, type="transform")
mc.select(selectionList)
if selectionList:
    for item in selectionList:
        #nc = item.split("|")
        print item
        for axe in ["X", "Y", "Z"]:
            mc.setAttr(item + ".translate" + axe, lock=True)
                       
import maya.cmds as cmds

print(cmds.objectTypeUI( 'viewPanes' ))
import sys
for c,e in enumerate(cmds.objectTypeUI(listAll=True)):
    c += 1
    sys.stdout.write(e + " ")
    if c % 3 == 0:
        sys.stdout.write('\n')

channelWindow = mc.layout('MayaWindow|MainChannelsLayersLayout', parent=True, q=1)
mc.window(channelWindow, active=True, q=1)

## probleme bounding box infini
mc.exactWorldBoundingBox(mc.ls(sl=True))

listBad = []
selectionList = mc.ls(sl=1)
if selectionList:
    for item in selectionList:
        values = mc.exactWorldBoundingBox(item)
        if values[0] < -1e+10 or values[0] > 1e+10 :
            listBad.append(item)
            print ">> " + item + " : " + str(values)
        else:
            print ">> " + item + " IS OK"
else:
    print ">> no selection"
print(listBad)
mc.select(listBad)

##
selectionList = mc.ls(sl=True)
shapeList = []
for obj in selectionList:
    shapeList.append(mc.listRelatives(obj, c=True, shapes=True, fullPath=True)[0])
for shapo in shapeList:
    mc.setAttr(shapo + ".smoothLevel", lock=False)
    mc.setAttr(shapo + ".smoothLevel", 2)
    mc.setAttr(shapo + ".smoothLevel", lock=True)

        
for obj in selectionList:
shapes = mc.listRelatives(obj, shapes=True)
for shape in shapes:
    mc.setAttr(shape + ".lev", lock=False)
    mc.setAttr(shape + ".lev", 0)
    mc.setAttr(shape + ".lev", lock=True)

# "addAttr", "connectAttr", "deleteAttr", "disconnectAttr", "parent", "setAttr", "lock" and "unlock"
objName = "*barrel01RN"
objList = mc.ls(objName)
mc.select(objName)

for obj in objList:
    editcmd = [x for x in cmds.referenceQuery(obj, es=True) if 'setAttr' in x]
    if editcmd:    
        filename = cmds.referenceQuery(obj, filename=True)
        mc.file(filename, ur=True)
        mc.referenceEdit(obj, removeEdits=True, editCommand="setAttr", successfulEdits=True)
        mc.file(filename, lr=True)

# Remove all edits
    ref = 'myrefRN'
    nodes = cmds.referenceQuery( ref, editNodes=True )
    attr_types = cmds.referenceQuery( ref, editAttrs=True )
    for node in nodes:
        for attr_type in attr_types:
            for edit_command in ['addAttr', 'connectAttr', 'deleteAttr', 'disconnectAttr', 'parent', 'setAttr', 'lock', 'unlock']:
                cmds.referenceEdit( node+'.'+attr_type, failedEdits=True, successfulEdits=True, removeEdits=True, editCommand=edit_command)
                
## import de tous les buildings
building = ("001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "012b", "013", "014", "015", "015a", "016", "017", "018")
ep = "666"
for b in building :
    mc.file("//ava_server/projets/avalor/ava_maya/scenes/ribarchives/" + ep + "/" + ep + "-building" + b + "/publish/ava_mts_" + ep + "-building" + b + "_v000.ma",
            i=1, type="mayaAscii", ignoreVersion=1, ra=1, mergeNamespacesOnClash=1, namespace=":", options="v=0;", pr=1)

# conversion UI to PY
def kmConvertUI(self):
    # transform UI to PY
    import pysideuic
    pysideuic.compileUiDir(r'C:\Users\m.terray\Documents\maya\2014-x64\scripts')