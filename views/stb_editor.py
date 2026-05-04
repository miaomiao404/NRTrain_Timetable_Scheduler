import os
import json
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QTableWidgetItem, QMessageBox, QAbstractItemView, 
    QDialog, QTableWidget, QHeaderView, QFrame, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt
from ui_py.ui_stb_editor import Ui_STB_Widget
from ui_py.ui_stb_editor_add_station import Ui_Dialog as Ui_AddStationDialog

# ==========================================
# 新增車站專用彈出視窗
# ==========================================
class AddStationDialog(QDialog, Ui_AddStationDialog):
    def __init__(self, stations_data, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("選擇要新增的車站")
        self.stations_data = stations_data
        
        # 🌟 修正：徹底拔除原本的 QTableView，防止它變成漂浮在 (0,0) 的白色幽靈色塊
        old_table = self.station_list
        self.verticalLayout.removeWidget(old_table)
        old_table.hide()              # 強制隱藏
        old_table.setParent(None)     # 徹底脫離父視窗
        old_table.deleteLater()       # 排程安樂死
        
        self.station_list = QTableWidget(self) # 給予明確的 parent
        self.station_list.setColumnCount(2) # 雙直欄設計
        self.station_list.horizontalHeader().setVisible(False)
        self.station_list.verticalHeader().setVisible(False)
        self.station_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.station_list.verticalHeader().setDefaultSectionSize(36) # 稍微加高以容納外框
        self.station_list.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.station_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.station_list.setShowGrid(False)
        
        # 加入點擊時不顯示預設虛線框的設定
        self.station_list.setFocusPolicy(Qt.NoFocus)
        self.station_list.setStyleSheet("QTableWidget::item { padding: 2px; }")
        
        self.verticalLayout.insertWidget(1, self.station_list)
        
        # 綁定事件
        self.searching_b.clicked.connect(self.populate_list)
        self.searching_editor.returnPressed.connect(self.populate_list)
        self.station_list.itemDoubleClicked.connect(self.on_double_click) 
        
        self.populate_list()
        
    def create_station_cell(self, display_name, line_ids, st_type):
        """建立帶有色塊、外框與左右排版的迷你 UI 容器"""
        w = QWidget()
        w.setObjectName("cell_wrapper")
        w.setStyleSheet("#cell_wrapper { border: 1px solid #b0b0b0; border-radius: 4px; background: transparent; }")
        
        layout = QHBoxLayout(w)
        layout.setContentsMargins(4, 2, 8, 2) # 加入內縮留白
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
        line_lbl.setStyleSheet("color: #2980b9; font-weight: bold; border: none;")
        line_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)

        layout.addWidget(color_block)     
        layout.addWidget(name_lbl)        
        layout.addStretch()               
        layout.addWidget(line_lbl)        
        return w

    def populate_list(self):
        search_text = self.searching_editor.text().strip().lower()
        filtered_stations = []
        
        for st_id, st_info in self.stations_data.items():
            st_type = st_info.get("type", "station")
            
            if st_type not in ["station", "main_station"]:
                continue
                
            st_name = st_info.get("name", "")
            display_name = st_name if st_name else f"(未命名) [{st_id}]"
            line_ids = st_info.get("line_id", "")
            
            if search_text and search_text not in display_name.lower() and search_text not in line_ids.lower():
                continue
                
            filtered_stations.append((st_id, display_name, line_ids, st_type, st_name))
            
        rows = (len(filtered_stations) + 1) // 2
        self.station_list.setRowCount(rows)
        self.station_list.clearContents()
        
        for idx, data in enumerate(filtered_stations):
            st_id, display_name, line_ids, st_type, st_name = data
            
            row = idx // 2
            col = idx % 2
            
            item = QTableWidgetItem()
            item.setData(Qt.UserRole, st_name if st_name else st_id) 
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            
            self.station_list.setItem(row, col, item)
            self.station_list.setCellWidget(row, col, self.create_station_cell(display_name, line_ids, st_type))

    def on_double_click(self, item):
        """雙擊觸發確定"""
        if item:
            self.accept()
            
    def get_selected_station_name(self):
        items = self.station_list.selectedItems()
        if items:
            return items[0].data(Qt.UserRole)
        return None
        
    def accept(self):
        """攔截確定按鈕，防呆檢查是否有選取"""
        if not self.get_selected_station_name():
            QMessageBox.warning(self, "警告", "請先選擇一個車站！")
            return
        super().accept()


