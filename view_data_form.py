from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from connection import create_connection

class ViewDataForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Data")

        self.layout = QVBoxLayout()

        self.data_display = QTextEdit(self)
        self.data_display.setReadOnly(True)
        self.layout.addWidget(self.data_display)

        self.fetch_button = QPushButton("Fetch Data", self)
        self.fetch_button.clicked.connect(self.fetch_data)
        self.layout.addWidget(self.fetch_button)

        self.setLayout(self.layout)

    def fetch_data(self):
        """Fetches data from the database and displays it."""
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            query = "SELECT * FROM data_entries"
            cursor.execute(query)
            rows = cursor.fetchall()

            data_text = ""
            for row in rows:
                username = row[1]
                password = row[2]
                tags = row[3]
                comment = row[4]
                environment = row[5]

                data_text += f"Username: {username}\n"
                data_text += f"Password: {password}\n"
                data_text += f"Tags: {tags}\n"
                data_text += f"Comment: {comment}\n"
                data_text += f"Environment: {environment}\n"
                data_text += "-" * 40 + "\n"

            self.data_display.setText(data_text)  
            connection.close()
