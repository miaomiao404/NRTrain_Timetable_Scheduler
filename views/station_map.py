import os
import json
import re
import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QGraphicsView, QGraphicsScene, QFrame)
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainter

class StationMapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = None
        self.stations_data = {}
        
        self._renderers = [] 
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # ==========================================
        # 建立固定在頂部的獨立資訊欄 (Sticky Info Bar)
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
        self.view.setRenderHint(QPainter.Antialiasing | QPainter.SmoothPixmapTransform) 
        self.view.setBackgroundBrush(QColor("#f4f6f7")) 
        self.view.setStyleSheet("border: none;")
        
        self.layout.addWidget(self.view)

    def set_engine(self, engine):
        self.engine = engine

    def get_svg_path(self, category, state):
        base_dir = os.path.join("assets", "station_map")
        
        if category == "left":
            mapping = {
                "double": "left_double_arrow.svg",
                "right": "left_in_arrow.svg",   
                "left": "left_out_arrow.svg",   
                "cross": "left_end.svg"         
            }
        elif category == "right":
            mapping = {
                "double": "right_double_arrow.svg",
                "right": "right_out_arrow.svg", 
                "left": "right_in_arrow.svg",   
                "cross": "right_end.svg"        
            }
        elif category == "route":
            mapping = {
                "double": "route_double_arrow.svg",
                "left": "route_left_arrow.svg",
                "right": "route_right_arrow.svg"
            }
        else:
            return None
            
        filename = mapping.get(state)
        if filename:
            return os.path.join(base_dir, filename)
        return None

    def load_colored_svg_item(self, filepath, hex_color):
        """讀取 SVG，精準染色並取得絕對尺寸"""
        if not filepath or not os.path.exists(filepath): 
            return None, 50, 20 
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                svg_content = f.read()

            svg_content = re.sub(r'(?i)#ffffff|#fff|\bwhite\b', hex_color, svg_content)
            
            style_injection = f"<style>path, polygon, rect, line {{ fill: {hex_color} !important; stroke: {hex_color} !important; stroke-width: 0.3px !important; }}</style>"
            svg_content = re.sub(r'(<svg[^>]*>)', r'\1' + style_injection, svg_content, count=1, flags=re.IGNORECASE)

            byte_array = QByteArray(svg_content.encode('utf-8'))
            renderer = QSvgRenderer()
            if not renderer.load(byte_array) or not renderer.isValid():
                return None, 50, 20

            self._renderers.append(renderer) 
            item = QGraphicsSvgItem()
            item.setSharedRenderer(renderer)
            
            vb = renderer.viewBox()
            if vb.isValid() and vb.width() > 0:
                w, h = vb.width(), vb.height()
            else:
                w, h = renderer.defaultSize().width(), renderer.defaultSize().height()
                
            return item, w, h
            
        except Exception as e:
            print(f"載入 SVG 發生錯誤: {e}")
            return None, 50, 20

    def load_map(self):
        self.scene.clear()
        self._renderers.clear() 
        
        self.route_name_lbl.setText("請先載入路線專案並確保包含時刻表資料")
        self.route_name_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #7f8c8d; border: none;")
        self.left_dir_lbl.setText("")
        self.right_dir_lbl.setText("")
        
        if not self.engine or not self.engine.current_project:
            txt = self.scene.addText("無可用的繪圖資料。")
            txt.setFont(QFont("Microsoft JhengHei", 12))
            return
            
        route_color = "#3498db" 
        route_name = self.engine.current_project
        info_path = os.path.join(self.engine.project_path, "information.json")
        if os.path.exists(info_path):
            try:
                with open(info_path, 'r', encoding='utf-8') as f:
                    info_data = json.load(f)
                    route_color = info_data.get("路線顏色", "#3498db")
                    route_name = info_data.get("路線名稱", route_name)
            except: pass

        if os.path.exists(self.engine.station_file):
            try:
                with open(self.engine.station_file, 'r', encoding='utf-8') as f:
                    self.stations_data = json.load(f)
            except:
                self.stations_data = {}
                
        proj_path = self.engine.project_path
        stb_up = os.path.join(proj_path, "stb_up.csv")
        stb_down = os.path.join(proj_path, "stb_down.csv")
        
        route_stations = []
        up_dest = ""
        down_dest = ""
        
        if os.path.exists(stb_up):
            df_up = pd.read_csv(stb_up)
            valid_up = [str(st) for st in df_up['車站'].tolist() if pd.notna(st)]
            if valid_up:
                up_dest = valid_up[-1]
                route_stations = valid_up
                
        if os.path.exists(stb_down):
            df_down = pd.read_csv(stb_down)
            valid_down = [str(st) for st in df_down['車站'].tolist() if pd.notna(st)]
            if valid_down:
                down_dest = valid_down[-1]
                if not route_stations:
                    route_stations = valid_down[::-1]
            
        if not route_stations:
            txt = self.scene.addText("找不到時刻表中的車站，請先匯入時刻表。")
            txt.setFont(QFont("Microsoft JhengHei", 12))
            return
            
        self.route_name_lbl.setText(route_name)
        self.route_name_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; border: none;")
        
        if down_dest:
            self.left_dir_lbl.setText(f"◀ 下行 往 {down_dest}")
            self.left_dir_lbl.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {route_color}; border: none;")
        if up_dest:
            self.right_dir_lbl.setText(f"上行 往 {up_dest} ▶")
            self.right_dir_lbl.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {route_color}; border: none;")
            
        name_to_id = {sdata.get('name'): sid for sid, sdata in self.stations_data.items()}
            
        x_offset = 50
        GLOBAL_CENTER_Y = 200 # 拉高中軸線，避免站名超出畫面上緣
        TRACK_SPACING = 30    
        OVERLAP = 0.5 

        for i, st_name in enumerate(route_stations):
            sid = name_to_id.get(st_name)
            if not sid:
                text = self.scene.addText(f"{st_name} (無設定資料)")
                text.setFont(QFont("Microsoft JhengHei", 12, QFont.Bold))
                text.setPos(x_offset, GLOBAL_CENTER_Y - 40)
                x_offset += 150
                continue
                
            sdata = self.stations_data.get(sid, {})
            tracks = sdata.get('tracks', [])
            num_tracks = len(tracks)
            station_width = 0
            
            # 🌟 邏輯修正：計算本站股道的 Y 軸分配，全部圍繞 GLOBAL_CENTER_Y 展開
            if num_tracks > 0:
                station_total_height = (num_tracks - 1) * TRACK_SPACING
                track_start_center_y = GLOBAL_CENTER_Y - (station_total_height / 2)
            else:
                track_start_center_y = GLOBAL_CENTER_Y
                station_width = 100
                
                # 繪製完美置中於中軸的虛線
                pen = QPen(QColor("#bdc3c7"), 2, Qt.DashLine)
                self.scene.addLine(x_offset, GLOBAL_CENTER_Y, x_offset + station_width, GLOBAL_CENTER_Y, pen)
                
                # 文字與中軸對齊，留出 2px 呼吸空間
                no_trk = self.scene.addText("(尚無股道)")
                no_trk.setFont(QFont("Microsoft JhengHei", 8, QFont.Bold))
                no_trk.setDefaultTextColor(QColor("#7f8c8d"))
                nt_rect = no_trk.boundingRect()
                no_trk.setPos(x_offset + (station_width - nt_rect.width()) / 2, GLOBAL_CENTER_Y - nt_rect.height() - 2)
            
            # --- 繪製股道與置中文字 ---
            for t_idx, track in enumerate(tracks):
                left_sig = track.get('left_signal', 'double')
                right_sig = track.get('right_signal', 'double')
                
                curr_x = x_offset
                current_track_center_y = track_start_center_y + t_idx * TRACK_SPACING
                
                # 左側 SVG
                l_path = self.get_svg_path("left", left_sig)
                l_item, l_w, l_h = self.load_colored_svg_item(l_path, route_color)
                if l_item:
                    # 🌟 絕對中軸對齊：Y座標 = 軌道中心線 - (圖形高度 / 2)
                    l_item.setPos(curr_x, current_track_center_y - (l_h / 2))
                    self.scene.addItem(l_item)
                else:
                    l_w, l_h = 50, 4
                    self.scene.addRect(curr_x, current_track_center_y - (l_h / 2), l_w, l_h, QPen(Qt.NoPen), QBrush(QColor(route_color)))
                    
                curr_x += l_w - OVERLAP 
                
                # 右側 SVG
                r_path = self.get_svg_path("right", right_sig)
                r_item, r_w, r_h = self.load_colored_svg_item(r_path, route_color)
                if r_item:
                    r_item.setPos(curr_x, current_track_center_y - (r_h / 2))
                    self.scene.addItem(r_item)
                else:
                    r_w, r_h = 50, 4
                    self.scene.addRect(curr_x, current_track_center_y - (r_h / 2), r_w, r_h, QPen(Qt.NoPen), QBrush(QColor(route_color)))
                    
                total_w = l_w + r_w - OVERLAP
                station_width = max(station_width, total_w)
                
                # 🌟 文字精準置中疊加，底部距離中心軌道 2px
                track_name = track.get("name", "股道")
                text_item = self.scene.addText(track_name)
                text_item.setFont(QFont("Microsoft JhengHei", 8, QFont.Bold))
                text_item.setDefaultTextColor(QColor("#2c3e50")) 
                text_item.setZValue(10)
                
                text_rect = text_item.boundingRect()
                t_x = x_offset + (total_w - text_rect.width()) / 2
                t_y = current_track_center_y - text_rect.height() - 2
                text_item.setPos(t_x, t_y)
                
            # --- 車站名稱 (固定距離最上方股道中軸線 45px 的位置) ---
            st_text = self.scene.addText(st_name)
            st_text.setFont(QFont("Microsoft JhengHei", 12, QFont.Bold))
            st_text.setDefaultTextColor(QColor("#111111"))
            st_rect = st_text.boundingRect()
            
            st_x = x_offset + (station_width - st_rect.width()) / 2
            st_y = track_start_center_y - 45 
            st_text.setPos(st_x, st_y)
            
            x_offset += station_width - OVERLAP
            
            # --- 繪製連接軌道 (一樣絕對中軸對齊) ---
            if i < len(route_stations) - 1:
                next_st_name = route_stations[i+1]
                next_sid = name_to_id.get(next_st_name)
                
                conn = next((c for c in sdata.get('connections', []) if c.get('target_station') == next_sid and c.get('side') != 'facility'), None)
                        
                conn_width = 0
                if conn:
                    conn_tracks = conn.get('tracks', [])
                    num_conn = len(conn_tracks)
                    
                    if num_conn > 0:
                        conn_total_height = (num_conn - 1) * TRACK_SPACING
                        conn_start_center_y = GLOBAL_CENTER_Y - (conn_total_height / 2)
                        
                        for c_idx, c_track in enumerate(conn_tracks):
                            c_dir = c_track.get('dir', 'double')
                            c_path = self.get_svg_path("route", c_dir)
                            
                            current_conn_center_y = conn_start_center_y + c_idx * TRACK_SPACING
                            
                            c_item, c_w, c_h = self.load_colored_svg_item(c_path, route_color)
                            if c_item:
                                c_item.setPos(x_offset, current_conn_center_y - (c_h / 2))
                                self.scene.addItem(c_item)
                            else:
                                c_w, c_h = 50, 4
                                self.scene.addRect(x_offset, current_conn_center_y - (c_h / 2), c_w, c_h, QPen(Qt.NoPen), QBrush(QColor(route_color)))
                                
                            conn_width = max(conn_width, c_w)
                else:
                    conn_width = 80 
                    pen = QPen(QColor(route_color), 2, Qt.DashLine)
                    self.scene.addLine(x_offset, GLOBAL_CENTER_Y, x_offset + conn_width, GLOBAL_CENTER_Y, pen)
                    
                    no_conn_text = self.scene.addText("(未設定)")
                    no_conn_text.setFont(QFont("Microsoft JhengHei", 8, QFont.Bold))
                    no_conn_text.setDefaultTextColor(QColor("#7f8c8d"))
                    nc_rect = no_conn_text.boundingRect()
                    
                    no_conn_text.setPos(x_offset + (conn_width - nc_rect.width()) / 2, GLOBAL_CENTER_Y - nc_rect.height() - 2)
                    
                x_offset += conn_width - OVERLAP
                
        self.scene.setSceneRect(0, 0, x_offset + 100, GLOBAL_CENTER_Y * 2)