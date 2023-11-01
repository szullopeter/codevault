import sys
import fitz
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QMimeData
from PIL import Image
from io import BytesIO
from PyQt5.QtGui import QPixmap

class DragAndDropWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drag and Drop PDF Files')
        self.setGeometry(100, 100, 400, 500)
        self.setLayout(QVBoxLayout())

        self.file_label = QLabel()
        self.pdf_page_label = QLabel()
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clearText)

        self.nav_layout = QHBoxLayout()
        self.prev_button = QPushButton('Previous')
        self.prev_button.clicked.connect(self.showPrevPage)
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.showNextPage)

        self.nav_layout.addWidget(self.prev_button)
        self.nav_layout.addWidget(self.next_button)

        self.layout().addWidget(self.file_label)
        self.layout().addWidget(self.pdf_page_label)
        self.layout().addLayout(self.nav_layout)
        self.layout().addWidget(self.clear_button)

        self.setAcceptDrops(True)
        self.pdf_doc = None
        self.current_page = 0

    def clearText(self):
        self.file_label.setText('')
        self.pdf_page_label.clear()
        self.current_page = 0

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and all(url.toLocalFile().endswith('.pdf') for url in mime_data.urls()):
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        pdf_files = [url.toLocalFile() for url in mime_data.urls() if url.toLocalFile().endswith('.pdf')]

        if pdf_files:
            for pdf_file in pdf_files:
                self.pdf_doc = fitz.open(pdf_file)
                self.displayPage(self.current_page)
                self.file_label.setText(pdf_file)
            event.acceptProposedAction()

    def showPrevPage(self):
        if self.pdf_doc and self.current_page > 0:
            self.current_page -= 1
            self.displayPage(self.current_page)

    def showNextPage(self):
        if self.pdf_doc and self.current_page < self.pdf_doc.page_count - 1:
            self.current_page += 1
            self.displayPage(self.current_page)

    def displayPage(self, page_number):
        if self.pdf_doc:
            page = self.pdf_doc.load_page(page_number)
            pixmap = page.get_pixmap()
            image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            image_bytes = BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(image_bytes.read())
            self.pdf_page_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragAndDropWindow()
    window.show()
    sys.exit(app.exec_())
