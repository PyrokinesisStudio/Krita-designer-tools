import os
from krita import *
from PyQt5.QtWidgets import QFileDialog


class LayerExportSelected():
    def __init__(self):
        pass

    def exportDocument(self):
        document = Krita.instance().activeDocument()
        if not document:
            return
        fileName = QFileDialog.getSaveFileName()[0]
        document.exportImage(fileName, InfoObject())

    def exportSelected(self, parentWidget, fileType='PNG'):
        selectedNodes = Application.activeWindow().activeView().selectedNodes()
        if len(selectedNodes) == 0:
            return

        exportPath = os.path.join('.', 'export')
        if not os.path.exists(exportPath):
            os.makedirs(exportPath)

        for node in selectedNodes:
            fileName = node.name() + ".png"
            path = os.path.join(exportPath, fileName)
            self._exportLayer(node, path)

    def _exportLayer(self, layer, path):
        layerPixelData = layer.projectionPixelData(layer.bounds().x(),
                                            layer.bounds().y(),
                                            layer.bounds().width(),
                                            layer.bounds().height())

        exportDoc = Application.createDocument(layer.bounds().width(),
                                    layer.bounds().height(),
                                    layer.name(), "RGBA", "U8", "", 300.0)
        layerCopy = exportDoc.rootNode().childNodes()[0]
        layerCopy.setPixelData(layerPixelData, 0.0, 0.0,
                            layer.bounds().width(), layer.bounds().height())
        exportDoc.refreshProjection()
        exportDoc.setBatchmode(True)
        exportDoc.saveAs(path)
        exportDoc.close()

    def _askUserDirectory(self, parentWidget):
        dialog = QFileDialog(parentWidget)
        dialog.setFileMode(QFileDialog.Directory)
        # dialog.setDirectory()

        fileName = QFileDialog.getSaveFileName(caption="Select Directory")[0]
        return fileName


# TODO: still a WIP, experimenting with layer hierarchy manipulations
def getSelectedNodes():
    return Application.activeWindow().activeView().selectedNodes()

document = Krita.instance().activeDocument()
rootNode = document.rootNode()

def addToSelectedGroup(nodes):
    activeNode = document.activeNode()
    selectedLayers = [n for n in nodes if n.type != 'grouplayer']
    if not (activeNode.type() == 'grouplayer' and selectedLayers):
        return
    activeNode.setChildNodes(selectedLayers)

# For now, all I get is layers cycling regardless of the list I use in setChildNodes
def moveToTop(node):
    """Move the node to the top of the current parent"""
    parent = node.parentNode()
    nodeList = parent.childNodes()
    index = nodeList.index(node)
    newList = [node].extend([n for n in nodeList if n is not node])
    parent.setChildNodes(nodeList)

document.refreshProjection()
