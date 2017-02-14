# kMax mod tools
# Maxime Terray : kMax
# Remerciements a Sebastien Courtois et a Stephane Hoarau. Cyber Group Studios 
# 04/04/7/2015
# Version 0.2
# Panneau lateral pour Maya 2014
# Regroupant tous les outils de modelisation utiles

import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import os


class kModBar():
    def __init__(self):

        scaleIcon = 30
        scaleSeparator = 12
        #scaleColumn = scaleIcon+2

        #self.target =  "/homes/mte/maya/2016/scripts/kTools/icons/"

        #print ">> 1 :", os.path.realpath(__file__)
        path_nomr = os.path.normcase(os.path.realpath(__file__))    #os.path.normcase()
        path_list = os.path.realpath(path_nomr).split('/')[:-1]
        path_list.extend(['icons'])
        self.target = ''
        if path_list[5] == "2018":
            print ">> : ", path_list, " Version :", path_list[5]
            for item in path_list:
                self.target += item + '/'
        if path_list[4] == "2016":
            print ">> : ", path_list, " Version :", path_list[4]
            for item in path_list:
                self.target += item + '/'
                # target = "/homes/mte/maya/2016/scripts/kTools"

        print ">> :", self.target

        self.nPlane = 1

        window_name = "kWindow"
        dockName = "dockMod"
        toolName = "kMod"

        if mc.window(window_name, q=True, exists=True):
            mc.deleteUI(window_name)

        if mc.dockControl(dockName, q=True, exists=True):
            mc.deleteUI(dockName)
            
        if mc.toolBar(toolName, q=True, exists=True):
            mc.deleteUI(toolName)

        my_window = mc.window(window_name, toolbox=True, resizeToFitChildren=True, titleBar=False)

        modeling = mc.rowColumnLayout(numberOfColumns = 2, columnWidth=[(1,scaleIcon),(2,scaleIcon)])

        bt_plane = mc.iconTextButton(image1=self.target + "polykPlane.png", highlightImage=self.target + "polykPlane.png",
                                  label="Plane", annotation="Create a polygonal plane on the grid",
                                  command=self.kmPlane, doubleClickCommand="pm.mel.CreatePolygonPlaneOptions()", height=scaleIcon)

        bt_planeDisk = mc.iconTextButton(image1=self.target + "polykDisk.png", highlightImage=self.target + "polykDisk.png",
                                      label="Plane", annotation="Create a tuned polygonal plane on the grid",
                                      command=self.kmPlaneDisk, height=scaleIcon)

        bt_cube = mc.iconTextButton(image1=self.target + "polyCube.png", highlightImage=self.target + "polyCube.png",
                                 label="Cube", annotation="Create a polygonal cube on the grid",
                                 command=self.kmPolycube, doubleClickCommand="pm.mel.CreatePolygonCubeOptions()", height=scaleIcon)

        bt_cubeSphere = mc.iconTextButton(image1=self.target + "polykSphere.png", highlightImage=self.target + "polykSphere.png",
                                       label="kSphere", annotation="Create a tuned polygonal cube on the grid",
                                       command=self.kmPolycubeSphere, height=scaleIcon)

        bt_sphere = mc.iconTextButton(image1=self.target + "polySphere.png", highlightImage=self.target + "polySphere.png",
                                   label="Sphere", annotation="Create a polygonal sphere on the grid",
                                   command=self.kmSphere, doubleClickCommand="pm.mel.CreatePolygonSphereOptions()", height=scaleIcon)

        bt_cylinder = mc.iconTextButton(image1=self.target + "polyCylinder.png",
                                     highlightImage=self.target + "polyCylinder.png", label="Cylinder",
                                     annotation="Create a polygonal cylinder on the grid", command=self.kmCylinder,
                                     doubleClickCommand="pm.mel.CreatePolygonCylinderOptions()", height=scaleIcon)

        bt_torus = mc.iconTextButton(image1=self.target + "polyTorus.png", highlightImage=self.target + "polyTorus.png",
                                  label="Torus", annotation="Create a polygonal torus on the grid",
                                  command=self.kmTorus, doubleClickCommand="pm.mel.CreatePolygonTorusOptions()", height=scaleIcon)

        bt_cone = mc.iconTextButton(image1=self.target + "polyCone.png", highlightImage=self.target + "polyCone.png",
                                 label="Cone", annotation="Create a polygonal cone on the grid", command=self.kmCone,
                                 doubleClickCommand="pm.mel.CreatePolygonConeOptions()", height=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                          highlightImage=self.target + "separateHorizontal.png")
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                          highlightImage=self.target + "separateHorizontal.png")

        bt_locator = mc.iconTextButton(image1=self.target + "locator.png", highlightImage=self.target + "locator.png",
                                    label="Locator", annotation="Create a Locator", command=self.kmLocator, height=scaleIcon)


        bt_lattice = mc.iconTextButton(image1=self.target + "lattice.png", highlightImage=self.target + "lattice.png",
                                    label="Lattice", annotation="Create lattice",
                                    command="mc.lattice(divisions=(2, 2, 2), objectCentered=True, ldv=(2, 2, 2))", height=scaleIcon)

        #mc.separator( style='none', height=scaleIcon)
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                                   highlightImage=self.target + "separateHorizontal.png")
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                                   highlightImage=self.target + "separateHorizontal.png")

        bt_extrude = mc.iconTextButton(image1=self.target + "polyExtrudeFacet.png",
                                    highlightImage=self.target + "polyExtrudeFacet.png", label="Extrude",
                                    annotation="Extrude the selected component", command=self.kmExtrude, height=scaleIcon)#"pm.mel.performPolyExtrude(0)")

        bt_duplicateFace = mc.iconTextButton(image1=self.target + "polyDuplicateFacet.png",
									highlightImage=self.target + "polyDuplicateFacet.png", label="DuplicateFace",
									annotation="Duplicate the currently selected faces in a new shell and shows a manipulator to adjust their offset",
                                    command="pm.mel.performPolyChipOff(0,1)", height=scaleIcon)

        bt_extract = mc.iconTextButton(image1=self.target + "polyChipOff.png",
                                    highlightImage=self.target + "polyChipOff.png", label="Extract",
                                    annotation="Extract the currently selected faces from their shell and shows a manipulator to adjust their offset",
                                    command="pm.mel.performPolyChipOff(0,0)", height=scaleIcon)

        bt_mirrorOption = mc.iconTextButton(image1=self.target + "polyMirrorGeometry.png",
                                    highlightImage=self.target + "polyMirrorGeometry.png", label="Poly Mirror Options",
                                    annotation="Mirror Geometry",
                                    command="pm.mel.MirrorPolygonGeometryOptions()", height=scaleIcon)

        #mc.separator(style='none', height=scaleIcon)

        bt_separate = mc.iconTextButton(image1=self.target + "polySeparate.png",
                                    highlightImage=self.target + "polySeparate.png",
									label="Separate",
                                    annotation="Separate the selected polygon object shells or the shells of any selected faces from the object into distinct objects",
                                    command="pm.mel.SeparatePolygon()", height=scaleIcon)

        bt_combine = mc.iconTextButton(image1=self.target + "polyUnite.png",
									highlightImage=self.target + "polyUnite.png",
                                    label="Combine",
                                    annotation="Combine the selected polygon objects into one single object to allow operations such as merges or face trims",
                                    command="pm.mel.polyUnite()", height=scaleIcon)

        # bt_mergeEdge = mc.iconTextButton(image1="polyMergeEdge.png", label="MergeEdge", annotation="Merge the two selected border edges, if topologically possible", command="pm.mel.MergeEdgeTool()")

        bt_mergeVertexTool = mc.iconTextButton(image1="polyMergeVertex.png",
									highlightImage="polyMergeVertex.png",
									label="MergeVertexTool",
									annotation="Interactively select and merge vertices",
									command="pm.mel.MergeVertexTool()",
									doubleClickCommand="pm.mel.MergeVertexToolOptions()", height=scaleIcon)

        bt_mergeVertex = mc.iconTextButton(image1=self.target + "polyMerge.png", 
									highlightImage=self.target + "polyMerge.png",
									label="MergeVertex",
									annotation="Merge vertices / border edges based on selection",
									command="pm.mel.performPolyMerge(0)",
									doubleClickCommand="pm.mel.PolyMergeOptions()", height=scaleIcon)

        bt_collapse = mc.iconTextButton(image1=self.target + "polyCollapseEdge.png",
                                     highlightImage=self.target + "polyCollapseEdge.png", label="Collapse",
                                     annotation="Collapse the selected edges or faces",
                                     command="pm.mel.performPolyCollapse(0)", height=scaleIcon)

        bt_deleteVertexEdges = mc.iconTextButton(image1=self.target + "polyDelEdgeVertex.png",
                                              highlightImage=self.target + "polyDelEdgeVertex.png",
                                              label="DeleteVertexEdges",
                                              annotation="Delete the selected Vertices / Edges",
                                              command="pm.mel.performPolyDeleteElements()", height=scaleIcon)

        bt_splitPolygon = mc.iconTextButton(image1=self.target + "multicutnex.png",
                                         highlightImage=self.target + "multicutnex.png", label="SplitFace",
                                         annotation="Split polygon", command=self.multiCut,
                                         doubleClickCommand="pm.mel.InteractiveSplitTool()", height=scaleIcon)

        #CutPolygon cut face

        bt_connectComponents = mc.iconTextButton(image1=self.target + "polyConnectComponents.png",
                                              highlightImage=self.target + "polyConnectComponents.png", label="Connect",
                                              annotation="Connect components", command="pm.mel.ConnectComponents()", height=scaleIcon)

        bt_duplicateEdge = mc.iconTextButton(image1=self.target + "splitEdge.png", highlightImage=self.target + "splitEdgeC.png",
                                          label="DuplicateEdge", annotation="Duplicate edges",
                                          command="pm.modeling.polyDuplicateEdge(pm.ls(selection=True), of=0.5, aef=1.0)", height=scaleIcon)

        bt_insertEdgeLoop = mc.iconTextButton(image1=self.target + "polySplitEdgeRing.png",
                                           highlightImage=self.target + "polySplitEdgeRing.png", label="InsertEdge",
                                           annotation="Insert edge loop", command="pm.mel.SplitEdgeRingTool()", height=scaleIcon)

        bt_slideEdge = mc.iconTextButton(image1=self.target + "slideEdgeTool.png", highlightImage=self.target + "slideEdgeTool.png",
                                      label="SlideEdge", annotation="Slide edge tool", command="pm.mel.SlideEdgeTool()",
                                      doubleClickCommand="pm.mel.SlideEdgeToolOptions()", height=scaleIcon)

        bt_offsetEdgeLoop = mc.iconTextButton(image1=self.target + "polyDuplicateEdgeLoop.png",
                                           highlightImage=self.target + "polyDuplicateEdgeLoop.png", label="OffsetEdge",
                                           annotation="Offset edge loop", command="pm.mel.performPolyDuplicateEdge(0)",
                                           doubleClickCommand="pm.mel.DuplicateEdgesOptions()", height=scaleIcon)

        bt_bevel = mc.iconTextButton(image1=self.target + "polyBevel.png", highlightImage=self.target + "polyBevel.png",
                                  label="Bevel", annotation="Bevel selected edges",
                                  command="pm.mel.polyBevel(offset=0.5, offsetAsFraction=1, autoFit=1, segments=1, worldSpace=1, uvAssignment=1, fillNgons=1, mergeVertices=1, mergeVertexTolerance=0.0001, smoothingAngle=30, miteringAngle=180, angleTolerance=180)",
                                  doubleClickCommand="pm.mel.BevelPolygonOptions()", height=scaleIcon)

        mc.separator(style='none', height=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                          highlightImage=self.target + "separateHorizontal.png")
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                          highlightImage=self.target + "separateHorizontal.png")

        bt_bridge = mc.iconTextButton(image1=self.target + "polyBridge.png", highlightImage=self.target + "polyBridge.png",
                                   label="Bridge", annotation="Create a bridge between two sets of edges or faces",
                                   command="mc.polyBridgeEdge(divisions=0)",
                                   doubleClickCommand="pm.mel.BridgeEdgeOptions()", height=scaleIcon)

        bt_appendPolygon = mc.iconTextButton(image1=self.target + "polyAppendFacet.png",
                                          highlightImage=self.target + "polyAppendFacet.png", label="Append",
                                          annotation="Select border edges to append a face to the selected shell",
                                          command="pm.mel.setToolTo('polyAppendFacetContext')", height=scaleIcon)

        bt_fillHole = mc.iconTextButton(image1=self.target + "polyCloseBorder.png",
                                     highlightImage=self.target + "polyCloseBorder.png", label="Fill",
                                     annotation="Create a face filling the hole around the selected border edge(s)",
                                     command="pm.mel.FillHole()", height=scaleIcon)

        mc.separator( style='none', height=scaleIcon)
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                                   highlightImage=self.target + "separateHorizontal.png")
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                                   highlightImage=self.target + "separateHorizontal.png")
        
        bt_smooth = mc.iconTextButton(image1=self.target + "polySmooth.png", highlightImage=self.target + "polySmooth.png",
                                   label="Smooth", annotation="Smooth mesh", command=self.kmSmooth,
                                   doubleClickCommand="pm.mel.SmoothPolygonOptions()", height=scaleIcon)

        bt_reduce = mc.iconTextButton(image1=self.target + "polyReduce.png", highlightImage=self.target + "polyReduce.png",
                                   label="Reduce", annotation="Reduce Polygon", command=self.kmReduce,
                                   doubleClickCommand="pm.mel.ReducePolygonOptions()", height=scaleIcon)

        bt_sculpt = mc.iconTextButton(image1=self.target + "putty.png", highlightImage=self.target + "putty.png",
                                   label="Sculpt", annotation="Sculpt a geometry object",
                                   command="pm.mel.SculptGeometryTool()",
                                   doubleClickCommand="pm.mel.SculptGeometryToolOptions()", height=scaleIcon)

        bt_transform = mc.iconTextButton(image1=self.target + "polyMoveVertex.png",
                                      highlightImage=self.target + "polyMoveVertex.png", label="Transform",
                                      annotation="Transform (Scale, Rotate, Translate...) the selected components (Vertices, Edges or Faces). UVs are moved in the UV Texture Editor",
                                      command="pm.mel.performPolyMove('',0)", height=scaleIcon)

        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                                   highlightImage=self.target + "separateHorizontal.png")
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                                   highlightImage=self.target + "separateHorizontal.png")

        bt_softEdge30 = mc.iconTextButton(image1=self.target + "polyNormalSetAngle.png",
                                       highlightImage=self.target + "polyNormalSetAngle.png", label="NormalAngle",
                                       annotation="Set the soft/hard threshold angles for edge normals",
                                       command=self.kmSoftEdge30, height=scaleIcon)

        bt_setToFace = mc.iconTextButton(image1=self.target + "polyNormalSetToFace.png", highlightImage=self.target + "polyNormalSetToFace.png",
                                      label="Set to face", annotation="Set to face", command=self.kmSetToFace, height=scaleIcon)

        bt_softEdge180 = mc.iconTextButton(image1=self.target + "polySoftEdge.png", highlightImage=self.target + "polySoftEdge.png",
                                        label="SoftEdge",
                                        annotation="Set the soft/hard threshold angles for edge normals",
                                        command=self.kmSoftEdge180, height=scaleIcon)

        bt_kmSoftEdge0 = mc.iconTextButton(image1=self.target + "polyHardEdge.png",
                                        highlightImage=self.target + "polyHardEdge.png",
                                        label="Set to face", annotation="Set to face", command=self.kmSoftEdge0, height=scaleIcon)

        bt_reverse = mc.iconTextButton(image1=self.target + "polyNormal.png", highlightImage=self.target + "polyNormal.png",
                                    label="ReverseNormal", annotation="Reverse the normals of the selected faces",
                                    command=self.kmReverseNormal,
                                    doubleClickCommand="pm.mel.ReversePolygonNormalsOptions()", height=scaleIcon)

        mc.separator( style='none', height=scaleIcon)
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                                   highlightImage=self.target + "separateHorizontal.png")
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                                   highlightImage=self.target + "separateHorizontal.png")
                                   
        bt_instObj = mc.iconTextButton(image1=self.target + "instanceToObject.png",
                                    highlightImage=self.target + "instanceToObject.png", label="InstanceToObject",
                                    annotation="Convert selected instance(s) to object(s)",
                                    command="pm.mel.ConvertInstanceToObject()", height=scaleIcon)

        bt_edgeToCurve = mc.iconTextButton(image1=self.target + "polyEdgeToCurve.png",
                                       highlightImage=self.target + "polyEdgeToCurve.png", label="EdgeToCurve",
                                       annotation="Convert selected edges to curve",
                                       command="pm.mel.CreateCurveFromPoly()", height=scaleIcon)

        # mc.setParent('..') pour le shelfTabLayout

        #mc.separator( style='none', height=scaleIcon)
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=9, enable=0,
                                   highlightImage=self.target + "separateHorizontal.png")
        mc.iconTextButton(image1=self.target + "separateHorizontal.png", width=scaleIcon, height=scaleSeparator, enable=0,
                          highlightImage=self.target + "separateHorizontal.png")

        #my_dock = mc.dockControl(dockName, label="", area='left', content=my_window, allowedArea=['right', 'left'],
                                 #sizeable=False, width=2*scaleColumn+2) #label="kMod",
        allowedAreas = ['left', 'right']                         
        myTool = mc.toolBar(toolName, area='left', content=my_window, allowedArea=allowedAreas)

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
        #pm.mel.SplitPolygonTool()
        mel.eval("SplitPolygonTool()")
        # dR_multiCutTool() 2016

    def kmExtrude(self):
        #pm.mel.performPolyExtrude(0)
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
                mc.polyReduce(obj, version=1, termination=0, percentage=50, sharpness=0, preserveTopology=1, keepQuadsWeight=1,
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

    def kmSetToFace(selfself):
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

kModBar()
