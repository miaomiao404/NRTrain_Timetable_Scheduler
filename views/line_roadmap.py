import os
import json
import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QGraphicsView, QGraphicsScene, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainter

class LineRoadmapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = None
        self.stations_data = {}
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # ==========================================
        # 固定在頂部的獨立資訊欄 (Sticky Info Bar)
        # ==========================================
        self.info_bar = QFrame()
        self.info_bar.setFixedHeight(50)
        self.info_bar.setStyleSheet("background-color: #ffffff; border-bottom: 2px solid #dcdde1;")
        
        self.info_layout = QHBoxLayout(self.info_bar)
        self.info_layout.setContentsMargins(20, 0, 20, 0)
        
        self.left_dir_lbl = QLabel("")
        self.route_name_lbl = QLabel("請先載入路線專案並確保包含時刻表資料")
        self.route_name_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #7f8c8d; border: none;")
        self.right_dir_lbl = QLabel("")
        
        self.left_dir_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.route_name_lbl.setAlignment(Qt.AlignCenter)
        self.right_dir_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.info_layout.addWidget(self.left_dir_lbl, 1)
        self.info_layout.addWidget(self.route_name_lbl, 2)
        self.info_layout.addWidget(self.right_dir_lbl, 1)
        
        self.layout.addWidget(self.info_bar)
        
        # ==========================================
        # 建立地圖畫布
        # ==========================================
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing) 
        self.view.setBackgroundBrush(QColor("#fcfcfc")) # 乾淨的亮白背景
        self.view.setStyleSheet("border: none;")
        
        self.layout.addWidget(self.view)

    def set_engine(self, engine):
        self.engine = engine

    def _get_stops_from_df(self, df, target_cols):
        """解析 CSV，判斷在指定的欄位中，各車站是否有停靠時間"""
        stops = {}
        if df is None or df.empty: return stops
        
        current_st = None
        for idx, row in df.iterrows():
            st_val = str(row.get('車站', ''))
            if st_val != 'nan' and st_val.strip() != '':
                current_st = st_val.strip()
                if current_st not in stops:
                    stops[current_st] = False
            
            if current_st:
                for col in target_cols:
                    if col in df.columns:
                        val = str(row[col])
                        # 只要有填時間，且不是跳過符號，就判定為停靠
                        if val != 'nan' and val.strip() not in ['', '|', '~', '通過']:
                            stops[current_st] = True
        return stops

    def load_map(self):
        self.scene.clear()
        
        self.route_name_lbl.setText("請先載入路線專案並確保包含時刻表資料")
        self.route_name_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #7f8c8d; border: none;")
        self.left_dir_lbl.setText("")
        self.right_dir_lbl.setText("")
        
        if not self.engine or not self.engine.current_project:
            return
            
        proj_path = self.engine.project_path
        
        # 1. 抓取目前路線的顏色與名稱
        route_color = "#3498db" 
        route_name = self.engine.current_project
        info_path = os.path.join(proj_path, "information.json")
        if os.path.exists(info_path):
            try:
                with open(info_path, 'r', encoding='utf-8') as f:
                    info_data = json.load(f)
                    route_color = info_data.get("路線顏色", "#3498db")
                    route_name = info_data.get("路線名稱", route_name)
            except: pass

        # 2. 抓取車站屬性庫 (為了取得代號)
        if os.path.exists(self.engine.station_file):
            try:
                with open(self.engine.station_file, 'r', encoding='utf-8') as f:
                    self.stations_data = json.load(f)
            except:
                self.stations_data = {}
        name_to_id = {sdata.get('name'): sid for sid, sdata in self.stations_data.items()}

        # 3. 解析時刻表
        stb_up = os.path.join(proj_path, "stb_up.csv")
        stb_down = os.path.join(proj_path, "stb_down.csv")
        
        df_up = pd.read_csv(stb_up) if os.path.exists(stb_up) else None
        df_down = pd.read_csv(stb_down) if os.path.exists(stb_down) else None
        
        route_stations = []
        if df_up is not None:
            route_stations = [str(st).strip() for st in df_up['車站'].tolist() if pd.notna(st) and str(st).strip() != '']
            route_stations = list(dict.fromkeys(route_stations)) # 保留順序去重
        elif df_down is not None:
            route_stations = [str(st).strip() for st in df_down['車站'].tolist() if pd.notna(st) and str(st).strip() != ''][::-1]
            route_stations = list(dict.fromkeys(route_stations))
            
        if not route_stations:
            txt = self.scene.addText("找不到時刻表中的車站，請先匯入時刻表。")
            txt.setFont(QFont("Microsoft JhengHei", 12))
            return

        # 更新上方資訊列
        self.route_name_lbl.setText(f"{route_name} - 列車停靠路線圖")
        self.route_name_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; border: none;")
        
        down_dest = route_stations[0]
        up_dest = route_stations[-1]
        self.left_dir_lbl.setText(f"◀ 下行 往 {down_dest}")
        self.left_dir_lbl.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {route_color}; border: none;")
        self.right_dir_lbl.setText(f"上行 往 {up_dest} ▶")
        self.right_dir_lbl.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {route_color}; border: none;")

        # 4. 抓取並合併列車等級
        unique_grades = {}
        json_path = os.path.join(proj_path, "train_levels.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    levels = json.load(f)
                    for k, v in levels.items():
                        name = v.get('name', k)
                        if name not in unique_grades:
                            unique_grades[name] = {'color': v.get('color', '#333333'), 'up_cols': [], 'down_cols': []}
                        if v.get('direction') == '上行':
                            unique_grades[name]['up_cols'].append(k)
                        else:
                            unique_grades[name]['down_cols'].append(k)
            except: pass

        if not unique_grades:
            txt = self.scene.addText("尚未設定任何列車等級。")
            txt.setFont(QFont("Microsoft JhengHei", 12))
            return

        # 5. 分析停靠邏輯
        stops = {}
        for g_name, g_info in unique_grades.items():
            stops[g_name] = {st: {'up': False, 'down': False} for st in route_stations}
            
            up_stops = self._get_stops_from_df(df_up, g_info['up_cols'])
            for st in route_stations:
                stops[g_name][st]['up'] = up_stops.get(st, False)
                
            down_stops = self._get_stops_from_df(df_down, g_info['down_cols'])
            for st in route_stations:
                stops[g_name][st]['down'] = down_stops.get(st, False)

        # 6. 開始繪圖參數設定
        STATION_SPACING = 120
        GRADE_SPACING = 40
        X_START = 150
        Y_START = 150
        LINE_THICKNESS = 12
        
        # 繪製垂直基準引導線 (淡灰色)
        for s_idx, st in enumerate(route_stations):
            x = X_START + s_idx * STATION_SPACING
            line_y_end = Y_START + len(unique_grades) * GRADE_SPACING
            self.scene.addLine(x, Y_START - 20, x, line_y_end, QPen(QColor("#ecf0f1"), 1))

        # 繪製等級橫線與左側標籤
        for i, (g_name, g_info) in enumerate(unique_grades.items()):
            y = Y_START + i * GRADE_SPACING
            color = g_info['color']
            
            # 尋找該等級的第一個與最後一個停靠站，智慧決定線條長度
            stop_indices = [s_idx for s_idx, st in enumerate(route_stations) 
                            if stops[g_name][st]['up'] or stops[g_name][st]['down']]
                            
            if stop_indices:
                start_idx = min(stop_indices)
                end_idx = max(stop_indices)
                line_x_start = X_START + start_idx * STATION_SPACING
                line_w = (end_idx - start_idx) * STATION_SPACING
                
                # 畫 12px 粗線 (中心點對齊 Y)
                self.scene.addRect(line_x_start, y, line_w, LINE_THICKNESS, QPen(Qt.NoPen), QBrush(QColor(color)))

            # 左側等級名稱標籤
            txt_grade = self.scene.addText(g_name)
            txt_grade.setFont(QFont("Microsoft JhengHei", 11, QFont.Bold))
            txt_grade.setDefaultTextColor(QColor(color))
            g_rect = txt_grade.boundingRect()
            # 置於起始點左側
            txt_grade.setPos(X_START - g_rect.width() - 30, y + (LINE_THICKNESS/2) - (g_rect.height()/2))

        # 繪製各站停靠圓圈與站名
        for s_idx, st in enumerate(route_stations):
            x = X_START + s_idx * STATION_SPACING
            
            sid = name_to_id.get(st, "")
            line_id = self.stations_data.get(sid, {}).get("line_id", "")
            
            # 畫頂部站名 (第一行)
            txt_st = self.scene.addText(st)
            txt_st.setFont(QFont("Microsoft JhengHei", 13, QFont.Bold))
            txt_st.setDefaultTextColor(QColor("#2c3e50"))
            rect_st = txt_st.boundingRect()
            txt_st.setPos(x - rect_st.width()/2, Y_START - 75)
            
            # 畫頂部路線代號 (第二行)
            txt_id = self.scene.addText(line_id if line_id else "-")
            txt_id.setFont(QFont("Arial", 9, QFont.Bold))
            txt_id.setDefaultTextColor(QColor("#7f8c8d"))
            rect_id = txt_id.boundingRect()
            txt_id.setPos(x - rect_id.width()/2, Y_START - 45)

            # 畫停靠點 (圓圈)
            for i, (g_name, g_info) in enumerate(unique_grades.items()):
                y = Y_START + i * GRADE_SPACING
                color = g_info['color']
                
                stop_up = stops[g_name][st]['up']
                stop_down = stops[g_name][st]['down']
                
                # 直線的中心點在 y + (LINE_THICKNESS/2) 即 y + 6
                center_y = y + 6
                
                if stop_up and stop_down:
                    # 雙向停靠：畫直徑 12px 圓圈
                    r = 6 
                    self.scene.addEllipse(x - r, center_y - r, r*2, r*2, 
                                          QPen(QColor(color), 2), QBrush(QColor("white")))
                elif stop_up or stop_down:
                    # 單向停靠：畫直徑 6px 圓圈
                    r = 3 
                    self.scene.addEllipse(x - r, center_y - r, r*2, r*2, 
                                          QPen(QColor(color), 1.5), QBrush(QColor("white")))
                                          
        total_width = X_START + (len(route_stations) - 1) * STATION_SPACING + 100
        total_height = Y_START + len(unique_grades) * GRADE_SPACING + 50
        self.scene.setSceneRect(0, 0, total_width, total_height)