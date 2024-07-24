from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        label_title = QLabel()
        label_title.setText("Login")
        label_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_title.setStyleSheet("margin-bottom: 30px; color: #4785d9;")
        layout.addWidget(label_title)

        form_layout = QVBoxLayout()  # Use QVBoxLayout for aligning fields vertically

        # Email field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFont(QFont("Arial", 12))
        self.email_input.setFixedHeight(40)
        self.email_input.setStyleSheet("padding: 10px; border: 1px solid #4785d9; border-radius: 10px;")
        form_layout.addWidget(self.email_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Parola")
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setFixedHeight(40)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 10px; border: 1px solid #4785d9; border-radius: 10px;")
        form_layout.addWidget(self.password_input)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        login_button = QPushButton()
        login_button.setText("Logheaza-te")
        login_button.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        login_button.setStyleSheet("""
            background-color: #4785d9;
            color: #ffffff;
            padding: 10px 20px;
            border-radius: 10px;
        """)
        login_button.clicked.connect(self.login_user)
        button_layout.addWidget(login_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def login_user(self):
        email = self.email_input.text()
        password = self.password_input.text()

        print(f"Login successful with {email}, {password}")
        QMessageBox.information(self, "Success", "Login successful!")

        self.clear_fields()

    def clear_fields(self):
        self.email_input.clear()
        self.password_input.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Intra in cont - bacOS")
        self.setGeometry(100, 100, 600, 300)

        self.login_page = LoginPage()
        self.setCentralWidget(self.login_page)

# Application setup
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Set up the dark theme (if needed)
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#C5C3C6"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#C5C3C6"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#C5C3C6"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#C5C3C6"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#C5C3C6"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#C5C3C6"))
    palette.setColor(QPalette.ColorRole.Link, QColor("#C5C3C6"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#C5C3C6"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    # Create and show main window
    main_window = MainWindow()
    main_window.show()

    # Run the application event loop
    sys.exit(app.exec())
