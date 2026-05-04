import os
import json
import uuid
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QScrollArea, QFrame,
                               QCheckBox, QMessageBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QIcon

class TrainsEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = None
        self.train_levels = {"up": {}, "down": {}}
        self.trains_data = {}
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        # 標題列 (🌟 修正：置中對齊)
        title_lbl = QLabel("車輛資訊與編號設定")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(title_lbl)
        
        # 說明列 (🌟 修正：置中對齊)
        desc_lbl = QLabel("請設定可派發的車輛型號。在「列車編號方式」中使用 ## 作為流水號佔位符 (例如: E233-80## 將會生成 E233-8001, E233-8002...)")
        desc_lbl.setAlignment(Qt.AlignCenter)
        desc_lbl.setStyleSheet("font-size: 13px; color: #7f8c8d; margin-bottom: 10px;")
        self.layout.addWidget(desc_lbl)

        # 滾動區域 (讓卡片過多時可以往下滾)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #f4f6f7; }")
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: #f4f6f7;")
        self.cards_layout = QVBoxLayout(self.scroll_content)
        self.cards_layout.setAlignment(Qt.AlignTop)
        self.cards_layout.setSpacing(15)
        
        # 新增按鈕 (永遠在最後面)
        self.add_btn = QPushButton("+ 新增車輛")
        self.add_btn.setFixedHeight(40)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; font-weight: bold; 
                font-size: 14px; border-radius: 5px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.add_btn.clicked.connect(self.action_add_train)
        
        self.cards_layout.addWidget(self.add_btn)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

    def set_engine(self, engine):
        self.engine = engine
        self.load_train_levels()
        self.load_data()

    def load_train_levels(self):
        """讀取列車等級，並分為上下行"""
        self.train_levels = {"up": {}, "down": {}}
        if not self.engine or not self.engine.current_project: return
        
        json_path = os.path.join(self.engine.project_path, "train_levels.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for k, v in data.items():
                        name = v.get("name", k)
                        direction = v.get("direction", "")
                        if direction == "上行":
                            self.train_levels["up"][k] = name
                        elif direction == "下行":
                            self.train_levels["down"][k] = name
            except Exception as e:
                print(f"讀取列車等級錯誤: {e}")

    def load_data(self):
        """讀取 trains.json 並生成卡片"""
        if not self.engine or not self.engine.current_project: return
        
        json_path = os.path.join(self.engine.project_path, "trains.json")
        self.trains_data = {}
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    self.trains_data = json.load(f)
            except Exception: pass
            
        # 清除現有卡片 (除了 add_btn)
        while self.cards_layout.count() > 1:
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # 依序重建卡片
        for t_id, t_data in self.trains_data.items():
            self.create_train_card(t_id, t_data)

    def save_data(self):
        """將 UI 上的所有卡片資料收集並寫回 trains.json"""
        if not self.engine or not self.engine.current_project: return
        
        new_data = {}
        # 遍歷 cards_layout，扣掉最後一個 add_btn
        for i in range(self.cards_layout.count() - 1):
            card = self.cards_layout.itemAt(i).widget()
            if not card: continue
            
            t_id = card.property("train_id")
            
            name_input = card.findChild(QLineEdit, "name_input")
            rule_input = card.findChild(QLineEdit, "rule_input")
            
            name = name_input.text().strip() if name_input else ""
            rule = rule_input.text().strip() if rule_input else ""
            
            if not name: continue
            
            allowed_up = []
            allowed_down = []
            
            if hasattr(card, "up_cb_dict"):
                if card.up_cb_all.isChecked():
                    allowed_up = ["all"]
                else:
                    allowed_up = [g_id for g_id, cb in card.up_cb_dict.items() if cb.isChecked()]
                    
            if hasattr(card, "down_cb_dict"):
                if card.down_cb_all.isChecked():
                    allowed_down = ["all"]
                else:
                    allowed_down = [g_id for g_id, cb in card.down_cb_dict.items() if cb.isChecked()]
                    
            new_data[t_id] = {
                "name": name,
                "number_rule": rule,
                "allowed_grades_up": allowed_up,
                "allowed_grades_down": allowed_down
            }
            
        self.trains_data = new_data
        json_path = os.path.join(self.engine.project_path, "trains.json")
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.trains_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"儲存 trains.json 失敗: {e}")

    # 🌟 新增：全域互斥鎖定邏輯
    def handle_checkbox_exclusive(self, source_card, direction, grade_id, is_checked):
        """確保每一個列車等級只能被分配到一種車輛，並自動解除其他車輛的佔用"""
        if not is_checked:
            self.save_data()
            return
            
        # 遍歷所有車輛卡片
        for i in range(self.cards_layout.count() - 1):
            card = self.cards_layout.itemAt(i).widget()
            if not card: continue
            
            cb_all = card.up_cb_all if direction == "up" else card.down_cb_all
            cb_dict = card.up_cb_dict if direction == "up" else card.down_cb_dict
            
            if card == source_card:
                # 情況 A：在自己這張卡片內，如果勾選了「無限制」，就要取消自己其餘的細項勾選
                if grade_id == "all":
                    for gid, cb in cb_dict.items():
                        cb.blockSignals(True)
                        cb.setChecked(False)
                        cb.blockSignals(False)
                # 情況 B：在自己這張卡片內，如果勾選了「細項」，就要取消自己的「無限制」勾選
                else:
                    cb_all.blockSignals(True)
                    cb_all.setChecked(False)
                    cb_all.blockSignals(False)
            else:
                # 情況 C：其他車輛卡片的處理
                if grade_id == "all":
                    # 別人選了無限制，我就什麼都不剩了
                    cb_all.blockSignals(True)
                    cb_all.setChecked(False)
                    cb_all.blockSignals(False)
                    for gid, cb in cb_dict.items():
                        cb.blockSignals(True)
                        cb.setChecked(False)
                        cb.blockSignals(False)
                else:
                    # 別人選了某個細項，我必須讓出該細項，且我也失去「無限制」的資格
                    cb_all.blockSignals(True)
                    cb_all.setChecked(False)
                    cb_all.blockSignals(False)
                    if grade_id in cb_dict:
                        cb_dict[grade_id].blockSignals(True)
                        cb_dict[grade_id].setChecked(False)
                        cb_dict[grade_id].blockSignals(False)
                        
        self.save_data()

    def create_train_card(self, t_id, t_data=None):
        """動態生成一張車輛設定卡片"""
        if t_data is None: t_data = {}
        
        card = QFrame()
        card.setProperty("train_id", t_id)
        card.setStyleSheet("""
            QFrame { background-color: white; border: 1px solid #dcdde1; border-radius: 8px; }
            QLabel { border: none; }
            QCheckBox { border: none; }
        """)
        
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(15, 15, 15, 15)
        c_layout.setSpacing(10)
        
        # --- 第一排：基本資訊與刪除按鈕 ---
        row1 = QHBoxLayout()
        row1.setSpacing(15)
        
        name_lbl = QLabel("列車名稱:")
        name_lbl.setStyleSheet("font-weight: bold; color: #34495e;")
        name_input = QLineEdit(t_data.get("name", ""))
        name_input.setObjectName("name_input")
        name_input.setPlaceholderText("例: E233系8000番台")
        name_input.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
        name_input.editingFinished.connect(self.save_data)
        
        rule_lbl = QLabel("列車編號方式:")
        rule_lbl.setStyleSheet("font-weight: bold; color: #34495e;")
        rule_input = QLineEdit(t_data.get("number_rule", ""))
        rule_input.setObjectName("rule_input")
        rule_input.setPlaceholderText("例: E233-80##")
        rule_input.setStyleSheet("padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;")
        rule_input.editingFinished.connect(self.save_data)
        
        del_btn = QPushButton("❌ 刪除")
        del_btn.setStyleSheet("color: #e74c3c; font-weight: bold; border: 1px solid #e74c3c; padding: 5px 10px;")
        del_btn.clicked.connect(lambda: self.action_delete_train(card))
        
        row1.addWidget(name_lbl)
        row1.addWidget(name_input, 2)
        row1.addWidget(rule_lbl)
        row1.addWidget(rule_input, 2)
        row1.addStretch()
        row1.addWidget(del_btn)
        c_layout.addLayout(row1)
        
        # --- 第二排：上行允許等級 ---
        row2 = QHBoxLayout()
        up_lbl = QLabel("上行可行駛等級:")
        up_lbl.setFixedWidth(110)
        up_lbl.setStyleSheet("font-weight: bold; color: #34495e;")
        row2.addWidget(up_lbl)
        
        card.up_cb_all = QCheckBox("無限制")
        card.up_cb_all.setChecked("all" in t_data.get("allowed_grades_up", []))
        row2.addWidget(card.up_cb_all)
        
        card.up_cb_dict = {}
        for g_id, g_name in self.train_levels["up"].items():
            cb = QCheckBox(g_name)
            if card.up_cb_all.isChecked(): 
                cb.setChecked(False)
            else: 
                cb.setChecked(g_id in t_data.get("allowed_grades_up", []))
            card.up_cb_dict[g_id] = cb
            row2.addWidget(cb)
            
        row2.addStretch()
        c_layout.addLayout(row2)
        
        # 綁定上行互斥訊號
        card.up_cb_all.stateChanged.connect(lambda state, c=card: self.handle_checkbox_exclusive(c, "up", "all", bool(state)))
        for g_id, cb in card.up_cb_dict.items():
            cb.stateChanged.connect(lambda state, c=card, gid=g_id: self.handle_checkbox_exclusive(c, "up", gid, bool(state)))
        
        # --- 第三排：下行允許等級 ---
        row3 = QHBoxLayout()
        down_lbl = QLabel("下行可行駛等級:")
        down_lbl.setFixedWidth(110)
        down_lbl.setStyleSheet("font-weight: bold; color: #34495e;")
        row3.addWidget(down_lbl)
        
        card.down_cb_all = QCheckBox("無限制")
        card.down_cb_all.setChecked("all" in t_data.get("allowed_grades_down", []))
        row3.addWidget(card.down_cb_all)
        
        card.down_cb_dict = {}
        for g_id, g_name in self.train_levels["down"].items():
            cb = QCheckBox(g_name)
            if card.down_cb_all.isChecked(): 
                cb.setChecked(False)
            else: 
                cb.setChecked(g_id in t_data.get("allowed_grades_down", []))
            card.down_cb_dict[g_id] = cb
            row3.addWidget(cb)
            
        row3.addStretch()
        c_layout.addLayout(row3)

        # 綁定下行互斥訊號
        card.down_cb_all.stateChanged.connect(lambda state, c=card: self.handle_checkbox_exclusive(c, "down", "all", bool(state)))
        for g_id, cb in card.down_cb_dict.items():
            cb.stateChanged.connect(lambda state, c=card, gid=g_id: self.handle_checkbox_exclusive(c, "down", gid, bool(state)))

        self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)

    def action_add_train(self):
        """按下新增按鈕時觸發"""
        if not self.engine or not self.engine.current_project:
            QMessageBox.warning(self, "警告", "請先載入路線專案！")
            return
            
        new_id = f"TR_{uuid.uuid4().hex[:6].upper()}"
        
        # 🌟 修正：為了防止新增車輛時，預設的「無限制」直接把別的車輛分配吃掉，預設改為空分配
        default_data = {
            "name": "",
            "number_rule": "",
            "allowed_grades_up": [],
            "allowed_grades_down": []
        }
        self.create_train_card(new_id, default_data)
        
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def action_delete_train(self, card_widget):
        """刪除指定卡片"""
        reply = QMessageBox.question(self, "確認", "確定要刪除這個車輛設定嗎？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cards_layout.removeWidget(card_widget)
            card_widget.deleteLater()
            self.save_data()