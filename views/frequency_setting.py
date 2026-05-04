import os
import json
from PySide6.QtWidgets import (QWidget, QTableWidgetItem, QSpinBox, 
                               QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

# 載入由 Designer 產生的 Widget UI
from ui_py.ui_frequency_setting import Ui_frequency_setting

class FrequencySettingWidget(QWidget, Ui_frequency_setting):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.engine = None
        self.is_loading = True 
        
        # 🌟 UI 映射：加入 _through 對應表格
        self.ui_map = {
            'weekday_morning': {'combo': self.cycle_b1, 'table_up': self.morning_peak_table_up, 'table_down': self.morning_peak_table_down, 'table_through': getattr(self, 'morning_peak_table_through', None), 'total_up': self.total_l1_up, 'total_down': self.total_l1_down},
            'weekday_night': {'combo': self.cycle_b1_2, 'table_up': self.night_peak_table_up, 'table_down': self.night_peak_table_down, 'table_through': getattr(self, 'night_peak_table_through', None), 'total_up': self.total_l2_up, 'total_down': self.total_l2_down},
            'weekday_offpeak': {'combo': self.cycle_b1_3, 'table_up': self.weekdays_off_peak_table_up, 'table_down': self.weekdays_off_peak_table_down, 'table_through': getattr(self, 'weekdays_off_peak_table_through', None), 'total_up': self.total_l3_up, 'total_down': self.total_l3_down},
            'weekday_latenight': {'combo': self.cycle_b1_4, 'table_up': self.weekdays_late_night_table_up, 'table_down': self.weekdays_late_night_table_down, 'table_through': getattr(self, 'weekdays_late_night_table_through', None), 'total_up': self.total_l4_up, 'total_down': self.total_l4_down},
            'weekend_offpeak': {'combo': self.cycle_b1_5, 'table_up': self.weekends_off_peak_table_up, 'table_down': self.weekends_off_peak_table_down, 'table_through': getattr(self, 'weekends_off_peak_table_through', None), 'total_up': self.total_l5_up, 'total_down': self.total_l5_down},
            'weekend_latenight': {'combo': self.cycle_b1_6, 'table_up': self.weekends_late_night_table_up, 'table_down': self.weekends_late_night_table_down, 'table_through': getattr(self, 'weekends_late_night_table_through', None), 'total_up': self.total_l6_up, 'total_down': self.total_l6_down},
        }
        
        self.train_levels = {}
        self.levels_up = []
        self.levels_down = []

        # 全域直通資料
        self.line_id = ""
        self.env_path = ""
        self.through_rules = []
        self.global_freq_file = ""
        self.global_freq_data = {}

    def set_engine(self, engine):
        self.engine = engine
        self.is_loading = True
        
        route_name = "未知路線"
        if self.engine and self.engine.project_path:
            self.line_id = os.path.basename(self.engine.project_path)
            self.env_path = os.path.dirname(self.engine.project_path)
            self.global_freq_file = os.path.join(self.env_path, "global_through_freq.json")
            
            info_path = os.path.join(self.engine.project_path, "information.json")
            if os.path.exists(info_path):
                try:
                    with open(info_path, 'r', encoding='utf-8') as f:
                        route_name = json.load(f).get("路線名稱", "未知路線")
                except Exception: pass
                
        self.line_name_l.setText(f"{route_name} 發車頻率設定")
        
        self.setup_header_styles()
        self.load_global_through_data()
        self.setup_combos()
        self.load_train_levels()
        self.setup_tables()
        self.load_data()
        
        self.is_loading = False 

    # 🌟 神級補強：當使用者切換分頁回來看時，自動重新載入全域規則，不必重啟！
    def showEvent(self, event):
        super().showEvent(event)
        if not self.is_loading and self.engine:
            self.load_global_through_data()
            for period_key, comps in self.ui_map.items():
                self._init_through_table(comps['table_through'], period_key)
            self.update_all_totals()

    def load_global_through_data(self):
        """讀取直通規則與全域頻率帳本"""
        if not self.env_path: return
        self.through_rules = []
        rules_path = os.path.join(self.env_path, "through_rules.json")
        if os.path.exists(rules_path):
            with open(rules_path, 'r', encoding='utf-8') as f:
                self.through_rules = json.load(f)
                
        if os.path.exists(self.global_freq_file):
            with open(self.global_freq_file, 'r', encoding='utf-8') as f:
                self.global_freq_data = json.load(f)

    def setup_header_styles(self):
        self.line_name_l.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; padding: 4px;")
        if hasattr(self, 'weekdays_l'): self.weekdays_l.setStyleSheet("font-size: 16px; font-weight: bold; color: #2980b9; padding: 2px;")
        if hasattr(self, 'weekends_l'): self.weekends_l.setStyleSheet("font-size: 16px; font-weight: bold; color: #27ae60; padding: 2px;")
        
        for lbl in [self.morning_peak_l, getattr(self, 'night_peak_l', None), getattr(self, 'weekdays_off_peak_l', None), 
                    getattr(self, 'weekdays_late_night_l', None), getattr(self, 'weekends_off_peak_l', None), getattr(self, 'weekends_late_night_l', None)]:
            if lbl: lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #34495e;")

    def setup_combos(self):
        cycle_options = [
            ("60 分鐘", 60), ("30 分鐘", 30), ("20 分鐘", 20), ("15 分鐘", 15),
            ("10 分鐘", 10), ("6 分鐘", 6), ("5 分鐘", 5), ("3 分鐘", 3)
        ]
        for comps in self.ui_map.values():
            combo = comps['combo']
            combo.blockSignals(True)
            combo.clear()
            for text, val in cycle_options: combo.addItem(text, val)
            combo.setStyleSheet("QComboBox { padding: 3px; font-size: 12px; font-weight: bold; border: 1px solid #bdc3c7; border-radius: 4px; }")
            combo.blockSignals(False)

    def load_train_levels(self):
        if not self.engine or not self.engine.project_path: return
        json_path = os.path.join(self.engine.project_path, "train_levels.json")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                self.train_levels = json.load(f)
        self.levels_up = sorted([(k, v) for k, v in self.train_levels.items() if v.get('direction') == '上行'], key=lambda x: x[1].get('priority', 99))
        self.levels_down = sorted([(k, v) for k, v in self.train_levels.items() if v.get('direction') == '下行'], key=lambda x: x[1].get('priority', 99))

    def _init_table(self, table, levels, direction, period_key):
        if not table: return
        table.setRowCount(len(levels))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels([f"{direction} 列車 (本線自發)", "每循環設定班次"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.setWordWrap(False)
        table.verticalHeader().setDefaultSectionSize(26)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget { background-color: #fcfcfc; border: 1px solid #dcdde1; border-radius: 4px; } 
            QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; border: none; padding: 4px; }
        """)
        
        for r, (lvl_id, lvl_data) in enumerate(levels):
            name = lvl_data.get('name', '未知')
            color = lvl_data.get('color', '#000000')
            
            item = QTableWidgetItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(QFont("Microsoft JhengHei", 9, QFont.Bold))
            item.setForeground(QColor(color))
            item.setData(Qt.UserRole, lvl_id)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable) 
            table.setItem(r, 0, item)
            
            spinbox = QSpinBox()
            spinbox.setRange(0, 99)
            spinbox.setAlignment(Qt.AlignCenter)
            spinbox.setStyleSheet("QSpinBox { padding: 2px; font-size: 12px; font-weight: bold; border: 1px solid #95a5a6; border-radius: 3px; background: white; }")
            spinbox.valueChanged.connect(lambda _, pk=period_key: self.on_value_changed(pk))
            table.setCellWidget(r, 1, spinbox)

    def _init_through_table(self, table, period_key):
        if not table: return
        table.clearContents()
        
        relevant_rules = []
        for rule in self.through_rules:
            chain = rule.get('chain', [])
            for i, c in enumerate(chain):
                if c.get('line_id') == self.line_id:
                    relevant_rules.append((rule, i, chain))
                    break
        
        # 🌟 修改 1：就算沒有直通規則，也不會把表格變不見！而是顯示友善的提示
        if not relevant_rules:
            table.setVisible(True)
            table.setRowCount(1)
            table.setColumnCount(1)
            table.setHorizontalHeaderLabels(["跨線直通群組 (獨立班次)"])
            item = QTableWidgetItem("尚無直通設定\n請至「環境設定 > 全域直通運轉設定」新增")
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QColor("#95a5a6"))
            item.setFont(QFont("Microsoft JhengHei", 9, QFont.Bold))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            table.setItem(0, 0, item)
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            table.setRowHeight(0, 50)
            table.setStyleSheet("""
                QTableWidget { background-color: #fdfefe; border: 1px dashed #bdc3c7; border-radius: 4px; }
                QHeaderView::section { background-color: #bdc3c7; color: white; font-weight: bold; border: none; padding: 4px; }
            """)
            return
            
        table.setVisible(True)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["跨線直通群組 (每小時班次)", "發車數"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.setWordWrap(False)
        
        table.setStyleSheet("""
            QTableWidget { background-color: #fdfefe; border: 1px solid #dcdde1; border-radius: 4px; }
            QHeaderView::section { background-color: #8e44ad; color: white; font-weight: bold; border: none; padding: 4px; }
        """)
        
        table.setRowCount(len(relevant_rules) * 3) 
        
        row = 0
        for rule, my_idx, chain in relevant_rules:
            rule_id = rule.get('id')
            my_info = chain[my_idx]
            is_master = (my_idx == 0)
            
            prev_info = chain[my_idx - 1] if my_idx > 0 else None
            next_info = chain[my_idx + 1] if my_idx < len(chain) - 1 else None
            
            # 第一列：方向與等級 + 發車數
            title = f"🔗 {my_info['direction']} - {my_info['grade']}"
            item_name = QTableWidgetItem(title)
            item_name.setTextAlignment(Qt.AlignCenter)
            item_name.setFont(QFont("Microsoft JhengHei", 9, QFont.Bold))
            item_name.setForeground(QColor("#8e44ad"))
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 0, item_name)
            
            spinbox = QSpinBox()
            spinbox.setRange(0, 99)
            spinbox.setAlignment(Qt.AlignCenter)
            saved_val = self.global_freq_data.get(rule_id, {}).get(period_key, 0)
            spinbox.setValue(saved_val)
            
            # 🌟 修改 2：極度明確的主從視覺防呆
            if is_master:
                spinbox.setStyleSheet("QSpinBox { padding: 2px; font-size: 12px; font-weight: bold; border: 1px solid #8e44ad; border-radius: 3px; background: white; }")
                spinbox.valueChanged.connect(lambda val, rid=rule_id, pk=period_key: self.on_through_value_changed(rid, pk, val))
            else:
                spinbox.setReadOnly(True)
                spinbox.setButtonSymbols(QSpinBox.NoButtons) # 隱藏上下箭頭，暗示無法點擊
                spinbox.setToolTip(f"此路線為接收端 (Slave)\n發車頻率由【{chain[0].get('line_id')}】控制，無法在此修改！")
                spinbox.setStyleSheet("QSpinBox { padding: 2px; font-size: 12px; font-weight: bold; border: 1px solid #bdc3c7; border-radius: 3px; background: #ecf0f1; color: #7f8c8d; }")
            
            table.setCellWidget(row, 1, spinbox)
            
            # 第二列：從哪個路線來
            text_from = f"↳ 從 [{prev_info['line_id']}] 來 ({prev_info['grade']})" if prev_info else "↳ (本路線為發起端 Master)"
            item_from = QTableWidgetItem(text_from)
            item_from.setTextAlignment(Qt.AlignCenter)
            item_from.setFont(QFont("Microsoft JhengHei", 8))
            item_from.setBackground(QColor("#f4ecf7"))
            item_from.setForeground(QColor("#7f8c8d"))
            item_from.setFlags(item_from.flags() & ~Qt.ItemIsEditable)
            table.setItem(row+1, 0, item_from)
            table.setSpan(row+1, 0, 1, 2)
            
            # 第三列：往哪個路線去
            text_to = f"↳ 往 [{next_info['line_id']}] 去 ({next_info['grade']})" if next_info else "↳ (本路線為最終端)"
            item_to = QTableWidgetItem(text_to)
            item_to.setTextAlignment(Qt.AlignCenter)
            item_to.setFont(QFont("Microsoft JhengHei", 8))
            item_to.setBackground(QColor("#f4ecf7"))
            item_to.setForeground(QColor("#7f8c8d"))
            item_to.setFlags(item_to.flags() & ~Qt.ItemIsEditable)
            table.setItem(row+2, 0, item_to)
            table.setSpan(row+2, 0, 1, 2)
            
            for r in range(3):
                table.setRowHeight(row + r, 26)
            
            row += 3

    def setup_tables(self):
        for period_key, comps in self.ui_map.items():
            self._init_table(comps['table_up'], self.levels_up, "上行", period_key)
            self._init_table(comps['table_down'], self.levels_down, "下行", period_key)
            self._init_through_table(comps['table_through'], period_key)
            comps['combo'].currentIndexChanged.connect(lambda _, pk=period_key: self.on_value_changed(pk))

    def on_value_changed(self, period_key):
        if self.is_loading: return
        self.update_total(period_key)
        self.auto_save_data()

    def on_through_value_changed(self, rule_id, period_key, value):
        if self.is_loading: return
        if rule_id not in self.global_freq_data: self.global_freq_data[rule_id] = {}
        self.global_freq_data[rule_id][period_key] = value
        
        try:
            with open(self.global_freq_file, 'w', encoding='utf-8') as f:
                json.dump(self.global_freq_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.engine.log_msg(f"全域直通頻率存檔失敗：{e}")

    def update_all_totals(self):
        for pk in self.ui_map.keys():
            self.update_total(pk)

    def update_total(self, period_key):
        comps = self.ui_map[period_key]
        cycle_min = comps['combo'].currentData()
        
        def calc_total(table):
            if not table: return 0
            total = sum(table.cellWidget(r, 1).value() for r in range(table.rowCount()) if table.cellWidget(r, 1) and isinstance(table.cellWidget(r, 1), QSpinBox))
            return (total * (60 / cycle_min)) if cycle_min and cycle_min > 0 else 0
            
        total_up = calc_total(comps['table_up'])
        total_down = calc_total(comps['table_down'])
        
        comps['total_up'].setText(f"上行 每小時: {total_up:.1f} 班")
        comps['total_up'].setStyleSheet("color: #2980b9; font-weight: bold; font-size: 12px;")
        
        comps['total_down'].setText(f"下行 每小時: {total_down:.1f} 班")
        comps['total_down'].setStyleSheet("color: #c0392b; font-weight: bold; font-size: 12px;")

    def load_data(self):
        if not self.engine or not self.engine.project_path: return
        json_path = os.path.join(self.engine.project_path, "frequency.json")
        if not os.path.exists(json_path): return
            
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                
            for period_key, comps in self.ui_map.items():
                cfg = saved_data.get(period_key, {})
                idx = comps['combo'].findData(cfg.get('cycle_min', 60))
                if idx >= 0: comps['combo'].setCurrentIndex(idx)
                
                def set_freqs(table, freqs):
                    if not table: return
                    for r in range(table.rowCount()):
                        if table.item(r, 0) and table.item(r, 0).data(Qt.UserRole):
                            lvl_id = table.item(r, 0).data(Qt.UserRole)
                            if lvl_id in freqs and table.cellWidget(r, 1):
                                w = table.cellWidget(r, 1)
                                w.blockSignals(True); w.setValue(freqs[lvl_id]); w.blockSignals(False)
                                
                set_freqs(comps['table_up'], cfg.get('frequencies_up', {}))
                set_freqs(comps['table_down'], cfg.get('frequencies_down', {}))
                self.update_total(period_key)
                
        except Exception as e: pass

    def auto_save_data(self):
        if not self.engine or not self.engine.project_path or self.is_loading: return
        save_data = {}
        for period_key, comps in self.ui_map.items():
            def get_freqs(table):
                freqs = {}
                if not table: return freqs
                for r in range(table.rowCount()):
                    if table.item(r, 0) and table.item(r, 0).data(Qt.UserRole):
                        w = table.cellWidget(r, 1)
                        if w and isinstance(w, QSpinBox) and w.value() > 0:
                            freqs[table.item(r, 0).data(Qt.UserRole)] = w.value()
                return freqs
                
            save_data[period_key] = {
                'cycle_min': comps['combo'].currentData(),
                'frequencies_up': get_freqs(comps['table_up']),
                'frequencies_down': get_freqs(comps['table_down'])
            }
        try:
            with open(os.path.join(self.engine.project_path, "frequency.json"), 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=4)
        except Exception: pass