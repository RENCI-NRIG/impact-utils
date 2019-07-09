#!/usr/bin/env python

__author__ = "Ilya Baldin"
__version__ = "0.1"
__maintainer__ = "Ilya Baldin"


import pyforms
import uuid

from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlTextArea
from pyforms.controls import ControlFile

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtWidgets

import safe_helper

"""
Displays appropriate forms for a Data Provider/DataSet Owner to issue GUIDs
to workflows and a dataset and register the policy for the dataset with the
associated SAFE server.
"""


class AppGUI(BaseWidget):

    _safe_default_url = 'http://localhost:7777/'

    def __init__(self):
        super(AppGUI, self).__init__('Dataset Policy Registration')

        # form fields
        self._wp1 = ControlText('Research Approval Workflow ID      ')
        self._wp1gen = ControlButton('Generate')
        self._wp2 = ControlText('Infrastructure Approval Workflow ID')
        self._wp2gen = ControlButton('Generate')
        self._ds = ControlText('Dataset ID                         ')
        self._dsgen = ControlButton('Generate')
        self._safeURL = ControlText('SAFE Server URL', default=self._safe_default_url,
                                    helptext='Root URL of the SAFE server')
        self._safePubKeyPath = ControlFile('SAFE Public Key Path')
        self._push = ControlButton('Push Combined Policy to SAFE')
        self._results = ControlTextArea('Outputs')
        self._results.readonly = True
        self._results.autoscroll = True

        # button actions
        self._wp1gen.value = self._getGUIDClosure(self._wp1)
        self._wp2gen.value = self._getGUIDClosure(self._wp2)
        self._dsgen.value = self._getGUIDClosure(self._ds)
        self._push.value = self.__pushToSafe

        # formset layout
        self.formset = [{'B. SAFE Parameters': ['_safeURL', '_safePubKeyPath'],
                        'A. Workflows and Datasets': [('_wp1', '_wp1gen'), ('_wp2', '_wp2gen'), ('_ds', '_dsgen')]},
                        '=',
                        (' ', '_push'), '=', ('_results')]

    def _getGUIDClosure(self, field):
        """ couldn't find a way to determine the field for which the button is pressed """

        def genGUID(self):
            field.value = uuid.uuid4().__str__()

        return genGUID

    @staticmethod
    def _findMainWindow():
        """ find the main window of the app """
        app = QApplication.instance()
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                return widget
        return None

    @staticmethod
    def _resizeWindow():
        win = AppGUI._findMainWindow()
        if win is not None:
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            win.setSizePolicy(sizePolicy)
            win.resize(800, 600)
            #win.show()
        else:
            print("Unable to find main window")

    @staticmethod
    def _warningWindow(message, explain):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error: " + message)
        msg.setInformativeText(explain)
        msg.setWindowTitle("Error")
        msg.exec_()

    def __pushToSafe(self):
        """ post the necessary rules"""

        # hash the pulic key of the principal
        try:
            principal = safe_helper.hashKey(self._safePubKeyPath.value)
        except safe_helper.SafeException as e:
            AppGUI._warningWindow(e.__str__(), "Please use the 'B' tab to fill the parameters")
            return

        if len(self._wp1.value) == 0 or \
                len(self._wp2.value) == 0 or \
                len(self._ds.value) == 0:
            AppGUI._warningWindow("Workflow or Dataset IDs are not unique",
                                  "Please specify or generate unique IDs for workflows "
                                  "and the dataset using the 'A' tab")
            return

        # create complete IDs for WF1, WF2 and DS
        wf1_id = ":".join([principal, self._wp1.value])
        wf2_id = ":".join([principal, self._wp2.value])
        dataset_id = ":".join([principal, self._ds.value])

        try:
            res1 = safe_helper.postRawIdSet(self._safeURL.value, principal)
            res2 = safe_helper.postPerFlowRule(self._safeURL.value, principal, wf1_id)
            res3 = safe_helper.postPerFlowRule(self._safeURL.value, principal, wf2_id)
            res4 = safe_helper.postTwoFlowDataOwnerPolicy(self._safeURL.value, principal, dataset_id, wf1_id, wf2_id)
        except safe_helper.SafeException as e:
            AppGUI._warningWindow(e.__str__(), f"Unable to post to SAFE server {self._safeURL.value}")

        # output the results needed by the user for Notary Service
        self._results.value = f"All policies have been posted to the SAFE server. \
Please take note of the following identifiers for the Notary Service: \n\
Research Approval Workflow ID = {wf1_id}\n\
Infrastructure Approval Workflow ID = {wf2_id}\n\
Dataset ID = {dataset_id}\n\n\n\
For debugging purposes here are SAFE identifiers for posted policies:\n\
postRawIdSet = {res1}\n\
postPerFlowRule (Research Approval) = {res2}\n\
postPerFlowRule (Infrastructure Approval) = {res3}\n\
postTwoFlowDataOwnerPolicy = {res4}"


#Execute the application
if __name__ == "__main__":   pyforms.start_app(AppGUI, geometry=[100, 100, 500, 700])

