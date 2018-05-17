## create light set for viewport2
import maya.cmds as mc
sel = mc.ls('groupLightA')
if not sel :
    mc.ambientLight(n='ambiantLightA', intensity=0.6)
    mc.spotLight(n='spotLightA', intensity=0.6, coneAngle=80)
    mc.setAttr( 'spotLightA.rotateX', -90 )
    mc.setAttr( 'spotLightA.translateY', 300)
    mc.setAttr( 'spotLightA.scale', 200, 200, 200, type="double3")
    mc.group( 'ambiantLightA', 'spotLightA', n='groupLightA' )
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
            
            
mc.ls("|root_*", type="transform")[0]

## integration matte
import maya.cmds as mc

selectionMatte = mc.ls(sl=True)
mc.parent(selectionMatte, "GEO")
mc.rename(selectionMatte, "grp_matte")


selectionList = mc.ls("msh_*_matte_*", type="transform")
if selectionList :
    for item in selectionList :
        mc.sets(item, addElement="smooth1")
        oldSet = mc.ls("ava_mts_*_matte_*_smooth*", type="objectSet")
        mc.delete(oldSet)
        setList = mc.listSets(allSets=True)
        if "geo_matte" not in setList :
            mc.sets(item, name="geo_matte")
        else :
            mc.sets(item, addElement="geo_matte")
            
## uncheck shapes opposite attribute
import maya.cmds as mc
selectionList = mc.ls(selection=True)
mc.listAttr(string="opposite")
for item in selectionList:
    if mc.objExists(item + ".opposite"):
        mc.setAttr( item + ".opposite", 0)

## switch all/polygon view
import maya.cmds as mc

allModelPanel = mc.getPanel(type='modelPanel')
if allModelPanel:
    for modelPanelName in allModelPanel:
        print ">> " , mc.modelEditor(modelPanelName, nCloths=1, q=1)
        if mc.modelEditor(modelPanelName, nCloths=1, q=1):
            mc.modelEditor(modelPanelName, allObjects=0, e=1)
            mc.modelEditor(modelPanelName, polymeshes=1, e=1)
        else:
            mc.modelEditor(modelPanelName, allObjects=1, e=1)
    
# combine dans un grp
selectionGrp = mc.ls(sl=True)
for item in selectionGrp :
    name = item.split('grp_')[1]
    newName = "msh_" + name
    listMsh = mc.listRelatives(children=True)
    mc.polyUnite(listMsh, n=newName)
    mc.xform(cp=True)    
    mc.parent(newName, item)
    mc.delete(constructionHistory=True)
    
# delete all rs attr
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