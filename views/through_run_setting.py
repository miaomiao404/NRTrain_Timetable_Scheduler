import os
import json
import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QScrollArea, QComboBox, QSpinBox, 
                               QLineEdit, QMessageBox, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

class DirectionToggle(QFrame):
    """並排的上/下行切換按鈕"""
    toggled = Signal(str) # 當方向改變時發出信號

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.btn_up = QPushButton("上行")
        self.btn_down = QPushButton("下行")
        self.btn_up.setCheckable(True)
        self.btn_down.setCheckable(True)
        self.btn_up.setChecked(True)
        
        self.btn_up.setFixedHeight(26)
        self.btn_down.setFixedHeight(26)
        
        self.btn_up.clicked.connect(self._on_up_clicked)
        self.btn_down.clicked.connect(self._on_down_clicked)
        
        self.setStyleSheet("""
            QPushButton { background-color: #f1f2f6; border: 1px solid #ced6e0; padding: 2px 4px; font-weight: bold; color: #7f8c8d; font-size: 12px; }
            QPushButton:checked { background-color: #3498db; color: white; border: 1px solid #2980b9; }
            QPushButton:first-child { border-top-left-radius: 4px; border-bottom-left-radius: 4px; border-right: none; }
            QPushButton:last-child { border-top-right-radius: 4px; border-bottom-right-radius: 4px; }
            QPushButton:hover:!checked { background-color: #dfe4ea; }
        """)
        layout.addWidget(self.btn_up)
        layout.addWidget(self.btn_down)
        
    def _on_up_clicked(self):
        if not self.btn_up.isChecked(): self.btn_up.setChecked(True)
        self.btn_down.setChecked(False)
        self.toggled.emit("上行")

    def _on_down_clicked(self):
        if not self.btn_down.isChecked(): self.btn_down.setChecked(True)
        self.btn_up.setChecked(False)
        self.toggled.emit("下行")

    def get_direction(self):
        return "上行" if self.btn_up.isChecked() else "下行"

    def set_direction(self, direction):
        if direction == "下行":
            self.btn_down.setChecked(True); self.btn_up.setChecked(False)
        else:
            self.btn_up.setChecked(True); self.btn_down.setChecked(False)


