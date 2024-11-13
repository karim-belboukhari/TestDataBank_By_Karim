from PySide6.QtWidgets import QWidget, QVBoxLayout,QComboBox, QLineEdit, QTextEdit, QPushButton
from connection import create_connection


class StoreDataForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Store Data")
        
        self.main_window = main_window  
        self.layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")

        self.tags_input = QLineEdit(self)
        self.tags_input.setPlaceholderText("Enter tags")

        self.comment_input = QTextEdit(self)
        self.comment_input.setPlaceholderText("Enter comment")

        self.environment_input = QComboBox(self)
        self.environment_input.addItems(["Production","Staging","UAT","Vld","Beta","SIT","Hotfix","Team Env","Release Env","Null"])

        self.store_button = QPushButton("Store Data")
        self.store_button.clicked.connect(self.store_data)


        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("back_button") 
        self.back_button.clicked.connect(self.go_back)


        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.tags_input)
        self.layout.addWidget(self.comment_input)
        self.layout.addWidget(self.environment_input)
        self.layout.addWidget(self.store_button)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def store_data(self):
        """Handles storing data to the database."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        tags = self.tags_input.text().strip()
        comment = self.comment_input.toPlainText().strip()
        environment = self.environment_input.currentText().strip()

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO data_entries (username, password, tags, comment, environment) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (username, password, tags, comment, environment)
                )
                connection.commit()
                self.username_input.clear()
                self.password_input.clear()
                self.tags_input.clear()
                self.comment_input.clear()
                self.environment_input.setCurrentIndex(-1)  
                print("Data stored successfully!")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                connection.close()


    def go_back(self):
        """Handles going back to the main page."""
        self.main_window.show_main_page()  


