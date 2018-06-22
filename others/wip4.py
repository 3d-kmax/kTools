# align pivot to vertex
import maya.cmds as mc

selectionList = mc.ls(sl=True)
pos = []
for item in selectionList:
    shape = mc.listRelatives(item, shapes=True)[0]
    pos = mc.xform(shape + ".pnts[314]", query=True, translation=True, worldSpace=True)
    mc.move(pos[0], pos[1], pos[2], item + ".scalePivot", item + ".rotatePivot")

# move -rpr -0.661308 9.84445 2.404782 leaf_01_hi.scalePivot leaf_01_hi.rotatePivot ;


nodes = mc.ls("*_lo", recursive=True)
if nodes:
    mc.select(nodes)
    if mc.getAttr(nodes[0] + '.visibility'):
        mc.hide(nodes)
    else:
        mc.showHidden(nodes)

mc.listAttr()

###
vtxWorldPosition = []  # contiendra les positions dans l'espace de tout les vertex de l'objet
vtxIndexList = cmds.getAttr(shapeNode + ".vrts", multiIndices=True)
for i in vtxIndexList:
    curPointPosition = cmds.xform(str(shapeNode) + ".pnts[" + str(i) + "]", query=True, translation=True,
                                  worldSpace=True)  # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]
    vtxWorldPosition.append(curPointPosition)
return vtxWorldPosition