# ==========================================
# 主體：時刻表編輯器
# ==========================================
class STBEditorWidget(QWidget, Ui_STB_Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.engine = None
        self.current_csv_path = None
        self.current_direction = None
        self.train_levels = {}
        self._is_loading = False 
        
        self.add_station_b.clicked.connect(self.add_station_row)
        self.delete_b.clicked.connect(self.delete_selected)
        
        self.main_table.setAlternatingRowColors(True)
        self.main_table.horizontalHeader().setVisible(True)
        self.main_table.verticalHeader().setVisible(True) 
        self.main_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.main_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        self.move_up_b.clicked.connect(self.move_row_up)
        self.move_down_b.clicked.connect(self.move_row_down)
        self.move_left_b.clicked.connect(self.move_col_left)
        self.move_right_b.clicked.connect(self.move_col_right)
        
        self.main_table.itemChanged.connect(self.auto_save)

    def set_engine(self, engine):
        self.engine = engine

    def load_csv_direction(self, csv_path, json_path, direction):
        self._is_loading = True
        self.current_csv_path = csv_path
        self.current_direction = direction
        
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                all_levels = json.load(f)
                self.train_levels = {k: v for k, v in all_levels.items() if v.get("direction") == direction}
        
        if not os.path.exists(csv_path): return
        df = pd.read_csv(csv_path)
        
        for gid in self.train_levels.keys():
            if gid not in df.columns:
                df[gid] = ""
                
        valid_cols = ["車站", "到發"] + list(self.train_levels.keys())
        df = df[[c for c in valid_cols if c in df.columns]]
        
        self.main_table.setRowCount(df.shape[0])
        self.main_table.setColumnCount(df.shape[1])
        
        headers = ["車站名", "到發"]
        for c in df.columns[2:]:
            info = self.train_levels.get(c, {"name": c, "priority": "?"})
            headers.append(f"{info['name']}\n(Pri:{info['priority']})")
        self.main_table.setHorizontalHeaderLabels(headers)
        
        for c_idx, col_name in enumerate(df.columns):
            self.main_table.horizontalHeaderItem(c_idx).setData(Qt.UserRole, col_name)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                val = str(df.iloc[row, col]) if not pd.isna(df.iloc[row, col]) else ""
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                
                if col < 2: 
                    item.setBackground(Qt.lightGray)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable) 
                    
                self.main_table.setItem(row, col, item)
                
        self.main_table.resizeColumnsToContents()
        self._is_loading = False

    def auto_save(self):
        if self._is_loading or not self.current_csv_path: return
        
        headers = []
        for c in range(self.main_table.columnCount()):
            headers.append(self.main_table.horizontalHeaderItem(c).data(Qt.UserRole))
            
        data = []
        for r in range(self.main_table.rowCount()):
            row_data = [self.main_table.item(r, c).text().strip() if self.main_table.item(r, c) else "" for c in range(self.main_table.columnCount())]
            data.append(row_data)
            
        pd.DataFrame(data, columns=headers).to_csv(self.current_csv_path, index=False, encoding='utf-8-sig')

    # ==========================================
    # 車站移動與自動格式化系統
    # ==========================================
    def get_all_stations_data(self):
        stations = []
        current_station = None
        for r in range(self.main_table.rowCount()):
            st_name = self.main_table.item(r, 0).text().strip() if self.main_table.item(r, 0) else ""
            arr_dep = self.main_table.item(r, 1).text().strip() if self.main_table.item(r, 1) else ""
            row_data = [self.main_table.item(r, c).text().strip() if self.main_table.item(r, c) else "" for c in range(2, self.main_table.columnCount())]
            
            if st_name:
                current_station = {"name": st_name, "arr_times": [""] * (self.main_table.columnCount() - 2), "dep_times": [""] * (self.main_table.columnCount() - 2)}
                stations.append(current_station)
            if current_station:
                if arr_dep == "到": current_station["arr_times"] = row_data
                elif arr_dep == "發": current_station["dep_times"] = row_data
        return stations

    def render_stations(self, stations):
        self._is_loading = True
        self.main_table.setRowCount(0)
        
        for i, st in enumerate(stations):
            is_first, is_last = (i == 0), (i == len(stations) - 1)
            if not is_first:
                r = self.main_table.rowCount()
                self.main_table.insertRow(r)
                self.main_table.setItem(r, 0, QTableWidgetItem(st["name"]))
                self.main_table.setItem(r, 1, QTableWidgetItem("到"))
                for c_idx, val in enumerate(st["arr_times"]): self.main_table.setItem(r, c_idx + 2, QTableWidgetItem(val))
            if not is_last:
                r = self.main_table.rowCount()
                self.main_table.insertRow(r)
                self.main_table.setItem(r, 0, QTableWidgetItem("" if not is_first else st["name"]))
                self.main_table.setItem(r, 1, QTableWidgetItem("發"))
                for c_idx, val in enumerate(st["dep_times"]): self.main_table.setItem(r, c_idx + 2, QTableWidgetItem(val))
                
        for r in range(self.main_table.rowCount()):
            for c in [0, 1]:
                if self.main_table.item(r, c): 
                    self.main_table.item(r, c).setBackground(Qt.lightGray)
                    self.main_table.item(r, c).setFlags(self.main_table.item(r, c).flags() & ~Qt.ItemIsEditable)
                    
        self._is_loading = False
        self.auto_save()

    def get_station_index_from_row(self, row, stations):
        current_row = 0
        for i, st in enumerate(stations):
            is_first, is_last = (i == 0), (i == len(stations) - 1)
            rows = 0
            if not is_first: rows += 1
            if not is_last: rows += 1
            if current_row <= row < current_row + rows: return i
            current_row += rows
        return -1

    def select_station_by_index(self, target_idx, stations):
        current_row = 0
        for i, st in enumerate(stations):
            if i == target_idx:
                self.main_table.clearSelection()
                self.main_table.selectRow(current_row)
                return
            if i != 0: current_row += 1
            if i != len(stations) - 1: current_row += 1

    def move_row_up(self):
        row = self.main_table.currentRow()
        if row < 0: return
        stations = self.get_all_stations_data()
        idx = self.get_station_index_from_row(row, stations)
        if idx <= 0: return
        stations[idx], stations[idx - 1] = stations[idx - 1], stations[idx]
        self.render_stations(stations)
        self.select_station_by_index(idx - 1, stations)

    def move_row_down(self):
        row = self.main_table.currentRow()
        if row < 0: return
        stations = self.get_all_stations_data()
        idx = self.get_station_index_from_row(row, stations)
        if idx == -1 or idx >= len(stations) - 1: return
        stations[idx], stations[idx + 1] = stations[idx + 1], stations[idx]
        self.render_stations(stations)
        self.select_station_by_index(idx + 1, stations)

    def add_station_row(self):
        stations_data = {}
        if self.engine and getattr(self.engine, 'station_file', None) and os.path.exists(self.engine.station_file):
            try:
                with open(self.engine.station_file, 'r', encoding='utf-8') as f:
                    stations_data = json.load(f)
            except Exception as e:
                print(f"載入車站資料錯誤: {e}")
                
        dialog = AddStationDialog(stations_data, self)
        
        if dialog.exec():
            new_name = dialog.get_selected_station_name()
            if not new_name: return
            
            self._is_loading = True
            stations = self.get_all_stations_data()
            
            new_station = {"name": new_name, "arr_times": [""] * (self.main_table.columnCount() - 2), "dep_times": [""] * (self.main_table.columnCount() - 2)}
            row = self.main_table.currentRow()
            idx = self.get_station_index_from_row(row, stations) if row >= 0 else -1
            insert_idx = idx + 1 if idx != -1 else len(stations)
            
            stations.insert(insert_idx, new_station)
            self.render_stations(stations)
            self.select_station_by_index(insert_idx, stations)
            self._is_loading = False

    def delete_selected(self):
        selected = self.main_table.selectedRanges()
        if not selected: return
        r = selected[0]
        if r.rightColumn() - r.leftColumn() < r.bottomRow() - r.topRow():
            QMessageBox.warning(self, "警告", "無法在此刪除列車等級！\n請至左側功能列的「列車等級表」進行刪除。")
            return
            
        stations = self.get_all_stations_data()
        idx = self.get_station_index_from_row(r.topRow(), stations)
        if idx != -1:
            st_name = stations[idx]['name']
            if QMessageBox.question(self, "確認刪除", f"確定要從時刻表中移除車站 [{st_name}] 嗎？") == QMessageBox.Yes:
                stations.pop(idx)
                self.render_stations(stations)

    # ==========================================
    # 直欄(等級)移動邏輯
    # ==========================================
    def _swap_cols(self, c1, c2):
        for row in range(self.main_table.rowCount()):
            item1 = self.main_table.takeItem(row, c1) or QTableWidgetItem("")
            item2 = self.main_table.takeItem(row, c2) or QTableWidgetItem("")
            self.main_table.setItem(row, c1, item2)
            self.main_table.setItem(row, c2, item1)
            
        text1 = self.main_table.horizontalHeaderItem(c1).text()
        text2 = self.main_table.horizontalHeaderItem(c2).text()
        self.main_table.horizontalHeaderItem(c1).setText(text2)
        self.main_table.horizontalHeaderItem(c2).setText(text1)
        
        id1 = self.main_table.horizontalHeaderItem(c1).data(Qt.UserRole)
        id2 = self.main_table.horizontalHeaderItem(c2).data(Qt.UserRole)
        self.main_table.horizontalHeaderItem(c1).setData(Qt.UserRole, id2)
        self.main_table.horizontalHeaderItem(c2).setData(Qt.UserRole, id1)

    def move_col_left(self):
        col = self.main_table.currentColumn()
        if col <= 2: return
        self._is_loading = True
        self._swap_cols(col, col - 1)
        self.main_table.selectColumn(col - 1)
        self._is_loading = False
        self.auto_save()

    def move_col_right(self):
        col = self.main_table.currentColumn()
        if col < 2 or col >= self.main_table.columnCount() - 1: return
        self._is_loading = True
        self._swap_cols(col, col + 1)
        self.main_table.selectColumn(col + 1)
        self._is_loading = False
        self.auto_save()