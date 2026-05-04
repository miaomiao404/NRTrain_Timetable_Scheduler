import os
import json
import uuid
import copy
from PySide6.QtWidgets import (
    QWidget, QTableWidgetItem, QMessageBox, QGraphicsScene, 
    QGraphicsProxyWidget, QHBoxLayout, QLineEdit, QComboBox, 
    QSpinBox, QPushButton, QLabel, QFrame, QTableWidget, QAbstractItemView,
    QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QDialogButtonBox
)
from PySide6.QtCore import Qt, QRectF, QTimer, QSize
from PySide6.QtGui import QColor, QPen, QBrush, QPainterPath, QPainter, QFont, QIcon

from ui_py.ui_stations_facilities_editor import Ui_stations_facilities_frame

# ==========================================
# 節點類別對照表 (UI 顯示 <-> JSON 儲存)
# ==========================================
TYPE_MAP_UI2DB = {
    "一般車站": "station",
    "主要車站": "main_station",
    "車輛中心/車庫": "depot",
    "暫留線/儲車軌": "pocket_track"
}
TYPE_MAP_DB2UI = {v: k for k, v in TYPE_MAP_UI2DB.items()}


class StationsFacilitiesEditorWidget(QWidget, Ui_stations_facilities_frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.engine = None
        self.json_path = None
        self.stations_data = {}
        self.current_station_id = None
        self.used_lines_map = {}
        self.route_dir_map = {} 
        
        # 1. 初始化圖形畫布
        self.track_scene = QGraphicsScene(self)
        self.tracks_editor_view.setScene(self.track_scene)
        self.tracks_editor_view.setRenderHint(QPainter.Antialiasing)
        
        self.conn_scene = QGraphicsScene(self)
        self.connections_editor_view.setScene(self.conn_scene)
        self.connections_editor_view.setRenderHint(QPainter.Antialiasing)
        
        # 2. 初始化左側雙表格
        for lst in [self.stations_list, self.facilities_list]:
            lst.setColumnCount(1)
            lst.setHorizontalHeaderLabels(["節點名稱"])
            lst.horizontalHeader().setVisible(False)
            lst.horizontalHeader().setStretchLastSection(True)
            lst.verticalHeader().setVisible(False)
            lst.verticalHeader().setDefaultSectionSize(32) 
            lst.setSelectionBehavior(QAbstractItemView.SelectRows)
            lst.setAlternatingRowColors(True)
            lst.setShowGrid(False) 
        
        self.used_lines_editor.setReadOnly(True)
        self.station_id_editor.setReadOnly(True)
        
        # 3. 初始化下拉選單
        self.connection_side_box.clear()
        self.connection_side_box.addItems(["左", "右"])
        
        self.track_amount_selection_b.clear()
        self.track_amount_selection_b.addItems(["1(單線)", "2(複線)", "3", "4(複複線)", "5", "6", "7", "8"])
        self.track_amount_selection_b.setCurrentIndex(1)
        
        self.station_type_b.addItems(["一般車站", "主要車站", "車輛中心/車庫", "暫留線/儲車軌"])
        
        # 4. 綁定事件
        self.stations_list.itemSelectionChanged.connect(self.on_stations_list_selected)
        self.facilities_list.itemSelectionChanged.connect(self.on_facilities_list_selected)
        
        self.add_stations_b.clicked.connect(self.action_add_station)
        self.add_facilities_b.clicked.connect(self.action_add_facility)
        
        self.add_track_b.clicked.connect(self.action_add_track)
        self.add_connections_b.clicked.connect(self.action_add_connection)
        self.delete_station_b.clicked.connect(self.delete_station)
        
        self.station_name_editor.textChanged.connect(self.on_basic_info_changed)
        self.station_line_id_editor.textChanged.connect(self.on_line_id_changed)
        self.station_type_b.currentTextChanged.connect(self.on_type_changed)
        
        # 5. 綁定搜尋與過濾
        self.searching_b.clicked.connect(self.refresh_station_list)
        self.searching_bar.returnPressed.connect(self.refresh_station_list)
        self.line_filter_box.currentTextChanged.connect(self.refresh_station_list)
        self.reset_filter_b.clicked.connect(self.reset_filters)

    def set_engine(self, engine):
        self.engine = engine

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'resize_timer'):
            self.resize_timer.stop()
        else:
            self.resize_timer = QTimer(self)
            self.resize_timer.setSingleShot(True)
            self.resize_timer.timeout.connect(self.on_resize_timeout)
        self.resize_timer.start(100)

    def on_resize_timeout(self):
        if self.current_station_id:
            self.render_tracks_view()
            self.render_connections_view()

    # ==========================================
    # 資料存取與動態掃描 (🌟 自動洗淨壞檔機制)
    # ==========================================
    def load_json(self, json_path):
        self.json_path = json_path
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)
                    
                if isinstance(raw_data, dict):
                    # 🌟 核心修復：如果讀到舊版的 arrays 格式，進行無痛轉換
                    if "nodes" in raw_data or "connections" in raw_data:
                        normalized_data = {}
                        for node in raw_data.get("nodes", []):
                            if isinstance(node, dict):
                                nid = node.get("id")
                                if nid:
                                    normalized_data[nid] = {
                                        "name": node.get("name", ""),
                                        "type": node.get("type", "station"),
                                        "line_id": node.get("line_id", ""),
                                        "tracks": node.get("tracks", []),
                                        "connections": node.get("connections", [])
                                    }
                        self.stations_data = normalized_data
                        self.save_json() # 洗掉壞檔
                    else:
                        # 🌟 終極防呆：確保讀出來的所有節點真的都是「字典」，剔除不小心混入的 List
                        clean_data = {}
                        for k, v in raw_data.items():
                            if isinstance(v, dict):
                                clean_data[k] = v
                        self.stations_data = clean_data
                else:
                    self.stations_data = {}
                    
            except Exception:
                self.stations_data = {}
        else:
            self.stations_data = {}
            
        self.scan_used_lines()
        self.update_line_filter_options()
        self.refresh_station_list()
        self.update_connection_target_combo()

    def save_json(self):
        if self.json_path:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(self.stations_data, f, ensure_ascii=False, indent=4)

    def scan_used_lines(self):
        self.used_lines_map.clear()
        self.route_dir_map.clear()
        if not self.engine: return
        
        projects = self.engine.scan_projects()
        for proj in projects:
            proj_path = os.path.join(self.engine.env_path, proj)
            route_name = proj
            info_path = os.path.join(proj_path, "information.json")
            if os.path.exists(info_path):
                try:
                    with open(info_path, 'r', encoding='utf-8') as f:
                        route_name = json.load(f).get("路線名稱", proj)
                except: pass
            
            self.route_dir_map[route_name] = proj 
            for csv_name in ["stb_up.csv", "stb_down.csv"]:
                csv_path = os.path.join(proj_path, csv_name)
                if os.path.exists(csv_path):
                    try:
                        with open(csv_path, 'r', encoding='utf-8-sig') as f:
                            for line in f:
                                parts = line.strip().split(',')
                                if parts and parts[0] not in ["", "車站", "上行", "下行"]:
                                    st_name = parts[0].strip()
                                    if st_name not in self.used_lines_map:
                                        self.used_lines_map[st_name] = set()
                                    self.used_lines_map[st_name].add(route_name)
                    except: pass

    def get_grades_for_routes(self, route_ids_list):
        if not self.engine: return []
        
        if "all" in route_ids_list or not route_ids_list:
            return []
            
        grades_list = [] 
        
        for r_id in route_ids_list:
            r_name = next((k for k, v in self.route_dir_map.items() if v == r_id), r_id)
            json_path = os.path.join(self.engine.env_path, r_id, "train_levels.json")
            
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for g_id, g_info in data.items():
                            g_name = g_info.get("name", g_id) if isinstance(g_info, dict) else (g_info if isinstance(g_info, str) else str(g_id))
                            grades_list.append((f"{r_name}-上行-{g_name}", f"{r_id}:up_{g_id}"))
                            grades_list.append((f"{r_name}-下行-{g_name}", f"{r_id}:down_{g_id}"))
                except: pass
        return grades_list

    def update_line_filter_options(self):
        self.line_filter_box.blockSignals(True)
        self.line_filter_box.clear()
        self.line_filter_box.addItem("所有路線")
        for route in sorted(self.route_dir_map.keys()):
            self.line_filter_box.addItem(route)
        self.line_filter_box.blockSignals(False)

    def reset_filters(self):
        self.searching_bar.setText("")
        self.line_filter_box.blockSignals(True)
        self.line_filter_box.setCurrentIndex(0)
        self.line_filter_box.blockSignals(False)
        self.refresh_station_list()

    def get_node_used_lines(self, node_id):
        st_data = self.stations_data.get(node_id, {})
        st_name = st_data.get("name", "")
        st_type = st_data.get("type", "station")
        
        if st_type in ["depot", "pocket_track"]:
            used_by = set()
            for conn in st_data.get("connections", []):
                if conn.get("side") == "facility":
                    t_id = conn.get("target_station")
                    t_name = self.stations_data.get(t_id, {}).get("name", "")
                    if t_name:
                        used_by.update(self.used_lines_map.get(t_name, set()))
            return used_by
        else:
            return self.used_lines_map.get(st_name, set()) if st_name else set()

    # ==========================================
    # 複選視窗與 UI 工具
    # ==========================================
    def open_multi_select_dialog(self, title, options_dict, current_selections):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(250, 300)
        layout = QVBoxLayout(dialog)
        
        list_widget = QListWidget()
        layout.addWidget(list_widget)
        
        all_item = QListWidgetItem("無限制 (全部允許)")
        all_item.setFlags(all_item.flags() | Qt.ItemIsUserCheckable)
        all_item.setCheckState(Qt.Checked if "all" in current_selections or not current_selections else Qt.Unchecked)
        list_widget.addItem(all_item)
        
        for display_txt, internal_id in options_dict.items():
            item = QListWidgetItem(display_txt)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            state = Qt.Checked if internal_id in current_selections and "all" not in current_selections else Qt.Unchecked
            item.setCheckState(state)
            item.setData(Qt.UserRole, internal_id) 
            list_widget.addItem(item)
            
        def on_item_changed(item):
            list_widget.blockSignals(True)
            if item == all_item and item.checkState() == Qt.Checked:
                for i in range(1, list_widget.count()):
                    list_widget.item(i).setCheckState(Qt.Unchecked)
            elif item != all_item and item.checkState() == Qt.Checked:
                all_item.setCheckState(Qt.Unchecked)
            list_widget.blockSignals(False)
            
        list_widget.itemChanged.connect(on_item_changed)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        layout.addWidget(btn_box)
        
        if dialog.exec():
            if all_item.checkState() == Qt.Checked:
                return ["all"]
            else:
                res = [list_widget.item(i).data(Qt.UserRole) for i in range(1, list_widget.count()) if list_widget.item(i).checkState() == Qt.Checked]
                return res if res else ["all"]
        return None

    def format_multi_select_text(self, selected_list, options_dict):
        if not selected_list or "all" in selected_list:
            return "無限制"
        if len(selected_list) == 1:
            internal = selected_list[0]
            display = next((k for k, v in options_dict.items() if v == internal), internal)
            return display[:7] + ".." if len(display) > 7 else display
        return f"已選 {len(selected_list)} 項"

    # ==========================================
    # UI 清單邏輯與自訂儲存格元件
    # ==========================================
    def safe_clear_scene(self, scene):
        if not scene: return
        for item in scene.items():
            if isinstance(item, QGraphicsProxyWidget):
                w = item.widget()
                if w: w.blockSignals(True)
                item.setWidget(None)
                if w: w.deleteLater()
        scene.clear()

    def clear_editor_panel(self):
        self.current_station_id = None
        self.station_name_editor.setText("")
        self.station_id_editor.setText("")
        self.station_line_id_editor.setText("")
        self.used_lines_editor.setText("")
        self.station_type_b.blockSignals(True)
        self.station_type_b.setCurrentIndex(0)
        self.station_type_b.blockSignals(False)
        self.safe_clear_scene(self.track_scene)
        self.safe_clear_scene(self.conn_scene)

    def create_station_list_widget(self, display_name, line_ids, st_type):
        w = QWidget()
        w.setStyleSheet("background: transparent;") 
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 2, 5, 2)
        layout.setSpacing(6)

        color_block = QFrame()
        color_block.setFixedWidth(4)
        if st_type in ["main_station", "depot"]:
            color_block.setStyleSheet("background-color: #aaffff; border-radius: 2px;")
        else:
            color_block.setStyleSheet("background-color: transparent;")
        color_block.setAttribute(Qt.WA_TransparentForMouseEvents) 

        name_lbl = QLabel(display_name)
        name_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        line_lbl = QLabel(line_ids)
        line_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        line_lbl.setStyleSheet("color: #2980b9; font-weight: bold;")
        line_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)

        layout.addWidget(color_block)     
        layout.addWidget(name_lbl)        
        layout.addStretch()               
        layout.addWidget(line_lbl)        
        return w

    def refresh_station_list(self):
        search_text = self.searching_bar.text().strip().lower()
        selected_route = self.line_filter_box.currentText()
        
        self.stations_list.setRowCount(0)
        self.facilities_list.setRowCount(0)
        
        for st_id, st_info in self.stations_data.items():
            if not isinstance(st_info, dict):
                continue
                
            st_type = st_info.get("type", "station")
            st_name = st_info.get("name", "")
            display_name = st_name if st_name else f"(未命名) [{st_id}]"
            line_ids = st_info.get("line_id", "")
            
            if search_text and search_text not in display_name.lower() and search_text not in line_ids.lower(): 
                continue
                
            if selected_route and selected_route != "所有路線":
                used_by = self.get_node_used_lines(st_id)
                if selected_route not in used_by: continue
            
            item = QTableWidgetItem()
            item.setData(Qt.UserRole, st_id)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            
            custom_widget = self.create_station_list_widget(display_name, line_ids, st_type)
            
            if st_type in ["station", "main_station"]:
                row = self.stations_list.rowCount()
                self.stations_list.insertRow(row)
                self.stations_list.setItem(row, 0, item)
                self.stations_list.setCellWidget(row, 0, custom_widget)
            else:
                row = self.facilities_list.rowCount()
                self.facilities_list.insertRow(row)
                self.facilities_list.setItem(row, 0, item)
                self.facilities_list.setCellWidget(row, 0, custom_widget)

    def reselect_node(self, node_id):
        for lst in [self.stations_list, self.facilities_list]:
            for row in range(lst.rowCount()):
                item = lst.item(row, 0)
                if item and item.data(Qt.UserRole) == node_id:
                    lst.blockSignals(True)
                    lst.selectRow(row)
                    lst.blockSignals(False)
                    return

    def on_stations_list_selected(self):
        selected_items = self.stations_list.selectedItems()
        if selected_items:
            self.facilities_list.blockSignals(True)
            self.facilities_list.clearSelection()
            self.facilities_list.blockSignals(False)
            self.load_node_data(selected_items[0].data(Qt.UserRole))
        else:
            if not self.facilities_list.selectedItems(): self.clear_editor_panel()

    def on_facilities_list_selected(self):
        selected_items = self.facilities_list.selectedItems()
        if selected_items:
            self.stations_list.blockSignals(True)
            self.stations_list.clearSelection()
            self.stations_list.blockSignals(False)
            self.load_node_data(selected_items[0].data(Qt.UserRole))
        else:
            if not self.stations_list.selectedItems(): self.clear_editor_panel()

    def load_node_data(self, node_id):
        self.current_station_id = node_id
        st_data = self.stations_data[self.current_station_id]
        st_name = st_data.get("name", "")
        st_type = st_data.get("type", "station")
        is_facility = st_type in ["depot", "pocket_track"]
        
        self.station_id_editor.setText(node_id)
        self.station_name_editor.setText(st_name)
        
        self.station_line_id_editor.blockSignals(True)
        self.station_line_id_editor.setText(st_data.get("line_id", ""))
        self.station_line_id_editor.blockSignals(False)
        
        self.station_type_b.blockSignals(True)
        ui_type = TYPE_MAP_DB2UI.get(st_type, "一般車站")
        self.station_type_b.setCurrentText(ui_type)
        self.station_type_b.blockSignals(False)
        
        self.connection_side_box.setVisible(not is_facility)
        self.track_amount_selection_b.setVisible(not is_facility)
        self.add_track_b.setVisible(not is_facility)
        
        for child in self.findChildren(QLabel):
            if child.text() in ["連接位置", "軌道數量"]:
                child.setVisible(not is_facility)
        
        used_by = self.get_node_used_lines(node_id)
        if used_by: self.used_lines_editor.setText(", ".join(sorted(used_by)))
        else: self.used_lines_editor.setText("無")
        
        self.render_tracks_view()
        self.render_connections_view()

    # ==========================================
    # 資料變更與新增刪除
    # ==========================================
    def action_add_station(self):
        new_id = self.add_stations_id_editor.text().strip()
        if not new_id: return QMessageBox.warning(self, "警告", "請輸入車站 ID！")
        if new_id in self.stations_data: return QMessageBox.warning(self, "警告", f"ID '{new_id}' 已存在！")
        self.stations_data[new_id] = {"name": "", "type": "station", "line_id": "", "tracks": [], "connections": []}
        self.add_stations_id_editor.clear()
        self.save_json()
        self.reset_filters() 
        self.load_node_data(new_id)
        self.reselect_node(new_id)
        self.update_connection_target_combo()

    def action_add_facility(self):
        new_id = self.add_facilities_id_editor.text().strip()
        if not new_id: return QMessageBox.warning(self, "警告", "請輸入設施 ID！")
        if new_id in self.stations_data: return QMessageBox.warning(self, "警告", f"ID '{new_id}' 已存在！")
        # 🌟 設施新建時也自動帶入預設的 allowed_routes
        self.stations_data[new_id] = {
            "name": "", "type": "depot", "line_id": "", 
            "tracks": [{"id": f"T_{uuid.uuid4().hex[:6].upper()}", "name": "儲車軌", "capacity": 10, "allowed_routes": ["all"]}], 
            "connections": []
        }
        self.add_facilities_id_editor.clear()
        self.save_json()
        self.reset_filters()
        self.load_node_data(new_id)
        self.reselect_node(new_id)
        self.update_connection_target_combo()

    def on_type_changed(self, new_type_ui):
        if not self.current_station_id: return
        new_type_db = TYPE_MAP_UI2DB.get(new_type_ui, "station")
        old_type_db = self.stations_data[self.current_station_id].get("type", "station")
        
        if new_type_db != old_type_db:
            was_facility = old_type_db in ["depot", "pocket_track"]
            is_facility = new_type_db in ["depot", "pocket_track"]
            
            if was_facility != is_facility:
                used_by = self.get_node_used_lines(self.current_station_id)
                if used_by:
                    st_name = self.stations_data[self.current_station_id].get("name", "未知")
                    QMessageBox.critical(self, "禁止轉換", 
                                         f"節點「{st_name}」目前正被以下時刻表使用：\n\n"
                                         f"{', '.join(used_by)}\n\n"
                                         "車站與設施的內部資料結構不同，若被時刻表使用中禁止跨越類別轉換！\n"
                                         "請先從所有相關時刻表中移除該站。")
                    
                    self.station_type_b.blockSignals(True)
                    self.station_type_b.setCurrentText(TYPE_MAP_DB2UI.get(old_type_db, "一般車站"))
                    self.station_type_b.blockSignals(False)
                    return
            
            self.stations_data[self.current_station_id]["type"] = new_type_db
            
            if was_facility != is_facility:
                for sid, sdata in self.stations_data.items():
                    if "connections" in sdata:
                        sdata["connections"] = [c for c in sdata["connections"] if c.get("target_station") != self.current_station_id]
                
                self.stations_data[self.current_station_id]["connections"] = []
                
                if is_facility:
                    self.stations_data[self.current_station_id]["tracks"] = [{
                        "id": f"T_{uuid.uuid4().hex[:6].upper()}",
                        "name": "儲車軌",
                        "capacity": 10,
                        "allowed_routes": ["all"]
                    }]
                else:
                    self.stations_data[self.current_station_id]["tracks"] = []
                    
            self.save_json()
            self.refresh_station_list()
            self.update_connection_target_combo()
            self.reselect_node(self.current_station_id)

    def on_basic_info_changed(self):
        if not self.current_station_id: return
        new_name = self.station_name_editor.text().strip()
        self.stations_data[self.current_station_id]["name"] = new_name
        
        st_type = self.stations_data[self.current_station_id].get("type", "station")
        target_list = self.stations_list if st_type in ["station", "main_station"] else self.facilities_list
        
        for row in range(target_list.rowCount()):
            item = target_list.item(row, 0)
            if item and item.data(Qt.UserRole) == self.current_station_id:
                w = target_list.cellWidget(row, 0)
                if w:
                    name_lbl = w.layout().itemAt(1).widget()
                    name_lbl.setText(new_name if new_name else f"(未命名) [{self.current_station_id}]")
                break
                
        self.save_json()
        self.render_connections_view()
        self.update_connection_target_combo()

    def on_line_id_changed(self):
        if not self.current_station_id: return
        new_line_id = self.station_line_id_editor.text().strip()
        self.stations_data[self.current_station_id]["line_id"] = new_line_id
        
        st_type = self.stations_data[self.current_station_id].get("type", "station")
        target_list = self.stations_list if st_type in ["station", "main_station"] else self.facilities_list
        
        for row in range(target_list.rowCount()):
            item = target_list.item(row, 0)
            if item and item.data(Qt.UserRole) == self.current_station_id:
                w = target_list.cellWidget(row, 0)
                if w:
                    line_lbl = w.layout().itemAt(3).widget()
                    line_lbl.setText(new_line_id)
                break
                
        self.save_json()
        self.render_connections_view()

    def delete_station(self):
        if not self.current_station_id: return
        
        used_by = self.get_node_used_lines(self.current_station_id)
        st_name = self.stations_data[self.current_station_id].get("name", "未知")
        
        if used_by:
            QMessageBox.critical(self, "禁止刪除", f"節點「{st_name}」目前正被以下時刻表使用：\n\n{', '.join(used_by)}\n\n請先移除或解除綁定才能刪除！")
            return
            
        reply = QMessageBox.warning(self, "確認刪除", f"確定要永久刪除這個節點嗎？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for sid, sdata in self.stations_data.items():
                if "connections" in sdata:
                    sdata["connections"] = [c for c in sdata["connections"] if c.get("target_station") != self.current_station_id]
            del self.stations_data[self.current_station_id]
            self.save_json()
            self.clear_editor_panel()
            self.refresh_station_list()
            self.update_connection_target_combo()

    # ==========================================
    # 本站股道與設施儲車軌編輯區
    # ==========================================
    def get_track_icon_path(self, state):
        if state == "cross": return "assets/stations_facilities_editor/cross_track.svg"
        return f"assets/stations_facilities_editor/{state}_arrow_track.svg"

    def cycle_track_signal(self, track_id, side):
        states = ["double", "left", "right", "cross"]
        track = next((t for t in self.stations_data[self.current_station_id]["tracks"] if t["id"] == track_id), None)
        if track:
            key = f"{side}_signal"
            current = track.get(key, "double")
            idx = states.index(current) if current in states else 0
            track[key] = states[(idx + 1) % len(states)]
            self.save_json()
            QTimer.singleShot(0, self.render_tracks_view)

    def cycle_track_platform(self, track_id):
        states = ["上側", "下側", "兩側", "無月台"]
        track = next((t for t in self.stations_data[self.current_station_id]["tracks"] if t["id"] == track_id), None)
        if track:
            current = track.get("platform_pos", "上側")
            mapping = {"upper side": "上側", "lower side": "下側", "double side": "兩側", "no platform": "無月台"}
            current = mapping.get(current, current)
            idx = states.index(current) if current in states else 0
            track["platform_pos"] = states[(idx + 1) % len(states)]
            self.save_json()
            QTimer.singleShot(0, self.render_tracks_view)

    def update_track_name(self, track_id, new_name):
        track = next((t for t in self.stations_data[self.current_station_id]["tracks"] if t["id"] == track_id), None)
        if track:
            track["name"] = new_name
            self.save_json()

    def update_track_capacity(self, track_id, capacity):
        track = next((t for t in self.stations_data[self.current_station_id]["tracks"] if t["id"] == track_id), None)
        if track:
            track["capacity"] = capacity
            self.save_json()

    def on_track_route_btn_clicked(self, track_id):
        track = next((t for t in self.stations_data[self.current_station_id]["tracks"] if t["id"] == track_id), None)
        if not track: return
        
        curr_routes = track.get("allowed_routes", track.get("allowed_route", ["all"]))
        if isinstance(curr_routes, str): curr_routes = ["all"] if curr_routes in ["無限制", "all"] else [curr_routes]
            
        used_routes = sorted(list(self.get_node_used_lines(self.current_station_id)))
        options_dict = {r_name: self.route_dir_map.get(r_name, r_name) for r_name in used_routes}
        
        selected = self.open_multi_select_dialog("選擇允許停靠路線", options_dict, curr_routes)
        if selected is not None:
            track["allowed_routes"] = selected
            track["allowed_grades"] = ["all"]
            self.save_json()
            QTimer.singleShot(0, self.render_tracks_view)

    # 🌟 新增：專為設施儲車軌設計的全環境路線選擇
    def on_facility_track_route_btn_clicked(self, track_id):
        track = next((t for t in self.stations_data[self.current_station_id]["tracks"] if t["id"] == track_id), None)
        if not track: return
        
        curr_routes = track.get("allowed_routes", ["all"])
        if isinstance(curr_routes, str): curr_routes = ["all"] if curr_routes in ["無限制", "all"] else [curr_routes]
            
        # 抓取「全環境」的所有路線，而不是只有該車站相關的路線
        all_routes = sorted(list(self.route_dir_map.keys()))
        options_dict = {r_name: self.route_dir_map[r_name] for r_name in all_routes}
        
        selected = self.open_multi_select_dialog("選擇允許使用路線", options_dict, curr_routes)
        if selected is not None:
            track["allowed_routes"] = selected
            self.save_json()
            QTimer.singleShot(0, self.render_tracks_view)

    def on_track_grade_btn_clicked(self, track_id):
        track = next((t for t in self.stations_data[self.current_station_id]["tracks"] if t["id"] == track_id), None)
        if not track: return
        
        curr_routes = track.get("allowed_routes", track.get("allowed_route", ["all"]))
        if isinstance(curr_routes, str): curr_routes = ["all"] if curr_routes in ["無限制", "all"] else [curr_routes]
        
        curr_grades = track.get("allowed_grades", track.get("allowed_grade", ["all"]))
        if isinstance(curr_grades, str): curr_grades = ["all"] if curr_grades in ["無限制", "all"] else [curr_grades]
        
        grades_data = self.get_grades_for_routes(curr_routes)
        options_dict = {display: internal for display, internal in grades_data}
        
        selected = self.open_multi_select_dialog("選擇允許停靠等級", options_dict, curr_grades)
        if selected is not None:
            track["allowed_grades"] = selected
            self.save_json()
            QTimer.singleShot(0, self.render_tracks_view)

    def delete_track(self, track_id):
        if not self.current_station_id: return
        tracks = self.stations_data[self.current_station_id].get("tracks", [])
        self.stations_data[self.current_station_id]["tracks"] = [t for t in tracks if t["id"] != track_id]
        self.save_json()
        QTimer.singleShot(0, self.render_tracks_view)

    def render_tracks_view(self):
        self.safe_clear_scene(self.track_scene)
        if not self.current_station_id: return
        
        st_type = self.stations_data[self.current_station_id].get("type", "station")
        is_facility = st_type in ["depot", "pocket_track"]
        tracks = self.stations_data[self.current_station_id].get("tracks", [])
        
        y_offset = 30
        view_width = max(900, self.tracks_editor_view.viewport().width())
        widget_width = view_width - 40 
        
        if is_facility:
            for idx_row, track in enumerate(tracks):
                control_widget = QWidget()
                layout = QHBoxLayout(control_widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(10)
                
                layout.addStretch(1)
                
                lbl_name = QLabel("設施/股道名稱:")
                lbl_name.setFixedHeight(26)
                layout.addWidget(lbl_name)
                
                name_input = QLineEdit(track.get("name", "儲車軌"))
                name_input.setFixedWidth(100)
                name_input.setFixedHeight(26)
                name_input.textChanged.connect(lambda t, tid=track["id"]: self.update_track_name(tid, t))
                layout.addWidget(name_input)
                
                layout.addSpacing(15)
                
                # 🌟 新增：設施專用的「允許路線」選擇 UI
                lbl_route = QLabel("允許路線:")
                lbl_route.setFixedHeight(26)
                layout.addWidget(lbl_route)
                
                route_btn = QPushButton()
                route_btn.setFixedHeight(26)
                route_btn.setMinimumWidth(80) 
                
                all_routes = sorted(list(self.route_dir_map.keys()))
                route_options = {r_name: self.route_dir_map[r_name] for r_name in all_routes}
                
                curr_routes = track.get("allowed_routes", ["all"])
                if isinstance(curr_routes, str): curr_routes = ["all"] if curr_routes in ["無限制", "all"] else [curr_routes]
                
                route_btn.setText(self.format_multi_select_text(curr_routes, route_options))
                route_btn.clicked.connect(lambda _, tid=track["id"]: self.on_facility_track_route_btn_clicked(tid))
                layout.addWidget(route_btn)
                
                layout.addSpacing(15)
                
                lbl_cap = QLabel("容納車輛數:")
                lbl_cap.setFixedHeight(26)
                layout.addWidget(lbl_cap)
                
                cap_spin = QSpinBox()
                cap_spin.setFixedHeight(26)
                cap_spin.setRange(1, 999)
                cap_spin.setValue(track.get("capacity", 10))
                cap_spin.setSuffix(" 輛")
                cap_spin.valueChanged.connect(lambda v, tid=track["id"]: self.update_track_capacity(tid, v))
                layout.addWidget(cap_spin)
                
                layout.addStretch(1)
                
                del_btn = QPushButton("❌")
                del_btn.setFixedSize(32, 26)
                del_btn.setStyleSheet("color: #e74c3c; font-weight: bold; border: 1px solid #e74c3c; border-radius: 4px; background-color: white;")
                del_btn.clicked.connect(lambda _, tid=track["id"]: self.delete_track(tid))
                layout.addWidget(del_btn)
                
                proxy = self.track_scene.addWidget(control_widget)
                proxy.setPos(20, y_offset)
                proxy.resize(widget_width, 30)
                y_offset += 45
            self.track_scene.setSceneRect(0, 0, view_width, y_offset + 20)
            return

        for idx_row, track in enumerate(tracks):
            plat_pos = track.get("platform_pos", "上側")
            mapping = {"upper side": "上側", "lower side": "下側", "double side": "兩側", "no platform": "無月台"}
            plat_pos = mapping.get(plat_pos, plat_pos)
            left_sig = track.get("left_signal", "double")
            right_sig = track.get("right_signal", "double")
            
            UI_HEIGHT, PLAT_HEIGHT, PLAT_GAP = 26, 12, 24
            plat_brush, plat_pen = QBrush(QColor("#bdc3c7")), QPen(Qt.NoPen)
            plat_width = widget_width - 120 
            center_x = 20 + (widget_width / 2)
            plat_x = center_x - (plat_width / 2)
            
            if plat_pos in ["上側", "兩側"]:
                rect = self.track_scene.addRect(plat_x, y_offset - PLAT_HEIGHT, plat_width, PLAT_HEIGHT, plat_pen, plat_brush)
                rect.setZValue(-1) 
            if plat_pos in ["下側", "兩側"]:
                rect = self.track_scene.addRect(plat_x, y_offset + UI_HEIGHT, plat_width, PLAT_HEIGHT, plat_pen, plat_brush)
                rect.setZValue(-1) 
                
            control_widget = QWidget()
            layout = QHBoxLayout(control_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(4)
            
            def make_hline(is_visible=True):
                line = QFrame()
                line.setFixedHeight(6) 
                line.setStyleSheet("background-color: #7f8c8d; border-radius: 3px;" if is_visible else "background-color: transparent;")
                return line
                
            layout.addWidget(make_hline(left_sig != "cross"), stretch=1)
            btn1 = QPushButton()
            btn1.setIcon(QIcon(self.get_track_icon_path(left_sig)))
            btn1.setIconSize(QSize(20, 20)) 
            btn1.setFixedSize(32, UI_HEIGHT) 
            btn1.clicked.connect(lambda _, tid=track["id"]: self.cycle_track_signal(tid, "left"))
            layout.addWidget(btn1)
            
            layout.addWidget(make_hline(True), stretch=1)
            
            lbl_name = QLabel("股道:")
            lbl_name.setFixedHeight(UI_HEIGHT)
            layout.addWidget(lbl_name)
            name_input = QLineEdit(track.get("name", "股道"))
            name_input.setFixedWidth(50)
            name_input.setFixedHeight(UI_HEIGHT)
            name_input.setAlignment(Qt.AlignCenter)
            name_input.textChanged.connect(lambda t, tid=track["id"]: self.update_track_name(tid, t))
            layout.addWidget(name_input)
            layout.addSpacing(5)
            
            lbl_plat = QLabel("月台:")
            lbl_plat.setFixedHeight(UI_HEIGHT)
            layout.addWidget(lbl_plat)
            btn2 = QPushButton(plat_pos)
            btn2.setFixedSize(60, UI_HEIGHT)
            btn2.clicked.connect(lambda _, tid=track["id"]: self.cycle_track_platform(tid))
            layout.addWidget(btn2)
            layout.addSpacing(5)
            
            lbl_route = QLabel("路線:")
            lbl_route.setFixedHeight(UI_HEIGHT)
            layout.addWidget(lbl_route)
            
            route_btn = QPushButton()
            route_btn.setFixedHeight(UI_HEIGHT)
            route_btn.setMinimumWidth(80) 
            
            used_routes = sorted(list(self.get_node_used_lines(self.current_station_id)))
            route_options = {r_name: self.route_dir_map.get(r_name, r_name) for r_name in used_routes}
            
            curr_routes = track.get("allowed_routes", track.get("allowed_route", ["all"]))
            if isinstance(curr_routes, str): curr_routes = ["all"] if curr_routes in ["無限制", "all"] else [curr_routes]
            
            route_btn.setText(self.format_multi_select_text(curr_routes, route_options))
            route_btn.clicked.connect(lambda _, tid=track["id"]: self.on_track_route_btn_clicked(tid))
            layout.addWidget(route_btn)
            layout.addSpacing(5)
            
            lbl_grade = QLabel("等級:")
            lbl_grade.setFixedHeight(UI_HEIGHT)
            layout.addWidget(lbl_grade)
            
            grade_btn = QPushButton()
            grade_btn.setFixedHeight(UI_HEIGHT)
            grade_btn.setMinimumWidth(100) 
            
            grades_data = self.get_grades_for_routes(curr_routes)
            grade_options = {display: internal for display, internal in grades_data}
            
            curr_grades = track.get("allowed_grades", track.get("allowed_grade", ["all"]))
            if isinstance(curr_grades, str): curr_grades = ["all"] if curr_grades in ["無限制", "all"] else [curr_grades]
            
            grade_btn.setText(self.format_multi_select_text(curr_grades, grade_options))
            grade_btn.clicked.connect(lambda _, tid=track["id"]: self.on_track_grade_btn_clicked(tid))
            layout.addWidget(grade_btn)
            
            layout.addWidget(make_hline(True), stretch=1) 
            btn3 = QPushButton()
            btn3.setIcon(QIcon(self.get_track_icon_path(right_sig)))
            btn3.setIconSize(QSize(20, 20))
            btn3.setFixedSize(32, UI_HEIGHT)
            btn3.clicked.connect(lambda _, tid=track["id"]: self.cycle_track_signal(tid, "right"))
            layout.addWidget(btn3)
            layout.addWidget(make_hline(right_sig != "cross"), stretch=1) 
            
            del_btn = QPushButton("❌")
            del_btn.setFixedSize(32, UI_HEIGHT)
            del_btn.setStyleSheet("color: #e74c3c; font-weight: bold; border: 1px solid #e74c3c; border-radius: 4px; background-color: white;")
            del_btn.clicked.connect(lambda _, tid=track["id"]: self.delete_track(tid))
            layout.addWidget(del_btn)
            
            proxy = self.track_scene.addWidget(control_widget)
            proxy.setZValue(100 - idx_row) 
            proxy.setPos(20, y_offset)
            proxy.resize(widget_width, UI_HEIGHT)
            
            y_offset += (UI_HEIGHT + PLAT_GAP) 
            
        self.track_scene.setSceneRect(0, 0, view_width, y_offset + 20)

    def action_add_track(self):
        if not self.current_station_id: return
        st_data = self.stations_data[self.current_station_id]
        
        if "tracks" not in st_data: st_data["tracks"] = []
        
        new_track = {
            "id": f"T_{uuid.uuid4().hex[:6].upper()}",
            "name": f"新股道 {len(st_data['tracks']) + 1}",
            "left_signal": "double",
            "right_signal": "double",
            "platform_pos": "上側",
            "allowed_routes": ["all"],
            "allowed_grades": ["all"],
            "capacity": 1
        }
            
        st_data["tracks"].append(new_track)
        self.save_json()
        QTimer.singleShot(0, self.render_tracks_view)

    # ==========================================
    # 連線編輯區：自動合併、平行線條與設施綁定
    # ==========================================
    def get_conn_icon_path(self, state):
        return f"assets/stations_facilities_editor/{state}_arrow_connection.svg"

    def update_connection_target_combo(self):
        self.connect_line_selection_box.blockSignals(True)
        self.connect_line_selection_box.clear()
        
        for st_id, st_info in self.stations_data.items():
            if not isinstance(st_info, dict): continue
            st_type = st_info.get("type", "station")
            if st_type in ["station", "main_station"]:
                name = st_info.get("name", "")
                display = name if name else f"(未命名) [{st_id}]"
                self.connect_line_selection_box.addItem(display, userData=st_id)
                
        self.connect_line_selection_box.blockSignals(False)

    def cycle_conn_track_signal(self, conn_id, track_idx):
        states = ["double", "right", "left"]
        for st_data in self.stations_data.values():
            if not isinstance(st_data, dict): continue
            for c in st_data.get("connections", []):
                if c["id"] == conn_id and "tracks" in c:
                    current = c["tracks"][track_idx].get("dir", "double")
                    idx = states.index(current) if current in states else 0
                    c["tracks"][track_idx]["dir"] = states[(idx + 1) % len(states)]
        self.save_json()
        QTimer.singleShot(0, self.render_connections_view)

    def on_conn_route_btn_clicked(self, conn_id, track_idx):
        curr_routes = ["all"]
        for c in self.stations_data[self.current_station_id].get("connections", []):
            if c["id"] == conn_id and "tracks" in c:
                val = c["tracks"][track_idx].get("allowed_routes", c["tracks"][track_idx].get("allowed_route", ["all"]))
                curr_routes = ["all"] if val in ["無限制", "all"] else (val if isinstance(val, list) else [val])
                break
                
        used_routes = sorted(list(self.get_node_used_lines(self.current_station_id)))
        options_dict = {r_name: self.route_dir_map.get(r_name, r_name) for r_name in used_routes}
        
        selected = self.open_multi_select_dialog("選擇連線允許路線", options_dict, curr_routes)
        if selected is not None:
            self.update_conn_track_global(conn_id, track_idx, "allowed_routes", selected)
            self.update_conn_track_global(conn_id, track_idx, "allowed_grades", ["all"])
            QTimer.singleShot(0, self.render_connections_view)

    def on_conn_grade_btn_clicked(self, conn_id, track_idx):
        curr_routes = ["all"]
        curr_grades = ["all"]
        for c in self.stations_data[self.current_station_id].get("connections", []):
            if c["id"] == conn_id and "tracks" in c:
                r_val = c["tracks"][track_idx].get("allowed_routes", c["tracks"][track_idx].get("allowed_route", ["all"]))
                curr_routes = ["all"] if r_val in ["無限制", "all"] else (r_val if isinstance(r_val, list) else [r_val])
                
                g_val = c["tracks"][track_idx].get("allowed_grades", c["tracks"][track_idx].get("allowed_grade", ["all"]))
                curr_grades = ["all"] if g_val in ["無限制", "all"] else (g_val if isinstance(g_val, list) else [g_val])
                break
                
        grades_data = self.get_grades_for_routes(curr_routes)
        options_dict = {display: internal for display, internal in grades_data}
        
        selected = self.open_multi_select_dialog("選擇連線允許等級", options_dict, curr_grades)
        if selected is not None:
            self.update_conn_track_global(conn_id, track_idx, "allowed_grades", selected)
            QTimer.singleShot(0, self.render_connections_view)

    def update_conn_track_global(self, conn_id, track_idx, key, value):
        for st_data in self.stations_data.values():
            if not isinstance(st_data, dict): continue
            for c in st_data.get("connections", []):
                if c["id"] == conn_id and "tracks" in c:
                    c["tracks"][track_idx][key] = value
        self.save_json()

    def update_conn_buffer_time_global(self, conn_id, value):
        for st_data in self.stations_data.values():
            if not isinstance(st_data, dict): continue
            for c in st_data.get("connections", []):
                if c["id"] == conn_id:
                    c["buffer_time"] = value
        self.save_json()

    def delete_connection_global(self, conn_id):
        reply = QMessageBox.warning(self, "確認刪除", "確定要刪除這組連線/綁定嗎？\n這將會同步刪除兩端節點的資料！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for st_data in self.stations_data.values():
                if not isinstance(st_data, dict): continue
                if "connections" in st_data:
                    st_data["connections"] = [c for c in st_data["connections"] if c["id"] != conn_id]
            self.save_json()
            QTimer.singleShot(0, self.render_connections_view)

    def action_add_connection(self):
        if not self.current_station_id: return
        target_st_id = self.connect_line_selection_box.currentData()
        if not target_st_id or target_st_id == self.current_station_id:
            QMessageBox.warning(self, "警告", "請選擇有效的目標節點 (不能連向自己)。")
            return
            
        st_data = self.stations_data[self.current_station_id]
        st_type = st_data.get("type", "station")
        is_facility = st_type in ["depot", "pocket_track"]
        
        target_data = self.stations_data.get(target_st_id, {})
        target_type = target_data.get("type", "station")
        target_is_facility = target_type in ["depot", "pocket_track"]

        if "connections" not in st_data: st_data["connections"] = []
        if "connections" not in target_data: target_data["connections"] = []
        
        if is_facility or target_is_facility:
            if is_facility and target_is_facility:
                QMessageBox.warning(self, "警告", "設施與設施之間不能直接連接！請綁定至車站。")
                return
                
            existing_binding = next((c for c in st_data["connections"] if c["target_station"] == target_st_id), None)
            if existing_binding:
                QMessageBox.warning(self, "警告", "此設施已與該車站綁定，無需重複新增！")
                return
                
            conn_id = f"C_{uuid.uuid4().hex[:6].upper()}"
            
            st_data["connections"].append({
                "id": conn_id, "side": "facility", "target_station": target_st_id, "buffer_time": 10 
            })
            target_data["connections"].append({
                "id": conn_id, "side": "facility", "target_station": self.current_station_id, "buffer_time": 10
            })

        else:
            side = "left" if self.connection_side_box.currentText() == "左" else "right"
            track_amount_text = self.track_amount_selection_b.currentText()
            track_count = int(track_amount_text.split("(")[0].strip()) 
            
            existing_conn_this = next((c for c in st_data["connections"] if c["target_station"] == target_st_id and c["side"] == side), None)
            tracks_to_add = [{"dir": "double", "allowed_routes": ["all"], "allowed_grades": ["all"]} for _ in range(track_count)]
            
            if existing_conn_this: 
                conn_id = existing_conn_this["id"]
                existing_conn_this["track_count"] = existing_conn_this.get("track_count", len(existing_conn_this.get("tracks", []))) + track_count
                if "tracks" not in existing_conn_this: existing_conn_this["tracks"] = []
                existing_conn_this["tracks"].extend(copy.deepcopy(tracks_to_add))
            else:
                conn_id = f"C_{uuid.uuid4().hex[:6].upper()}"
                st_data["connections"].append({
                    "id": conn_id, "side": side, "target_station": target_st_id, 
                    "track_count": track_count, "tracks": copy.deepcopy(tracks_to_add)
                })
                
            opp_side = "right" if side == "left" else "left"
            existing_conn_target = next((c for c in target_data["connections"] if c["id"] == conn_id), None)
            if existing_conn_target:
                existing_conn_target["track_count"] = existing_conn_target.get("track_count", len(existing_conn_target.get("tracks", []))) + track_count
                if "tracks" not in existing_conn_target: existing_conn_target["tracks"] = []
                existing_conn_target["tracks"].extend(copy.deepcopy(tracks_to_add))
            else:
                target_data["connections"].append({
                    "id": conn_id, "side": opp_side, "target_station": self.current_station_id, 
                    "track_count": track_count, "tracks": copy.deepcopy(tracks_to_add)
                })
            
        self.save_json()
        QTimer.singleShot(0, self.render_connections_view)

    def render_connections_view(self):
        self.safe_clear_scene(self.conn_scene)
        if not self.current_station_id: return
        
        st_data = self.stations_data.get(self.current_station_id, {})
        st_type = st_data.get("type", "station")
        is_facility = st_type in ["depot", "pocket_track"]
        conns = st_data.get("connections", [])
        
        view_width = max(900, self.connections_editor_view.viewport().width())
        
        if is_facility:
            curr_y = 30
            for idx_conn, conn in enumerate(conns):
                target_st_id = conn.get("target_station")
                target_data = self.stations_data.get(target_st_id, {})
                t_name = target_data.get("name", "")
                target_name = t_name if t_name else f"(未命名) [{target_st_id}]"
                
                row_w = QWidget()
                row_l = QHBoxLayout(row_w)
                row_l.setContentsMargins(8, 0, 0, 0)
                row_l.setSpacing(10)
                
                line1 = QFrame(); line1.setFixedHeight(6); line1.setStyleSheet("background-color: #3498db; border-radius: 3px;")
                row_l.addWidget(line1, stretch=1)
                
                row_l.addWidget(QLabel("進入緩衝時間:"))
                buf_spin = QSpinBox()
                buf_spin.setRange(0, 999)
                buf_spin.setValue(conn.get("buffer_time", 10))
                buf_spin.setSuffix(" 分鐘")
                buf_spin.setFixedHeight(26)
                buf_spin.valueChanged.connect(lambda v, cid=conn["id"]: self.update_conn_buffer_time_global(cid, v))
                row_l.addWidget(buf_spin)
                
                line2 = QFrame(); line2.setFixedHeight(6); line2.setStyleSheet("background-color: #3498db; border-radius: 3px;")
                row_l.addWidget(line2, stretch=1)
                
                lbl_target = QLabel(f"往 {target_name}")
                lbl_target.setStyleSheet("font-weight: bold; color: #2c3e50;")
                row_l.addWidget(lbl_target)
                
                del_btn = QPushButton()
                del_btn.setIcon(QIcon("assets/stations_facilities_editor/cross_connection.svg"))
                del_btn.setFixedSize(24, 24)
                del_btn.setStyleSheet("border: none; background: transparent;")
                del_btn.clicked.connect(lambda _, cid=conn["id"]: self.delete_connection_global(cid))
                row_l.addWidget(del_btn)
                
                proxy = self.conn_scene.addWidget(row_w)
                proxy.setPos(40, curr_y)
                proxy.resize(view_width - 80, 30)
                curr_y += 45
            self.conn_scene.setSceneRect(0, 0, view_width, curr_y + 20)
            return

        center_x = view_width / 2
        
        station_conns = [c for c in conns if c.get("side") != "facility"]
        facility_conns = [c for c in conns if c.get("side") == "facility"]
        
        left_h = sum(40 + len(c.get("tracks", [1]*c.get("track_count", 2))) * 36 for c in station_conns if c["side"] == "left")
        right_h = sum(40 + len(c.get("tracks", [1]*c.get("track_count", 2))) * 36 for c in station_conns if c["side"] == "right")
        max_h = max(left_h, right_h, 160) 
        
        self.conn_scene.addRect(center_x - 60, 20, 120, max_h, QPen(Qt.black), QBrush(QColor("#bdc3c7")))
        
        line_ids = st_data.get("line_id", "")
        st_name = st_data.get("name", "")
        display_name = st_name if st_name else f"(未命名) [{self.current_station_id}]"
        
        txt1 = self.conn_scene.addText("【 節點 】")
        txt1.setPos(center_x - txt1.boundingRect().width()/2, 40)
        txt2 = self.conn_scene.addText(line_ids if line_ids else "- 無代號 -")
        txt2.setDefaultTextColor(QColor("#2980b9"))
        txt2.setPos(center_x - txt2.boundingRect().width()/2, 60)
        txt3 = self.conn_scene.addText(display_name)
        font = txt3.font(); font.setBold(True); font.setPointSize(12); txt3.setFont(font)
        txt3.setPos(center_x - txt3.boundingRect().width()/2, 80)
        
        left_y, right_y = 30, 30
        for conn in station_conns:
            if "tracks" not in conn: continue
            
            target_st_id = conn.get("target_station")
            target_name = self.stations_data.get(target_st_id, {}).get("name", "")
            target_name = target_name if target_name else f"(未命名) [{target_st_id}]"
            
            is_left = (conn.get("side") == "left")
            curr_y = left_y if is_left else right_y
            
            header_w = QWidget()
            header_l = QHBoxLayout(header_w)
            header_l.setContentsMargins(0, 0, 0, 0)
            
            del_btn = QPushButton()
            del_btn.setIcon(QIcon("assets/stations_facilities_editor/cross_connection.svg"))
            del_btn.setFixedSize(24, 24)
            del_btn.setStyleSheet("border: none; background: transparent;")
            del_btn.clicked.connect(lambda _, cid=conn["id"]: self.delete_connection_global(cid))
            
            lbl = QLabel(f"往 {target_name} ({len(conn['tracks'])} 線)")
            lbl.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 13px;")
            
            if is_left:
                header_l.addStretch(); header_l.addWidget(lbl); header_l.addWidget(del_btn)
            else:
                header_l.addWidget(del_btn); header_l.addWidget(lbl); header_l.addStretch()
                
            h_proxy = self.conn_scene.addWidget(header_w)
            h_proxy.setPos(center_x - 300 if is_left else center_x + 80, curr_y)
            h_proxy.resize(220, 30)
            curr_y += 30
            
            for t_idx, tk in enumerate(conn["tracks"]):
                row_w = QWidget()
                row_l = QHBoxLayout(row_w)
                row_l.setContentsMargins(0, 0, 0, 0)
                row_l.setSpacing(6)
                
                dir_btn = QPushButton()
                dir_btn.setIcon(QIcon(self.get_conn_icon_path(tk.get("dir", "double"))))
                dir_btn.setIconSize(QSize(18, 18))
                dir_btn.setFixedSize(30, 24)
                dir_btn.clicked.connect(lambda _, cid=conn["id"], tidx=t_idx: self.cycle_conn_track_signal(cid, tidx))
                
                route_btn = QPushButton()
                route_btn.setFixedHeight(24)
                route_btn.setMinimumWidth(80) 
                
                used_routes = sorted(list(self.get_node_used_lines(self.current_station_id)))
                route_options = {r_name: self.route_dir_map.get(r_name, r_name) for r_name in used_routes}
                
                curr_routes = tk.get("allowed_routes", tk.get("allowed_route", ["all"]))
                if isinstance(curr_routes, str): curr_routes = ["all"] if curr_routes in ["無限制", "all"] else [curr_routes]
                
                route_btn.setText(self.format_multi_select_text(curr_routes, route_options))
                route_btn.clicked.connect(lambda _, cid=conn["id"], tidx=t_idx: self.on_conn_route_btn_clicked(cid, tidx))
                
                grade_btn = QPushButton()
                grade_btn.setFixedHeight(24)
                grade_btn.setMinimumWidth(100) 
                
                grades_data = self.get_grades_for_routes(curr_routes)
                grade_options = {display: internal for display, internal in grades_data}
                
                curr_grades = tk.get("allowed_grades", tk.get("allowed_grade", ["all"]))
                if isinstance(curr_grades, str): curr_grades = ["all"] if curr_grades in ["無限制", "all"] else [curr_grades]
                
                grade_btn.setText(self.format_multi_select_text(curr_grades, grade_options))
                grade_btn.clicked.connect(lambda _, cid=conn["id"], tidx=t_idx: self.on_conn_grade_btn_clicked(cid, tidx))
                
                if is_left:
                    row_l.addWidget(route_btn); row_l.addWidget(grade_btn); row_l.addWidget(dir_btn)
                else:
                    row_l.addWidget(dir_btn); row_l.addWidget(route_btn); row_l.addWidget(grade_btn)
                
                proxy = self.conn_scene.addWidget(row_w)
                proxy.setZValue(100 - t_idx) 
                proxy.setPos(center_x - 300 if is_left else center_x + 80, curr_y)
                proxy.resize(220, 26)
                
                path = QPainterPath(); line_y = curr_y + 13
                if is_left:
                    path.moveTo(center_x - 80, line_y); path.lineTo(center_x - 60, line_y)
                else:
                    path.moveTo(center_x + 60, line_y); path.lineTo(center_x + 80, line_y)
                self.conn_scene.addPath(path, QPen(QColor("#7f8c8d"), 4))
                curr_y += 30
            
            curr_y += 15
            if is_left: left_y = curr_y
            else: right_y = curr_y

        fac_y = 20 + max_h + 20
        
        if facility_conns:
            trunk_bottom = fac_y + (len(facility_conns) - 1) * 40 + 15
            self.conn_scene.addLine(center_x, 20 + max_h, center_x, trunk_bottom, QPen(QColor("#8e44ad"), 3))
            
        for conn in facility_conns:
            target_st_id = conn.get("target_station")
            t_name = self.stations_data.get(target_st_id, {}).get("name", "")
            target_name = t_name if t_name else f"(未命名) [{target_st_id}]"
            
            row_w = QWidget()
            row_l = QHBoxLayout(row_w)
            row_l.setContentsMargins(8, 0, 0, 0)
            row_l.setSpacing(10)
            
            lbl_fac = QLabel(f"已綁定設施: {target_name}")
            lbl_fac.setStyleSheet("font-weight: bold; color: #8e44ad; font-size: 13px;")
            row_l.addWidget(lbl_fac)
            
            row_l.addWidget(QLabel("進入緩衝時間:"))
            buf_spin = QSpinBox()
            buf_spin.setRange(0, 999)
            buf_spin.setValue(conn.get("buffer_time", 10))
            buf_spin.setSuffix(" 分鐘")
            buf_spin.setFixedHeight(26)
            buf_spin.valueChanged.connect(lambda v, cid=conn["id"]: self.update_conn_buffer_time_global(cid, v))
            row_l.addWidget(buf_spin)
            
            del_btn = QPushButton()
            del_btn.setIcon(QIcon("assets/stations_facilities_editor/cross_connection.svg"))
            del_btn.setFixedSize(24, 24)
            del_btn.setStyleSheet("border: none; background: transparent;")
            del_btn.clicked.connect(lambda _, cid=conn["id"]: self.delete_connection_global(cid))
            row_l.addWidget(del_btn)
            
            proxy = self.conn_scene.addWidget(row_w)
            proxy.setPos(center_x + 20, fac_y) 
            proxy.resize(320, 30)
            
            self.conn_scene.addLine(center_x, fac_y + 15, center_x + 20, fac_y + 15, QPen(QColor("#8e44ad"), 3))
            
            fac_y += 40
            
        self.conn_scene.setSceneRect(0, 0, view_width, max(left_y, right_y, fac_y) + 40)