import os
import json
import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                               QTableWidgetItem, QLabel, QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt, QSize, QTimer, QEvent
from PySide6.QtGui import QColor, QFont, QBrush

# 載入您設計好的 UI
from ui_py.ui_stations_timetable import Ui_Form

class StationsTimetableWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.splitter)
        self.setLayout(main_layout)
        
        self.engine = None
        self.schedule_type = "weekdays" # 預設平日
        
        self.stations_list = []
        self.current_station = ""
        self.current_direction = "上行"
        
        self.timetable_data = {'上行': {}, '下行': {}}
        self.destinations = {'上行': {}, '下行': {}}
        self.train_levels = {}
        self.route_name = ""
        
        self.current_cols_per_row = 12 
        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.check_and_re_render)
        
        self.setup_ui_components()

    def setup_ui_components(self):
        if hasattr(self, 'searching_b_2'):
            self.searching_b_2.clicked.connect(self.filter_stations)
            
        if hasattr(self, 'line_filter_box_2'):
            self.line_filter_box_2.textChanged.connect(self.filter_stations)
            
        if hasattr(self, 'stations_list_2'):
            self.stations_list_2.itemClicked.connect(self.on_station_selected)
            self.stations_list_2.setColumnCount(1)
            self.stations_list_2.horizontalHeader().setVisible(False)
            self.stations_list_2.verticalHeader().setVisible(False)
            self.stations_list_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.stations_list_2.setEditTriggers(QTableWidget.NoEditTriggers)
            self.stations_list_2.setSelectionMode(QAbstractItemView.SingleSelection)
            self.stations_list_2.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.stations_list_2.setShowGrid(False)
            self.stations_list_2.setStyleSheet("""
                QTableWidget { border: 1px solid #bdc3c7; background-color: #fcfcfc; }
                QTableWidget::item { padding: 5px; border-bottom: 1px solid #ecf0f1; }
                QTableWidget::item:selected { background-color: #d2e4f6; color: #2c3e50; font-weight: bold; }
            """)
        
        if hasattr(self, 'choose_direction'):
            self.choose_direction.setRowCount(2)
            self.choose_direction.setColumnCount(2)
            self.choose_direction.horizontalHeader().setVisible(False)
            self.choose_direction.verticalHeader().setVisible(False)
            self.choose_direction.setEditTriggers(QTableWidget.NoEditTriggers)
            self.choose_direction.setSelectionMode(QTableWidget.SingleSelection)
            self.choose_direction.setFocusPolicy(Qt.NoFocus)
            self.choose_direction.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.choose_direction.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.choose_direction.cellClicked.connect(self.on_direction_selected)
            self.update_direction_table("未選擇車站")
        
        if hasattr(self, 'main_timetable'):
            self.main_timetable.setEditTriggers(QTableWidget.NoEditTriggers)
            self.main_timetable.setSelectionMode(QAbstractItemView.NoSelection)
            self.main_timetable.horizontalHeader().setVisible(False)
            self.main_timetable.verticalHeader().setVisible(False)
            self.main_timetable.setShowGrid(False)
            self.main_timetable.installEventFilter(self)

    def eventFilter(self, source, event):
        if hasattr(self, 'main_timetable') and source == self.main_timetable:
            if event.type() == QEvent.Resize:
                self.resize_timer.start(60)
        return super().eventFilter(source, event)

    def check_and_re_render(self):
        if not self.current_station or not hasattr(self, 'main_timetable'):
            return
        available_width = self.main_timetable.viewport().width()
        usable_width = available_width - 80 
        box_width = 42
        new_cols_per_row = max(1, usable_width // box_width)
        
        if new_cols_per_row != self.current_cols_per_row:
            self.current_cols_per_row = new_cols_per_row
            v_scroll = self.main_timetable.verticalScrollBar().value()
            self.render_main_timetable()
            self.main_timetable.verticalScrollBar().setValue(v_scroll)

    def set_engine(self, engine, schedule_type):
        self.engine = engine
        self.schedule_type = schedule_type
        self.refresh_data()

    def refresh_data(self):
        if not self.engine or not self.engine.project_path: return
        
        info_path = os.path.join(self.engine.project_path, "information.json")
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding='utf-8') as f:
                self.route_name = json.load(f).get("路線名稱", "未知路線")

        lvl_path = os.path.join(self.engine.project_path, "train_levels.json")
        if os.path.exists(lvl_path):
            with open(lvl_path, 'r', encoding='utf-8') as f:
                self.train_levels = json.load(f)

        # 🌟 核心升級：一鍵掃描所有路線 CSV，建立「合約連連看」快取！
        self.build_global_dest_cache()

        for direction in ['上行', '下行']:
            suffix = 'up' if direction == '上行' else 'down'
            csv_path = os.path.join(self.engine.project_path, f"{self.schedule_type}_sch_{suffix}.csv")
            self.parse_csv(direction, csv_path)

        stations_set = set(self.timetable_data['上行'].keys()) | set(self.timetable_data['下行'].keys())
        self.stations_list = []
        
        st_json = os.path.join(self.engine.env_path, "station.json")
        if os.path.exists(st_json):
            with open(st_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for k, v in data.items():
                    name = v.get("name")
                    if name and name in stations_set and name not in self.stations_list:
                        self.stations_list.append(name)
                        
        for st in stations_set:
            if st not in self.stations_list: self.stations_list.append(st)

        self.update_station_list()
        
        if self.current_station and self.current_station in self.stations_list:
            self.render_main_timetable()
        elif self.stations_list and hasattr(self, 'stations_list_2'):
            if self.stations_list_2.rowCount() > 0:
                self.stations_list_2.selectRow(0)
                first_item = self.stations_list_2.item(0, 0)
                if first_item:
                    self.on_station_selected(first_item)

    # 🌟 顯式合約解析：完全捨棄 TUD 盲猜，直接看合約追蹤終點！
    def build_global_dest_cache(self):
        self.global_dest_cache = {}
        local_dest_map = {}
        link_map = {}

        if not getattr(self.engine, 'env_path', None): return

        # 掃描全環境所有路線，讀取它們的 CSV 合約
        projects = self.engine.scan_projects()
        for p_id in projects:
            for d_suffix in ['up', 'down']:
                csv_path = os.path.join(self.engine.env_path, p_id, f"{self.schedule_type}_sch_{d_suffix}.csv")
                if not os.path.exists(csv_path): continue

                try:
                    df = pd.read_csv(csv_path, header=None, dtype=str).fillna("")
                    if df.empty or len(df) < 3: continue

                    train_ids = df.iloc[0, 2:].tolist()

                    # 尋找顯式合約的三橫列 (從下往上找)
                    next_line_row, next_id_row = None, None
                    for r in range(len(df)-1, max(0, len(df)-5), -1):
                        val = str(df.iloc[r, 0]).strip()
                        if val == '接續路線': next_line_row = r
                        elif val == '接續車次': next_id_row = r

                    for c_idx in range(2, len(df.columns)):
                        tid = str(train_ids[c_idx-2]).strip()
                        if not tid: continue

                        # 1. 尋找這台車在「這張表(本地)」的終點站
                        dest_st = ""
                        search_end = next_line_row if next_line_row is not None else len(df)
                        for r_idx in range(search_end - 1, 1, -1):
                            cell_val = str(df.iloc[r_idx, c_idx]).strip()
                            if cell_val not in ["", "|", "~"]:
                                st_name = str(df.iloc[r_idx, 0]).strip()
                                if not st_name:
                                    st_name = str(df.iloc[r_idx-1, 0]).strip()
                                dest_st = st_name
                                break
                        local_dest_map[(p_id, tid)] = dest_st

                        # 2. 如果合約說有下一棒，就記錄下來 (連連看)
                        if next_line_row is not None and next_id_row is not None:
                            n_line = str(df.iloc[next_line_row, c_idx]).strip()
                            n_tid = str(df.iloc[next_id_row, c_idx]).strip()
                            if n_line and n_tid:
                                link_map[(p_id, tid)] = (n_line, n_tid)

                except Exception as e:
                    print(f"快取 {p_id} 發生錯誤: {e}")

        # 3. 沿著合約「連連看」，找出真正的最後一站
        for key in local_dest_map.keys():
            visited = set()
            curr = key
            # 一路追下去，直到沒有下一棒為止
            while curr in link_map and curr not in visited:
                visited.add(curr)
                curr = link_map[curr]
            
            final_dest = local_dest_map.get(curr, local_dest_map.get(key, "未知"))
            self.global_dest_cache[key] = final_dest

    def parse_csv(self, direction, filepath):
        self.timetable_data[direction] = {}
        self.destinations[direction] = {}
        
        if not os.path.exists(filepath): return
        
        df = pd.read_csv(filepath, header=None, dtype=str).fillna("")
        if df.empty or len(df) < 3: return
        
        train_ids = df.iloc[0, 2:].tolist()
        grades = df.iloc[1, 2:].tolist()

        # 找出合約的行數，以免把 "接續路線" 當成火車站來畫時刻表
        contract_rows = []
        for r in range(len(df)-1, max(0, len(df)-5), -1):
            if str(df.iloc[r, 0]).strip() in ['接續路線', '接續等級', '接續車次']:
                contract_rows.append(r)
        
        search_end = min(contract_rows) if contract_rows else len(df)
        current_project = getattr(self.engine, 'current_project', "")

        for c_idx in range(2, len(df.columns)):
            tid = str(train_ids[c_idx-2]).strip()
            # 🌟 直接套用剛才算好的「合約追蹤」最終目的地！
            self.destinations[direction][tid] = self.global_dest_cache.get((current_project, tid), "")

        # 解析時刻 (只讀到 search_end，避開底部的合約行)
        for row_idx in range(2, search_end, 2):
            if row_idx + 1 >= search_end: break
            st_name = df.iloc[row_idx, 0].strip()
            if not st_name: continue
            
            if st_name not in self.timetable_data[direction]:
                self.timetable_data[direction][st_name] = []
                
            for c_idx in range(2, len(df.columns)):
                arr_time = df.iloc[row_idx, c_idx].strip()
                dep_time = df.iloc[row_idx + 1, c_idx].strip()
                
                if not dep_time or dep_time in ['|', '~']: 
                    continue
                
                tid = str(train_ids[c_idx-2]).strip()
                g_name = str(grades[c_idx-2]).strip()
                
                from core.timetable_parser import TimetableParser
                sec = TimetableParser.to_seconds(dep_time)
                if sec is not None:
                    h = int(sec // 3600)
                    m = int((sec % 3600) // 60)
                    self.timetable_data[direction][st_name].append((h, m, g_name, tid))

    def update_station_list(self):
        if not hasattr(self, 'stations_list_2'): return
        self.stations_list_2.clearContents()
        self.stations_list_2.setRowCount(len(self.stations_list))
        
        for row, st in enumerate(self.stations_list):
            item = QTableWidgetItem(st)
            item.setTextAlignment(Qt.AlignCenter) 
            font = QFont("Microsoft JhengHei", 12, QFont.Bold)
            item.setFont(font)
            self.stations_list_2.setItem(row, 0, item)
            self.stations_list_2.setRowHeight(row, 45) 

    def filter_stations(self):
        if not hasattr(self, 'line_filter_box_2') or not hasattr(self, 'stations_list_2'): return
        kw = self.line_filter_box_2.text().strip()
        
        for row in range(self.stations_list_2.rowCount()):
            item = self.stations_list_2.item(row, 0)
            if item:
                hidden = (kw not in item.text()) if kw != "" else False
                self.stations_list_2.setRowHidden(row, hidden)

    def on_station_selected(self, item):
        self.current_station = item.text()
        self.update_direction_table(self.current_station)
        self.render_main_timetable()

    def update_direction_table(self, st_name):
        if not hasattr(self, 'choose_direction'): return
        self.choose_direction.clear()
        
        self.choose_direction.setSpan(0, 0, 1, 2)
        title_item = QTableWidgetItem(f"選擇方向 ({st_name})")
        title_item.setTextAlignment(Qt.AlignCenter)
        title_item.setFont(QFont("Microsoft JhengHei", 11, QFont.Bold))
        title_item.setBackground(QColor("#ecf0f1"))
        title_item.setForeground(QColor("#2c3e50"))
        self.choose_direction.setItem(0, 0, title_item)
        
        up_item = QTableWidgetItem("上行")
        up_item.setTextAlignment(Qt.AlignCenter)
        up_item.setFont(QFont("Microsoft JhengHei", 12, QFont.Bold))
        
        down_item = QTableWidgetItem("下行")
        down_item.setTextAlignment(Qt.AlignCenter)
        down_item.setFont(QFont("Microsoft JhengHei", 12, QFont.Bold))
        
        if self.current_direction == "上行":
            up_item.setBackground(QColor("#2980b9"))
            up_item.setForeground(QColor("white"))
            down_item.setBackground(QColor("white"))
            down_item.setForeground(QColor("#7f8c8d"))
        else:
            down_item.setBackground(QColor("#2980b9"))
            down_item.setForeground(QColor("white"))
            up_item.setBackground(QColor("white"))
            up_item.setForeground(QColor("#7f8c8d"))

        self.choose_direction.setItem(1, 0, up_item)
        self.choose_direction.setItem(1, 1, down_item)

    def on_direction_selected(self, row, col):
        if row == 1:
            self.current_direction = "上行" if col == 0 else "下行"
            self.update_direction_table(self.current_station)
            self.render_main_timetable()

    def render_main_timetable(self):
        if not hasattr(self, 'main_timetable'): return
        self.main_timetable.clear()
        
        if not self.current_station: return
        
        trains = self.timetable_data[self.current_direction].get(self.current_station, [])
        if not trains:
            self.main_timetable.setRowCount(1)
            self.main_timetable.setColumnCount(1)
            self.main_timetable.setItem(0, 0, QTableWidgetItem("此方向無發車資料。"))
            return

        grouped_times = {}
        min_h, max_h = 99, 0
        for h, m, g, tid in trains:
            dest = self.destinations[self.current_direction].get(tid, "")
            if h not in grouped_times: grouped_times[h] = []
            grouped_times[h].append((m, g, dest))
            min_h = min(min_h, h)
            max_h = max(max_h, h)
            
        for h in grouped_times:
            grouped_times[h].sort(key=lambda x: x[0]) 
            
        row_count = (max_h - min_h + 1) + 1 
        self.main_timetable.setRowCount(row_count)
        self.main_timetable.setColumnCount(5)
        
        dests = set(self.destinations[self.current_direction].get(tid, "") for h, m, g, tid in trains if self.destinations[self.current_direction].get(tid, ""))
        dest_list = list(dests)
        dest_str = f"往 {'、'.join(dest_list[:3])}" + (" 等" if len(dest_list)>3 else "") + " 方面"
        
        headers = [
            f"{self.current_station} 站",
            f"{self.route_name}",
            f"{self.current_direction}",
            f"{dest_str}",
            f"{'平日' if self.schedule_type == 'weekdays' else '假日'}"
        ]
        
        for i, text in enumerate(headers):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("#2c3e50"))
            item.setForeground(QColor("white"))
            item.setFont(QFont("Microsoft JhengHei", 11, QFont.Bold))
            self.main_timetable.setItem(0, i, item)
            
        for i, h in enumerate(range(min_h, max_h + 1)):
            row = i + 1
            
            display_h = h % 24 if h >= 24 else h 
            h_item = QTableWidgetItem(f"{display_h:02d}")
            h_item.setTextAlignment(Qt.AlignCenter)
            h_item.setFont(QFont("Arial", 16, QFont.Bold))
            h_item.setBackground(QColor("#ecf0f1"))
            h_item.setForeground(QColor("#2c3e50"))
            self.main_timetable.setItem(row, 0, h_item)
            
            self.main_timetable.setSpan(row, 1, 1, 4)
            
            trains_in_hour = grouped_times.get(h, [])
            
            html_parts = ['<table cellpadding="4" cellspacing="5">']
            
            if not trains_in_hour:
                html_parts.append('<tr><td style="min-width: 70px; padding: 2px 6px;"></td></tr>')
                num_lines = 1
            else:
                chunks = [trains_in_hour[k:k + self.current_cols_per_row] for k in range(0, len(trains_in_hour), self.current_cols_per_row)]
                num_lines = len(chunks)
                
                for chunk in chunks:
                    html_parts.append('<tr>')
                    for m, g, dest in chunk:
                        color = "#000000"
                        display_name = g
                        
                        if g in self.train_levels:
                            tinfo = self.train_levels[g]
                            display_name = tinfo.get('name', g)
                            color = tinfo.get('color', color)
                        else:
                            for tid, tinfo in self.train_levels.items():
                                if tinfo.get('name') == g:
                                    display_name = g
                                    color = tinfo.get('color', color)
                                    break
                        
                        g_short = display_name[:2] 
                        dest_short = dest[:2] if dest else "" 

                        html_parts.append(f"""
                        <td align="center" style="min-width: 70px; padding: 2px 6px; border: 1px solid #dcdde1; background-color: #fcfcfc; border-radius: 4px;">
                            <span style="color:{color}; font-size:11px; font-weight:bold;">{g_short}</span><br>
                            <span style="color:{color}; font-size:20px; font-weight:bold;">{m:02d}</span><br>
                            <span style="color:#7f8c8d; font-size:11px; font-weight:bold;">{dest_short}</span>
                        </td>
                        """)
                    
                    if len(chunk) < self.current_cols_per_row:
                        for _ in range(self.current_cols_per_row - len(chunk)):
                            html_parts.append('<td style="min-width: 70px; padding: 2px 6px;"></td>')
                            
                    html_parts.append('</tr>')
                    
            html_parts.append('</table>')
            
            cell_widget = QLabel("".join(html_parts))
            cell_widget.setTextFormat(Qt.RichText)
            cell_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.main_timetable.setCellWidget(row, 1, cell_widget)
            
            self.main_timetable.setRowHeight(row, 75 * num_lines)
            
        self.main_timetable.setColumnWidth(0, 60)
        self.main_timetable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)