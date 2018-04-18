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