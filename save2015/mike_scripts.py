# unlock all attribut
selectionList = mc.ls(selection=True, l=True)
        if selectionList:
            lock_l = mc.listRelatives(selectionList, ad=True, type='transform', f=True)
            lock_l = sorted(lock_l, key=lambda s: s.count('|'), reverse=False)

            transformAttr_l = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.shearXY', '.shearXZ',
                           '.shearYZ', '.rotateAxisX', '.rotateAxisY', '.rotateAxisZ', '.visibility']
            # transform_global_l = ['.translate', '.rotate', '.scale', '.shear']

            for obj in lock_l:
                obj_sn = obj.split('|')[-1:][0]
                if mc.nodeType(obj) == 'transform' and ':' not in obj:
                    if obj_sn.startswith('c_') != True:
                        for attr in transformAttr_l:
                            mc.setAttr(obj + attr, lock=False)
                        print obj + " >> All Attributs unlock !"

# unfreeze
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

# import/remove lighting
item = mc.ls("*:c_lighting_work")
if item != []:
    if mc.referenceQuery(item, isNodeReferenced=True):
        refFile = mc.referenceQuery(item, filename=True)
        mc.file(refFile, removeReference=True)
else:
    mc.file("//tak_server/projets/take-it-easy-mike/tak_maya/scenes/lights/for_work/lighting_shading_work/lighting_shading_work_v000.ma", r=1, type="mayaAscii", ignoreVersion=1, mergeNamespacesOnClash=1, namespace="", options="v=0;", pr=1)

# dice_watertight
for obj in cmds.ls(type='PxrDisplace'):
    if ':' not in obj:
        if cmds.objExists(obj + '.rman__riattr__dice_watertight') != True:
            mel.eval('rmanAddAttr [node] rman__riattr__dice_watertight [val]'.replace("[node]", obj).replace("[val]",
                                                                                                             str(1)))

# presenceCached
for obj in cmds.ls(type='PxrSurface'):
    if cmds.connectionInfo(obj + '.presence', sfd=True):
        cmds.setAttr(obj + '.presenceCached', 0)
        print ">> : ", obj, ".presence set to Non Cached"
    else:
        print ">> : ", obj, "got NO attr.presence"

# RENAME PXR NODES

# fileNodes RIS
pxrFileNode_l = cmds.ls(type=('PxrTexture'))
for obj in pxrFileNode_l:
    if ':' not in obj:
        mapPath = cmds.getAttr(obj + '.filename')
        mapNameExt = mapPath.split('/')[-1:]
        mapName = mapNameExt[0].split('.')[0]
        fileNodeName = 'pxr_file_' + mapName
        cmds.rename(obj, fileNodeName)

# fileNodes nml RIS
pxrNmlFileNode_l = cmds.ls(type=('PxrNormalMap'))
for obj in pxrNmlFileNode_l:
    if ':' not in obj:
        mapPath = cmds.getAttr(obj + '.filename')
        mapNameExt = mapPath.split('/')[-1:]
        mapName = mapNameExt[0].split('.')[0]
        if mapName.startswith('nml_'):
            pass
        else:
            mapName = 'nml_' + mapName
        fileNodeName = 'pxr_' + mapName
        cmds.rename(obj, fileNodeName)

# rename PxrNormalMap
pxrNmlFileNode_l = cmds.ls(type=('PxrNormalMap', 'PxrBump'))
for obj in pxrNmlFileNode_l:
    if ':' not in obj:
        output = cmds.connectionInfo(obj + '.resultN', dfs=True)[0].split('.')[0]
        if ':' in output:
            output = output.split(':')[-1]
        if cmds.nodeType(obj) == 'PxrBump':
            typ = 'pxr_bmp_'
        else:
            typ = 'pxr_nml_'
        cmds.rename(obj, typ + output)

# Rename SG from shaders
SG_l = cmds.ls(type='shadingEngine', r=False)
baseSG_l = [u'initialParticleSE', u'initialShadingGroup']
for baseSG in baseSG_l:
    SG_l.remove(baseSG)

