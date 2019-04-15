import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm
import os


class KMod():
    path = "E:/kTools/icons/"
    iconSize = 28
    separatorSize = 12
    wscName = "kMod"

    @classmethod
    def buildUI(cls):
        mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, cls.iconSize), (2, cls.iconSize)], rowSpacing=(1, 2),
                           columnSpacing=(2, 2), width=2 * cls.iconSize + 2)

        allButtons = [("bt_plane", "polykPlane.png", "polykPlane.png", "Plane", "Create a polygonal plane on the grid",
                       'KMod().kmPlane()', "pm.mel.CreatePolygonPlaneOptions()"),
                      ("bt_planeDisk", "polykDisk.png", "polykDisk.png", "Plane",
                       "Create a tuned polygonal plane on the grid", 'KMod().kmPlaneDisk()', ""),
                      ("bt_cube", "polyCube.png", "polyCube.png", "Cube", "Create a polygonal cube on the grid",
                       'KMod().kmPolycube()', "pm.mel.CreatePolygonCubeOptions()"),
                      ("bt_cubeSphere", "polykSphere.png", "polykSphere.png", "kSphere",
                       "Create a tuned polygonal cube on the grid", 'KMod().kmPolycubeSphere()', ""),
                      ("bt_sphere", "polySphere.png", "polySphere.png", "Sphere",
                       "Create a polygonal sphere on the grid", 'KMod().kmSphere()', "pm.mel.CreatePolygonSphereOptions()"),
                      ("bt_cylinder", "polyCylinder.png", "polyCylinder.png", "Cylinder",
                       "Create a polygonal cylinder on the grid", 'KMod().kmCylinder()',
                       "pm.mel.CreatePolygonCylinderOptions()"),
                      ("bt_torus", "polyTorus.png", "polyTorus.png", "Torus", "Create a polygonal torus on the grid",
                       'KMod().kmTorus()', "pm.mel.CreatePolygonTorusOptions()"),
                      ("bt_cone", "polyCone.png", "polyCone.png", "Cone", "Create a polygonal cone on the grid",
                       'KMod().kmCone()', "pm.mel.CreatePolygonConeOptions()"),
                      ("bt_separator_01", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_separator_02", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_locator", "locator.png", "locator.png", "Locator", "Create a Locator", 'KMod().kmLocator()', ""),
                      ("bt_lattice", "lattice.png", "lattice.png", "Lattice", "Create lattice",
                       "mc.lattice(divisions=(2, 2, 2), objectCentered=True, ldv=(2, 2, 2))", ""),
                      ("bt_separator_03", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_separator_04", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_extrude", "polyExtrudeFacet.png", "polyExtrudeFacet.png", "Extrude",
                       "Extrude the selected component", 'KMod().kmExtrude()', "pm.mel.performPolyExtrude(0)"),
                      ("bt_duplicateFace", "polyDuplicateFacet.png", "polyDuplicateFacet.png", "DuplicateFace",
                       "Duplicate the currently selected faces in a new shell", "pm.mel.performPolyChipOff(0,1)", ""),
                      ("bt_extract", "polyChipOff.png", "polyChipOff.png", "Extract",
                       "Extract the currently selected faces from their shell", "pm.mel.performPolyChipOff(0,0)", ""),
                      ("bt_mirrorOption", "polyMirrorGeometry.png", "polyMirrorGeometry.png", "Poly Mirror Options",
                       "Mirror Geometry", "pm.mel.MirrorPolygonGeometryOptions()", ""),
                      ("bt_separate", "polySeparate.png", "polySeparate.png", "Separate",
                       "Separate the selected polygon object shells or the shells of any selected faces from the object into distinct objects",
                       "pm.mel.SeparatePolygon()", ""),
                      ("bt_combine", "polyUnite.png", "polyUnite.png", "Combine",
                       "Combine the selected polygon objects into one single object to allow operations such as merges or face trims",
                       "pm.mel.polyUnite()", ""),
                      ("bt_mergeVertexTool", "polyMergeVertex.png", "polyMergeVertex.png", "MergeVertexTool",
                       "Interactively select and merge vertices", "pm.mel.MergeVertexTool()",
                       "pm.mel.MergeVertexToolOptions()"),
                      ("bt_mergeVertex", "polyMerge.png", "polyMerge.png", "MergeVertex",
                       "Merge vertices / border edges based on selection", "pm.mel.performPolyMerge(0)",
                       "pm.mel.PolyMergeOptions()"),
                      ("bt_collapse", "polyCollapseEdge.png", "polyCollapseEdge.png", "Collapse",
                       "Collapse the selected edges or faces", "pm.mel.performPolyCollapse(0)", ""),
                      ("bt_deleteVertexEdges", "polyDelEdgeVertex.png", "polyDelEdgeVertex.png", "DeleteVertexEdges",
                       "Delete the selected Vertices / Edges", "pm.mel.performPolyDeleteElements()", ""),
                      ("bt_splitPolygon", "multicutnex.png", "multicutnex.png", "SplitFace", "Split polygon",
                       'KMod().multiCut()', "pm.mel.InteractiveSplitTool()"),
                      ("bt_connectComponents", "polyConnectComponents.png", "polyConnectComponents.png", "Connect",
                       "Connect components", "pm.mel.ConnectComponents()", ""),
                      ("bt_duplicateEdge", "splitEdge.png", "splitEdge.png", "DuplicateEdge", "Duplicate edges",
                       "pm.modeling.polyDuplicateEdge(pm.ls(selection=True), of=0.5, aef=1.0)", ""),
                      ("bt_insertEdgeLoop", "polySplitEdgeRing.png", "polySplitEdgeRing.png", "InsertEdge",
                       "Insert edge loop", "pm.mel.SplitEdgeRingTool()", ""),
                      ("bt_slideEdge", "slideEdgeTool.png", "slideEdgeTool.png", "SlideEdge", "Slide edge tool",
                       "pm.mel.SlideEdgeTool()", "pm.mel.SlideEdgeToolOptions()"),
                      ("bt_offsetEdgeLoop", "polyDuplicateEdgeLoop.png", "polyDuplicateEdgeLoop.png", "OffsetEdge",
                       "Offset edge loop", "pm.mel.performPolyDuplicateEdge(0)", "pm.mel.DuplicateEdgesOptions()"),
                      ("bt_bevel", "polyBevel.png", "polyBevel.png", "Bevel", "Bevel selected edges",
                       "pm.mel.polyBevel(offset=0.5, offsetAsFraction=1, autoFit=1, segments=1, worldSpace=1, uvAssignment=1, fillNgons=1, mergeVertices=1, mergeVertexTolerance=0.0001, smoothingAngle=30, miteringAngle=180, angleTolerance=180)",
                       "pm.mel.BevelPolygonOptions()",),
                      ("bt_empty_00", "", "", "", "", "", ""),
                      ("bt_separator_05", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_separator_06", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_bridge", "polyBridge.png", "polyBridge.png", "Bridge",
                       "Create a bridge between two sets of edges or faces", "mc.polyBridgeEdge(divisions=0)",
                       "pm.mel.BridgeEdgeOptions()"),
                      ("bt_appendPolygon", "polyAppendFacet.png", "polyAppendFacet.png", "Append",
                       "Select border edges to append a face to the selected shell",
                       "pm.mel.setToolTo('polyAppendFacetContext')", ""),
                      ("bt_fillHole", "polyCloseBorder.png", "polyCloseBorder.png", "Fill",
                       "Create a face filling the hole around the selected border edge(s)", "pm.mel.FillHole()", ""),
                      ("bt_empty_00", "", "", "", "", "", ""),
                      ("bt_separator_07", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_separator_08", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_smooth", "polySmooth.png", "polySmooth.png", "Smooth", "Smooth mesh", 'KMod().kmSmooth()',
                       "pm.mel.SmoothPolygonOptions()"),
                      ("bt_reduce", "polyReduce.png", "polyReduce.png", "Reduce", "Reduce Polygon", 'KMod().kmReduce()',
                       "pm.mel.ReducePolygonOptions()"),
                      ("bt_sculpt", "putty.png", "putty.png", "Sculpt", "Sculpt a geometry object",
                       "pm.mel.SculptGeometryTool()", "pm.mel.SculptGeometryToolOptions()",),
                      ("bt_transform", "polyMoveVertex.png", "polyMoveVertex.png", "Transform",
                       "Transform (Scale, Rotate, Translate...) the selected components (Vertices, Edges or Faces). UVs are moved in the UV Texture Editor",
                       "pm.mel.performPolyMove('',0)", ""),
                      ("bt_separator_09", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_separator_10", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_softEdge30", "polyNormalSetAngle.png", "polyNormalSetAngle.png", "NormalAngle",
                       "Set the soft/hard threshold angles for edge normals", 'KMod().kmSoftEdge30()', ""),
                      ("bt_setToFace", "polyNormalSetToFace.png", "polyNormalSetToFace.png", "Set to face",
                       "Set to face", 'KMod().kmSetToFace()', ""),
                      ("bt_softEdge180", "polySoftEdge.png", "polySoftEdge.png", "SoftEdge",
                       "Set the soft/hard threshold angles for edge normals", 'KMod().kmSoftEdge180()', ""),
                      ("bt_kmSoftEdge0", "polyHardEdge.png", "polyHardEdge.png", "Set to face", "Set to face",
                       'KMod().kmSoftEdge0()', ""),
                      ("bt_reverse", "polyNormal.png", "polyNormal.png", "ReverseNormal",
                       "Reverse the normals of the selected faces", 'KMod().kmReverseNormal()',
                       "pm.mel.ReversePolygonNormalsOptions()",),
                      ("bt_empty_00", "", "", "", "", "", ""),
                      ("bt_separator_11", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_separator_12", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_instObj", "instanceToObject.png", "instanceToObject.png", "InstanceToObject",
                       "Convert selected instance(s) to object(s)", "pm.mel.ConvertInstanceToObject()", ""),
                      ("bt_edgeToCurve", "polyEdgeToCurve.png", "polyEdgeToCurve.png", "EdgeToCurve",
                       "Convert selected edges to curve", "pm.mel.CreateCurveFromPoly()", ""),
                      ("bt_separator_13", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", ""),
                      ("bt_separator_14", "separateHorizontal.png", "separateHorizontal.png", "Separator", "", "", "")]

        mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, cls.iconSize), (2, cls.iconSize)], rowSpacing=(1, 2),
                           columnSpacing=(2, 2), width=2 * cls.iconSize + 2)

        for btnName, imgFileName, imgHltFileName, btnLabel, btnAnnotation, btnCommand, btnDoubleClic in allButtons:

            if btnName == "bt_empty_00":
                mc.separator(style='none', height=cls.iconSize)

            else:
                btnName = mc.iconTextButton(image1=cls.path + imgFileName,
                                            highlightImage=cls.path + imgHltFileName,
                                            label=btnLabel, annotation=btnAnnotation,
                                            command=btnCommand,
                                            doubleClickCommand=btnDoubleClic,
                                            height=cls.iconSize)

            if imgFileName == "separateHorizontal.png":
                mc.iconTextButton(btnName, edit=True, height=cls.separatorSize, enable=0)

    def launch(self):
        if mc.workspaceControl(self.wscName, query=True, exists=True):
            mc.workspaceControl(self.wscName, edit=True, close=True)
            try:
                mc.deleteUI(self.wscName, control=True)
            except:
                pass

        mc.workspaceControl(self.wscName, uiScript="KMod.buildUI()", floating=False, retain=False)
        mc.workspaceControl(self.wscName, edit=True, minimumWidth=58)
        mc.workspaceControl(self.wscName, edit=True, resizeWidth=58)
        mc.workspaceControl(self.wscName, edit=True, tabPosition = ("west", 1))
        mc.workspaceControl(self.wscName, edit=True, dockToControl=("Outliner", "left"))
        #print ">> width = ", mc.workspaceControl(self.wscName, query=True, width=True)
        mc.workspaceControl("ToolBox", edit=True, visible=False)

    def kmPlane(self):
        mc.polyPlane(w=10, h=10, sx=2, sy=2, ax=[0, 1, 0], cuv=2, ch=1)

    def kmPlaneDisk(self):
        myPlane = mc.polyPlane(w=10, h=10, sx=1, sy=1, ax=[0, 1, 0], cuv=2, ch=1)
        mc.polySmooth(myPlane, method=1)
        mc.select(myPlane)

    def kmPolycube(self):
        mc.polyCube(w=10, h=10, d=10, sx=2, sy=2, sz=2, ax=[0, 1, 0], cuv=4, ch=1)

    def kmPolycubeSphere(self):
        myCube = mc.polyCube(w=10, h=10, d=10, sx=1, sy=1, sz=1, ax=[0, 1, 0], cuv=4, ch=1)
        mc.polySmooth(myCube, method=1)
        mc.select(myCube)

    def kmSphere(self):
        mc.polySphere(r=10, sx=8, sy=6, ax=[0, 1, 0], cuv=2, ch=1)

    def kmCylinder(self):
        mc.polyCylinder(r=10, h=20, sx=8, sy=1, sz=1, ax=[0, 1, 0], rcp=0, cuv=3, ch=1)

    def kmTorus(self):
        mc.polyTorus(r=6, sr=3, tw=0, sx=8, sy=8, ax=[0, 1, 0], cuv=1, ch=1)

    def kmCone(self):
        mc.polyCone(r=5, h=10, sx=8, sy=1, sz=1, ax=[0, 1, 0], rcp=0, cuv=3, ch=1)

    def kmLocator(self):
        mc.spaceLocator()

    def multiCut(self):
        # pm.mel.SplitPolygonTool()
        mel.eval("SplitPolygonTool()")
        # dR_multiCutTool() 2016

    def kmExtrude(self):
        # pm.mel.performPolyExtrude(0)
        mel.eval("performPolyExtrude(0)")

    def kmSmooth(self):
        selectionList = mc.ls(selection=True)
        if selectionList:
            for obj in selectionList:
                mc.polySmooth(obj, divisions=1, continuity=1, keepBorder=0)
        else:
            print ">> No selection"

    def kmReduce(self):
        selectionList = mc.ls(selection=True)
        if selectionList:
            for obj in selectionList:
                mc.polyReduce(obj, version=1, termination=0, percentage=50, sharpness=0, preserveTopology=1,
                              keepQuadsWeight=1,
                              cachingReduce=1)
        else:
            print ">> No selection"

    def kmSoftEdge180(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polySoftEdge(obj, angle=180)
            sel = mc.select(selectionList)
        else:
            print ">> No selection"

    def kmSetToFace(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polySetToFaceNormal()
            sel = mc.select(selectionList)
        else:
            print ">> No selection"

    def kmSoftEdge30(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polySoftEdge(obj, angle=30)
            sel = mc.select(selectionList)
        else:
            print ">> No selection"

    def kmSoftEdge0(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polySoftEdge(obj, angle=0)
            sel = mc.select(selectionList)
        else:
            print ">> No selection"

    def kmReverseNormal(self):
        selectionList = mc.ls(selection=True, type='transform')
        if selectionList:
            for obj in selectionList:
                mc.polyNormal(obj, normalMode=0)
            sel = mc.select(selectionList)
        else:
            print ">> No selection"


KMod().launch()


'''
dockToPanel("outlinerPanel2","left",-1)
mc.workspaceControl(wscName, edit=True, minimumWidth=58, widthProperty="fixed")
mc.workspaceControl(wscName, edit=True, resizeWidth=58)#, widthProperty="free")#dockToControl=("Outliner","left"))
print ">> width = ", mc.workspaceControl(self.wscName, query=True, width=True)
print ">> width Min = ", mc.workspaceControl(wscName, query=True, minimumWidth=True)
'''
