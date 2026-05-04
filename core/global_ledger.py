import bisect

class GlobalLedger:
    """
    全域時間帳本 (Global Time Ledger)
    負責管理整個環境 (Environment) 內所有實體車站與連接軌道的佔用狀況。
    這是一本凌駕於單一路線之上的「時空行事曆」，提供 O(log N) 的極速防撞查詢。
    """
    def __init__(self, logger=None):
        self.logger = logger
        # 紀錄車站股道佔用 { st_name: { track_id: [(start, end, line_id, train_id)] } }
        self.st_bookings = {}    
        # 紀錄連接軌佔用 { conn_entity: { track_id: [(start, end, direction, line_id, train_id)] } }
        self.conn_bookings = {}  

    def book_st_track(self, st_name, track_id, p_enter, p_leave, line_id, train_id):
        """登記車站股道使用權"""
        if "MOCK" in track_id: return
        if st_name not in self.st_bookings: self.st_bookings[st_name] = {}
        if track_id not in self.st_bookings[st_name]: self.st_bookings[st_name][track_id] = []
        
        # 保持時間軸有序插入
        bisect.insort(self.st_bookings[st_name][track_id], (p_enter, p_leave, line_id, train_id))

    def book_conn_track(self, stA, stB, ct_id, p_enter, p_leave, line_id, train_id):
        """登記區間連接軌使用權"""
        if "MOCK" in ct_id: return
        entity_id = f"{min(stA, stB)}<->{max(stA, stB)}"
        req_dir = 1 if stA < stB else -1
        
        if entity_id not in self.conn_bookings: self.conn_bookings[entity_id] = {}
        if ct_id not in self.conn_bookings[entity_id]: self.conn_bookings[entity_id][ct_id] = []
        
        bisect.insort(self.conn_bookings[entity_id][ct_id], (p_enter, p_leave, req_dir, line_id, train_id))

    def is_st_track_free(self, st_name, track_id, p_enter, p_leave, buffer_sec=45):
        """查詢車站股道在此時間段內是否空閒"""
        if "MOCK" in track_id: return True
        if st_name not in self.st_bookings or track_id not in self.st_bookings[st_name]: return True
        
        for b_start, b_end, _, _ in self.st_bookings[st_name][track_id]:
            # 檢查是否與現有班次發生重疊 (含安全緩衝時間)
            if max(p_enter, b_start) < min(p_leave + buffer_sec, b_end + buffer_sec):
                return False
        return True

    def is_conn_track_free(self, stA, stB, ct_id, p_enter, p_leave, buffer_sec=45):
        """查詢連接軌在此時間段內是否空閒 (支援雙向防追撞與防對撞演算)"""
        if "MOCK" in ct_id: return True
        entity_id = f"{min(stA, stB)}<->{max(stA, stB)}"
        if entity_id not in self.conn_bookings or ct_id not in self.conn_bookings[entity_id]: return True
        
        req_dir = 1 if stA < stB else -1
        for b_start, b_end, b_dir, _, _ in self.conn_bookings[entity_id][ct_id]:
            if req_dir == b_dir:
                # 同向行駛：檢查是否靠太近或發生超車交叉
                if abs(p_enter - b_start) < buffer_sec: return False
                if abs(p_leave - b_end) < buffer_sec: return False
                if (p_enter - b_start) * (p_leave - b_end) <= 0: return False 
            else:
                # 反向行駛：絕對不可重疊區間
                if max(p_enter, b_start) < min(p_leave + buffer_sec, b_end + buffer_sec):
                    return False
        return True