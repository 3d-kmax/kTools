import maya.cmds as mc

# Create a new regular outliner in its own window
mc.window(title="Outliner", toolbox=True)
mc.frameLayout(labelVisible=False, width=300, height=500)
panel = mc.outlinerPanel()
outliner = mc.outlinerPanel(panel, query=True, outlinerEditor=True)
mc.outlinerEditor(outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList',
                  showShapes=False, showReferenceNodes=False, showReferenceMembers=False, showAttributes=False,
                  showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True,
                  ignoreDagHierarchy=False, expandConnections=False, showNamespace=True, showCompounds=True,
                  showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False,
                  doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True,
                  setFilter='defaultSetFilter')
mc.showWindow()