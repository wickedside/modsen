import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidget, QMessageBox
from ImageRecognition.image_processing.load_images import load_images_from_folder
from ImageRecognition.utils.find_duplicates import find_duplicates
from ImageRecognition.image_processing.display import display_duplicates

STYLESHEET = """
    QMainWindow {
        background-color: #2e3440;
    }
    QLabel {
        color: #d8dee9;
        font-size: 14pt;
    }
    QPushButton {
        background-color: #4c566a;
        color: #d8dee9;
        border: 1px solid #d8dee9;
        border-radius: 5px;
        padding: 10px;
        font-size: 14pt;
    }
    QPushButton:hover {
        background-color: #5e81ac;
    }
    QPushButton:pressed {
        background-color: #81a1c1;
    }
    QListWidget {
        background-color: #3b4252;
        color: #d8dee9;
        border: 1px solid #d8dee9;
        font-size: 12pt;
    }
"""

class ImageDuplicateFinderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLESHEET)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Duplicate Finder')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.label1 = QLabel('Selected Folder 1: None', self)
        self.label2 = QLabel('Selected Folder 2: None', self)

        self.btn_select_folder1 = QPushButton('Select Folder 1', self)
        self.btn_select_folder1.clicked.connect(self.select_folder1)

        self.btn_select_folder2 = QPushButton('Select Folder 2', self)
        self.btn_select_folder2.clicked.connect(self.select_folder2)

        self.btn_find_duplicates = QPushButton('Find Duplicates', self)
        self.btn_find_duplicates.clicked.connect(self.find_duplicates)

        self.result_list = QListWidget(self)

        layout.addWidget(self.label1)
        layout.addWidget(self.btn_select_folder1)
        layout.addWidget(self.label2)
        layout.addWidget(self.btn_select_folder2)
        layout.addWidget(self.btn_find_duplicates)
        layout.addWidget(self.result_list)

        self.folder1 = None
        self.folder2 = None

    def select_folder1(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder 1')
        if folder:
            self.folder1 = folder
            self.label1.setText(f'Selected Folder 1: {folder}')

    def select_folder2(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder 2')
        if folder:
            self.folder2 = folder
            self.label2.setText(f'Selected Folder 2: {folder}')

    def find_duplicates(self):
        if not self.folder1:
            QMessageBox.warning(self, 'Error', 'Please select at least one folder.')
            return

        images1 = load_images_from_folder(self.folder1)
        all_images = images1

        if self.folder2:
            images2 = load_images_from_folder(self.folder2)
            all_images += images2

        hash_duplicates, feature_duplicates = find_duplicates(all_images)

        self.result_list.clear()

        if hash_duplicates:
            self.result_list.addItem("Found hash duplicates:")
            for dup in hash_duplicates:
                self.result_list.addItem("\n".join(dup))
            display_duplicates(hash_duplicates)
        else:
            self.result_list.addItem("No hash duplicates found.")

        if feature_duplicates:
            self.result_list.addItem("Found feature duplicates:")
            for dup in feature_duplicates:
                self.result_list.addItem("\n".join(dup))
            display_duplicates(feature_duplicates)
        else:
            self.result_list.addItem("No feature duplicates found.")

def main():
    app = QApplication(sys.argv)
    ex = ImageDuplicateFinderGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()