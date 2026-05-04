import pandas as pd
import re
import os
import json

class TimetableParser:
    """
    負責解析時刻表 CSV 檔案的核心解析器。
    能將基準時刻表轉換為相對時間網格 (Patterns)，並結合列車等級設定 (Priority)。
    """
    def __init__(self, project_path=None, logger=None):
        self.logger = logger
        self.project_path = project_path
        
        self.patterns = {'上行': {}, '下行': {}}      
        self.priorities = {'上行': {}, '下行': {}}    
        self.stations = {'上行': [], '下行': []}      
        
        # 🌟 追加：回送車網格快取庫 {(起點, 終點): 虛擬等級ID}
        self.deadhead_patterns = {'上行': {}, '下行': {}}
        
        self.level_mapping = {}
        
        if self.project_path:
            self.load_train_levels()

    def log(self, msg):
        if self.logger:
            self.logger(msg)
        else:
            print(msg)

    def load_train_levels(self, project_path=None):
        """讀取 train_levels.json 以取得等級名稱與排班優先權"""
        if project_path:
            self.project_path = project_path
            
        if not self.project_path: return
            
        json_path = os.path.join(self.project_path, "train_levels.json")
        if os.path.exists(json_path):
            try:
                self.log("⏳ 正在讀取列車等級與優先權設定...")
                with open(json_path, 'r', encoding='utf-8') as f:
                    self.level_mapping = json.load(f)
                self.log(f"✅ 成功載入 {len(self.level_mapping)} 種列車等級。")
            except Exception as e:
                self.log(f"⚠️ 讀取 train_levels.json 失敗: {e}")

    @staticmethod
    def to_seconds(time_str):
        if not time_str or str(time_str).strip() in ['', '|', '~', 'nan']: return None
        try:
            parts = str(time_str).strip().split(':')
            h = int(parts[0])
            m = int(parts[1])
            s = int(parts[2]) if len(parts) > 2 else 0
            sec = h * 3600 + m * 60 + s
            
            # 若時間小於 03:00:00，視為「前一天的深夜跨日車次」，加上 24 小時
            if sec < 3 * 3600:
                sec += 24 * 3600
                
            return sec
        except Exception:
            return None

    @staticmethod
    def to_str(sec):
        if sec is None: return ""
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        display_h = h % 24
        return f"{display_h:02d}:{m:02d}:{s:02d}"

    def parse_csv(self, filepath, direction="上行"):
        pass

    def parse_template(self, filepath, direction="上行"):
        """解析擴充格式的基準運輸時刻表 (動態等級 ID)"""
        self.log(f"⏳ 開始解析 [{direction}] 基準時刻表...")
        
        try:
            df_raw = pd.read_csv(filepath, header=None).fillna("")
            
            contract_keywords = ['接續路線', '接續等級', '接續車次']
            clean_rows = []
            for i in range(len(df_raw)):
                val = str(df_raw.iloc[i, 0]).strip()
                if val in contract_keywords:
                    break  
                clean_rows.append(df_raw.iloc[i])
            
            df = pd.DataFrame(clean_rows)
            
        except Exception as e:
            self.log(f"❌ 讀取 CSV 失敗: {e}")
            return False

        if len(df) < 2:
            self.log("❌ CSV 格式錯誤：行數不足。")
            return False

        header_ids = df.iloc[0, 2:].astype(str).tolist()
        
        station_list = []
        for i in range(1, len(df)):
            st_name = str(df.iloc[i, 0]).strip()
            if st_name and st_name not in station_list:
                station_list.append(st_name)

        self.stations[direction] = station_list
        
        for col_idx in range(2, len(df.columns)):
            g_id = header_ids[col_idx-2].strip()
            if not g_id: continue
            
            priority = 3
            if g_id in self.level_mapping:
                priority = self.level_mapping[g_id].get("priority", 3)

            absolute_times = {}
            current_st = ""
            
            for row_idx in range(1, len(df)):
                st_col = str(df.iloc[row_idx, 0]).strip()
                if st_col:
                    current_st = st_col
                    
                if not current_st: 
                    continue
                    
                if current_st not in absolute_times:
                    absolute_times[current_st] = {'到': None, '發': None}
                
                arr_dep_type = str(df.iloc[row_idx, 1]).strip()
                t_str = str(df.iloc[row_idx, col_idx]).strip()
                
                sec = self.to_seconds(t_str)
                if sec is not None:
                    if arr_dep_type == '到':
                        absolute_times[current_st]['到'] = sec
                    elif arr_dep_type == '發':
                        absolute_times[current_st]['發'] = sec
                        
            pattern = self._build_relative_pattern(absolute_times, station_list)
            
            if pattern:
                self.patterns[direction][g_id] = pattern
                self.priorities[direction][g_id] = priority

        self.log(f"✅ [{direction}] 解析完成：萃取 {len(station_list)} 停靠站，{len(self.patterns[direction])} 種列車網格。")
        return True

    def _build_relative_pattern(self, times_dict, station_list):
        base_sec = None
        for st in station_list:
            if st in times_dict:
                if times_dict[st]['發'] is not None:
                    base_sec = times_dict[st]['發']
                    break
                elif times_dict[st]['到'] is not None:
                    base_sec = times_dict[st]['到']
                    break
                    
        if base_sec is None: return None

        pattern = {}
        for st in station_list:
            if st in times_dict:
                arr = times_dict[st]['到']
                dep = times_dict[st]['發']
                pattern[st] = {
                    '到': (arr - base_sec) if arr is not None else None,
                    '發': (dep - base_sec) if dep is not None else None
                }
        return pattern

    def get_shift_params(self):
        params = {'shift_step': 5, 'buffer_time': 45, 'stretch': False}
        if not self.project_path: return params
            
        info_path = os.path.join(self.project_path, "information.json")
        if os.path.exists(info_path):
            try:
                with open(info_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    params['shift_step'] = int(data.get('班次平移精度', 5))
                    params['buffer_time'] = int(data.get('發車間隔緩衝時間', 45))
                    params['stretch'] = bool(data.get('停靠時間可否拉伸', False))
            except Exception: pass
        return params

    # ==========================================
    # 🌟 Step 1 核心功能：智能回送網格生成器
    # ==========================================
    def get_or_create_deadhead_pattern(self, start_st, end_st, direction="上行"):
        """
        根據起迄站動態生成並快取最速回送網格。
        自動尋找停靠此兩站的最高優先度車次，截取區間並將停靠時間歸零。
        """
        cache_key = (start_st, end_st)
        if cache_key in self.deadhead_patterns[direction]:
            return self.deadhead_patterns[direction][cache_key]

        station_list = self.stations[direction]
        if start_st not in station_list or end_st not in station_list:
            return None
            
        start_idx = station_list.index(start_st)
        end_idx = station_list.index(end_st)
        if start_idx >= end_idx:
            return None 

        # 1. 尋找速度最快（優先權最高）的母體網格
        best_grade = None
        best_prio = 999
        
        for g_id, pattern in self.patterns[direction].items():
            prio = self.priorities[direction].get(g_id, 99)
            p_start = pattern.get(start_st)
            p_end = pattern.get(end_st)
            
            if p_start and p_end:
                has_start = p_start.get('到') is not None or p_start.get('發') is not None
                has_end = p_end.get('到') is not None or p_end.get('發') is not None
                if has_start and has_end and prio < best_prio:
                    best_prio = prio
                    best_grade = g_id

        if not best_grade:
            return None 

        orig_pattern = self.patterns[direction][best_grade]
        
        # 2. 補間運算 (Interpolation)：填補母體網格中原本通過的車站時間
        proj_off = {}
        for st in station_list:
            p = orig_pattern.get(st, {})
            a = p.get('到')
            d = p.get('發')
            if a is None and d is not None: a = d
            if d is None and a is not None: d = a
            proj_off[st] = {'arr': a, 'dep': d}

        last_k = -1
        for i, st in enumerate(station_list):
            if proj_off[st]['arr'] is not None:
                if last_k == -1: 
                    last_k = i 
                else:
                    miss = i - last_k - 1
                    if miss > 0:
                        t0 = proj_off[station_list[last_k]]['dep']
                        t1 = proj_off[st]['arr']
                        step = (t1 - t0) / (miss + 1)
                        for j in range(1, miss + 1):
                            t_interp = t0 + step * j
                            proj_off[station_list[last_k + j]]['arr'] = t_interp
                            proj_off[station_list[last_k + j]]['dep'] = t_interp
                    last_k = i
        
        # 3. 動態截取與歸零 (Slicing & Zero-Dwell)
        new_pattern = {}
        accumulated_dwell = 0
        base_sec = proj_off[start_st]['dep']
        
        for i in range(start_idx, end_idx + 1):
            st = station_list[i]
            orig_arr = proj_off[st]['arr']
            orig_dep = proj_off[st]['dep']
            
            if i == start_idx:
                new_pattern[st] = {'到': None, '發': 0}
            elif i == end_idx:
                new_arr = orig_arr - base_sec - accumulated_dwell
                new_pattern[st] = {'到': new_arr, '發': None}
            else:
                new_arr = orig_arr - base_sec - accumulated_dwell
                # 中間站強制將到發時間設為一致，即停留時間歸零 (通過)
                new_pattern[st] = {'到': new_arr, '發': new_arr} 
                # 累加原本被我們沒收的停留時間，讓後面的站提早到達
                accumulated_dwell += (orig_dep - orig_arr) 
                
        # 4. 快取與註冊虛擬列車等級
        dh_id = f"DH_{start_st}_{end_st}"
        self.patterns[direction][dh_id] = new_pattern
        self.priorities[direction][dh_id] = 1 
        
        self.level_mapping[dh_id] = {
            "name": "回送",
            "priority": 1,
            "direction": direction,
            "color": "#808080",
            "is_revenue": False
        }
        
        self.deadhead_patterns[direction][cache_key] = dh_id
        self.log(f"   🔧 成功生成並快取回送網格 [{dh_id}] (參考基底: {best_grade})")
        
        return dh_id