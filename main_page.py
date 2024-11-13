from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from store_data_form import StoreDataForm
from search_data_form import SearchDataForm

class MainPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Main Page")

        self.main_window = main_window
        self.layout = QVBoxLayout()

        self.store_button = QPushButton("Store Data")
        self.store_button.clicked.connect(self.open_store_data_form)

        self.search_button = QPushButton("Search Data")
        self.search_button.clicked.connect(self.open_search_data_form)


        self.documentation_button = QPushButton("Documentation")
        self.documentation_button.clicked.connect(self.open_documentation)
        self.documentation_button.setFixedSize(150, 40)

        # Add buttons to layout
        self.layout.addWidget(self.store_button)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.documentation_button)

        self.setLayout(self.layout)

    def open_store_data_form(self):
        """Open the Store Data form."""
        self.main_window.show_store_data_form()

    def open_search_data_form(self):
        """Open the Search Data form."""
        self.main_window.show_search_data_form()

    def open_documentation(self):
        """Open the documentation URL in the default web browser."""
        documentation_url = QUrl("https://github.com/karim-belboukhari")  
        QDesktopServices.openUrl(documentation_url)
