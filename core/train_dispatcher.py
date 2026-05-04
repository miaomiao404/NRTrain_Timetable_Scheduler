import os
import json
import pandas as pd
import random
import re

class Facility:
    """管理車庫或暫留線的容量與佔用狀態，並加入路線白名單限制與配屬容量"""
    def __init__(self, name, station, f_type, capacity, allowed_routes=None, buffer_sec=600):
        self.name = name
        self.station = station     
        self.f_type = f_type       
        self.capacity = capacity   
        self.allowed_routes = allowed_routes if allowed_routes is not None else set(["all"])
        self.buffer_sec = buffer_sec
        self.occupancy = [] 
        self.registered_vehicles = 0 

    def can_accommodate(self, enter_time, leave_time):
        if self.capacity <= 0: return False
        
        events = []
        for e, l in self.occupancy:
            if e < leave_time and l > enter_time: 
                events.append((max(e, enter_time), 1))   
                events.append((min(l, leave_time), -1))  
        
        if not events: return self.capacity > 0
        events.sort(key=lambda x: (x[0], x[1])) 
        
        max_occ, curr_occ = 0, 0
        for t, diff in events:
            curr_occ += diff
            if curr_occ > max_occ: max_occ = curr_occ
        
        return max_occ < self.capacity

    def add_occupancy(self, enter_time, leave_time):
        self.occupancy.append((enter_time, leave_time))

class Vehicle:
    """實體車輛，擁有固定配屬基地，可跨越多條路線執行任務"""
    def __init__(self, vid, type_name="一般列車"):
        self.vid = vid
        self.type_name = type_name
        self.history = []
        self.initial_loc = ""
        self.end_facility = ""
        self.end_facility_st = "" 
        self.end_facility_buffer = 0 
        self.end_time = 0
        self.home_line = "" 
        self.home_base = None 

