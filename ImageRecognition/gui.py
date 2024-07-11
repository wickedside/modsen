import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidget, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ImageRecognition.image_processing.load_images import load_images_from_folder
from ImageRecognition.utils.find_duplicates import find_duplicates

# css stylesheet to make the app look little better
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

class DuplicateViewer(QMainWindow):
    def __init__(self, duplicates):
        super().__init__()
        self.setStyleSheet(STYLESHEET)
        self.duplicates = duplicates
        self.index = 0

        self.initUI()

    def initUI(self):
        # setting up the duplicate viewer window
        self.setWindowTitle('Duplicate Viewer')
        self.setGeometry(150, 150, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.image_label1 = QLabel(self)
        self.image_label2 = QLabel(self)

        # center the image labels
        self.image_label1.setAlignment(Qt.AlignCenter)
        self.image_label2.setAlignment(Qt.AlignCenter)

        btn_layout = QHBoxLayout()

        # create previous and next buttons
        self.btn_prev = QPushButton('Previous', self)
        self.btn_prev.clicked.connect(self.show_previous)

        self.btn_next = QPushButton('Next', self)
        self.btn_next.clicked.connect(self.show_next)

        btn_layout.addWidget(self.btn_prev)
        btn_layout.addWidget(self.btn_next)

        layout.addWidget(self.image_label1)
        layout.addWidget(self.image_label2)
        layout.addLayout(btn_layout)

        self.show_images()

    def show_images(self):
        # display current pair of duplicate images
        if not self.duplicates:
            return

        # wrap around the index if out of bounds
        if self.index < 0:
            self.index = len(self.duplicates) - 1
        elif self.index >= len(self.duplicates):
            self.index = 0

        dup_pair = self.duplicates[self.index]
        pixmap1 = QPixmap(dup_pair[0])
        pixmap2 = QPixmap(dup_pair[1])

        # scale images to fit the labels
        self.image_label1.setPixmap(pixmap1.scaled(350, 350, Qt.KeepAspectRatio))
        self.image_label2.setPixmap(pixmap2.scaled(350, 350, Qt.KeepAspectRatio))

    def show_previous(self):
        # show the previous pair
        self.index -= 1
        self.show_images()

    def show_next(self):
        # show the next pair
        self.index += 1
        self.show_images()

class ImageDuplicateFinderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLESHEET)
        self.initUI()

    def initUI(self):
        # setting up the main window
        self.setWindowTitle('Image Duplicate Finder')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # create labels and buttons
        self.label1 = QLabel('Selected Folder 1: None', self)
        self.label2 = QLabel('Selected Folder 2: None', self)

        self.btn_select_folder1 = QPushButton('Select Folder 1', self)
        self.btn_select_folder1.clicked.connect(self.select_folder1)

        self.btn_select_folder2 = QPushButton('Select Folder 2', self)
        self.btn_select_folder2.clicked.connect(self.select_folder2)

        self.btn_find_duplicates = QPushButton('Find Duplicates', self)
        self.btn_find_duplicates.clicked.connect(self.find_duplicates)

        self.result_list = QListWidget(self)

        # add widgets to the layout
        layout.addWidget(self.label1)
        layout.addWidget(self.btn_select_folder1)
        layout.addWidget(self.label2)
        layout.addWidget(self.btn_select_folder2)
        layout.addWidget(self.btn_find_duplicates)
        layout.addWidget(self.result_list)

        self.folder1 = None
        self.folder2 = None

    def select_folder1(self):
        # open a dialog to select folder 1
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder 1')
        if folder:
            self.folder1 = folder
            self.label1.setText(f'Selected Folder 1: {folder}')

    def select_folder2(self):
        # open a dialog to select folder 2
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder 2')
        if folder:
            self.folder2 = folder
            self.label2.setText(f'Selected Folder 2: {folder}')

    def find_duplicates(self):
        # check if at least one folder is selected
        if not self.folder1:
            QMessageBox.warning(self, 'Error', 'Please select at least one folder.')
            return

        # load images from the selected folders
        images1 = load_images_from_folder(self.folder1)
        all_images = images1

        if self.folder2:
            images2 = load_images_from_folder(self.folder2)
            all_images += images2

        # find duplicates using hash and feature methods
        hash_duplicates, feature_duplicates = find_duplicates(all_images)

        self.result_list.clear()

        # display found hash duplicates
        if hash_duplicates:
            self.result_list.addItem("Found hash duplicates:")
            for dup in hash_duplicates:
                self.result_list.addItem("\n".join(dup))
            self.show_duplicates(hash_duplicates)
        else:
            self.result_list.addItem("No hash duplicates found.")

        # display found feature duplicates
        if feature_duplicates:
            self.result_list.addItem("Found feature duplicates:")
            for dup in feature_duplicates:
                self.result_list.addItem("\n".join(dup))
            self.show_duplicates(feature_duplicates)
        else:
            self.result_list.addItem("No feature duplicates found.")

    def show_duplicates(self, duplicates):
        # open the duplicate viewer window
        self.viewer = DuplicateViewer(duplicates)
        self.viewer.show()

def main():
    app = QApplication(sys.argv)
    ex = ImageDuplicateFinderGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
