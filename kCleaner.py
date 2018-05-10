# ----------------------------------------------------------------------
# functions clean
# Author : Maxime.Terray
# Date   : avril 2018
# Ver    : xxx
# felixlechA.com | f.rault
# ----------------------------------------------------------------------
import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import os


class kCleaner():
    def __init__(self):
        self.initPath()
        self.cleanerUI()

    # ----------------------------------------------------------------------
    def cleanerUI(self):

        '''path_list = os.path.realpath(__file__).split('/')[:-1]
        path_list.extend(['icons'])
        target = ''
        for item in path_list:
            target += item + '/'
            '''

        allButtons = [("delNameSpace32.png", self.nameSpace_removeAll, "Remove all nameSpace in current scene"),
                      ("delUnusedNode32.png", self.unknowNodes_remove, "Remove unknow noReferenced nodes"),
                      ("del_curve32.png", self.unused_animCurve_remove, "Remove unused noReferenced animCurves"),
                      ("deleteHyperView32.png", self.unused_hyperView_remove, "Remove unused hyperView, hyperLayout"),
                      ("del_fosterParent32.png", self.fosterParent_remove, "Remove all fosterParent in scene"),
                      ("delGhostMesh32.png", self.ghostMesh_remove,"Remove all mesh intermediate shape connected to nothing"),
                      ("delTurtle32.png", self.turtleNode_remove, "Remove 4 turtle nodes in scene"),
                      ("delUnusedNode32.png", self.delUnknowNodes, "Delete unknow nodes on hyperShade"),
                      ("selNgones32.png", self.kmExeNgones, "Isolate objects with ngones, and create a Set")]
        # ("separateHor","no"),("cleaner32", self.cleanAll)

        self.nbBtn = len(allButtons)
        self.widthWin = self.nbBtn * 32 + 50
        # print ">> Size : ", self.widthWin

        windowName = "kCleaner"

        if mc.window(windowName, q=True, exists=True):
            mc.deleteUI(windowName)

        self.myWindow = mc.window(windowName, sizeable=False, toolbox=True, titleBar=True, minimizeButton=False,
                                  maximizeButton=False)
        mc.window(self.myWindow, width=self.widthWin - 2, height=40, edit=True)

        mc.rowLayout(numberOfColumns=self.nbBtn + 2)
        # mc.frameLayout(labelVisible=0, borderVisible=0)
        # mc.shelfLayout(windowName, style="iconOnly", cellWidthHeight=[32, 32], height=38, width=self.widthWin)

        for btn in allButtons:
            mc.iconTextButton(image=self.target + btn[0], command=btn[1], annotation=btn[2])

        mc.iconTextButton(image1=self.target + "separateHor.png", disabledImage=self.target + "separateHor.png",
                          width=9, enable=0)
        mc.iconTextButton(image1=self.target + "cleanAll32.png", command=self.cleanAll, annotation="Clean All")

        mc.showWindow(self.myWindow)

    def initPath(self):
        # self.target = "/homes/mte/maya/2016/scripts/kTools/icons/"
        path_brut = os.path.realpath(__file__)
        print ">> path brut : ", path_brut
        path_norm = os.path.normpath(path_brut)  # os.path.normcase()
        print ">> path norm : ", path_norm
        path_clean = path_norm.replace("\\", "/")
        print ">> path clean : ", path_clean
        path_list = path_clean.split('/')[:-1]
        print ">> path split : ", path_list
        path_list.extend(['icons'])
        self.target = ''
        for item in path_list:
            self.target += item + '/'
        print ">> :", self.target

    # ----------------------------------------------------------------------
    def nameSpace_removeAll(self):
        '''
        Remove all nameSpace in current scene

        :return: none
        '''
        # --- Get all assembly in current scene
        assembly_all = mc.ls(type='assemblyReference') or list()

        # --- Get assembly nameSpace
        ns_to_skip = ['UI', 'shared']

        for ass in assembly_all:
            ass_ns = mc.getAttr(ass + '.repNamespace')

            if not ass_ns in ns_to_skip:
                ns_to_skip.append(ass_ns)

        # --- Get All NameSpace
        nameSpace = mc.namespaceInfo(':', lon=True, recurse=True)
        nameSpace.reverse()

        # --- Delete NameSpace
        nbr = 0
        for ns in nameSpace:
            if not ns.split(':')[-1] in ns_to_skip:
                mc.namespace(removeNamespace=ns, mergeNamespaceWithParent=True)
                nbr = nbr + 1

        if nbr:
            logMsg = str(nbr) + ' nameSpace have been Removed'
        else:
            logMsg = 'no nameSpace to delete'

        print logMsg

    # ----------------------------------------------------------------------
    def unknowNodes_remove(self):
        '''
        Remove unknow noReferenced nodes

        :return: none
        '''
        # --- Get unknow node
        unknown_node = mc.ls(type=['unknown', 'unknownDag', 'unknownTransform'])

        # --- Delete only noReferenced node
        delete_node = list()
        for node in unknown_node:
            if mc.objExists(node):
                if not mc.referenceQuery(node, isNodeReferenced=True):
                    delete_node.append(node)
                    mc.delete(node)

        if delete_node:
            logMsg = str(len(delete_node)) + ' Unknow node deleted :' + ' '.join(delete_node)
        else:
            logMsg = 'no Unknow Referenced Node to delete'

        print logMsg

    # ----------------------------------------------------------------------
    def delUnknowNodes(self):
        pm.mel.hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")
        print 'Unknow nodes deleted'

    # ----------------------------------------------------------------------
    def unused_animCurve_remove(self):
        '''
        Remove unused noReferenced animCurves

        :return: none
        '''
        # --- Get animCurves node
        keys_node = mc.ls(type='animCurve') or list()

        # --- Delete only noReferenced animCurves node
        delete_node = list()
        for key_node in keys_node:
            connections = mc.listConnections(key_node + '.output', s=False, d=True, plugs=True) or list()
            if not mc.referenceQuery(key_node, isNodeReferenced=True) and len(connections) == 0:
                delete_node.append(key_node)
                mc.delete(key_node)

        if delete_node:
            logMsg = str(len(delete_node)) + ' animCurve nodes deleted'
        else:
            logMsg = 'no animCurve nodes to delete'

        print logMsg

    # ----------------------------------------------------------------------
    def unused_hyperView_remove(self):
        '''
        Remove unused hyperView, hyperLayout

        :return: none
        '''
        # --- Get all hyperView in current scene
        hyperViewNodes = mc.ls(type=['hyperView']) or list()

        # - Calculate how mutch hyperView we have
        hyperView_nbr = len(hyperViewNodes)

        # --- Remove hyperView
        if hyperViewNodes:
            mc.delete(hyperViewNodes)
            hyperView = mc.ls(type=['hyperView']) or list()
            logMsg = str(hyperView_nbr - len(hyperView)) + ' hyperView remove'
            print hyperView
        else:
            logMsg = 'no hyperView to delete found'

        print logMsg

    # ----------------------------------------------------------------------
    def useless_scriptNode_remove(self):
        '''
        Remove useless scriptNodes

        :return: none
        '''
        # --- Get all scriptNode in current scene
        scriptNodes = mc.ls(type='script') or list()

        # - Calculate how mutch scriptNode we have
        scriptNodes_nbr = len(scriptNodes)

        # - Keep the sceneConfigurationScriptNode node
        if 'sceneConfigurationScriptNode' in scriptNodes:
            scriptNodes.remove('sceneConfigurationScriptNode')

        # --- Remove useless scriptNode
        if scriptNodes:
            mc.delete(scriptNodes)
            scriptNodes = mc.ls(type='script') or list()
            logMsg = str(scriptNodes_nbr - len(scriptNodes)) + ' scriptNode remove'
        else:
            logMsg = 'no scriptNode to delete found'

        print logMsg

    # ----------------------------------------------------------------------
    def fosterParent_remove(self):
        '''
        Remove all fosterParent in scene

        :return: none
        '''
        fosterParent = mc.ls(type='fosterParent') or list()

        if fosterParent:
            for foster in fosterParent:
                mc.lockNode(foster, lock=False)
                mc.delete(foster)
            logMsg = str(len(fosterParent)) + ' fosterParent remove'
        else:
            logMsg = 'no fosterParent to remove'

        print logMsg

    # ----------------------------------------------------------------------
    def ghostMesh_remove(self):
        '''
        Remove all mesh intermediate shape connected to nothing

        :param mode: Define if command is launch by 'menu' or by 'command'
        :type mode: string

        :return: none
        '''
        allShape = mc.ls(type='mesh', intermediateObjects=True)

        ghostShape = list()
        for item in allShape:
            link = mc.listConnections(item)
            # link= mc.listConnections( item ) or list() //
            if not link:
                ghostShape.append(item)

        if ghostShape:
            mc.delete(ghostShape)
            logMsg = str(len(ghostShape)) + ' ghostShape remove'
        else:
            logMsg = 'no ghostMesh to remove'

        print logMsg

    # ----------------------------------------------------------------------
    def turtleNode_remove(self):
        '''
        Remove 4 turtle node
        '''

        # mc.pluginInfo( query=True, listPlugins=True)
        if mc.pluginInfo("Turtle", loaded=True, q=True):
            pm.mel.ilrClearScene()
            pm.mel.unloadPluginWithCheck("D:/64/Autodesk/Maya2015/bin/plug-ins/Turtle.mll")
        else:
            selectionList = mc.ls(type=['ilrBakeLayer', 'ilrOptionsNode', 'ilrBakeLayerManager', 'ilrUIOptionsNode'])
            if selectionList:
                for item in selectionList:
                    mc.lockNode(item, lock=False)
                    mc.delete(item)
                print len(selectionList), " Turtle nodes DELETED"
            else:
                print "no Turtle Node"

    # ----------------------------------------------------------------------
    def kmExeNgones(self):
        mel.eval(
            'polyCleanupArgList 3 { "0","2","1","0","1","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" };')
        mel.eval('toggleSelMode;')
        # km.toggleIsolateObject()
        allModelPanel = mc.getPanel(type='modelPanel')
        if allModelPanel:
            for modelPanelName in allModelPanel:
                state = mc.isolateSelect(modelPanelName, query=True, state=True)
                if state == 0:
                    if mc.selectMode(q=True, object=True):
                        pm.mel.enableIsolateSelect(modelPanelName, 1)
                    else:
                        mc.selectMode(object=True)
                        pm.mel.enableIsolateSelect(modelPanelName, 1)
                        mc.selectMode(component=True)
                    print ">> Isolate : ON."
                else:
                    pm.mel.enableIsolateSelect(modelPanelName, 0)
                    print ">> Isolate : OFF."
        mc.sets(name="ObjWithNGones")

    # ----------------------------------------------------------------------
    def cleanAll(self):
        self.unknowNodes_remove()
        self.nameSpace_removeAll()
        self.unused_hyperView_remove()
        self.unused_animCurve_remove()
        self.fosterParent_remove()
        self.ghostMesh_remove()
        self.turtleNode_remove()
        self.kmExeNgones()
        # self.delUnknowNodes()


kCleaner()