class EdgeWidget(QFrame):
    """路線區段積木 (動態連動等級與起終點)"""
    def __init__(self, all_lines, env_path, change_callback=None):
        super().__init__()
        self.env_path = env_path
        self.change_callback = change_callback
        self.setMinimumWidth(160)
        self.setStyleSheet("""
            EdgeWidget { background-color: #ffffff; border: 1px solid #dcdde1; border-radius: 6px; }
            QComboBox { border: 1px solid #bdc3c7; border-radius: 4px; padding: 2px 6px; font-weight: bold; color: #2c3e50; }
            QComboBox:hover { border: 1px solid #3498db; }
            QComboBox::drop-down { border: none; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        
        self.line_cb = QComboBox()
        self.line_cb.addItems(["--選擇路線--"] + all_lines)
        self.line_cb.setFixedHeight(28)
        
        self.dir_toggle = DirectionToggle()
        
        self.grade_cb = QComboBox()
        self.grade_cb.addItem("--列車等級--")
        self.grade_cb.setFixedHeight(28)
        
        layout.addWidget(self.line_cb)
        layout.addWidget(self.dir_toggle)
        layout.addWidget(self.grade_cb)
        layout.setAlignment(Qt.AlignCenter)

        # 綁定信號
        self.line_cb.currentIndexChanged.connect(self._on_line_or_dir_changed)
        self.dir_toggle.toggled.connect(self._on_line_or_dir_changed)
        self.grade_cb.currentIndexChanged.connect(self._notify_parent)

    def _on_line_or_dir_changed(self, *args):
        """當路線或方向改變時，重新讀取對應的列車等級"""
        line_id = self.line_cb.currentText()
        direction = self.dir_toggle.get_direction()
        self.grade_cb.blockSignals(True)
        self.grade_cb.clear()
        self.grade_cb.addItem("--列車等級--")
        
        if line_id and line_id != "--選擇路線--":
            levels_path = os.path.join(self.env_path, line_id, "train_levels.json")
            if os.path.exists(levels_path):
                try:
                    with open(levels_path, 'r', encoding='utf-8') as f:
                        levels_data = json.load(f)
                    # 🌟 核心修復：將中文名稱顯示在選單上，但把系統 ID 隱藏在 UserData 中
                    for k, v in levels_data.items():
                        if v.get('direction') == direction and v.get('name'):
                            self.grade_cb.addItem(v.get('name'), k)
                except Exception: pass
        
        self.grade_cb.blockSignals(False)
        self._notify_parent()

    def _notify_parent(self, *args):
        if self.change_callback:
            self.change_callback()


class NodeWidget(QFrame):
    """站點積木 (由系統自動填入站名，取代下拉選單)"""
    def __init__(self, node_type="start"):
        super().__init__()
        self.node_type = node_type
        self.setMinimumWidth(140)
        self.set_normal_style()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # 自動填入的站名標籤
        self.station_lbl = QLabel("等待設定...")
        self.station_lbl.setAlignment(Qt.AlignCenter)
        self.station_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        self.station_lbl.setFixedHeight(28)
        
        layout.addWidget(self.station_lbl)
        
        if node_type == "start":
            role_lbl = QLabel("(起始站)")
            role_lbl.setAlignment(Qt.AlignCenter)
            role_lbl.setStyleSheet("color: #34495e; font-size: 12px;")
            layout.addWidget(role_lbl)
            
        elif node_type == "end":
            role_lbl = QLabel("(終點站)")
            role_lbl.setAlignment(Qt.AlignCenter)
            role_lbl.setStyleSheet("color: #34495e; font-size: 12px;")
            layout.addWidget(role_lbl)
            
        elif node_type == "junction":
            role_lbl = QLabel("銜接時間 (秒)")
            role_lbl.setAlignment(Qt.AlignCenter)
            role_lbl.setStyleSheet("font-size: 11px; color: #d35400; font-weight: bold;")
            
            buf_layout = QHBoxLayout()
            buf_layout.setContentsMargins(0, 0, 0, 0)
            buf_layout.setSpacing(2)
            self.min_spin = QSpinBox(); self.min_spin.setRange(0, 999); self.min_spin.setValue(120); self.min_spin.setButtonSymbols(QSpinBox.NoButtons)
            self.min_spin.setAlignment(Qt.AlignCenter)
            self.min_spin.setStyleSheet("border: 1px solid #e67e22; border-radius: 3px; background: white; font-weight: bold;")
            
            lbl_mid = QLabel("~")
            lbl_mid.setStyleSheet("color: #e67e22; font-weight: bold;")
            
            self.max_spin = QSpinBox(); self.max_spin.setRange(0, 999); self.max_spin.setValue(300); self.max_spin.setButtonSymbols(QSpinBox.NoButtons)
            self.max_spin.setAlignment(Qt.AlignCenter)
            self.max_spin.setStyleSheet("border: 1px solid #e67e22; border-radius: 3px; background: white; font-weight: bold;")
            
            buf_layout.addWidget(self.min_spin)
            buf_layout.addWidget(lbl_mid)
            buf_layout.addWidget(self.max_spin)
            
            buf_widget = QWidget()
            buf_widget.setLayout(buf_layout)
            buf_widget.setFixedHeight(26)
            
            layout.insertWidget(0, role_lbl)
            layout.addWidget(buf_widget)

    def set_normal_style(self):
        if self.node_type == "junction":
            self.setStyleSheet("NodeWidget { background-color: #fdf2e9; border: 2px solid #e67e22; border-radius: 8px; }")
        else:
            self.setStyleSheet("NodeWidget { background-color: #ebf5fb; border: 2px solid #3498db; border-radius: 8px; }")

    def set_error_style(self):
        self.setStyleSheet("NodeWidget { background-color: #fdedec; border: 2px solid #e74c3c; border-radius: 8px; }")
        self.station_lbl.setText("⚠️ 路線無法銜接")
        self.station_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #c0392b;")

    def set_station_name(self, name):
        self.station_lbl.setText(name)
        self.station_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")


class ThroughRunGroup(QFrame):
    """水平鏈條卡片"""
    def __init__(self, all_lines, env_path):
        super().__init__()
        self.all_lines = all_lines
        self.env_path = env_path
        self.setStyleSheet("""
            ThroughRunGroup { border: 2px solid #bdc3c7; border-radius: 8px; background-color: #fafbfc; margin-bottom: 12px; }
            ThroughRunGroup:hover { border: 2px solid #95a5a6; }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        
        # 標題
        self.title_edit = QLineEdit("未命名直通群組")
        self.title_edit.setStyleSheet("font-size: 16px; font-weight: bold; border: none; border-bottom: 2px solid #ecf0f1; color: #2c3e50; background: transparent; padding-bottom: 4px; margin-bottom: 8px;")
        main_layout.addWidget(self.title_edit)
        
        self.chain_layout = QHBoxLayout()
        self.chain_layout.setSpacing(4)
        main_layout.addLayout(self.chain_layout)
        
        self.nodes = []
        self.edges = []
        
        # 預設產生: 起點 -> 路線段 -> 終點
        self.nodes.append(NodeWidget("start"))
        self.edges.append(EdgeWidget(self.all_lines, self.env_path, self.recalculate_chain))
        self.nodes.append(NodeWidget("end"))
        
        self._rebuild_chain_ui()

    def _rebuild_chain_ui(self):
        while self.chain_layout.count():
            item = self.chain_layout.takeAt(0)
            if item.widget(): item.widget().setParent(None)
                
        for i in range(len(self.nodes)):
            self.chain_layout.addWidget(self.nodes[i])
            if i < len(self.edges):
                arrow1 = QLabel("▶"); arrow1.setStyleSheet("font-size: 18px; color: #bdc3c7; font-weight: bold; margin: 0px 4px;")
                self.chain_layout.addWidget(arrow1)
                self.chain_layout.addWidget(self.edges[i])
                arrow2 = QLabel("▶"); arrow2.setStyleSheet("font-size: 18px; color: #bdc3c7; font-weight: bold; margin: 0px 4px;")
                self.chain_layout.addWidget(arrow2)
                
        # 右側控制區
        action_layout = QVBoxLayout()
        action_layout.setContentsMargins(10, 0, 0, 0)
        action_layout.setSpacing(8)
        
        add_btn = QPushButton("新增路線")
        add_btn.setStyleSheet("background-color: #34495e; color: white; padding: 6px 10px; border-radius: 4px; font-weight: bold;")
        add_btn.clicked.connect(self.add_segment)
        
        del_btn = QPushButton("刪除群組")
        del_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 6px 10px; border-radius: 4px; font-weight: bold;")
        del_btn.clicked.connect(self.deleteLater)
        
        action_layout.addWidget(add_btn)
        action_layout.addWidget(del_btn)
        action_layout.setAlignment(Qt.AlignCenter)
        
        action_widget = QWidget()
        action_widget.setLayout(action_layout)
        self.chain_layout.addWidget(action_widget)
        self.chain_layout.addStretch()

    def add_segment(self):
        old_end = self.nodes.pop()
        junc = NodeWidget("junction")
        junc.set_station_name(old_end.station_lbl.text())
        self.nodes.append(junc)
        
        self.edges.append(EdgeWidget(self.all_lines, self.env_path, self.recalculate_chain))
        self.nodes.append(NodeWidget("end"))
        
        self._rebuild_chain_ui()
        self.recalculate_chain()

    # 核心：自動計算所有節點的起終點，並進行防呆檢查
    def recalculate_chain(self):
        for i, edge in enumerate(self.edges):
            line_id = edge.line_cb.currentText()
            direction = edge.dir_toggle.get_direction()
            grade_id = edge.grade_cb.currentData() # 🌟 現在可以直接取得系統 ID 了！
            
            start_st, end_st = self._get_start_end_from_stb(line_id, direction, grade_id)
            
            # 填入左側 Node (如果是第一段就是 start，否則就是 junction)
            left_node = self.nodes[i]
            if left_node.node_type == "start":
                left_node.set_normal_style()
                left_node.set_station_name(start_st)
            elif left_node.node_type == "junction":
                # 檢查前一段的終點，是否等於這一段的起點
                prev_edge_end = self.nodes[i].station_lbl.text() 
                if prev_edge_end != start_st and prev_edge_end != "等待設定..." and start_st != "等待設定...":
                    left_node.set_error_style() # ⚠️ 無法銜接！
                else:
                    left_node.set_normal_style()
                    left_node.set_station_name(start_st)
            
            # 填入右側 Node
            right_node = self.nodes[i+1]
            if right_node.node_type != "junction": # 如果是 junction，它的名字由下一次迴圈決定並檢查
                right_node.set_normal_style()
                right_node.set_station_name(end_st)
            else:
                # 暫存給下一個 edge 檢查用
                right_node.set_station_name(end_st)

    def _get_start_end_from_stb(self, line_id, direction, grade_id):
        """從基準時刻表中尋找該等級的第一站與最後一站"""
        if not line_id or line_id.startswith("--") or not grade_id:
            return "等待設定...", "等待設定..."
            
        # 🌟 核心優化：不用再比對字典了，直接拿 grade_id 去找 CSV 表頭！
        csv_name = "stb_up.csv" if direction == "上行" else "stb_down.csv"
        csv_path = os.path.join(self.env_path, line_id, csv_name)
        
        if not os.path.exists(csv_path): return "查無時刻表", "查無時刻表"
        
        try:
            df = pd.read_csv(csv_path, header=None)
            csv_grade_ids = df.iloc[0, 2:].fillna("").astype(str).tolist()
            
            col_idx = -1
            for i, gid in enumerate(csv_grade_ids):
                if gid.strip() == grade_id:
                    col_idx = i + 2 # 加上前面兩欄 (車站, 到發) 的偏移
                    break
                    
            if col_idx == -1: return "時刻表內無此等級", "時刻表內無此等級"
            
            # 往下掃描資料，排除空白與通過符號 (| 或 ~)，找出起終站
            start_st, end_st = None, None
            for row in range(1, len(df)):
                st = df.iloc[row, 0]
                if pd.isna(st) or str(st).strip() == "": continue
                
                val = df.iloc[row, col_idx]
                val_str = str(val).strip()
                
                # 若儲存格有資料，且不是空白、不是通過符號
                if pd.notna(val) and val_str != "" and val_str not in ["|", "~"]:
                    if start_st is None: 
                        start_st = str(st).strip()
                    end_st = str(st).strip() # 不斷覆蓋，最後留下來的就是終點站
                    
            return start_st or "未知", end_st or "未知"
            
        except Exception as e:
            return "讀取錯誤", "讀取錯誤"

    def get_data(self, idx):
        edges_data = []
        for edge in self.edges:
            edges_data.append({
                'line_id': edge.line_cb.currentText(),
                'direction': edge.dir_toggle.get_direction(),
                'grade': edge.grade_cb.currentData() or "" # 🌟 儲存時，直接抽出系統 ID！
            })
            
        nodes_data = []
        for node in self.nodes:
            nd = {'type': node.node_type, 'station': node.station_lbl.text()}
            if node.node_type == 'junction':
                nd['min'] = node.min_spin.value()
                nd['max'] = node.max_spin.value()
            nodes_data.append(nd)
            
        return {
            'id': f"TR_{idx:03d}",
            'name': self.title_edit.text(),
            'chain': edges_data,
            'nodes': nodes_data
        }

    def load_data(self, rule_data):
        self.title_edit.setText(rule_data.get('name', '未命名直通群組'))
        edges_data = rule_data.get('chain', [])
        nodes_data = rule_data.get('nodes', [])
        
        if not edges_data or not nodes_data: return
        
        self.nodes = []
        self.edges = []
        
        for nd in nodes_data:
            node = NodeWidget(nd.get('type', 'start'))
            node.set_station_name(nd.get('station', '等待設定...'))
            if nd.get('type') == 'junction':
                node.min_spin.setValue(nd.get('min', 120))
                node.max_spin.setValue(nd.get('max', 300))
            self.nodes.append(node)
            
        for ed in edges_data:
            edge = EdgeWidget(self.all_lines, self.env_path, self.recalculate_chain)
            edge.line_cb.setCurrentText(ed.get('line_id', ''))
            edge.dir_toggle.set_direction(ed.get('direction', '上行'))
            # 強制觸發一次讀取等級
            edge._on_line_or_dir_changed()
            
            # 🌟 讀取時，透過隱藏在 Data 裡的系統 ID 去尋找對應的選項！
            grade_id = ed.get('grade', '')
            idx = edge.grade_cb.findData(grade_id)
            if idx >= 0:
                edge.grade_cb.setCurrentIndex(idx)
                
            self.edges.append(edge)
            
        self._rebuild_chain_ui()
        self.recalculate_chain()


class ThroughRunSettingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = None
        self.env_path = ""
        self.rules_file = ""
        self.all_lines = []
        self.init_ui()

    def set_engine(self, engine):
        self.engine = engine
        if self.engine and self.engine.project_path:
            self.env_path = os.path.dirname(self.engine.project_path)
            self.rules_file = os.path.join(self.env_path, "through_rules.json")
            self.scan_environment()
            self.load_data()

    def scan_environment(self):
        self.all_lines = []
        if not self.env_path: return
        for item in os.listdir(self.env_path):
            p = os.path.join(self.env_path, item)
            if os.path.isdir(p) and os.path.exists(os.path.join(p, "information.json")):
                self.all_lines.append(item)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        top_bar = QHBoxLayout()
        add_btn = QPushButton("➕ 新增直通群組")
        add_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 6px 16px; border-radius: 4px; font-size: 14px;")
        add_btn.clicked.connect(lambda: self.add_new_group())
        
        save_btn = QPushButton("💾 儲存所有設定")
        save_btn.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; padding: 6px 16px; border-radius: 4px; font-size: 14px;")
        save_btn.clicked.connect(self.save_data)
        
        top_bar.addWidget(add_btn)
        top_bar.addWidget(save_btn)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #f1f2f6; }")
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: #f1f2f6;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)
        
        main_layout.addWidget(self.scroll_area)

    def add_new_group(self, rule_data=None):
        group = ThroughRunGroup(self.all_lines, self.env_path)
        if rule_data:
            group.load_data(rule_data)
        self.scroll_layout.addWidget(group)

    def save_data(self):
        rules = []
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, ThroughRunGroup):
                rules.append(widget.get_data(i))
        
        try:
            with open(self.rules_file, 'w', encoding='utf-8') as f:
                json.dump(rules, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "成功", "直通設定已成功儲存至全域環境！")
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"儲存失敗：{e}")

    def load_data(self):
        if not os.path.exists(self.rules_file): return
        with open(self.rules_file, 'r', encoding='utf-8') as f:
            rules = json.load(f)
            for r in rules:
                self.add_new_group(r)