import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QTextEdit,
                             QComboBox, QVBoxLayout, QHBoxLayout, QLabel,
                             QMessageBox)
from quote_manager import get_random_quote, get_unique_authors, get_unique_topics
from history_manager import add_to_history, load_history

class QuoteGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.update_history_display()

    def initUI(self):
        self.setWindowTitle('Генератор случайных цитат')
        self.setGeometry(300, 300, 500, 450)

        layout = QVBoxLayout()

        # Блок генерации и фильтрации
        top_layout = QHBoxLayout()
        self.generate_button = QPushButton('Сгенерировать цитату')
        self.generate_button.clicked.connect(self.generate_quote)

        self.author_filter = QComboBox()
        self.author_filter.addItem("Все авторы")
        self.author_filter.addItems(get_unique_authors())

        self.topic_filter = QComboBox()
        self.topic_filter.addItem("Все темы")
        self.topic_filter.addItems(get_unique_topics())

        top_layout.addWidget(self.generate_button)
        top_layout.addWidget(QLabel("Фильтр по автору:"))
        top_layout.addWidget(self.author_filter)
        top_layout.addWidget(QLabel("Фильтр по теме:"))
        top_layout.addWidget(self.topic_filter)

        # Поле для отображения цитаты
        self.quote_display = QTextEdit()
        self.quote_display.setReadOnly(True)
        self.quote_display.setPlaceholderText("Здесь появится цитата...")

        # История цитат
        self.history_label = QLabel("История сгенерированных цитат:")
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)

        # Добавление виджетов в layout
        layout.addLayout(top_layout)
        layout.addWidget(self.quote_display)
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_display)

        self.setLayout(layout)

    def generate_quote(self):
        quote = get_random_quote()
        
        # Проверка фильтров
        selected_author = self.author_filter.currentText()
        selected_topic = self.topic_filter.currentText()
        
        if selected_author != "Все авторы" and quote["author"] != selected_author:
            return self.generate_quote()  # Повторная генерация, если не подходит фильтр

        if selected_topic != "Все темы" and quote["topic"] != selected_topic:
            return self.generate_quote()

        self.quote_display.setText(f'"{quote["text"]}"\n\n— {quote["author"]} ({quote["topic"]})')
        
        # Сохранение в историю и обновление списка
        add_to_history(quote)
        self.update_history_display()
        
    def update_history_display(self):
        history = load_history()
        text = ""
        for i, q in enumerate(history):
            text += f"{i+1}. \"{q['text']}\"\n   — {q['author']} ({q['topic']})\n\n"
        self.history_display.setText(text.strip())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuoteGeneratorApp()
    window.show()
    sys.exit(app.exec_())
