import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QInputDialog, QLabel

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Two Buttons")
label = QLabel("")
def on_button1_clicked(): 
    print("Button 1 が押されました") 
    url, ok = QInputDialog.getText( window, "URL入力", f"Button 1 が押されました。URLを入力してください:" ) 
    
    if ok and url:
        print(f"入力されたURL: {url}")
        label.setText(f"入力されたURL: {url}")
    else: 
        print("URL入力がキャンセルされました")
    
def on_button2_clicked(): 
    print("Button 2 が押されました")

# ボタン作成
button1 = QPushButton("Button 1")
button2 = QPushButton("Button 2")

button1.clicked.connect(on_button1_clicked) 
button2.clicked.connect(on_button2_clicked)

# レイアウト作成
layout = QVBoxLayout()
layout.addWidget(button1)
layout.addWidget(button2)
layout.addWidget(label)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