for obj in SG_l:
    if ':' not in obj:
        shader = cmds.connectionInfo(obj + '.surfaceShader', sfd=True)
        shaderdisp = cmds.connectionInfo(obj + '.displacementShader', sfd=True)
        if shader == '' and shaderdisp == '':
            cmds.lockNode(obj, lock=False)
            cmds.delete(obj)

        shader = cmds.connectionInfo(obj + '.surfaceShader', sfd=True)
        shader = (str(shader)).replace('.outColor', '')
        cmds.rename(obj, shader + 'SG')
        #
        dspShader_l = cmds.connectionInfo(shader + 'SG' + '.displacementShader', sfd=True)
        if dspShader_l != '':
            dspShader = (str(dspShader_l)).replace('.outColor', '')
            dspShader_name = shader.replace('sh_', 'sh_dsp_')
            cmds.rename(dspShader, dspShader_name)

dspShader_l = []

# ref list edit
for refNode in cmds.ls(type='reference'):
    # selectionList=("tak_mts_brindilles_patch_01_v000RN","tak_mts_brindilles_patch_01_v000RN1","tak_mts_brindilles_patch_01_v000RN2","tak_mts_brindilles_patch_01_v000RN3")
    # for refNode in selectionList:
    if cmds.referenceQuery(refNode, isLoaded=True):
        filePath = cmds.referenceQuery(refNode, filename=True)
        refEdit_l = cmds.referenceQuery(refNode, editStrings=True, sdp=True)
        trueEdit_l = []
        for refEdit in refEdit_l:
            if '.translate' in refEdit or '.rotate' in refEdit or '.scale' in refEdit or '.visibility' in refEdit or 'parent' in refEdit:
                trueEdit_l.append(refEdit)
        if trueEdit_l != []:
            refName_TT = refNode.split('RN')[0] + 'TT' + refNode.split('RN')[-1]
            while cmds.objExists(refName_TT):
                refName_TT = refName_TT + str(1)
            cmds.file(filePath, r=True, namespace=refName_TT)
            for trueEdit in trueEdit_l:
                namespaceEdit = trueEdit.split(':')[0].split('|')[-1]
                mel.eval(trueEdit.replace(namespaceEdit, refName_TT))
        cmds.file(filePath, unloadReference=True)

# match transforms
def matchTranslate(self):
    selectionList = mc.ls(selection=True, type='transform')
    if selectionList >= 2:
        newTranslation = mc.xform(selectionList[-1], q=True, translation=True, worldSpace=True)
        for objMacth in selectionList[:-1]:
            mc.xform(objMacth, p=True, translation=newTranslation, worldSpace=True)
    print ">> Match Translate"

def matchRotate(self):
    selectionList = mc.ls(selection=True, type='transform')
    if selectionList >= 2:
        newRotation = mc.xform(selectionList[-1], q=True, rotation=True, worldSpace=True)
        for objMacth in selectionList[:-1]:
            mc.xform(objMacth, p=True, rotation=newRotation, worldSpace=True)
    print ">> Match Rotate"

def matchScale(self):
    selectionList = mc.ls(selection=True, type='transform')
    if selectionList >= 2:
        newScale = mc.xform(selectionList[-1], q=True, scale=True)
        for objMacth in selectionList[:-1]:
            mc.xform(objMacth, p=True, scale=newScale)
    print ">> Match Scale"

def matchAllTransforms(self):
    self.matchTranslate()
    self.matchRotate()
    self.matchScale()
    print ">> Match All Transfroms"


