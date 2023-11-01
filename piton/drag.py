import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QMimeData

class DragAndDropWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drag and Drop Text Files')
        self.setGeometry(100, 100, 300, 200)
        self.setLayout(QVBoxLayout())

        self.file_label = QLabel()
        self.text_label = QLabel()
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clearText)

        self.layout().addWidget(self.file_label)
        self.layout().addWidget(self.text_label)
        self.layout().addWidget(self.clear_button)

        self.setAcceptDrops(True)

    def clearText(self):
        self.file_label.setText('')
        self.text_label.setText('')

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and all(url.toLocalFile().endswith('.txt') for url in mime_data.urls()):
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        txt_files = [url.toLocalFile() for url in mime_data.urls() if url.toLocalFile().endswith('.txt')]

        if txt_files:
            for txt_file in txt_files:
                with open(txt_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.file_label.setText(txt_file)
                    self.text_label.setText(content)
            event.acceptProposedAction()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragAndDropWindow()
    window.show()
    sys.exit(app.exec_())
