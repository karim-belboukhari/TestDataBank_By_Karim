from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QTextEdit, QFileDialog, QSizePolicy
from connection import create_connection
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import xlsxwriter
import json
from datetime import datetime

class SearchDataForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Search Data")

        self.main_window = main_window 

        self.layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")

        self.tags_input = QLineEdit(self)
        self.tags_input.setPlaceholderText("Enter tags")

        self.comment_input = QLineEdit(self)
        self.comment_input.setPlaceholderText("Enter comment")

        self.environment_input = QComboBox(self)
        self.environment_input.addItems(["Production", "Staging", "UAT", "Vld", "Beta", "SIT", "Hotfix", "team Env", "Release Env"])

        self.search_button = QPushButton("Search Data")
        self.search_button.clicked.connect(self.search_data)

        self.results_display = QTextEdit(self)
        self.results_display.setReadOnly(True)
        self.results_display.setMinimumHeight(145)

        self.results_display.setMaximumHeight(400)

        download_layout = QHBoxLayout()
        self.download_json_button = QPushButton("Download as JSON")
        self.download_json_button.clicked.connect(self.download_as_json)
        
        self.download_pdf_button = QPushButton("Download as PDF")
        self.download_pdf_button.clicked.connect(self.download_as_pdf)

        self.download_excel_button = QPushButton("Download as Excel")
        self.download_excel_button.clicked.connect(self.download_as_excel)

        download_layout.addWidget(self.download_json_button)
        download_layout.addWidget(self.download_pdf_button)
        download_layout.addWidget(self.download_excel_button)

        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("back_button") 
        self.back_button.clicked.connect(self.go_back)


        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.tags_input)
        self.layout.addWidget(self.comment_input)
        self.layout.addWidget(self.environment_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.results_display)
        self.layout.addLayout(download_layout)  
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def search_data(self):
        """Handles searching the data from the database."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        tags = self.tags_input.text().strip()
        comment = self.comment_input.text().strip()
        environment = self.environment_input.currentText().strip()


        query = "SELECT * FROM data_entries WHERE 1"
        params = []

        if username:
            query += " AND username LIKE %s"
            params.append(f"%{username}%")
        if password:
            query += " AND password LIKE %s"
            params.append(f"%{password}%")
        if tags:
            query += " AND tags LIKE %s"
            params.append(f"%{tags}%")
        if comment:
            query += " AND comment LIKE %s"
            params.append(f"%{comment}%")
        if environment:
            query += " AND environment LIKE %s"
            params.append(f"%{environment}%")


        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, tuple(params))
            self.results = cursor.fetchall() 
            connection.close()

            if self.results:
                display_text = ""
                for result in self.results:
                    display_text += f"<b style='color:black;'>Username:</b> <span style='color:black;'>{result['username']}</span><br>"
                    display_text += f"<b style='color:black;'>Password:</b> <span style='color:black;'>{result['password']}</span><br>"
                    display_text += f"<b style='color:blue;'>Tags:</b> <span style='color:black;'>{result['tags']}</span><br>"
                    display_text += f"<b style='color:black;'>Comment:</b> <span style='color:black;'>{result['comment']}</span><br>"
                    display_text += f"<b style='color:red;'>Environment:</b> <span style='color:black;'>{result['environment']}</span><br>"
                    display_text += "<hr>" 
                self.results_display.setHtml(display_text)  
            else:
                self.results_display.setHtml("<p>No matching results found.</p>")

    def download_as_json(self):
        """Download search results as JSON."""
        if not getattr(self, 'results', None): 
            self.results_display.setHtml("<p style='color:red;'>No data to download. Perform a search first.</p>")
            return

        sanitized_results = [
            {k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in result.items()}
            for result in self.results
        ]

        file_path, _ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(sanitized_results, file, indent=4)

    def download_as_pdf(self):
        """Download search results as PDF."""
        if not hasattr(self, 'results') or not self.results:
            self.results_display.setHtml("<p style='color:red;'>No data to download. Perform a search first.</p>")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            y = height - 40
            for result in self.results:
                c.drawString(40, y, f"Username: {result['username']}")
                y -= 20
                c.drawString(40, y, f"Password: {result['password']}")
                y -= 20
                c.drawString(40, y, f"Tags: {result['tags']}")
                y -= 20
                c.drawString(40, y, f"Comment: {result['comment']}")
                y -= 20
                c.drawString(40, y, f"Environment: {result['environment']}")
                y -= 40  
                if y < 40:  
                    c.showPage()
                    y = height - 40
            c.save()

    def download_as_excel(self):
        """Download search results as Excel."""
        if not hasattr(self, 'results') or not self.results:
            self.results_display.setHtml("<p style='color:red;'>No data to download. Perform a search first.</p>")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet()

            headers = ["Username", "Password", "Tags", "Comment", "Environment"]
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            for row, result in enumerate(self.results, start=1):
                worksheet.write(row, 0, result["username"])
                worksheet.write(row, 1, result["password"])
                worksheet.write(row, 2, result["tags"])
                worksheet.write(row, 3, result["comment"])
                worksheet.write(row, 4, result["environment"])

            workbook.close()

    def go_back(self):
        """Handles going back to the main page."""
        self.main_window.show_main_page()  
