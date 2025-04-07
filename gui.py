import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QProgressBar, QTextEdit, QFileDialog)
from PyQt5.QtCore import QThread, pyqtSignal
from GameIdList import GameIdList
from GamePage import game_info


class ScraperThread(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, url, start_page, end_page, filter_str, output_file):
        super().__init__()
        self.url = url
        self.start_page = start_page
        self.end_page = end_page
        self.filter_str = filter_str
        self.output_file = output_file

    def run(self):
        try:
            game_id_list = GameIdList()
            page_game_id_list = game_id_list.read_all_game_ids_in_page(
                self.url,
                self.start_page,
                self.end_page,
                self.filter_str
            )

            total_games = len(page_game_id_list)
            for i, game_id in enumerate(page_game_id_list):
                general_url = f"https://store.playstation.com/en-tr/concept/{game_id}"

                game_data = game_info(general_url)
                game_name = game_data.get('name:',
                                          'Unknown Game')  # Get game name, default to 'Unknown Game' if not found
                self.log.emit(f"Processing game: {game_name}")

                self.write_game_info_to_csv(game_data, self.output_file)

                progress = int((i + 1) / total_games * 100)
                self.progress.emit(progress)

            self.log.emit("Scraping completed!")
            self.finished.emit()

        except Exception as e:
            self.log.emit(f"Error: {str(e)}")
            self.finished.emit()
    def write_game_info_to_csv(self, game_data, filename):
        import csv
        file_exists = False
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                file_exists = True
        except FileNotFoundError:
            pass

        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            fieldnames = game_data.keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(game_data)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PlayStation Store Scraper")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # URL input
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setText("https://store.playstation.com/tr-tr/pages/browse/1")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Page range inputs
        page_layout = QHBoxLayout()
        start_label = QLabel("Start Page:")
        self.start_page_input = QLineEdit()
        self.start_page_input.setText("1")
        end_label = QLabel("End Page:")
        self.end_page_input = QLineEdit()
        self.end_page_input.setText("1")
        page_layout.addWidget(start_label)
        page_layout.addWidget(self.start_page_input)
        page_layout.addWidget(end_label)
        page_layout.addWidget(self.end_page_input)
        layout.addLayout(page_layout)

        # Filter input
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter:")
        self.filter_input = QLineEdit()
        self.filter_input.setText("?PS5=targetPlatforms")
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_input)
        layout.addLayout(filter_layout)

        # Output file selection
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setText("output.csv")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(QLabel("Output File:"))
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        # Start button
        self.start_button = QPushButton("Start Scraping")
        self.start_button.clicked.connect(self.start_scraping)
        layout.addWidget(self.start_button)

        self.scraper_thread = None

    def browse_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if filename:
            self.file_path.setText(filename)

    def start_scraping(self):
        if self.scraper_thread is None or not self.scraper_thread.isRunning():
            self.start_button.setEnabled(False)
            self.progress_bar.setValue(0)
            self.log_area.clear()

            self.scraper_thread = ScraperThread(
                self.url_input.text(),
                int(self.start_page_input.text()),
                int(self.end_page_input.text()),
                self.filter_input.text(),
                self.file_path.text()
            )

            self.scraper_thread.progress.connect(self.progress_bar.setValue)
            self.scraper_thread.log.connect(self.log_area.append)
            self.scraper_thread.finished.connect(self.scraping_finished)

            self.scraper_thread.start()

    def scraping_finished(self):
        self.start_button.setEnabled(True)
        self.load_csv_data()  # Load CSV data
        self.tab_widget.setCurrentIndex(1)  # Explicitly switch to CSV viewer tab (index 1)
        self.log_area.append("CSV file loaded and displayed in CSV Viewer tab")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())