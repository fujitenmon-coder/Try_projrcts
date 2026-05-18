import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt 基本")
        self.resize(300, 200)

        layout = QVBoxLayout()

        button = QPushButton("押してね")
        button.clicked.connect(self.on_click)

        layout.addWidget(button)
        self.setLayout(layout)
        
    def __init__(sew):
        super().__init__()

        sew.setWindowTitle("PyQt 基本")
        sew.resize(200, 200)

        layout = QVBoxLayout()

        button = QPushButton("押してね")
        button.clicked.connect(sew.on_click)

        layout.addWidget(button)
        sew.setLayout(layout)
        
    def on_click(sew):
        print("ボタンが...")    
        
    def on_click(self):
        print("ボタンが押されました")

app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())
