import os
import json
import pandas as pd
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QAbstractItemView, QColorDialog, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPixmap, QIcon
from ui_py.ui_train_levels_editor import Ui_Form

class TrainLevelsEditorWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.json_path = None
        self.levels_data = {}
        self.route_color = "#000000" # 紀錄路線預設顏色
        
        # 初始化表格 (新增顏色欄位)
        self.main_table.setColumnCount(5)
        self.main_table.setHorizontalHeaderLabels(["顏色", "ID", "方向", "等級名稱", "優先度"])
        self.main_table.setColumnWidth(0, 40)
        self.main_table.setIconSize(QSize(24, 24))
        
        # 調整顏色欄寬度，讓它看起來像個正方形的色塊標籤
        self.main_table.setColumnWidth(0, 40)
        self.main_table.horizontalHeader().setStretchLastSection(True)
        self.main_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.main_table.setAlternatingRowColors(True)
        
        # 綁定事件
        self.add_train_level_b.clicked.connect(self.add_level)
        self.delete_train_level_b.clicked.connect(self.delete_level)
        self.main_table.itemChanged.connect(self.on_item_changed)
        # 👇 綁定雙擊事件來叫出色選器
        self.main_table.itemDoubleClicked.connect(self.on_item_double_clicked)
        self._is_loading = False

    def load_json(self, json_path):
        self.json_path = json_path
        self._is_loading = True
        
        # 嘗試讀取該路線的 information.json 來取得路線預設顏色
        project_dir = os.path.dirname(self.json_path)
        info_path = os.path.join(project_dir, "information.json")
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding='utf-8') as f:
                self.route_color = json.load(f).get("路線顏色", "#000000")
                
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                self.levels_data = json.load(f)
        else:
            self.levels_data = {}
            
        self.refresh_table()
        self._is_loading = False
        
    def refresh_table(self):
        """重新繪製表格"""
        self.main_table.setRowCount(0)
        
        def sort_key(item):
            k, v = item
            dir_score = 0 if v.get("direction") == "上行" else 1
            return (dir_score, v.get("priority", 99))
            
        for k, v in sorted(self.levels_data.items(), key=sort_key):
            row = self.main_table.rowCount()
            self.main_table.insertRow(row)
            
            bg_color = QColor(220, 245, 255) if v.get("direction") == "上行" else QColor(255, 250, 220)
            
            # 1. 繪製顏色色塊 (第 0 欄)
            hex_color = v.get("color", self.route_color)
            
            # 建立一個 QLabel 來顯示色塊圖片
            icon_label = QLabel()
            pixmap = QPixmap(20, 20)
            pixmap.fill(QColor(hex_color))
            icon_label.setPixmap(pixmap)
            icon_label.setToolTip(f"雙擊以修改顏色 ({hex_color})")
            
            # 建立一個容器 Widget，並使用水平佈局讓 Label 強制置中
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_label)
            
            # 將容器塞進表格的儲存格中
            self.main_table.setCellWidget(row, 0, container)
            
            # 還是要放一個空的 Item，這樣選取整列時才不會出錯
            empty_item = QTableWidgetItem("")
            empty_item.setFlags(empty_item.flags() & ~Qt.ItemIsEditable)
            self.main_table.setItem(row, 0, empty_item)
            
            # 2. 繪製其他文字資訊 (第 1~4 欄)
            cols_data = [k, v.get("direction", ""), v.get("name", ""), str(v.get("priority", ""))]
            for i, text in enumerate(cols_data):
                col_idx = i + 1
                item = QTableWidgetItem(text)
                if col_idx in [1, 2]: item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setBackground(bg_color)
                item.setTextAlignment(Qt.AlignCenter)
                self.main_table.setItem(row, col_idx, item)

    def on_item_double_clicked(self, item):
        """雙擊顏色欄位時，開啟選色視窗"""
        if item.column() == 0:
            row = item.row()
            grade_id = self.main_table.item(row, 1).text()
            current_color = self.levels_data[grade_id].get("color", self.route_color)
            
            new_color = QColorDialog.getColor(QColor(current_color), self, "選擇列車等級顏色")
            
            if new_color.isValid():
                hex_color = new_color.name() 
                self.levels_data[grade_id]["color"] = hex_color
                
                # 從儲存格中抓出剛剛放進去的容器與 Label
                container = self.main_table.cellWidget(row, 0)
                if container:
                    icon_label = container.layout().itemAt(0).widget()
                    new_pixmap = QPixmap(20, 20)
                    new_pixmap.fill(QColor(hex_color))
                    icon_label.setPixmap(new_pixmap)
                    icon_label.setToolTip(f"雙擊以修改顏色 ({hex_color})")
                    
                self.save_json()

    def add_level(self):
        """新增列車等級"""
        name = self.train_level_name_input.text().strip()
        prio = self.train_level_priority_input.text().strip()
        direction = self.comboBox.currentText()
        
        if not name or not prio.isdigit():
            QMessageBox.warning(self, "錯誤", "請輸入有效的名稱與數字優先度")
            return
            
        for existing_v in self.levels_data.values():
            if existing_v.get("name") == name and existing_v.get("direction") == direction:
                QMessageBox.warning(self, "新增失敗", f"「{direction}」已經存在名為「{name}」的列車等級！")
                return
            
        existing_ids = [k for k, v in self.levels_data.items() if v.get("direction") == direction]
        if existing_ids:
            nums = [int(k.split('_')[-1]) for k in existing_ids if k.split('_')[-1].isdigit()]
            next_num = max(nums) + 1
        else:
            next_num = 0 if direction == "上行" else 50
            
        project_id = os.path.basename(os.path.dirname(self.json_path))
        new_id = f"{project_id}_{next_num:02d}"
        
        self.levels_data[new_id] = {
            "name": name,
            "priority": int(prio),
            "direction": direction,
            "color": self.route_color # 👇 預設套用路線顏色
        }
        
        self.save_json()
        self._is_loading = True
        self.refresh_table()
        self._is_loading = False
        
        self.train_level_name_input.setText("")
        self.train_level_priority_input.setText("")

    def delete_level(self):
        """刪除選取的列車等級"""
        selected_rows = set(item.row() for item in self.main_table.selectedItems())
        
        if not selected_rows:
            QMessageBox.information(self, "提示", "請先選取要刪除的列車等級")
            return
            
        to_delete = []
        for row in selected_rows:
            grade_id = self.main_table.item(row, 1).text() # ID 跑到第 1 欄了
            if grade_id in self.levels_data:
                name = self.levels_data[grade_id]["name"]
                dir_ = self.levels_data[grade_id]["direction"]
                to_delete.append((grade_id, name, dir_))
                
        msg = "確定要刪除以下列車等級嗎？\n\n"
        for gid, name, dir_ in to_delete:
            msg += f"• [{dir_}] {name}\n"
        msg += "\n警告：這將會同步永久刪除基準時刻表中對應的直欄與時間資料！"
        
        reply = QMessageBox.warning(self, "確認刪除", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            project_dir = os.path.dirname(self.json_path)
            for gid, name, dir_ in to_delete:
                del self.levels_data[gid]
                csv_name = "stb_up.csv" if dir_ == "上行" else "stb_down.csv"
                csv_path = os.path.join(project_dir, csv_name)
                
                if os.path.exists(csv_path):
                    try:
                        df = pd.read_csv(csv_path)
                        if gid in df.columns:
                            df.drop(columns=[gid], inplace=True)
                            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                    except Exception as e:
                        print(f"刪除 CSV 欄位時發生錯誤: {e}")
            
            self.save_json()
            self._is_loading = True
            self.refresh_table()
            self._is_loading = False

    def on_item_changed(self, item):
        """表格內容被直接編輯時觸發存檔"""
        if self._is_loading: return
        row = item.row()
        col = item.column()
        grade_id = self.main_table.item(row, 1).text() # ID 跑到第 1 欄了
        
        if col == 3: # 名字跑到第 3 欄了
            self.levels_data[grade_id]["name"] = item.text()
        elif col == 4: # 優先度跑到第 4 欄了
            if item.text().isdigit():
                self.levels_data[grade_id]["priority"] = int(item.text())
        self.save_json()
        
    def save_json(self):
        if self.json_path:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(self.levels_data, f, ensure_ascii=False, indent=4)