class Dispatcher:
    def __init__(self, parser=None, project_path=None, env_path=None, schedule_type="weekdays", logger=None, existing_fleet_state=None, dry_run_assignments=None):
        self.parser = parser
        self.project_path = project_path
        self.env_path = env_path or (os.path.dirname(project_path) if project_path else "")
        self.schedule_type = schedule_type
        self.logger = logger
        
        self.facilities = []
        self.vehicles = []
        self.dry_run_assignments = dry_run_assignments or {}
        
        self.line_configs = {}  
        self.line_counters = {} 
        self.line_stations = {} 
        
        self.load_facilities()
        self.load_line_configs()
        
        if existing_fleet_state:
            self._restore_fleet(existing_fleet_state)

    def log(self, msg):
        if self.logger: self.logger(msg)
        else: print(msg)

    def load_facilities(self):
        if not self.env_path: return
        st_path = os.path.join(self.env_path, "station.json")
        if not os.path.exists(st_path): return
        
        with open(st_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            id_to_name = {k: v.get("name", "") for k, v in data.items() if isinstance(v, dict)}

            for st_id, info in data.items():
                if info.get("type") in ["depot", "pocket_track"]:
                    cap = sum(t.get("capacity", 0) for t in info.get("tracks", []))
                    if cap > 0:
                        allowed = set()
                        for t in info.get("tracks", []):
                            rts = t.get("allowed_routes", ["all"])
                            if isinstance(rts, str): rts = [rts]
                            allowed.update(rts)
                            
                        connected_station_name = info.get("name", "未命名")
                        buf_sec = 600 
                        for conn in info.get("connections", []):
                            if conn.get("side") == "facility":
                                target_id = conn.get("target_station")
                                if target_id in id_to_name:
                                    connected_station_name = id_to_name[target_id]
                                buf_sec = int(conn.get("buffer_time", 10)) * 60
                                break
                                    
                        self.facilities.append(Facility(
                            info.get("name", "未命名"), 
                            connected_station_name, 
                            info.get("type"), 
                            cap, 
                            allowed_routes=allowed,
                            buffer_sec=buf_sec
                        ))

    def load_line_configs(self):
        if not self.env_path or not os.path.exists(self.env_path): return
        for line in os.listdir(self.env_path):
            info_path = os.path.join(self.env_path, line, "information.json")
            if os.path.exists(info_path):
                try:
                    with open(info_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.line_configs[line] = {
                            'prefix': data.get('車輛編號前綴', data.get('車隊代號', f"{line[:1].upper()}_")),
                            'type_name': data.get('主力車型', data.get('使用車型', '一般列車'))
                        }
                except Exception:
                    pass

    def _restore_fleet(self, state_list):
        for st in state_list:
            v = Vehicle(st['vid'], st['type_name'])
            v.home_line = st['home_line']
            
            hb_name = st['home_base_name']
            if hb_name:
                for fac in self.facilities:
                    if fac.name == hb_name:
                        v.home_base = fac
                        fac.registered_vehicles += 1
                        v.initial_loc = fac.station 
                        break
            
            if not v.initial_loc:
                v.initial_loc = "未知"
                
            self.vehicles.append(v)
            
            m = re.search(r'\d+$', v.vid)
            if m:
                num = int(m.group())
                if self.line_counters.get(v.home_line, 0) < num:
                    self.line_counters[v.home_line] = num

    def _assign_home_base(self, start_st, end_st, line_id):
        valid_facs = []
        for fac in self.facilities:
            if fac.capacity <= fac.registered_vehicles:
                continue
            if "all" not in fac.allowed_routes and line_id not in fac.allowed_routes:
                continue
            if line_id in self.line_stations and fac.station not in self.line_stations[line_id]:
                continue
            valid_facs.append(fac)
        
        if not valid_facs:
            return None
            
        def sort_key(fac):
            type_score = 0 if fac.f_type == 'depot' else 1
            if fac.station == start_st: geo_score = 0
            elif fac.station == end_st: geo_score = 1
            else: geo_score = 2
            return (type_score, geo_score, -fac.capacity)
            
        valid_facs.sort(key=sort_key)
        chosen = valid_facs[0]
        chosen.registered_vehicles += 1
        return chosen

    @staticmethod
    def to_str(sec):
        if sec is None: return ""
        h = int(sec // 3600) % 24
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def run_dispatch(self, up_or_dict, down_schedule=None, params=None):
        if params is None: params = {}
        all_schedules_dict = {}
        
        if isinstance(up_or_dict, dict):
            all_schedules_dict = up_or_dict
        else:
            line_id = os.path.basename(self.project_path) if self.project_path else "目前路線"
            all_schedules_dict = {
                line_id: (up_or_dict or []) + (down_schedule or [])
            }

        self.line_stations = {}
        for line_id, trips in all_schedules_dict.items():
            if line_id not in self.line_stations:
                self.line_stations[line_id] = set()
            for t in trips:
                if 'times' in t:
                    self.line_stations[line_id].update(t['times'].keys())

        flat_trips = []
        for line_id, trips in all_schedules_dict.items():
            for t in trips:
                times = t['times']
                valid_times = []
                for st, st_time in times.items():
                    c_arr = st_time.get('_calc_arr', st_time.get('到'))
                    c_dep = st_time.get('_calc_dep', st_time.get('發'))
                    if c_arr is not None or c_dep is not None:
                        valid_times.append((st, c_arr, c_dep))
                
                if not valid_times: continue
                valid_times.sort(key=lambda x: x[1] if x[1] is not None else x[2])
                
                start_st = valid_times[0][0]
                start_sec = valid_times[0][2] if valid_times[0][2] is not None else valid_times[0][1]
                end_st = valid_times[-1][0]
                end_sec = valid_times[-1][1] if valid_times[-1][1] is not None else valid_times[-1][2]
                
                flat_trips.append({
                    'line_id': line_id,
                    'direction': t['direction'],
                    'id': t['id'],
                    'grade': t['grade'],
                    'start_st': start_st,
                    'start_sec': start_sec,
                    'end_st': end_st,
                    'end_sec': end_sec,
                    'is_seed': t.get('is_seed', False),
                    'source_train_id': t.get('source_train_id')
                })

        flat_trips.sort(key=lambda x: x['start_sec'])
        
        self.log("⚙️ 啟動全域車輛派發與直通運轉尋跡...")

        for trip in flat_trips:
            assigned_v = None
            is_dh_trip = trip.get('grade', '').startswith('DH_')
            
            if trip.get('is_seed') and trip.get('source_train_id'):
                for v in self.vehicles:
                    if not v.history: continue
                    last_trip = v.history[-1]
                    if last_trip.get('type') == 'trip' and last_trip.get('id') == trip['source_train_id']:
                        if last_trip['end_st'] == trip['start_st'] and trip['start_sec'] >= last_trip['end_sec']:
                            assigned_v = v
                            break
                            
                if assigned_v:
                    self.log(f"   🔗 直通銜接成功: 車輛 {assigned_v.vid} 從 [{last_trip['line_id']}] 駛入 [{trip['line_id']}]")

            if not assigned_v:
                available = []
                idle_anywhere = []
                
                for v in self.vehicles:
                    if not v.history:
                        if getattr(v, 'home_line', '') == trip['line_id'] or is_dh_trip:
                            idle_anywhere.append(v)
                            if v.initial_loc == trip['start_st']:
                                available.append((v, 0)) 
                    else:
                        last_event = v.history[-1]
                        end_st = last_event.get('end_st')
                        end_sec = last_event.get('end_sec', float('inf'))
                        
                        if end_st == trip['start_st'] and end_sec <= trip['start_sec']:
                            if getattr(v, 'home_line', '') == trip['line_id'] or last_event.get('line_id', '') == trip['line_id'] or last_event.get('grade', '').startswith('DH_'):
                                available.append((v, trip['start_sec'] - end_sec)) 
                
                if available:
                    target_vid = self.dry_run_assignments.get(trip['id'])
                    
                    def sort_key(x):
                        v, idle_time = x
                        is_target = 0 if v.vid == target_vid else 1
                        return (is_target, idle_time)
                        
                    available.sort(key=sort_key)
                    assigned_v = available[0][0]
                elif idle_anywhere:
                    target_vid = self.dry_run_assignments.get(trip['id'])
                    
                    def sort_key_idle(v):
                        return 0 if v.vid == target_vid else 1
                        
                    idle_anywhere.sort(key=sort_key_idle)
                    assigned_v = idle_anywhere[0]
                    
                if not assigned_v:
                    home_line = trip['line_id']
                    conf = self.line_configs.get(home_line, {})
                    prefix = conf.get('prefix', f"V_")
                    v_type = conf.get('type_name', "一般列車")
                    
                    self.line_counters[home_line] = self.line_counters.get(home_line, 0) + 1
                    vid = f"{prefix}{self.line_counters[home_line]:03d}"
                    
                    assigned_v = Vehicle(vid, type_name=v_type)
                    assigned_v.home_line = home_line
                    
                    home_base = self._assign_home_base(trip['start_st'], trip['end_st'], home_line)
                    if home_base:
                        assigned_v.home_base = home_base
                        assigned_v.initial_loc = home_base.station
                        self.log(f"   🏭 新車出廠: {vid} (配屬基地: {home_base.name})")
                    else:
                        assigned_v.initial_loc = trip['start_st']
                        self.log(f"   ⚠️ 新車出廠: {vid} (無可用基地，暫置 {trip['start_st']})")
                        
                    self.vehicles.append(assigned_v)

            assigned_v.history.append({
                'type': 'trip',
                'line_id': trip['line_id'],
                'direction': trip['direction'],
                'id': trip['id'],
                'grade': trip['grade'],
                'start_st': trip['start_st'],
                'start_sec': trip['start_sec'],
                'end_st': trip['end_st'],
                'end_sec': trip['end_sec']
            })

        for v in self.vehicles:
            new_history = []
            for i in range(len(v.history)):
                trip = v.history[i]
                new_history.append(trip)
                
                if i < len(v.history) - 1:
                    next_trip = v.history[i+1]
                    if trip['end_st'] == next_trip['start_st']:
                        fac = self._find_best_facility_for_wait(trip['end_st'], v.home_line, trip['end_sec'], next_trip['start_sec'])
                        if fac:
                            is_dh = trip.get('grade', '').startswith('DH_')
                            actual_buffer = 0 if is_dh else fac.buffer_sec
                            enter_t = trip['end_sec'] + actual_buffer
                            leave_t = next_trip['start_sec'] - 60 
                            
                            if leave_t > enter_t:
                                fac.add_occupancy(enter_t, leave_t)
                                new_history.append({
                                    'type': 'depot_in',
                                    'facility_name': fac.name,
                                    'entry_time': enter_t,
                                    'end_st': fac.station,
                                    'end_sec': leave_t
                                })
            v.history = new_history

        unaccommodated_count = 0
        for v in self.vehicles:
            if not v.history: 
                if v.home_base:
                    v.end_facility = v.home_base.name
                    v.end_facility_st = v.home_base.station
                    v.end_time = 0
                continue
            
            trips = [h for h in v.history if h.get('type') == 'trip']
            if not trips: continue
            last_trip = trips[-1]
            
            end_st = last_trip['end_st']
            end_sec = last_trip['end_sec']
            
            if v.home_base:
                fac = v.home_base
                v.end_facility_st = fac.station
                v.end_facility_buffer = fac.buffer_sec 
                
                if fac.station == end_st:
                    is_dh = last_trip.get('grade', '').startswith('DH_')
                    actual_buffer = 0 if is_dh else fac.buffer_sec
                    enter_t = end_sec + actual_buffer
                    
                    fac.add_occupancy(enter_t, enter_t + 28800)
                    v.history.append({
                        'type': 'depot_in',
                        'facility_name': fac.name,
                        'entry_time': enter_t,
                        'end_st': fac.station,
                        'end_sec': enter_t
                    })
                    v.end_facility = fac.name
                    v.end_time = enter_t
                else:
                    v.end_facility = f"前往 {fac.name} (等待回送)"
                    v.end_time = end_sec
            else:
                v.end_facility = f"{end_st} (月台駐停)"
                v.end_facility_st = end_st
                v.end_facility_buffer = 0
                v.end_time = end_sec
                unaccommodated_count += 1
                
        if unaccommodated_count > 0:
            self.log(f"   ⚠️ 警告: 有 {unaccommodated_count} 台車輛因無配屬基地，被迫駐停於月台過夜！")

        return self.vehicles

    def _find_best_facility_for_wait(self, st_name, line_id, end_sec, next_start_sec):
        valid_facs = []
        for fac in self.facilities:
            if fac.station == st_name:
                if line_id in self.line_stations and fac.station not in self.line_stations[line_id]:
                    continue
                if "all" in fac.allowed_routes or line_id in fac.allowed_routes:
                    enter_t = end_sec + fac.buffer_sec
                    leave_t = next_start_sec - 60
                    if leave_t > enter_t and fac.can_accommodate(enter_t, leave_t):
                        valid_facs.append(fac)
        if valid_facs:
            return random.choice(valid_facs)
        return None

    def audit_deadhead_requests(self):
        self.log("\n🔍 [查帳系統] 啟動日夜當日歸建與早晨出庫盤點...")
        
        sos_requests = []
        for v in self.vehicles:
            if not v.history: continue
            
            trips = [h for h in v.history if h.get('type') == 'trip']
            if not trips: continue
            
            first_trip = trips[0]
            last_trip = trips[-1]
            
            home_st = v.home_base.station if v.home_base else v.initial_loc
            
            if home_st != first_trip['start_st']:
                sos_requests.append({
                    'req_type': 'morning',
                    'from_st': home_st,
                    'to_st': first_trip['start_st'],
                    'count': 1,
                    'min_after_sec': max(0, first_trip['start_sec'] - 7200),
                    'source_train_id': None,
                    'source_line': None
                })
                
            if home_st != last_trip['end_st']:
                buffer_time = v.home_base.buffer_sec if v.home_base else getattr(v, 'end_facility_buffer', 300)
                sos_requests.append({
                    'req_type': 'night',
                    'from_st': last_trip['end_st'],
                    'to_st': home_st,
                    'count': 1,
                    'min_after_sec': last_trip['end_sec'] + buffer_time,
                    'source_train_id': last_trip['id'],
                    'source_line': last_trip['line_id']
                })

        if sos_requests:
            self.log(f"   ⚠️ 發現 {len(sos_requests)} 項個別出入庫位移需求，已開立專屬獨立之 SOS 回送單。")
        else:
            self.log("   ✅ 所有車輛皆已完美出入庫歸建，無需額外回送。")
            
        return sos_requests

    def _write_tud_csv(self, vehicles_list, filepath):
        if not vehicles_list: return False
        
        rows = []
        max_tasks = 0
        
        for idx, v in enumerate(sorted(vehicles_list, key=lambda x: x.vid)):
            seq_num = str(idx + 1)
            
            top_row = [seq_num, v.type_name, v.initial_loc]
            bot_row = ["", v.vid, ""]
            
            task_idx = 1
            for h in v.history:
                if h.get('type') == 'trip':
                    is_dh = h.get('grade', '').startswith('DH_')
                    
                    if is_dh:
                        top_row.extend([str(task_idx), "回送", str(h.get('id', '')), h.get('start_st', ''), ">", h.get('end_st', '')])
                        bot_row.extend(["", "", "", self.to_str(h.get('start_sec', 0)), "", self.to_str(h.get('end_sec', 0))])
                    else:
                        top_row.extend([str(task_idx), h.get('line_id', '未知'), str(h.get('id', '')), h.get('start_st', ''), ">", h.get('end_st', '')])
                        bot_row.extend(["", h.get('direction', ''), h.get('grade', ''), self.to_str(h.get('start_sec', 0)), "", self.to_str(h.get('end_sec', 0))])
                        
                    task_idx += 1
                elif h.get('type') == 'depot_in':
                    top_row.extend([str(task_idx), "入庫", "", "", ">", h.get('facility_name', '')])
                    bot_row.extend(["", h.get('facility_name', ''), "", "", "", self.to_str(h.get('entry_time', 0))])
                    task_idx += 1
                    
            if (task_idx - 1) > max_tasks:
                max_tasks = task_idx - 1
                
            top_row.append(getattr(v, 'end_facility', ''))
            bot_row.append(self.to_str(getattr(v, 'end_time', 0)))
            
            rows.append(top_row)
            rows.append(bot_row)
            
        target_len = 3 + max_tasks * 6 + 1
        for r in rows:
            while len(r) < target_len:
                r.insert(-1, "") 
                
        header_row = ['編號', '車輛資訊', '初始出發地']
        for i in range(max_tasks):
            header_row.extend([f'運用{i+1}', '', '', '', '', ''])
        header_row.append('收班停留地')
        
        rows.insert(0, header_row)
        
        df = pd.DataFrame(rows)
        df.to_csv(filepath, index=False, header=False, encoding='utf-8-sig')
        return True

    def export_to_csv(self, filepath):
        if self._write_tud_csv(self.vehicles, filepath):
            self.log(f"📄 產出全域 TUD 報表: {os.path.basename(filepath)}")
            return True
        return False
        
    def export_line_specific_csvs(self, lines):
        for line in lines:
            line_vehicles = [v for v in self.vehicles if getattr(v, 'home_line', '') == line]
            if line_vehicles:
                filepath = os.path.join(self.env_path, line, f"{self.schedule_type}_tud.csv")
                if self._write_tud_csv(line_vehicles, filepath):
                    self.log(f"📄 產出專屬 TUD 報表: {line}/{os.path.basename(filepath)}")