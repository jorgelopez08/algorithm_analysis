import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QFileDialog, QMessageBox, QPlainTextEdit
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from PyQt5.QtGui import QIcon, QPixmap

from main_window import Ui_MainWindow
from schedule_generator import ScheduleGenerator

import json
import os
import shutil

import resources


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Add icons
        home_icon_1 = QIcon(":/icons/home_icon_off")
        self.ui.home_btn_1.setIcon(home_icon_1)
        home_icon_2 = QIcon(":/icons/home_icon_off")
        self.ui.home_btn_2.setIcon(home_icon_2)

        register_icon_1 = QIcon(":/icons/register_icon_off")
        self.ui.register_btn_1.setIcon(register_icon_1)
        register_icon_2 = QIcon(":/icons/register_icon_off")
        self.ui.register_btn_2.setIcon(register_icon_2)
        
        visualize_icon_1 = QIcon(":/icons/visualize_icon_off")
        self.ui.visualize_btn_1.setIcon(visualize_icon_1)
        visualize_icon_2 = QIcon(":/icons/visualize_icon_off")
        self.ui.visualize_btn_2.setIcon(visualize_icon_2)

        download_icon_1 = QIcon(":/icons/download_icon_off")
        self.ui.download_btn1.setIcon(download_icon_1)
        download_icon_2 = QIcon(":/icons/download_icon_off")
        self.ui.download_btn_2.setIcon(download_icon_2)

        close_icon = QIcon(":/icons/close_icon")
        self.ui.exit_btn_1.setIcon(close_icon)
        self.ui.exit_btn_2.setIcon(close_icon)

        menu_icon = QIcon(":/icons/menu_icon")
        self.ui.change_btn.setIcon(menu_icon)

        logo_icon = QPixmap(":/icons/logo_icon")
        self.ui.logo_label_2.setPixmap(logo_icon)
        self.ui.logo_label_4.setPixmap(logo_icon)

        with open("actual_input_file_path.txt", "r") as input_path:
            input_path_str = input_path.readline()

        # Stores the actual input JSON file path
        self.actual_input_file_path = input_path_str
        if self.actual_input_file_path != "":
            # Updates actual input file labels
            self.ui.actual_input_file_label.setText(self.actual_input_file_path)
            self.ui.actual_input_file_visualize_label.setText(self.actual_input_file_path)

        with open("view_schedule_plain_text.txt", "r") as view_schedule:
            view_schedule_str = view_schedule.read()

        # Stores the schedule in a string
        self.view_schedule = view_schedule_str
        if self.view_schedule != "":
            # Updates schedule view
            self.ui.view_schedule_plain_text_edit.setPlainText(self.view_schedule)

        # Set view schedule to read only
        self.ui.view_schedule_plain_text_edit.setReadOnly(True)

        #Add horizontal scroll to view schedule
        self.ui.view_schedule_plain_text_edit.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.ui.icons_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)

        # Set function to browse button
        self.ui.browse.clicked.connect(self.browse_files)

        # Set function to generate_schedule_btn button
        self.ui.generate_schedule_btn.clicked.connect(self.generate_and_export_schedule)

        # Set function to download_btn button
        self.ui.download_btn.clicked.connect(self.download_schedule)

    ## Change QPushButton checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icons_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)

        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    ## Function for changing menu pages
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_register_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_register_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_visualize_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_visualize_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_download_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_download_btn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def browse_files(self):
        desktop_path = os.path.expanduser("~/Desktop")
        fname = QFileDialog.getOpenFileName(self, 'Abrir archivo', desktop_path , 'Archivos JSON (*.json)')
        self.ui.file_name.setText(fname[0])
        if fname[0] != "":
             print(fname)
             print("Se ha seleccionado la ruta del archivo JSON con éxito\n\n")

    def generate_and_export_schedule(self):
        try:
            # Carga tus datos desde el archivo JSON
            archivo_json = self.ui.file_name.text()
            print(archivo_json)
            with open(archivo_json, 'r', encoding='utf-8') as file:
                datos = json.load(file)
                file.close()
            print(datos)
            subjects = [curso for curso in (datos["Datos"][2]["Curso"])]
            professors = [profesor for profesor in (datos["Datos"][0]["Profesor"])]
            classrooms = [aula for aula in (datos["Datos"][1]["Aula"])]
            time_slots = ['9:00-11:00', '11:00-1:00', '1:00-3:00', '3:00-5:00']
            days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

            # Create ScheduleGenerator instance
            schedule_generator = ScheduleGenerator(subjects, professors, classrooms, time_slots, days_list)

            # Generate schedule for the whole week
            schedule_generator.generate_schedule()

            # Print the generated schedule
            view_schedule_text = schedule_generator.export_to_file()

            # Update actual input JSON file path
            self.actual_input_file_path = archivo_json
            with open("actual_input_file_path.txt", "w") as input_path:
                input_path.write(self.actual_input_file_path)
            self.ui.actual_input_file_label.setText(self.actual_input_file_path)
            self.ui.actual_input_file_visualize_label.setText(self.actual_input_file_path)

            # Update schedule 
            self.view_schedule = view_schedule_text
            with open("view_schedule_plain_text.txt", "w") as view_schedule:
                view_schedule.write(self.view_schedule)
            self.ui.view_schedule_plain_text_edit.setPlainText(self.view_schedule)

        except Exception as e:
            print(e)
            print("El archivo .json proporcionado no es válido, revise el formato\n\n")
            QMessageBox.warning(self, "Error", "El archivo .json proporcionado no es válido, revise el formato")
        else:
            # Show success schedule generation message
            print("Se ha generado el horario con éxito\n\n")
            QMessageBox.information(self, "Carga exitosa", "El archivo se ha cargado correctamente")

    def download_schedule(self):
        schedule_json_path = "schedule.json"
        downloads_path = os.path.expanduser("~/Downloads")

        try:
            # Copy "schedule.json" to Downloads
            shutil.copy(schedule_json_path, downloads_path)
        except:
            print("No se ha podido descargar schedule.json\n\n")
            QMessageBox.warning(self, 'Error', 'No se ha podido descargar schedule.json, primero cargue un archivo .json en la sección "Registrar"')
        else:
            print("Se ha copiado el archivo exitosamente a ", downloads_path)
            QMessageBox.information(self, 'Descarga exitosa', f'Se ha descargado schedule.json en {downloads_path}')



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ## Load "style.qss" file
    with open("style.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())




