from PyQt5.QtWidgets import QApplication
from interface import SynchroEditorUI

if __name__ == "__main__":
	app = QApplication([])
	window = SynchroEditorUI()
	app.exec()