import os
import json
import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                               QTableWidgetItem, QLabel, QFrame, QHeaderView, QStyledItemDelegate)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QBrush, QPen

# 🌟 新增：專屬區塊繪圖器，用來繪製 2x6 的運用外框線
class BlockBorderDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # 先畫出原本的儲存格內容與背景
        super().paint(painter, option, index)
        
        r = index.row()
        c = index.column()
        cols = index.model().columnCount()
        
        painter.save()
        # 設定較粗的框線顏色 (冷灰藍色)
        pen = QPen(QColor("#a5b1c2"), 2)
        painter.setPen(pen)
        
        rect = option.rect
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        
        # 1. 畫水平分隔線：每台車的底部 (也就是單數列的下方)
        if r % 2 == 1:
            painter.drawLine(x, y + h - 1, x + w, y + h - 1)
            
        # 2. 畫垂直分隔線：區分基本資料區與每一個運用區塊
        # 條件：第 2 欄 (初始出發地右側) 或是 每一個運用區塊的最後一欄 (c-3)%6 == 5
        if c == 2 or (c >= 3 and c < cols - 1 and (c - 3) % 6 == 5):
            painter.drawLine(x + w - 1, y, x + w - 1, y + h)
            
        painter.restore()

class TudTableWidget(QWidget):
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
        
        self.title_lbl = QLabel("車輛運用表")
        self.title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        self.info_layout.addWidget(self.title_lbl)
        self.layout.addWidget(self.info_bar)
        
        # 報表表格本體
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f9fbfd;
                gridline-color: #ecf0f1;
                border: none;
            }
            QHeaderView::section {
                background-color: #f1f2f6;
                color: #2f3640;
                font-weight: bold;
                border: none;
                border-right: 1px solid #dcdde1;
                border-bottom: 1px solid #dcdde1;
                padding: 4px;
            }
        """)
        # 隱藏左側的預設行號，讓版面更乾淨
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(28) # 緊湊排版
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # 🌟 套用自訂的區塊邊框繪圖器
        self.table.setItemDelegate(BlockBorderDelegate(self.table))
        
        self.layout.addWidget(self.table)

    def load_csv(self, filepath, title_text=""):
        if not os.path.exists(filepath): return
        
        self.current_csv_path = filepath
        self.current_title = title_text
        self.title_lbl.setText(f"{title_text}")
        
        try:
            df = pd.read_csv(filepath, header=None, encoding='utf-8-sig').fillna("")
            if df.empty: return
            
            headers = [str(x) for x in df.iloc[0].tolist()]
            self.table.clear()
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            
            self.table.setRowCount(len(df) - 1)
            
            for r_idx in range(1, len(df)):
                table_row = r_idx - 1
                is_top_row = (table_row % 2 == 0)
                
                # 每兩列換一次背景顏色，形成斑馬紋群組
                bg_color = QColor("#ffffff") if (table_row // 2) % 2 == 0 else QColor("#f4f8f9")
                
                for c_idx in range(len(headers)):
                    val = str(df.iloc[r_idx, c_idx]).strip()
                    item = QTableWidgetItem(val)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(bg_color))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable) 
                    
                    font = QFont("Microsoft JhengHei", 9)
                    
                    # [1] 車輛編號區 (Col 0)
                    if c_idx == 0:
                        font.setBold(True)
                        item.setForeground(QColor("#7f8c8d"))
                        
                    # [2] 車輛資訊區 (Col 1)
                    elif c_idx == 1:
                        if is_top_row:
                            font.setBold(True)
                            item.setForeground(QColor("#2c3e50")) # 車型 (深色)
                        else:
                            # 🌟 取消斜體，改為粗體加強判讀性
                            font.setBold(True)
                            item.setForeground(QColor("#2980b9")) # 車編 (藍色)
                            
                    # [3] 初始出發地 (Col 2) & 收班停留地 (Last Col)
                    elif c_idx == 2 or c_idx == len(headers) - 1:
                        if is_top_row:
                            font.setBold(True)
                            item.setForeground(QColor("#16a085")) # 車站/車庫 (綠色)
                        else:
                            item.setForeground(QColor("#34495e")) # 時間
                            
                    # [4] 中間的運用任務區塊 (每 6 欄一組)
                    elif 3 <= c_idx < len(headers) - 1:
                        task_offset = (c_idx - 3) % 6
                        
                        # (4.0) 任務序號
                        if task_offset == 0:
                            font.setBold(True)
                            item.setForeground(QColor("#95a5a6"))
                            
                        # (4.1) 路線 (上) / 方向或車庫 (下)
                        elif task_offset == 1:
                            if is_top_row:
                                font.setBold(True)
                                if val == "回送": item.setForeground(QColor("#7f8c8d"))
                                elif val == "入庫": item.setForeground(QColor("#8e44ad"))
                                else: item.setForeground(QColor("#2980b9"))
                            else:
                                item.setForeground(QColor("#34495e"))
                                
                        # (4.2) 車次 (上) / 等級 (下)
                        elif task_offset == 2:
                            if is_top_row:
                                font.setFamily("Arial")
                                font.setBold(True)
                            else:
                                font.setBold(True)
                                color = "#34495e"
                                for tid, tinfo in self.train_levels.items():
                                    if tinfo['name'] == val:
                                        color = tinfo.get('color', color)
                                        break
                                item.setForeground(QColor(color))
                                
                        # (4.3 & 4.5) 起點與終點 (上) / 發車與到站時間 (下)
                        elif task_offset == 3 or task_offset == 5:
                            if is_top_row:
                                font.setBold(True)
                                item.setForeground(QColor("#2c3e50"))
                            else:
                                font.setFamily("Arial")
                                item.setForeground(QColor("#d35400")) # 時間呈現深橘色
                                
                        # (4.4) 視覺箭頭 > 
                        elif task_offset == 4:
                            item.setForeground(QColor("#bdc3c7"))

                    item.setFont(font)
                    self.table.setItem(table_row, c_idx, item)
                    
                # 垂直合併儲存格 (僅在處理 Top Row 時呼叫)
                if is_top_row:
                    self.table.setSpan(table_row, 0, 2, 1) # 合併序號
                    self.table.setSpan(table_row, 2, 2, 1) # 合併初始出發地
            
            # 🌟 智慧欄寬設定：先讓系統自動適應，接著保底展開，確保時間格式與標題絕對裝得下
            self.table.resizeColumnsToContents()
            for c in range(len(headers)):
                current_w = self.table.columnWidth(c)
                if c == 0:
                    self.table.setColumnWidth(c, max(40, current_w))
                elif c == 1:
                    self.table.setColumnWidth(c, max(90, current_w))
                elif c == 2:
                    self.table.setColumnWidth(c, max(90, current_w))
                elif 3 <= c < len(headers) - 1:
                    offset = (c - 3) % 6
                    if offset == 0: self.table.setColumnWidth(c, max(40, current_w))     # 序號
                    elif offset == 4: self.table.setColumnWidth(c, 25)                   # 固定小箭頭欄位
                    else: self.table.setColumnWidth(c, max(85, current_w))               # 其他確保能塞下 05:00:00
                else:
                    self.table.setColumnWidth(c, max(90, current_w))                     # 收班停留地
            
        except Exception as e:
            self.title_lbl.setText(f"{title_text} - 讀取失敗: {e}")
            
    def refresh(self):
        if self.current_csv_path and self.current_title:
            self.load_csv(self.current_csv_path, self.current_title)