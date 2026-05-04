import sys
import os
import json
import traceback
import re
import faulthandler
import datetime
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                               QTableWidgetItem, QProgressBar, QLabel, QVBoxLayout,
                               QDialog, QMessageBox, QFileDialog, QColorDialog, QProgressDialog)
from PySide6.QtCore import Qt, QTimer, QUrl, QTime
from PySide6.QtGui import QColor, QDesktopServices
    
from ui_py.ui_main import Ui_MainWindow
from ui_py.ui_route_info import Ui_Dialog as Ui_RouteInfoDialog
from engine import RailwayEngine
from views.stb_editor import STBEditorWidget
from views.frequency_setting import FrequencySettingWidget
from views.trains_editor import TrainsEditorWidget

from core.timetable_parser import TimetableParser
from core.timetable_builder import TimetableBuilder
from core.simulation_worker import SimulationWorker  

# ==========================================
# 路線資訊表單視窗 (完全對接 route_info.ui)
# ==========================================
class RouteInfoDialog(QDialog, Ui_RouteInfoDialog):
    def __init__(self, parent=None, prefill_data=None, full_data=None, is_edit_mode=False):
        super().__init__(parent)
        self.setupUi(self) 
        
        self.line_color_c.clicked.connect(self.choose_color)
        self.line_color_i.textChanged.connect(self.update_color_button)
        
        self.line_color_i.setText("#0033A0") 
        
        self.line_start_i.setReadOnly(True)
        self.line_end_i.setReadOnly(True)
        self.line_count_i.setReadOnly(True)
        
        readonly_style = "background-color: #f0f0f0; color: #555;"
        self.line_start_i.setStyleSheet(readonly_style)
        self.line_end_i.setStyleSheet(readonly_style)
        self.line_count_i.setStyleSheet(readonly_style)
        
        if prefill_data:
            self.line_start_i.setText(str(prefill_data.get('start', '')))
            self.line_end_i.setText(str(prefill_data.get('end', '')))
            self.line_count_i.setText(str(prefill_data.get('count', '')))
            
        if full_data:
            self.line_name_i.setText(full_data.get('路線名稱', ''))
            self.line_id_i.setText(full_data.get('路線ID', ''))
            self.line_color_i.setText(full_data.get('路線顏色', '#0033A0'))
            self.line_country_i.setText(full_data.get('路線所在國家', ''))
            self.line_city_i.setText(full_data.get('路線經過城市', ''))
            self.line_type_i.setText(full_data.get('路線種類', ''))
            self.line_start_i.setText(full_data.get('起點', ''))
            self.line_end_i.setText(full_data.get('終點', ''))
            self.line_count_i.setText(str(full_data.get('車站數', '')))
            self.line_owner_i.setText(full_data.get('路線所有者', ''))
            self.line_operator_i.setText(full_data.get('路線營運者', ''))
            self.line_linetype_i.setText(full_data.get('線路數', ''))
            self.line_electric_i.setText(full_data.get('電氣化模式', ''))
            self.line_safety_i.setText(full_data.get('安全裝置', ''))
            self.line_speed_i.setText(full_data.get('最高營運速度', ''))
            
            self.interval_time_i.setText(str(full_data.get('發車間隔緩衝時間', 45)))
            self.stopping_time_stretching_c.setChecked(full_data.get('停靠時間可否拉伸', False))
            self.shift_step_i.setText(str(full_data.get('班次平移精度', 5)))
            
            t_first = QTime.fromString(full_data.get('首班車發車時間', '05:00:00'), "HH:mm:ss")
            if not t_first.isValid(): t_first = QTime(5, 0, 0)
            self.first_departure_t.setTime(t_first)
            
            t_last = QTime.fromString(full_data.get('末班車發車時間', '23:59:00'), "HH:mm:ss")
            if not t_last.isValid(): t_last = QTime(23, 59, 0)
            self.last_departure_t.setTime(t_last)
            
        else:
            self.interval_time_i.setText("45")
            self.shift_step_i.setText("5")
            self.first_departure_t.setTime(QTime(5, 0, 0))
            self.last_departure_t.setTime(QTime(23, 59, 0))

        if is_edit_mode:
            self.setWindowTitle("編輯路線設定")
            self.line_id_i.setReadOnly(True)
            self.line_id_i.setStyleSheet(readonly_style)
            
        self.buttonBox.accepted.disconnect() 
        self.buttonBox.accepted.connect(self.validate_and_accept)

    def choose_color(self):
        current_color = QColor(self.line_color_i.text()) if QColor.isValidColor(self.line_color_i.text()) else QColor("#0033A0")
        color = QColorDialog.getColor(current_color, self, "選擇路線顏色")
        if color.isValid():
            self.line_color_i.setText(color.name().upper())

    def update_color_button(self, hex_text):
        if len(hex_text) == 7 and hex_text.startswith('#'):
            self.line_color_c.setStyleSheet(f"background-color: {hex_text}; border: 1px solid #999; border-radius: 3px;")

    def validate_and_accept(self):
        name = self.line_name_i.text().strip()
        route_id = self.line_id_i.text().strip()
        color = self.line_color_i.text().strip()
        
        if not name or not route_id or not color:
            QMessageBox.warning(self, "錯誤", "請填寫所有必填欄位 (路線名稱、路線ID、路線顏色)！")
            return
            
        if not re.match(r'^[\w\u4e00-\u9fa5\-]+$', route_id):
            QMessageBox.warning(self, "錯誤", "路線ID包含非法字元，請勿使用空格或特殊符號 (將作為資料夾名稱)。")
            return
            
        interval_str = self.interval_time_i.text().strip()
        if interval_str and not interval_str.isdigit():
            QMessageBox.warning(self, "錯誤", "發車間隔時間必須為純數字！")
            return
            
        shift_str = self.shift_step_i.text().strip()
        if shift_str and not shift_str.isdigit():
            QMessageBox.warning(self, "錯誤", "班次平移精度必須為純數字！")
            return
            
        self.accept()
        
    def get_data(self):
        try:
            buffer_time = int(self.interval_time_i.text().strip())
        except ValueError:
            buffer_time = 45
            
        try:
            shift_step = int(self.shift_step_i.text().strip())
        except ValueError:
            shift_step = 5

        return {
            "路線名稱": self.line_name_i.text().strip(),
            "路線ID": self.line_id_i.text().strip(),
            "路線顏色": self.line_color_i.text().strip(),
            "路線所在國家": self.line_country_i.text().strip(),
            "路線經過城市": self.line_city_i.text().strip(),
            "路線種類": self.line_type_i.text().strip(),
            "起點": self.line_start_i.text(),
            "終點": self.line_end_i.text(),
            "車站數": self.line_count_i.text(),
            "路線所有者": self.line_owner_i.text().strip(),
            "路線營運者": self.line_operator_i.text().strip(),
            "線路數": self.line_linetype_i.text().strip(),
            "電氣化模式": self.line_electric_i.text().strip(),
            "安全裝置": self.line_safety_i.text().strip(),
            "最高營運速度": self.line_speed_i.text().strip(),
            "發車間隔緩衝時間": buffer_time,
            "停靠時間可否拉伸": self.stopping_time_stretching_c.isChecked(),
            "班次平移精度": shift_step,
            "首班車發車時間": self.first_departure_t.time().toString("HH:mm:ss"),
            "末班車發車時間": self.last_departure_t.time().toString("HH:mm:ss")
        }

class TimetableApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_loaded_route_name = ""
        self.update_line_color("#FFFFFF")

        self.engine = RailwayEngine(workspace_root="save")
        self.engine.logger = self.log_msg
        
        self.setup_statusbar()
        self.setup_workspaces()
        self.bind_events()

        self.refresh_project_list()
        
        self.log_msg("系統啟動成功。請先載入路線或匯入基準時刻表。")
        self.statusbar.showMessage("就緒")

        self.main_output.setTabsClosable(True)
        self.main_output.tabCloseRequested.connect(self.close_tab)
        
        self.main_output.setMovable(True)
        self.main_output.currentChanged.connect(self.on_tab_changed)

    # ==========================================
    # 1. UI 介面初始化與裝備
    # ==========================================
    def setup_statusbar(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()
        self.statusbar.addPermanentWidget(self.progress_bar)
        
        self.stat_label = QLabel(" 專案：未載入 | 班次：0 | 車輛數：0 ")
        self.statusbar.addPermanentWidget(self.stat_label)

    def update_progress(self, val):
        self.progress_bar.setValue(val)

    def setup_workspaces(self):
        while self.main_output.count() > 0:
            self.main_output.removeTab(0)
            
        self.opened_tabs = {}
    
    def open_or_switch_tab(self, tab_title, content_widget):
        if tab_title not in self.opened_tabs:
            from PySide6.QtWidgets import QWidget
            new_tab = QWidget()
            layout = QVBoxLayout(new_tab)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(content_widget)
            
            self.main_output.addTab(new_tab, tab_title)
            self.opened_tabs[tab_title] = new_tab 
            
        new_tab = self.opened_tabs[tab_title]
        target_index = self.main_output.indexOf(new_tab) 
        self.main_output.setCurrentIndex(target_index)
        
        if hasattr(content_widget, 'load_csv_direction') and getattr(content_widget, 'current_csv_path', None):
            json_path = os.path.join(self.engine.project_path, "train_levels.json")
            content_widget.load_csv_direction(
                content_widget.current_csv_path, 
                json_path, 
                content_widget.current_direction
            )

    def close_tab(self, index):
        tab_title = self.main_output.tabText(index)
        widget_to_remove = self.main_output.widget(index)
        
        self.main_output.removeTab(index)
        
        if tab_title in self.opened_tabs:
            del self.opened_tabs[tab_title]
            
        layout = widget_to_remove.layout()
        if layout and layout.count() > 0:
            item = layout.takeAt(0)
            content_widget = item.widget()
            if content_widget:
                content_widget.setParent(None)
                
        widget_to_remove.deleteLater() 

    def on_tab_changed(self, index):
        if index < 0: return
        
        tab_widget = self.main_output.widget(index)
        if not tab_widget: return
        
        layout = tab_widget.layout()
        if layout and layout.count() > 0:
            inner_widget = layout.itemAt(0).widget()
            
            widget_type = inner_widget.__class__.__name__
            if widget_type in ["StationMapWidget", "LineRoadmapWidget"]:
                if hasattr(inner_widget, "load_map"):
                    inner_widget.load_map()
            elif widget_type in ["ScheduleTableWidget", "TudTableWidget", "StationsTimetableWidget"]:
                if hasattr(inner_widget, "refresh_data"):
                    inner_widget.refresh_data()
                elif hasattr(inner_widget, "refresh"):
                    inner_widget.refresh()

    def refresh_project_list(self):
        self.line_Selection.clear() 
        env_dir = self.engine.env_path 
        projects = self.engine.scan_projects() 
        
        for proj_folder in projects:
            json_path = os.path.join(env_dir, proj_folder, "information.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        info = json.load(f)
                        display_name = info.get('路線名稱', proj_folder)
                        self.line_Selection.addItem(display_name, proj_folder)
                except:
                    self.line_Selection.addItem(proj_folder, proj_folder)
            else:
                self.line_Selection.addItem(proj_folder, proj_folder)
                
        if self.line_Selection.count() == 0:
            self.line_Selection.addItem("尚無路線，請新增", None)

    def bind_events(self):
        self.load_1.clicked.connect(self.action_load_project)
        self.do_schedule_1.clicked.connect(self.action_run_schedule)
        self.guide_treelist.itemClicked.connect(self.on_tree_item_clicked)
        
        if hasattr(self, 'add_line_1'): 
            self.add_line_1.clicked.connect(self.action_add_blank_line)
        if hasattr(self, 'add_line_csv_1'): 
            self.add_line_csv_1.clicked.connect(self.action_add_csv_line)
            
        if hasattr(self, 'add_line_m'): 
            self.add_line_m.triggered.connect(self.action_add_blank_line)
        if hasattr(self, 'add_line_csv_m'): 
            self.add_line_csv_m.triggered.connect(self.action_add_csv_line)

        if hasattr(self, 'delete_line_1'): 
            self.delete_line_1.clicked.connect(self.action_delete_line)
        if hasattr(self, 'delete_line_m'): 
            self.delete_line_m.triggered.connect(self.action_delete_line)
            
        if hasattr(self, 'clone_line_1'): 
            self.clone_line_1.clicked.connect(self.action_clone_line)
        if hasattr(self, 'clone_line_m'): 
            self.clone_line_m.triggered.connect(self.action_clone_line)

        if hasattr(self, 'import_stb_csv_1'):
            self.import_stb_csv_1.clicked.connect(self.action_import_stb_csv)
            
        if hasattr(self, 'import_stb_csv_m'):
            self.import_stb_csv_m.triggered.connect(self.action_import_stb_csv)
            
        if hasattr(self, 'open_save_folder_m'):
            self.open_save_folder_m.triggered.connect(self.action_open_save_folder)

        if hasattr(self, 'line_setting_1'):
            self.line_setting_1.clicked.connect(self.action_edit_line_setting)
        if hasattr(self, 'line_setting_m'):
            self.line_setting_m.triggered.connect(self.action_edit_line_setting)

        if hasattr(self, 'frequency_setting_1'):
            self.frequency_setting_1.clicked.connect(self.action_frequency_setting)
        if hasattr(self, 'frequency_setting_m'):
            self.frequency_setting_m.triggered.connect(self.action_frequency_setting)

    # ==========================================
    # 2. 核心交互邏輯 (Actions)
    # ==========================================
    
    def action_frequency_setting(self):
        if not getattr(self.engine, 'current_project', None):
            QMessageBox.warning(self, "警告", "請先載入一條路線，才能設定發車頻率。")
            return
            
        dialog = FrequencySettingWidget(self.engine, self)
        if dialog.exec():
            self.log_msg(f"✅ 路線 [{self.engine.current_project}] 的發車頻率設定已儲存！")

    def action_edit_line_setting(self):
        if not getattr(self.engine, 'current_project', None):
            QMessageBox.warning(self, "警告", "請先載入一條路線，才能修改設定。")
            return
            
        json_path = os.path.join(self.engine.project_path, "information.json")
        full_data = {}
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    full_data = json.load(f)
            except Exception as e:
                self.log_msg(f"⚠️ 讀取現有設定失敗，將開啟空白表單: {e}")
                
        dialog = RouteInfoDialog(self, full_data=full_data, is_edit_mode=True)
        if dialog.exec():
            updated_data = dialog.get_data()
            
            try:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(updated_data, f, ensure_ascii=False, indent=4)
                    
                self.log_msg(f"✅ 路線 [{self.engine.current_project}] 設定已成功更新！")
                
                self.current_loaded_route_name = updated_data.get("路線名稱", self.engine.current_project)
                self.update_line_color(updated_data.get("路線顏色", "#FFFFFF"))
                
                self.refresh_project_list()
                
                index = self.line_Selection.findData(self.engine.current_project)
                if index >= 0:
                    self.line_Selection.setCurrentIndex(index)
                    
            except Exception as e:
                self.log_msg(f"❌ 儲存路線設定時發生錯誤: {str(e)}")
                QMessageBox.critical(self, "錯誤", f"無法儲存設定：\n{str(e)}")

    def action_open_save_folder(self):
        save_dir = os.path.abspath(self.engine.workspace_root)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(save_dir))
        self.log_msg(f"📂 已開啟外部資料夾：{save_dir}")

    def action_add_blank_line(self):
        dialog = RouteInfoDialog(self)
        if dialog.exec():
            info_data = dialog.get_data()
            success, msg = self.engine.create_new_project(info_data)
            self.log_msg(msg)
            
            self.refresh_project_list() 
            index = self.line_Selection.findData(info_data['路線ID'])
            if index >= 0: 
                self.line_Selection.setCurrentIndex(index)
                self.action_load_project()

    def action_add_csv_line(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇基準運輸時刻表", "", "CSV Files (*.csv)")
        if not file_path:
            return 
            
        self.log_msg(f"正在解析 CSV 樣板：{os.path.basename(file_path)}...")
        
        start_st, end_st, count = self.engine.peek_csv_for_stations(file_path)
        
        if count == 0:
            QMessageBox.warning(self, "解析失敗", "無法從該 CSV 中讀取車站資訊，請確認檔案格式。")
            return
            
        prefill = {'start': start_st, 'end': end_st, 'count': count}
        
        dialog = RouteInfoDialog(self, prefill_data=prefill)
        if dialog.exec():
            info_data = dialog.get_data()
            
            success, msg = self.engine.create_new_project(info_data, template_csv_path=file_path)
            self.log_msg(msg)
            
            self.refresh_project_list()
            index = self.line_Selection.findData(info_data['路線ID'])
            if index >= 0: 
                self.line_Selection.setCurrentIndex(index)
                self.action_load_project()

    def action_delete_line(self):
        project_id = self.engine.current_project
        if not project_id:
            self.log_msg("⚠️ 尚未選擇路線，無法刪除。")
            return
            
        display_name = self.line_Selection.currentText()
            
        reply = QMessageBox.warning(self, "確認刪除", 
                                  f"您確定要刪除路線 [{display_name}] 嗎？\n此操作將永久刪除資料夾，無法復原！",
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                  
        if reply == QMessageBox.Yes:
            success, msg = self.engine.delete_project(project_id)
            self.log_msg(msg)
            
            self.refresh_project_list()
            self.update_line_color("#FFFFFF")
            self.stat_label.setText(" 專案：未載入 | 班次：0 | 車輛數：0 ")
            self.statusbar.showMessage("路線已刪除", 3000)
            
            while self.main_output.count() > 0:
                self.close_tab(0)

    def action_clone_line(self):
        source_id = self.engine.current_project
        if not source_id:
            self.log_msg("⚠️ 尚未選擇路線，無法複製。")
            return
            
        display_name = self.line_Selection.currentText()
            
        reply = QMessageBox.warning(self, "確認複製", 
                                  f"您即將複製路線 [{display_name}] 的所有檔案設定。\n是否繼續？",
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                                  
        if reply == QMessageBox.Yes:
            prefill = {}
            json_path = os.path.join(self.engine.project_path, "information.json")
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    prefill = json.load(f)
            
            dialog_prefill = {
                'start': prefill.get('起點', ''), 
                'end': prefill.get('終點', ''), 
                'count': prefill.get('車站數', '')
            }
            
            dialog = RouteInfoDialog(self, prefill_data=dialog_prefill)
            
            dialog.line_color_i.setText(prefill.get('路線顏色', '#0033A0'))
            dialog.line_country_i.setText(prefill.get('路線所在國家', ''))
            dialog.line_city_i.setText(prefill.get('路線經過城市', ''))
            dialog.line_type_i.setText(prefill.get('路線種類', ''))
            dialog.line_owner_i.setText(prefill.get('路線所有者', ''))
            dialog.line_operator_i.setText(prefill.get('路線營運者', ''))
            dialog.line_linetype_i.setText(prefill.get('線路數', ''))
            dialog.line_electric_i.setText(prefill.get('電氣化模式', ''))
            dialog.line_safety_i.setText(prefill.get('安全裝置', ''))
            dialog.line_speed_i.setText(prefill.get('最高營運速度', ''))
            
            dialog.interval_time_i.setText(str(prefill.get('發車間隔緩衝時間', 45)))
            dialog.stopping_time_stretching_c.setChecked(prefill.get('停靠時間可否拉伸', False))
            dialog.shift_step_i.setText(str(prefill.get('班次平移精度', 5)))
            
            t_first = QTime.fromString(prefill.get('首班車發車時間', '05:00:00'), "HH:mm:ss")
            if not t_first.isValid(): t_first = QTime(5, 0, 0)
            dialog.first_departure_t.setTime(t_first)
            
            t_last = QTime.fromString(prefill.get('末班車發車時間', '23:59:00'), "HH:mm:ss")
            if not t_last.isValid(): t_last = QTime(23, 59, 0)
            dialog.last_departure_t.setTime(t_last)
            
            dialog.line_name_i.setText("")
            dialog.line_id_i.setText("")
            
            if dialog.exec():
                new_info_data = dialog.get_data()
                new_id = new_info_data['路線ID']
                
                if os.path.exists(os.path.join(self.engine.env_path, new_id)):
                    QMessageBox.critical(self, "錯誤", f"路線 ID [{new_id}] 已存在！\n請使用不同的 ID，複製動作已取消。")
                    return
                
                success, msg = self.engine.clone_project(source_id, new_info_data)
                self.log_msg(msg)
                
                if success:
                    self.refresh_project_list()
                    index = self.line_Selection.findData(new_id)
                    if index >= 0:
                        self.line_Selection.setCurrentIndex(index)
                        self.action_load_project()

    def action_import_stb_csv(self):
        if not getattr(self.engine, 'current_project', None):
            QMessageBox.warning(self, "警告", "請先載入或新增一條路線，才能匯入時刻表。")
            return
            
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇要匯入的基準運輸時刻表", "", "CSV Files (*.csv)")
        if not file_path:
            return 
            
        display_name = self.current_loaded_route_name
        reply = QMessageBox.warning(self, "確認覆蓋", 
                                  f"您即將匯入新的時刻表至路線 [{display_name}]。\n\n"
                                  "警告：這將會完全覆蓋目前的「列車等級表」以及「上/下行時刻表」！\n"
                                  "是否確定要繼續？",
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                  
        if reply != QMessageBox.Yes:
            return
            
        self.log_msg(f"正在匯入並切割 CSV 樣板：{os.path.basename(file_path)}...")
        
        try:
            self.engine.process_and_split_timetable(
                template_csv_path=file_path, 
                project_id=self.engine.current_project, 
                project_path=self.engine.project_path
            )
            
            self.log_msg("✅ 時刻表匯入且分割成功！")
            self.statusbar.showMessage("時刻表更新成功", 3000)
            
            self.refresh_opened_stb_tabs()
            
        except Exception as e:
            self.log_msg(f"❌ 匯入失敗: {str(e)}")
            QMessageBox.critical(self, "錯誤", f"處理 CSV 時發生錯誤：\n{str(e)}")

    def refresh_opened_stb_tabs(self):
        if hasattr(self, 'stb_editor_up') and getattr(self.stb_editor_up, 'current_csv_path', None):
            json_path = os.path.join(self.engine.project_path, "train_levels.json")
            self.stb_editor_up.load_csv_direction(self.stb_editor_up.current_csv_path, json_path, "上行")
            
        if hasattr(self, 'stb_editor_down') and getattr(self.stb_editor_down, 'current_csv_path', None):
            json_path = os.path.join(self.engine.project_path, "train_levels.json")
            self.stb_editor_down.load_csv_direction(self.stb_editor_down.current_csv_path, json_path, "下行")
            
        if hasattr(self, 'train_levels_editor') and getattr(self.train_levels_editor, 'json_path', None):
            self.train_levels_editor.load_json(self.train_levels_editor.json_path)

    def load_project(self, project_name):
        self.engine.current_project = project_name
        self.current_loaded_route_name = project_name
        
        if self.engine.project_path:
            info_path = os.path.join(self.engine.project_path, "information.json")
            if os.path.exists(info_path):
                try:
                    with open(info_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.current_loaded_route_name = data.get("路線名稱", project_name)
                except Exception:
                    pass
                    
        self.setWindowTitle(f"Timetable_scheduler_v0.1 - {self.current_loaded_route_name}")
    
    def action_load_project(self):
        project_id = self.line_Selection.currentData()
        
        if not project_id:
            self.log_msg("⚠️ 目前沒有可載入的路線。請先使用新增路線功能。")
            self.update_line_color("#FFFFFF") 
            return
            
        self.load_project(project_id)
        
        json_path = os.path.join(self.engine.project_path, "information.json")
        display_name = project_id
        route_color = "#FFFFFF" 
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    display_name = info.get("路線名稱", project_id)
                    route_color = info.get("路線顏色", "#FFFFFF")
            except Exception:
                pass

        self.update_line_color(route_color)
        self.stat_label.setText(f" 專案：{display_name} | 班次：等待排班 | 車輛數：等待排班 ")
        self.statusbar.showMessage(f"路線 [{display_name}] 載入完成", 3000)
        
        self.guide_treelist.expandAll()
        self.log_msg(f"✅ 成功載入路線: {display_name}")

    # 🌟 核心進化：一鍵觸發 365天 (平日+假日) 全域排班！
    def action_run_schedule(self):
        if not getattr(self.engine, 'current_project', None):
            self.log_msg("⚠️ 請先載入路線專案！")
            QMessageBox.warning(self, "警告", "請先載入一條路線！")
            return

        up_csv = os.path.join(self.engine.project_path, "stb_up.csv")
        if not os.path.exists(up_csv):
            self.log_msg("❌ 錯誤：此路線尚未匯入基準運輸時刻表，無法執行模擬排班！")
            QMessageBox.warning(self, "缺少時刻表", "此路線尚未匯入基準運輸時刻表，無法執行模擬排班！\n請先匯入 CSV 檔。")
            return

        self.progress_bar.show()
        self.update_progress(0)
        
        # 直接跳出進度條，不需任何詢問
        self.progress_dialog = QProgressDialog(f"準備啟動全域環境 [365天全日] 排班...", "取消", 0, 100, self)
        self.progress_dialog.setWindowTitle(f"正在執行全環境模擬排班 (涵蓋平假日)")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)
        self.progress_dialog.resize(450, 120)

        # 啟動非同步排班工作者，強制指定 schedule_type="all" 來觸發雙核連發引擎
        self.sim_worker = SimulationWorker(self.engine, schedule_type="all")

        self.sim_worker.progress_update.connect(self.update_simulation_progress)
        self.sim_worker.simulation_finished.connect(self.on_simulation_finished)
        self.sim_worker.error_occurred.connect(self.on_simulation_error)

        self.progress_dialog.canceled.connect(self.sim_worker.terminate)
        self.sim_worker.start()

    def update_simulation_progress(self, val, msg):
        if hasattr(self, 'progress_bar'):
            self.progress_bar.setValue(val)
        
        if hasattr(self, 'log_msg'):
            self.log_msg(msg)
            
        if hasattr(self, 'progress_dialog') and self.progress_dialog is not None:
            self.progress_dialog.setValue(val)
            if val >= 100:
                self.progress_dialog.close()

    def on_simulation_finished(self, success, msg):
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.setValue(100)
            self.progress_dialog.close()

        self.progress_bar.hide()

        if success:
            QMessageBox.information(self, "排班成功", "全環境 365天 (平/假日) 排班與派車已全數完成！")
            self.statusbar.showMessage("✅ 全環境 365天排班與派車完成！", 5000)
            
            for idx in range(self.main_output.count()):
                self.on_tab_changed(idx)
                
            vehicles = len(self.engine.vehicles) if hasattr(self.engine, 'vehicles') else 0
            self.stat_label.setText(f" 專案：{self.engine.current_project} | 365天全日排班完成 | 假日運用 {vehicles}車 ")
            
        else:
            QMessageBox.warning(self, "排班中斷", "排班過程發生錯誤或中斷。")

    def on_simulation_error(self, err_msg):
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
        self.progress_bar.hide()
        
        if hasattr(self, 'log_msg'):
            self.log_msg(f"❌ 發生致命錯誤：\n{err_msg}")
            
        QMessageBox.critical(self, "嚴重錯誤", err_msg)
        self.statusbar.showMessage("❌ 排班發生例外錯誤！", 5000)


    def on_tree_item_clicked(self, item, column):
        node_name = item.text(0)

        if not getattr(self.engine, 'current_project', None):
            self.statusbar.showMessage("請先載入或新增一條路線", 2000)
            return
        
        current_route_name = getattr(self, 'current_loaded_route_name', self.engine.current_project)
        if not current_route_name:
            self.statusbar.showMessage("請先載入或新增一條路線", 2000)
            return

        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())
            return

        parent_item = item.parent()
        parent_name = parent_item.text(0) if parent_item else ""

        if parent_name == "環境設定":
            prefix = getattr(self.engine, 'current_env', 'env_default')
            tab_title = f"[{prefix}] {node_name}"
        elif parent_name in ["平日時刻表", "假日時刻表"]:
            tab_title = f"{current_route_name}-{parent_name[:2]}{node_name}"
        else:
            tab_title = f"{current_route_name}-{node_name}"
            
        self.statusbar.showMessage(f"正在開啟：{tab_title}", 2000)

        if parent_name == "環境設定":
            if node_name == "車站與車輛設施設置表":
                if not hasattr(self, 'stations_editor'):
                    from views.stations_facilities_editor import StationsFacilitiesEditorWidget
                    self.stations_editor = StationsFacilitiesEditorWidget()
                    self.stations_editor.set_engine(self.engine) 
                    
                if not os.path.exists(self.engine.station_file):
                    with open(self.engine.station_file, 'w', encoding='utf-8') as f: json.dump({}, f)
                self.stations_editor.load_json(self.engine.station_file)
                self.open_or_switch_tab(tab_title, self.stations_editor)

            elif node_name == "車站與車輛設施圖":
                self.statusbar.showMessage(f"功能 [{node_name}] 準備中...", 2000)
                
            elif node_name == "路線總圖":
                self.statusbar.showMessage(f"功能 [{node_name}] 準備中...", 2000)

            elif node_name == "直通路線設置表":
                if not hasattr(self, 'through_run_setting_widget'):
                    from views.through_run_setting import ThroughRunSettingWidget
                    self.through_run_setting_widget = ThroughRunSettingWidget()
                self.through_run_setting_widget.set_engine(self.engine)
                self.open_or_switch_tab(tab_title, self.through_run_setting_widget)

        elif parent_name == "路線基本設定":
            if node_name == "基本運輸時刻表(上行)":
                if not hasattr(self, 'stb_editor_up'):
                    self.stb_editor_up = STBEditorWidget()
                    self.stb_editor_up.set_engine(self.engine)
                csv_path = os.path.join(self.engine.project_path, "stb_up.csv")  
                json_path = os.path.join(self.engine.project_path, "train_levels.json") 
                self.stb_editor_up.load_csv_direction(csv_path, json_path, "上行")
                self.open_or_switch_tab(tab_title, self.stb_editor_up)
                
            elif node_name == "基本運輸時刻表(下行)":
                if not hasattr(self, 'stb_editor_down'):
                    self.stb_editor_down = STBEditorWidget()
                    self.stb_editor_down.set_engine(self.engine)
                csv_path = os.path.join(self.engine.project_path, "stb_down.csv") 
                json_path = os.path.join(self.engine.project_path, "train_levels.json") 
                self.stb_editor_down.load_csv_direction(csv_path, json_path, "下行")
                self.open_or_switch_tab(tab_title, self.stb_editor_down)
                
            elif node_name == "列車等級表":
                if not hasattr(self, 'train_levels_editor'):
                    from views.train_levels_editor import TrainLevelsEditorWidget
                    self.train_levels_editor = TrainLevelsEditorWidget()
                if self.engine.project_path:
                    json_path = os.path.join(self.engine.project_path, "train_levels.json")
                    self.train_levels_editor.load_json(json_path)
                    self.open_or_switch_tab(tab_title, self.train_levels_editor)
                    
            elif node_name == "發車頻率設定表":
                if not hasattr(self, 'freq_setting_widget'):
                    from views.frequency_setting import FrequencySettingWidget
                    self.freq_setting_widget = FrequencySettingWidget()
                
                self.freq_setting_widget.set_engine(self.engine)
                self.open_or_switch_tab(tab_title, self.freq_setting_widget)

        elif parent_name == "路線基本資訊":
            if node_name == "路線圖":
                if not hasattr(self, 'line_roadmap_widget'):
                    from views.line_roadmap import LineRoadmapWidget
                    self.line_roadmap_widget = LineRoadmapWidget()
                self.line_roadmap_widget.set_engine(self.engine)
                self.line_roadmap_widget.load_map() 
                self.open_or_switch_tab(tab_title, self.line_roadmap_widget)
                
            elif node_name == "車站配置圖":
                if not hasattr(self, 'station_map_widget'):
                    from views.station_map import StationMapWidget
                    self.station_map_widget = StationMapWidget()
                self.station_map_widget.set_engine(self.engine)
                self.station_map_widget.load_map() 
                self.open_or_switch_tab(tab_title, self.station_map_widget)
                
            elif node_name == "車輛動態圖":
                self.statusbar.showMessage(f"功能 [{node_name}] 準備中...", 2000)

        elif parent_name == "路線車輛設定":
            if node_name == "車輛資訊表":
                if not hasattr(self, 'trains_editor_widget'):
                    self.trains_editor_widget = TrainsEditorWidget()
                self.trains_editor_widget.set_engine(self.engine)
                self.trains_editor_widget.load_train_levels()
                self.trains_editor_widget.load_data()
                self.open_or_switch_tab(tab_title, self.trains_editor_widget)

        elif parent_name in ["平日時刻表", "假日時刻表"]:
            is_weekday = (parent_name == "平日時刻表")
            schedule_type = "weekdays" if is_weekday else "weekends"
            
            if node_name in ["上行班次時刻表", "下行班次時刻表"]:
                dir_suffix = "up" if node_name == "上行班次時刻表" else "down"
                filename = f"{schedule_type}_sch_{dir_suffix}.csv"
                attr_name = f"sch_table_{schedule_type}_{dir_suffix}"
                
                if not hasattr(self, attr_name):
                    from views.sch_table import ScheduleTableWidget
                    setattr(self, attr_name, ScheduleTableWidget())
                    
                widget = getattr(self, attr_name)
                if hasattr(widget, 'set_engine'): widget.set_engine(self.engine)
                csv_path = os.path.join(self.engine.project_path, filename) if self.engine.project_path else ""
                widget.load_csv(csv_path, tab_title)
                self.open_or_switch_tab(tab_title, widget)

            elif node_name == "車站時刻表":
                attr_name = f"stations_timetable_{schedule_type}"
                if not hasattr(self, attr_name):
                    from views.stations_timetable import StationsTimetableWidget
                    setattr(self, attr_name, StationsTimetableWidget())
                    
                widget = getattr(self, attr_name)
                widget.set_engine(self.engine, schedule_type)
                self.open_or_switch_tab(tab_title, widget)

            elif node_name == "車輛運用表":
                filename = f"{schedule_type}_tud.csv"
                attr_name = f"tud_table_{schedule_type}"
                
                if not hasattr(self, attr_name):
                    from views.tud_table import TudTableWidget
                    setattr(self, attr_name, TudTableWidget())
                    
                widget = getattr(self, attr_name)
                if hasattr(widget, 'set_engine'): widget.set_engine(self.engine)
                csv_path = os.path.join(self.engine.project_path, filename) if self.engine.project_path else ""
                widget.load_csv(csv_path, tab_title)
                self.open_or_switch_tab(tab_title, widget)

        else:
            self.statusbar.showMessage(f"功能 [{node_name}] 尚未實作或不適用", 2000)

    # ==========================================
    # 3. 輔助與渲染工具
    # ==========================================
    def log_msg(self, message):
        self.plainTextEdit.appendPlainText(message)
        scrollbar = self.plainTextEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_line_color(self, hex_color="#FFFFFF"):
        if not hex_color or not str(hex_color).startswith('#'):
            hex_color = "#FFFFFF"
            
        self.line_color_changer.setStyleSheet(f"background-color: {hex_color};")

# ==========================================
# 🌟 全能黑盒子防護網 (Crash Reporter)
# ==========================================
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_log.txt")

CRASH_LOG_FILE = open(LOG_FILE_PATH, "w", encoding="utf-8")
CRASH_LOG_FILE.write(f"{'='*50}\n")
CRASH_LOG_FILE.write(f"🚀 系統啟動時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
CRASH_LOG_FILE.write(f"{'='*50}\n")
CRASH_LOG_FILE.flush()

faulthandler.enable(CRASH_LOG_FILE)

def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    CRASH_LOG_FILE.write(f"\n[Python 嚴重錯誤]\n{error_msg}\n")
    CRASH_LOG_FILE.flush()
    
    print("【系統崩潰】發生未預期錯誤:\n", error_msg)
    app = QApplication.instance()
    if app:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("系統崩潰 (Crash Report)")
        msg_box.setText("系統發生未預期的錯誤，操作已中斷。")
        msg_box.setInformativeText("請查看專案目錄下的 system_log.txt")
        msg_box.setDetailedText(error_msg)
        msg_box.exec()

if __name__ == "__main__":
    sys.excepthook = global_exception_handler
    app = QApplication(sys.argv)

    window = TimetableApp()
    
    original_log_msg = window.log_msg
    def dual_logger(msg):
        original_log_msg(msg)  
        CRASH_LOG_FILE.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        CRASH_LOG_FILE.flush() 
        
    window.log_msg = dual_logger
    window.engine.logger = dual_logger

    window.show()
    exit_code = app.exec()
    
    CRASH_LOG_FILE.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🛑 系統正常關閉。\n")
    CRASH_LOG_FILE.close()
    sys.exit(exit_code)