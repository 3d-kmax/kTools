# match all
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

#unfreeze transform PYMEL
import pymel.core as pm

def cleanupUnfreeze(*args):
    sel = pm.ls(sl=1)

    nodes = pm.ls(args)
    if not nodes:
        nodes = sel
    nodes = pm.ls(nodes, type='transform')
    if not nodes:
        raise RuntimeError()

    for node in nodes:
        _t = node.t.get()
        _rp = node.rp.get()
        _rpt = node.rpt.get()

        _shape = None
        shapes = node.getShapes()
        if shapes:
            _shape = pm.createNode('transform', p=node)
            for _sh in shapes:
                _sh.setParent(_shape, r=1, s=1)
            _shape.setParent(w=1)

        children = node.getChildren(type='transform')
        for _ch in children:
            if not (node.t.isSettable() and node.r.isSettable() and node.s.isSettable()):
                pm.warning('cleanupUnfreeze: "%s" (child of "%s") have locked or connected transformations!' % (
                    str(_ch), str(node)))
            _ch.setParent(w=1)

        node.rp.set(0, 0, 0)
        node.sp.set(0, 0, 0)
        node.rpt.set(0, 0, 0)
        node.spt.set(0, 0, 0)
        node.t.set(_t + _rp + _rpt)

        for _ch in children:
            _ch.setParent(node)

        if _shape:
            _shape.setParent(node)
            pm.makeIdentity(_shape, a=1)
            for _sh in shapes:
                _sh.setParent(node, r=1, s=1)
            pm.delete(_shape)

    pm.select(sel)

cleanupUnfreeze()

## copy all map in a directory TEAMTO
import shutil

def copy_all_maps_to_dest(dest):
    fileNode_l = cmds.ls(type='PxrTexture') + cmds.ls(type='file') + cmds.ls(type='PxrNormalMap') + cmds.ls(
        type='PxrBump') + cmds.ls(type='PxrMultiTexture')
    tex_l = []
    for n in fileNode_l:
        t = ''
        if cmds.nodeType(n) in ['PxrTexture', 'PxrNormalMap', 'PxrBump']:
            t = cmds.getAttr(n + '.filename')
        elif cmds.nodeType(n) in ['file']:
            t = cmds.getAttr(n + '.fileTextureName')
        if t not in tex_l and t != '':
            tex_l.append(t)
        if cmds.nodeType(n) in ['PxrMultiTexture']:
            t_l = []
            for i in range(0, 9):
                t = cmds.getAttr(n + '.filename' + str(i))
                if t and t != '':
                    t_l.append(t)
            for t in t_l:
                if t not in tex_l and t != '' or t != None:
                    tex_l.append(t)
    print tex_l

    for tex in tex_l:
        if tex != '':
            if '._MAPID_.' not in tex:
                shutil.copy(tex, dest)
            else:
                for rng in range(1001, 2000):
                    try:
                        shutil.copy(tex.replace('_MAPID_', str(rng)), dest)
                        print tex, ' copied'
                    except:
                        pass

    for n in fileNode_l:
        t = None
        try:
            t = cmds.getAttr(n + '.filename')
        except:
            t = cmds.getAttr(n + '.fileTextureName')
        if t != '':
            new_t = dest + t.split('/')[-1]
            try:
                cmds.setAttr(n + '.filename', new_t, type='string')
                print n, ' replaced'
            except:
                cmds.setAttr(n + '.fileTextureName', new_t, type='string')
                print n, ' replaced'


dest = '//tak_server/projets/take-it-easy-mike/tak_maya/sourceimages/ribarchives/nature-components/catalpa-04-debug/work/'
copy_all_maps_to_dest(dest)

# rename Shapes Curves shape from transform
controlList = cmds.ls('c_*', type='transform', l=True)
print ">> Nombre ce controleur :", len(controlList)
for obj in controlList:
    if ':' not in obj:
        child_l = cmds.listRelatives(obj, children=True, f=True)
        nurbs_l = []
        for child in child_l:
            if cmds.nodeType(child) == 'nurbsCurve':
                nurbs_l.append(child)
        for nurb in nurbs_l:
            transfName_l = obj.split('|')
            transfName = transfName_l[len(transfName_l) - 1]

            cmds.rename(nurb, transfName + 'Shape')
            print ">> : ", nurb, "renamed : ", transfName