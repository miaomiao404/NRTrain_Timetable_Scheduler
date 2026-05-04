import os
import json
import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                               QTableWidgetItem, QLabel, QFrame, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

class ScheduleTableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = None
        self.train_levels = {}
        self.current_csv_path = ""
        self.current_title = ""
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # 頂部資訊列
        self.info_bar = QFrame()
        self.info_bar.setFixedHeight(50)
        self.info_bar.setStyleSheet("background-color: #ffffff; border-bottom: 2px solid #dcdde1;")
        self.info_layout = QVBoxLayout(self.info_bar)
        self.info_layout.setContentsMargins(20, 0, 0, 0)
        
        self.title_lbl = QLabel("班次時刻表")
        self.title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        self.info_layout.addWidget(self.title_lbl)
        self.layout.addWidget(self.info_bar)
        
        # ==========================================
        # 🌟 核心修改：建立水平並排佈局放置雙表格
        # ==========================================
        self.tables_layout = QHBoxLayout()
        self.tables_layout.setContentsMargins(0, 0, 0, 0)
        self.tables_layout.setSpacing(0) # 兩表無縫接合
        self.layout.addLayout(self.tables_layout)
        
        # 左側表格 (固定顯示車站、到發)
        self.left_table = QTableWidget()
        self.left_table.setColumnCount(2)
        # 固定左表寬度 (站名 120 + 到發 50 + 邊框微調 2)
        self.left_table.setFixedWidth(172)
        
        # 🌟 修正點：直接對 table 設定捲軸顯示策略
        self.left_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # 隱藏左表水平捲軸
        self.left_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   # 隱藏左表垂直捲軸
        
        # 右側表格 (顯示車次與時間，可水平滑動)
        self.right_table = QTableWidget()
        
        # 雙表通用樣式設定
        for tb in (self.left_table, self.right_table):
            tb.setEditTriggers(QTableWidget.NoEditTriggers)
            tb.setAlternatingRowColors(True)
            tb.verticalHeader().hide() # 隱藏左側列號確保高度一致
            tb.setStyleSheet("""
                QTableWidget { background-color: #fcfcfc; border: none; }
                QTableWidget::item:selected { background-color: #d2e4f6; color: black; }
            """)
            
        # 在左右表中間加一條分隔線效果
        self.left_table.setStyleSheet(self.left_table.styleSheet() + "QTableWidget { border-right: 2px solid #bdc3c7; }")

        self.tables_layout.addWidget(self.left_table)
        self.tables_layout.addWidget(self.right_table)
        
        # 🌟 最關鍵的魔法：將左右表的垂直捲軸互相連動綁定 (同步滾動)
        self.left_table.verticalScrollBar().valueChanged.connect(self.right_table.verticalScrollBar().setValue)
        self.right_table.verticalScrollBar().valueChanged.connect(self.left_table.verticalScrollBar().setValue)

    def set_engine(self, engine):
        self.engine = engine

    def load_csv(self, csv_path, title_text):
        self.current_csv_path = csv_path
        self.current_title = title_text
        self.title_lbl.setText(title_text)
        
        self.left_table.clear()
        self.left_table.setRowCount(0)
        self.right_table.clear()
        self.right_table.setRowCount(0)
        self.right_table.setColumnCount(0)
        
        if not os.path.exists(csv_path):
            self.title_lbl.setText(f"{title_text} - 尚未生成 (請先執行模擬排班以產生報表)")
            self.title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")
            return
            
        self.title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        
        if self.engine and self.engine.project_path:
            lvl_path = os.path.join(self.engine.project_path, "train_levels.json")
            if os.path.exists(lvl_path):
                with open(lvl_path, 'r', encoding='utf-8') as f:
                    self.train_levels = json.load(f)
                    
        try:
            df = pd.read_csv(csv_path, header=None, dtype=str).fillna("")
            if df.empty: return
            
            row_count = df.shape[0] - 1
            col_count = df.shape[1]
            
            # 設定雙表的列數與欄數
            self.left_table.setRowCount(row_count)
            self.right_table.setRowCount(row_count)
            self.right_table.setColumnCount(col_count - 2)
            
            headers = [str(x) for x in df.iloc[0].tolist()]
            self.left_table.setHorizontalHeaderLabels(headers[:2])
            if len(headers) > 2:
                self.right_table.setHorizontalHeaderLabels(headers[2:])
            
            col_colors = {}
            if df.shape[0] > 1:
                for col_idx in range(2, col_count):
                    g_name = str(df.iloc[1, col_idx]).strip()
                    color = "#2980b9" 
                    for tid, tinfo in self.train_levels.items():
                        if tinfo['name'] == g_name:
                            color = tinfo.get('color', color)
                            break
                    col_colors[col_idx] = color
            
            for row_idx in range(1, df.shape[0]):
                r = row_idx - 1 # 表格的 index
                
                # 統一設定一個固定的列高，確保左右表完美對齊
                row_height = 30
                self.left_table.setRowHeight(r, row_height)
                self.right_table.setRowHeight(r, row_height)

                for col_idx in range(col_count):
                    val = str(df.iloc[row_idx, col_idx])
                    item = QTableWidgetItem(val)
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    # 填入左側凍結表
                    if col_idx < 2:
                        item.setFont(QFont("Microsoft JhengHei", 9, QFont.Bold))
                        item.setBackground(QColor("#f2f4f6"))
                        if val in ["到", "發"]:
                            item.setForeground(QColor("#7f8c8d"))
                        self.left_table.setItem(r, col_idx, item)
                        
                    # 填入右側滑動表
                    else:
                        c = col_idx - 2
                        if row_idx == 1: 
                            item.setFont(QFont("Microsoft JhengHei", 9, QFont.Bold))
                            item.setBackground(QColor("#eef5fa"))
                            if val:
                                item.setForeground(QColor(col_colors.get(col_idx, "#2980b9")))
                        else:            
                            if val and val not in ['|', '~']:
                                item.setForeground(QColor(col_colors.get(col_idx, "#000000")))
                            elif val in ['|', '~']:
                                item.setForeground(QColor("#bdc3c7"))
                                
                        self.right_table.setItem(r, c, item)
            
            # 固定左表欄寬
            self.left_table.setColumnWidth(0, 120) 
            self.left_table.setColumnWidth(1, 50)
            
            # 右表自動調整欄寬
            self.right_table.resizeColumnsToContents()
            
        except Exception as e:
            self.title_lbl.setText(f"{title_text} - 讀取失敗: {e}")
            
    def refresh(self):
        if self.current_csv_path and self.current_title:
            self.load_csv(self.current_csv_path, self.current_title)