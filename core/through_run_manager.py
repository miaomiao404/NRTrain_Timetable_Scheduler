import os

class ThroughRunManager:
    """
    直通運轉管理器 (Through-Running Manager)
    負責在多路線排班中，傳遞跨線的「幽靈種子 (Ghost Seeds)」。
    它會讀取上一個路線的到達時間，並加上緩衝視窗，提供給下一個路線進行「鳩佔鵲巢」。
    """
    def __init__(self, logger=None):
        self.logger = logger
        self.seeds = {}

    def log(self, msg):
        if self.logger: self.logger(msg)
        else: print(msg)

    def extract_seeds_from_schedule(self, source_schedule, boundary_station, source_line, source_grade, target_line, target_direction, target_grade, min_buffer_sec, max_buffer_sec):
        """
        從已經排好的主線時刻表中，萃取到達邊界站的車次，轉化為種子。
        """
        key = (target_line, target_direction)
        if key not in self.seeds:
            self.seeds[key] = []
            
        extracted_count = 0
        for train in source_schedule:
            # 只萃取符合直通規則指定的「等級」的車次
            if train.get('grade') != source_grade:
                continue
                
            # 如果這班車有到達邊界站
            if boundary_station in train['times']:
                arr_time = train['times'][boundary_station].get('到')
                if arr_time is not None:
                    min_dep = arr_time + min_buffer_sec
                    max_dep = arr_time + max_buffer_sec
                    
                    seed = {
                        'source_line': source_line,  # 🌟 確保母路線 DNA 存入
                        'grade': target_grade,
                        'arr_time': arr_time,
                        'min_dep': min_dep,
                        'max_dep': max_dep,
                        'source_train_id': train['id']
                    }
                    self.seeds[key].append(seed)
                    extracted_count += 1
        
        if extracted_count > 0:
            self.log(f"🔗 成功從 {boundary_station} 萃取 {extracted_count} 個等級為 [{source_grade}] 的跨線種子，準備交接給 {target_line} [{target_direction}]。")
        return extracted_count

    def get_seeds_in_window(self, target_line, direction, start_sec, end_sec):
        """取得落在該排班 Cycle 內的種子"""
        key = (target_line, direction)
        if key not in self.seeds:
            return []
        return [s for s in self.seeds[key] if start_sec <= s['min_dep'] < end_sec]