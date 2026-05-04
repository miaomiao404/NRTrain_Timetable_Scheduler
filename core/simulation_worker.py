import traceback
from PySide6.QtCore import QThread, Signal

class SimulationWorker(QThread):
    """
    非同步排班工作者 (Asynchronous Simulation Worker)
    負責在背景執行緒中運行極度耗時的全域排班迴圈，並即時將進度與狀態回報給主 UI，避免畫面卡頓。
    """
    
    # 定義與主 UI 溝通的專屬訊號 (Signals)
    progress_update = Signal(int, str)      # 傳遞：(進度百分比 0~100, 當前狀態文字)
    simulation_finished = Signal(bool, str) # 傳遞：(是否成功, 最終結語)
    error_occurred = Signal(str)            # 傳遞：(錯誤詳細資訊)

    def __init__(self, engine, schedule_type="weekdays", parent=None):
        super().__init__(parent)
        self.engine = engine
        self.schedule_type = schedule_type
        
        # 備份原本的 logger，並掛上攔截器
        self.original_logger = self.engine.logger
        self.engine.logger = self.custom_logger_interceptor
        
        self.current_progress = 0

    def custom_logger_interceptor(self, msg):
        """
        攔截 Engine 發出的日誌，解析關鍵字來推進進度條，並將文字拋給 UI。
        """
        # 簡單的進度條推進邏輯 (根據輸出的關鍵字動態計算)
        if "開始執行" in msg:
            self.current_progress = 5
        elif "決定為" in msg:
            self.current_progress = 10
        elif "開始排定路線" in msg:
            # 每次排新路線，進度推進 15% (最高卡在 85%，保留給派車)
            self.current_progress = min(85, self.current_progress + 15)
        elif "開始執行全境車輛" in msg or "無縫派發" in msg:
            self.current_progress = 90
            
        # 🌟 核心修復：嚴格限制只有「最終完成」時，才能把進度推到 100！
        # 避免被 Parser 印出的「解析完成」給騙了，導致執行緒被意外謀殺。
        elif "模擬排班與派車完成" in msg:
            self.current_progress = 100

        # 將狀態透過 Signal 發射給主執行緒的 UI
        self.progress_update.emit(self.current_progress, msg)
        
        # 注意：此處已刪除呼叫 self.original_logger(msg) 的邏輯，完全交由 main.py 接收訊號後安全寫入 UI。

    def run(self):
        """
        這是 QThread 啟動後，在「背景」獨立執行的主函式。
        """
        try:
            success = self.engine.run_full_simulation(self.schedule_type)
            
            if success:
                self.simulation_finished.emit(True, f"[{self.schedule_type}] 全域排班與派車已完美達成！")
            else:
                self.simulation_finished.emit(False, "模擬排班中斷或環境中無路線。")
                
        except Exception as e:
            # 如果排班過程中發生崩潰，捕捉錯誤並回報
            error_trace = traceback.format_exc()
            self.error_occurred.emit(f"排班引擎發生嚴重錯誤：\n{str(e)}\n\n{error_trace}")
            
        finally:
            # 執行結束後歸還控制權
            self.engine.logger = self.original_logger