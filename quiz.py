import sys, os, sqlite3, random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QButtonGroup, QHBoxLayout, QGraphicsOpacityEffect, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

DB_FILE = "questions.db"
TESTS_DIR = "tests"
DEFAULT_SOURCE = "questions.txt"  # varsayılan kaynak

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Quiz App")
        self.setFixedSize(900, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel, QPushButton, QComboBox {
                color: white;
                font-family: 'Segoe UI';
            }
            QComboBox {
                background-color: #2a2a2a;
                border: 1px solid #555;
                padding: 6px;
                border-radius: 6px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                selection-background-color: #3a3a3a;
            }
            QPushButton {
                background-color: #2e2e2e;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QPushButton:disabled {
                background-color: #1e1e1e;
                color: #666;
                border: 1px solid #333;
            }
        """)

        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.score = 0
        self.current_question = None
        self.questions = []
        self.current_index = 0

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(15)

        # Üst bar (skor, kaynak seçici, soruları getir butonu)
        top_bar = QHBoxLayout()
        self.score_label = QLabel("Skor: 0")
        self.score_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        top_bar.addWidget(self.score_label)

        top_bar.addStretch()

        self.source_selector = QComboBox()
        self.load_sources()
        top_bar.addWidget(self.source_selector)

        self.load_button = QPushButton("Soruları Getir")
        self.load_button.setFont(QFont("Segoe UI", 11))
        self.load_button.clicked.connect(self.load_selected_source)
        top_bar.addWidget(self.load_button)

        main_layout.addLayout(top_bar)

        # Soru kaynağı etiketi
        self.source_label = QLabel("")
        self.source_label.setFont(QFont("Segoe UI", 10))
        self.source_label.setStyleSheet("color: #aaa;")
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.source_label)

        # Soru metni
        self.question_label = QLabel("")
        self.question_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        self.question_label.setWordWrap(True)
        main_layout.addWidget(self.question_label)

        # Şıklar
        self.button_group = QButtonGroup()
        self.option_buttons = []

        for _ in range(4):
            btn = QPushButton("")
            btn.setFont(QFont("Segoe UI", 12))
            btn.clicked.connect(self.check_answer)
            self.option_buttons.append(btn)
            self.button_group.addButton(btn)
            main_layout.addWidget(btn)

        # Sonraki soru butonu
        self.next_button = QPushButton("Sonraki Soru")
        self.next_button.setFont(QFont("Segoe UI", 11))
        self.next_button.clicked.connect(self.load_next_question)
        self.next_button.setDisabled(True)
        main_layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setCentralWidget(main_widget)

        # varsayılan kaynak yükle
        if DEFAULT_SOURCE in [f for f in os.listdir(TESTS_DIR) if f.endswith(".txt")]:
            self.source_selector.setCurrentText(DEFAULT_SOURCE)
            self.load_selected_source()

    def load_sources(self):
        """tests klasöründeki txt dosyalarını dropdown’a yükler"""
        if not os.path.exists(TESTS_DIR):
            os.makedirs(TESTS_DIR)
        txt_files = [f for f in os.listdir(TESTS_DIR) if f.endswith(".txt")]
        self.source_selector.addItems(txt_files)

    def load_selected_source(self):
        file_name = self.source_selector.currentText()
        if not file_name:
            return
        table_name = os.path.splitext(file_name)[0]

        # tablo var mı kontrol et
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        exists = self.cursor.fetchone()

        if not exists:
            from to_db import insert_questions_from_txt
            insert_questions_from_txt(os.path.join(TESTS_DIR, file_name), DB_FILE, table_name)

        # soruları çek
        self.cursor.execute(f"SELECT question, A, B, C, D, correct, source FROM {table_name}")
        self.questions = self.cursor.fetchall()

        if not self.questions:
            QMessageBox.warning(self, "Uyarı", f"{file_name} içinde soru bulunamadı.")
            return

        random.shuffle(self.questions)
        self.score = 0
        self.score_label.setText("Skor: 0")
        self.current_index = -1
        self.load_button.setDisabled(True)
        self.next_button.setDisabled(False)
        self.load_next_question()

    def load_next_question(self):
        if not self.questions:
            return

        self.current_index += 1
        if self.current_index >= len(self.questions):
            QMessageBox.information(self, "Tamamlandı", f"Tüm soruları tamamladınız!\nSkorunuz: {self.score}")
            self.load_button.setDisabled(False)
            self.next_button.setDisabled(True)
            return

        q = self.questions[self.current_index]
        question, a, b, c, d, correct, source = q
        options = [("A", a), ("B", b), ("C", c), ("D", d)]
        random.shuffle(options)

        self.current_question = {"correct": correct, "options": options}
        self.source_label.setText(f"Kaynak: {source}")
        self.question_label.setText(f"{self.current_index + 1}. {question}")

        for i, btn in enumerate(self.option_buttons):
            btn.setText(options[i][1])
            btn.setStyleSheet("background-color: #2e2e2e; color: white;")

    def check_answer(self):
        if not self.current_question:
            return

        sender = self.sender()
        selected_text = sender.text()
        correct_letter = self.current_question["correct"]
        correct_text = None

        for opt in self.current_question["options"]:
            if opt[0] == correct_letter:
                correct_text = opt[1]
                break

        for btn in self.option_buttons:
            if btn.text() == correct_text:
                btn.setStyleSheet("background-color: #388e3c; color: white;")
            elif btn.text() == selected_text and selected_text != correct_text:
                btn.setStyleSheet("background-color: #d32f2f; color: white;")
            else:
                btn.setStyleSheet("background-color: #2e2e2e; color: white;")

        if selected_text == correct_text:
            self.score += 1
            self.score_label.setText(f"Skor: {self.score}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec())
