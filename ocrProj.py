import sys
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import language_tool_python
from googletrans import Translator
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QWidget,
    QMessageBox, QComboBox, QFileDialog, QGroupBox, QHBoxLayout,
    QTextEdit, QLineEdit, QCheckBox
)
from PyQt5.QtGui import QImage, QPixmap, QTextCursor, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QTimer, Qt


try:
    import nltk
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt')
    except:
        import ssl
        try:
            _create_unverified_https_context = ssl._create_unverified_context
            ssl._create_default_https_context = _create_unverified_https_context
            nltk.download('punkt')
        except:
            pass

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Real-Time OCR Scanner')
        self.setGeometry(100, 100, 1200, 700)
        self.tool = language_tool_python.LanguageTool('en-US')
        self.translator = Translator()
        self.last_captured_frame = None

        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)
        self.label.setStyleSheet("border: 2px solid white; border-radius: 5px;")

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(False)
        self.text_edit.setMinimumHeight(150)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("🔍 Search in text...")
        self.search_bar.textChanged.connect(self.highlight_text)

        self.capture_btn = QPushButton('📷 Capture & Recognize')
        self.upload_btn = QPushButton('📁 Upload File')
        self.copy_btn = QPushButton('📋 Copy Text')
        self.spell_btn = QPushButton('📝 Check Grammar')
        self.translate_hi_btn = QPushButton('🌐 Translate to Hindi')
        self.translate_ta_btn = QPushButton('🌐 Translate to Tamil')
        self.save_btn = QPushButton('💾 Save Recognized Text')
        self.summarize_btn = QPushButton('🧠 Summarize Text')
        self.dark_mode_checkbox = QCheckBox("🌙 Dark Mode")

        for btn in [self.capture_btn, self.upload_btn, self.copy_btn, self.spell_btn, self.translate_hi_btn, self.translate_ta_btn, self.save_btn, self.summarize_btn]:
            btn.setCursor(Qt.PointingHandCursor)

        self.dark_mode_checkbox.setChecked(True)
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_theme)

        self.format_selector_group = QGroupBox('Select Input Type')
        self.format_combo = QComboBox()
        self.format_combo.addItems(['Image (JPG, PNG)', 'PDF', 'Text File'])
        format_layout = QHBoxLayout()
        format_layout.addWidget(self.format_combo)
        self.format_selector_group.setLayout(format_layout)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.label)
        left_layout.addWidget(self.summarize_btn)
        left_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.format_selector_group)
        right_layout.addWidget(self.capture_btn)
        right_layout.addWidget(self.upload_btn)
        right_layout.addWidget(self.search_bar)
        right_layout.addWidget(self.text_edit)
        right_layout.addWidget(self.copy_btn)
        right_layout.addWidget(self.spell_btn)
        right_layout.addWidget(self.translate_hi_btn)
        right_layout.addWidget(self.translate_ta_btn)
        right_layout.addWidget(self.save_btn)
        right_layout.addWidget(self.dark_mode_checkbox)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        self.setLayout(main_layout)

        self.capture_btn.clicked.connect(self.capture_frame)
        self.upload_btn.clicked.connect(self.upload_file)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.spell_btn.clicked.connect(self.check_grammar)
        self.translate_hi_btn.clicked.connect(lambda: self.translate_to('hi'))
        self.translate_ta_btn.clicked.connect(lambda: self.translate_to('ta'))
        self.save_btn.clicked.connect(self.save_result)
        self.summarize_btn.clicked.connect(self.summarize_text)

        self.cap = None
        self.initialize_camera()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.toggle_theme()

    def toggle_theme(self):
        if self.dark_mode_checkbox.isChecked():
            self.setStyleSheet("background-color: #2a2a2a; color: white; font-family: 'Arial';")
            self.text_edit.setStyleSheet("background-color: #3a3a3a; color: white; font-size: 14px; border-radius: 5px;")
            self.search_bar.setStyleSheet("background-color: #3a3a3a; color: white; padding: 6px; border-radius: 5px;")
            for btn in [self.capture_btn, self.upload_btn, self.copy_btn, self.spell_btn, self.translate_hi_btn, self.translate_ta_btn, self.save_btn, self.summarize_btn]:
                btn.setStyleSheet("background-color: #444444; color: white; padding: 10px; border-radius: 5px;")
        else:
            self.setStyleSheet("background-color: #f0f0f0; color: black; font-family: 'Arial';")
            self.text_edit.setStyleSheet("background-color: white; color: black; font-size: 14px; border-radius: 5px;")
            self.search_bar.setStyleSheet("background-color: white; color: black; padding: 6px; border-radius: 5px;")
            for btn in [self.capture_btn, self.upload_btn, self.copy_btn, self.spell_btn, self.translate_hi_btn, self.translate_ta_btn, self.save_btn, self.summarize_btn]:
                btn.setStyleSheet("background-color: #e0e0e0; color: black; padding: 10px; border-radius: 5px;")

    def initialize_camera(self):
        for i in range(5):
            temp_cap = cv2.VideoCapture(i)
            if temp_cap.isOpened():
                self.cap = temp_cap
                return
        QMessageBox.critical(self, "Camera Error", "No available camera detected.")
        sys.exit()

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(image))

    def capture_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.last_captured_frame = frame.copy()
                self.perform_ocr(frame)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                    "PDF Files (*.pdf);;Text Files (*.txt);;Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.perform_recognition(file_path)

    def perform_recognition(self, file_path):
        if file_path.lower().endswith('.pdf'):
            self.perform_pdf_ocr(file_path)
        elif file_path.lower().endswith('.txt'):
            self.perform_txt_extraction(file_path)
        else:
            self.process_image(file_path)

    def perform_pdf_ocr(self, pdf_path):
        pages = convert_from_path(pdf_path)
        full_text = ""
        for page in pages:
            img = np.array(page)
            processed = self.preprocess_image(img)
            text = self.tesseract_ocr(processed)
            full_text += text + "\n"
        self.text_edit.setPlainText(full_text)

    def process_image(self, file_path):
        frame = cv2.imread(file_path)
        if frame is not None:
            self.perform_ocr(frame)

    def perform_txt_extraction(self, txt_path):
        with open(txt_path, 'r', encoding='utf-8') as file:
            text = file.read()
        self.text_edit.setPlainText(text)

    def perform_ocr(self, frame):
        processed = self.preprocess_image(frame)
        text = self.tesseract_ocr(processed)
        self.text_edit.setPlainText(text)

    def preprocess_image(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (gray.shape[1] * 2, gray.shape[0] * 2))
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        return dilated

    def tesseract_ocr(self, img):
        pil_img = Image.fromarray(img)
        return pytesseract.image_to_string(pil_img)

    def save_result(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "No text to save.")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Text", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            QMessageBox.information(self, "Saved", "Text saved successfully.")

    def copy_to_clipboard(self):
        text = self.text_edit.toPlainText()
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Copied", "Text copied to clipboard!")

    def check_grammar(self):
        text = self.text_edit.toPlainText()
        matches = self.tool.check(text)
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        for match in matches:
            start = match.offset
            length = match.errorLength
            if length == 0:
                continue
            cursor = QTextCursor(self.text_edit.document())
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, length)
            fmt = QTextCharFormat()
            fmt.setBackground(QColor("red"))
            fmt.setToolTip(f"Suggestion: {', '.join(match.replacements) or 'No suggestion'}")
            cursor.setCharFormat(fmt)
        QMessageBox.information(self, "Grammar Check", f"{len(matches)} issue(s) found and highlighted.")

    def translate_to(self, lang_code):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Translation Error", "No text to translate.")
            return
        try:
            detected = self.translator.detect(text)
            translated = self.translator.translate(text, src=detected.lang, dest=lang_code)
            self.text_edit.setPlainText(translated.text)
            QMessageBox.information(self, "Translation", f"Translated from {detected.lang.upper()} to {lang_code.upper()}.")
        except Exception as e:
            QMessageBox.critical(self, "Translation Error", f"Translation failed: {str(e)}")

    def highlight_text(self):
        search_text = self.search_bar.text()
        document = self.text_edit.document()
        cursor = QTextCursor(document)
        cursor.beginEditBlock()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        if search_text:
            fmt = QTextCharFormat()
            fmt.setBackground(QColor("yellow"))
            highlight_cursor = document.find(search_text)
            while not highlight_cursor.isNull():
                highlight_cursor.mergeCharFormat(fmt)
                highlight_cursor = document.find(search_text, highlight_cursor)
        cursor.endEditBlock()

    def summarize_text(self):
        try:
            text = self.text_edit.toPlainText().strip()
            if not text:
                QMessageBox.warning(self, "Summarization Error", "No text to summarize.")
                return
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, 3)
            summary_text = "\n".join(str(sentence) for sentence in summary)
            self.text_edit.setPlainText(summary_text)
            QMessageBox.information(self, "Summary", "Text summarized successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Summarization Error", f"Error summarizing text: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec_())
