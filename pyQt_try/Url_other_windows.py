import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QInputDialog, QLabel
)

class TextWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("別ウィンドウ")
        layout = QVBoxLayout()
        label = QLabel(text)
        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(300, 1)

def ask_url(button_name):
    url, ok = QInputDialog.getText(
        window,
        "URL入力",
        f"{button_name} が押されました。URLを入力してください:"
    )
    if ok and url:
        # 別ウィンドウを開く
        sub = TextWindow(f"入力されたURL: {url}")
        sub.show()
        # 参照が消えないように保持
        windows.append(sub)
    else:
        sub = TextWindow("URL入力がキャンセルされました")
        sub.show()
        windows.append(sub)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Two Buttons")

# ボタン作成
button1 = QPushButton("Button 1")
button2 = QPushButton("Button 2")

# ボタンが押されたときの処理
button1.clicked.connect(lambda: ask_url("Button 1"))
button2.clicked.connect(lambda: ask_url("Button 2"))

# レイアウト作成
layout = QVBoxLayout()
layout.addWidget(button1)
layout.addWidget(button2)

window.setLayout(layout)
window.show()

# 別ウィンドウを保持するリスト
windows = []

sys.exit(app.exec_())