##
        origin:geo_cupcake.visibility = 0;
        origin1:geo_chicken_leg.visibility = 0;
        origin2:geo_chili_pepper_jar.visibility = 0;
        origin4:geo_ananas_coin_sam.visibility = 0;
        origin5:root_ttMeta.visibility = 0;
        origin5:geo_apple_candy.visibility = 0;
        origin6:geo_apricot.visibility = 0;
        origin7:geo_fruit_banana.visibility = 0;
        origin8:geo_fruit_pear.visibility = 0;
        origin9:geo_orange.visibility = 0;
        origin10:geo_watermelon.visibility = 0;
        origin11:geo_hamknuckle.visibility = 0;
        origin12:geo_jar_jelly_apricot.visibility = 0;
        origin13:geo_jar_jelly_blueberry.visibility = 0;
        origin14:geo_jar_jelly_strawberry.visibility = 0;
        origin15:geo_kitchenflamby.visibility = 0;
        origin16:geo_kitchenmilkbottle.visibility = 0;
        origin17:geo_kitchensodacan.visibility = 0;
        origin18:geo_lettuce.visibility = 0;
        origin19:geo_box_cocktail.visibility = 0;
        origin20:geo_noodle_box.visibility = 0;
        origin21:geo_salami.visibility = 0;
        origin22:geo_broccoli_branch.visibility = 0;
        origin23:geo_veggiegarlic.visibility = 0;
        origin24:geo_onions_cuisine.visibility = 0;
        origin25:geo_poivron_vert_cuisine.visibility = 0;
        origin28:geo_cupcake.visibility = 0;
        origin29:geo_cupcake.visibility = 0;
        origin30:geo_chicken_leg.visibility = 0;
        origin31:geo_chicken_leg.visibility = 0;
        origin32:geo_chili_pepper_jar.visibility = 0;
        origin33:geo_chili_pepper_jar.visibility = 0;
        origin34:geo_ananas_coin_sam.visibility = 0;
        origin35:geo_ananas_coin_sam.visibility = 0;
        origin36:geo_ananas_coin_sam.visibility = 0;
        origin37:root_ttMeta.visibility = 0;
        origin37:geo_apple_candy.visibility = 0;
        origin38:geo_apricot.visibility = 0;
        origin39:geo_fruit_banana.visibility = 0;
        origin40:geo_fruit_banana.visibility = 0;
        origin41:geo_fruit_banana.visibility = 0;
        origin42:geo_fruit_banana.visibility = 0;
        origin43:geo_fruit_banana.visibility = 0;
        origin44:geo_fruit_pear.visibility = 0;
        origin45:geo_fruit_pear.visibility = 0;
        origin46:geo_fruit_pear.visibility = 0;
        origin47:geo_fruit_pear.visibility = 0;
        origin48:geo_orange.visibility = 0;
        origin49:geo_watermelon.visibility = 0;
        origin50:geo_hamknuckle.visibility = 0;
        origin51:geo_hamknuckle.visibility = 0;
        origin52:geo_jar_jelly_apricot.visibility = 0;
        origin53:geo_jar_jelly_apricot.visibility = 0;
        origin54:geo_jar_jelly_blueberry.visibility = 0;
        origin55:geo_jar_jelly_blueberry.visibility = 0;
        origin56:geo_jar_jelly_blueberry.visibility = 0;
        origin57:geo_jar_jelly_blueberry.visibility = 0;
        origin58:geo_jar_jelly_strawberry.visibility = 0;
        origin59:geo_kitchenflamby.visibility = 0;
        origin60:geo_kitchenflamby.visibility = 0;
        origin61:geo_kitchenmilkbottle.visibility = 0;
        origin62:geo_kitchenmilkbottle.visibility = 0;
        origin63:geo_kitchenmilkbottle.visibility = 0;
        origin64:geo_kitchensodacan.visibility = 0;
        origin65:geo_kitchensodacan.visibility = 0;
        origin66:geo_lettuce.visibility = 0;
        origin67:geo_lettuce.visibility = 0;
        origin68:geo_box_cocktail.visibility = 0;
        origin69:geo_box_cocktail.visibility = 0;
        origin70:geo_noodle_box.visibility = 0;
        origin71:geo_noodle_box.visibility = 0;
        origin72:geo_salami.visibility = 0;
        origin73:geo_salami.visibility = 0;
        origin74:geo_salami.visibility = 0;
        origin75:geo_salami.visibility = 0;
        origin76:geo_broccoli_branch.visibility = 0;
        origin77:geo_veggiegarlic.visibility = 0;
        origin78:geo_veggiegarlic.visibility = 0;
        origin79:geo_veggiegarlic.visibility = 0;
        origin80:geo_onions_cuisine.visibility = 0;
        origin81:geo_poivron_vert_cuisine.visibility = 0;
        origin82:geo_poivron_vert_cuisine.visibility = 0;
        origin83:geo_chili_pepper_jar.visibility = 0;
