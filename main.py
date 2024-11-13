from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QLabel
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
import sys
from main_page import MainPage
from store_data_form import StoreDataForm
from search_data_form import SearchDataForm

def apply_global_styles(app):
    style = """
    QWidget {
        background-color: #E0F7FA;  /* Light blue background */
        font-size: 16px;  /* Increase font size for readability */
        color: #01579B;  /* Dark blue text */
    }

    QLineEdit, QTextEdit, QPushButton {
        font-size: 18px;  /* Larger text size */
        padding: 10px;  /* More padding for buttons and text fields */
        border-radius: 10px;
        border: 2px solid #01579B;
        background-color: #B3E5FC;  /* Light blue background for input fields */
    }

    QLineEdit:focus, QTextEdit:focus {
        border-color: #0288D1;  /* Darker blue when focused */
    }

    QPushButton {
        background-color: #0288D1;  /* Blue background for button */
        color: white;
    }

    QPushButton:hover {
        background-color: #0277BD;  /* Darker blue when hovered */
    }

    QTextEdit {
        background-color: #ffffff;  /* White background for the text display */
        border: 2px solid #01579B;
        border-radius: 10px;
    }

    QPushButton#back_button {
        background-color: #FF7043;  /* Orange back button */
        color: white;
    }

    QPushButton#back_button:hover {
        background-color: #FF5722;  /* Darker orange on hover */
    }

    QComboBox {
        padding: 5px;
        border: 1px solid #01579B;  /* Dark border for better visibility */
        border-radius: 5px;
        font-size: 14px;
        background-color: #B3E5FC;  /* Light blue background */
        color: #01579B;  /* Dark text color for readability */
        min-width: 180px;
        height: 20px;
        text-align: center;
    }

    QComboBox::down-arrow {
        width: 18px;  /* Size of the arrow */
        height: 18px;
        image: url('drp_dn.png');  /* No custom image, uses default arrow */
    }

    QComboBox::drop-down {
        background-color: #4FC3F7;  /* Light blue background */
        border: 1px solid #01579B;
        border-radius: 5px;
    }

    QComboBox QAbstractItemView {
        background-color: #B3E5FC;  /* Same light blue for the dropdown list */
        color: #01579B;  /* Dark text color */
        selection-background-color: #0288D1;  /* Darker blue selection color */
        selection-color: white;  /* White text when selected */
    }

    QLabel {
        font-size: 18px;
    }
    """
    app.setStyleSheet(style)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test-Data BANK")
        
        pixmap = QPixmap("app_icon.ico").scaled(64, 64, Qt.KeepAspectRatio)
        self.setWindowIcon(QIcon(pixmap))

        main_layout = QVBoxLayout()

        logo_label = QLabel(self)
        pixmap = QPixmap("logo.png") 
        logo_label.setPixmap(pixmap)
        logo_label.setFixedSize(150, 45) 
        logo_label.setScaledContents(True)

        main_layout.addWidget(logo_label)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.main_page = MainPage(self)
        self.store_data_form = StoreDataForm(self)
        self.search_data_form = SearchDataForm(self)

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.store_data_form)
        self.stacked_widget.addWidget(self.search_data_form)

        self.stacked_widget.setCurrentWidget(self.main_page)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_store_data_form(self):
        self.stacked_widget.setCurrentWidget(self.store_data_form)

    def show_search_data_form(self):
        self.stacked_widget.setCurrentWidget(self.search_data_form)

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_global_styles(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
