from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
from PyQt6.QtCore import QRect, Qt

class Event:
    def __init__(self, ip, nume):
        self.ip = ip
        self.serverport = 80
        self.nume = nume

    def wait(self):
        # Simulated method for demonstration
        print(f"Waiting for event: {self.nume}")

    def start(self):
        # Simulated method for starting event
        print(f"Starting event: {self.nume}")

# Application setup
app = QApplication([])

# Set up the dark theme
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

# Set global font
app.setFont(QFont("Arial", 10))  # Fallback font in case specific font is not available

# Main window setup
window = QMainWindow()
window.setWindowTitle("bacOS")
window.setWindowIcon(QIcon('C:/Users/vlada/Downloads/favicon.ico'))  # Replace with your favicon path
window.setGeometry(100, 100, 600, 300)
screen = app.primaryScreen().availableGeometry()
window.setGeometry(
    QRect(
        screen.width() // 2 - window.width() // 2,
        screen.height() // 2 - window.height() // 2,
        window.width(),
        window.height()
    )
)

# Widget setup
widget = QWidget()
layout = QVBoxLayout()

# QLabel setup
label = QLabel()
label.setText("Introdu codul evenimentului")
label.setFont(QFont("Arial", 20, QFont.Weight.Bold))  # Set larger font size for the label
label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the label
label.setStyleSheet("margin-bottom: 150px; color: #4785d9;")
layout.addWidget(label)

# QLineEdit setup
input_box = QLineEdit()
input_box.setFont(QFont("Arial", 15, QFont.Weight.Bold))  # Use Courier as monospace font
input_box.setFixedHeight(40)
input_box.setFixedWidth(300)
input_box.setStyleSheet("""
    background-color: #ffffff; 
    color: #4785d9; 
    border: none; 
    border: 1px solid #4785d9;
    padding: 1px;
    border-radius: 10px;
""")
input_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
layout.addWidget(input_box, alignment=Qt.AlignmentFlag.AlignCenter)

# QPushButton setup
button = QPushButton()
button.setText("Porneste evenimentul")
button.setFont(QFont("Arial", 15, QFont.Weight.Bold))
button.setFixedHeight(80)
button.setFixedWidth(500)
button.setStyleSheet("""
    background-color: #4785d9;
    color: #ffffff;
    margin-top: 40px;
    border-radius: 10px;
""")
# Add button to layout and center horizontally
layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

# Connect button click event
def start_event():
    event_name = input_box.text()
    event = Event("192.168.1.7", event_name)
    event.wait()
    window.close()

button.clicked.connect(start_event)

# Set layout to widget and central widget to window
widget.setLayout(layout)
window.setCentralWidget(widget)

# Show window and start application event loop
window.show()
app.exec()
