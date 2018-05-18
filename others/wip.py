import maya.cmds as mc
import pymel.core as pm

## creation des numéros de plan pour la cam
shotList2 = ("011","012","013","014","021","056","057","210","223","254","255","257","266","269","270","273")
shotList = ("060","061","063","064","076","085","102","134","142","301")
shotLen = len(shotList)
mc.playbackOptions(maxTime=shotLen-1, animationEndTime=shotLen-1)
i=-1

shaderName = "constBlanc"
shadingGroupName = shaderName + 'SG'
mc.shadingNode("surfaceShader", asShader=True, name=shaderName)
mc.setAttr(shaderName + ".outColor", 1, 1, 1, type="double3")
mc.sets(renderable=True, empty=1, noSurfaceShader=True, name=shadingGroupName)
mc.defaultNavigation(source=shaderName, destination=shadingGroupName, connectToExisting=1)

for item in shotList:
    shotCurveName = "shotCurve" + item
    shotCurve = mc.textCurves(name=shotCurveName, ch=0, f="Arial", t="sc" + item)
    shotNumberName = "sc" + item
    shotNumber = mc.planarSrf(name=shotNumberName, polygon=3)
    ##mc.setAttr(shotNumberName + ".scale", 0.08, 0.08, 0.08, type="double3") 
    mc.sets("sc" + item, forceElement=shadingGroupName, e=1)
    mc.delete(shotCurveName + "Shape")
    mc.setKeyframe(value=0, t=i, attribute="visibility")
    i+=1
    mc.setKeyframe(value=1, t=i, attribute="visibility")
    mc.setKeyframe(value=0, t=i+1, attribute="visibility")

    
## clean / delete all attribute renderman
import maya.cmds as mc

selectionList = mc.ls("*rock*Shape*") ## revoir la selection !!
for item in selectionList:
    if mc.objExists(item + ".rmanCCs"):
        mc.deleteAttr( item + ".rmanCCs")
    attributList = mc.listAttr(item, string="*rman*")
    if attributList:        
        for itemAttr in attributList:
            mc.deleteAttr( item + "." + itemAttr )
            
## set shapes opposite attribute to 0
import maya.cmds as mc
selectionList = mc.ls(selection=True)
mc.listAttr(string="opposite")
for item in selectionList:
    if mc.objExists(item + ".opposite"):
        mc.setAttr( item + ".opposite", 0)
        
## delete turtle nodes
selectionList = mc.ls(type=['ilrBakeLayer','ilrOptionsNode','ilrBakeLayerManager','ilrUIOptionsNode'])
selectionNodes = ("TurtleBakeLayerManager", "TurtleDefaultBakeLayer", "TurtleRenderOptions", "TurtleUIOptions")
for item in selectionNodes:
    mc.lockNode( item, lock=False )
    mc.delete( item )
print ">> " + str(len(selectionList)) + " Turtle nodes DELETED"

## prepare scene for RIB

import maya.cmds as mc
if mc.objExists("*world2*"):
    mc.delete("world2")
    
selectionRoot = mc.ls("|root_*", type="transform")[0]
nameRoot= selectionRoot.split('_')[1]

if mc.objExists("sets_" + nameRoot):
	mc.delete("sets_" + nameRoot)

selectionList=mc.ls("*MOB_*")
renderGrp = mc.group(selectionList, n="rib_" + str(nameRoot) + "_RENDER", world=True)
proxyElt = mc.duplicate(selectionList,renameChildren=True )
proxyGrp = mc.group(proxyElt, n="grp_" + str(nameRoot) + "_PROXY", world=True)

mc.group( proxyGrp, renderGrp, n=str(nameRoot))
mc.delete(selectionRoot)

# move uv for matte painting
import maya.cmds as mc
selection = mc.ls(sl=True)
#print ">> : " + str(selection)
mc.polyEditUV(selection, relative=0, u=1.0001)

# Match transform
import maya.cmds as mc
selectionList = mc.ls(selection=True, type='transform')
if selectionList >= 2:
    newTranslation = mc.xform(selectionList[-1], q=True, translation=True, worldSpace=True)
    for objMacth in selectionList[:-1]:
        mc.xform(objMacth, p=True, translation=newTranslation, worldSpace=True)
print ">> Match Translate"

# rotate:
import maya.cmds as mc
selectionList = mc.ls(selection=True, type='transform')
if selectionList >= 2:
    newRotation = mc.xform(selectionList[-1], q=True, rotation=True, worldSpace=True)
    for objMacth in selectionList[:-1]:
        mc.xform(objMacth, p=True, rotation=newRotation, worldSpace=True)
print ">> Match Rotate"

# scale
import maya.cmds as mc
selectionList = mc.ls(selection=True, type='transform')
if selectionList >= 2:
    newScale = mc.xform(selectionList[-1], q=True, scale=True)
    for objMacth in selectionList[:-1]:
        mc.xform(objMacth, p=True, scale=newScale)
print ">> Match Scale"

# all
import maya.cmds as mc
selectionList = mc.ls(selection=True, type='transform')
if selectionList >= 2:
    newTranslation = mc.xform(selectionList[-1], q=True, translation=True, worldSpace=True)
    newRotation = mc.xform(selectionList[-1], q=True, rotation=True, worldSpace=True)
    newScale = mc.xform(selectionList[-1], q=True, scale=True)
 
for objMacth in selectionList[:-1]:
    mc.xform(objMacth, p=True, translation=newTranslation, worldSpace=True)
    mc.xform(objMacth, p=True, rotation=newRotation, worldSpace=True)
    mc.xform(objMacth, p=True, scale=newScale)
print ">> Match All"

## clean / delete  renderman and MI attr
selectionList = mc.ls(sl=True)
for item in selectionList:
    if mc.objExists(item + "Shape" + ".miSubdivApprox"):
        itemMIAttr = mc.listAttr(item + "Shape", string="*miSubdivApprox*")[0]
        mc.deleteAttr( item + "Shape." + itemMIAttr )
        
    if mc.objExists(item + "Shape" + ".rman__torattr___subdivScheme"):
        itemRDMAttr = mc.listAttr(item + "Shape", string="*rman__torattr___subdivScheme*")[0]
        mc.deleteAttr( item + "Shape." + itemRDMAttr )
        
        
## unlock , set , relock a attr
selectionList = mc.ls(sl=True)

for item in selectionList:
    mc.setAttr(item + "Shape.lev", lock=False)
    mc.setAttr(item + "Shape.lev", 0)
    mc.setAttr(item + "Shape.lev", lock=True)