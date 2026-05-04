import math
import os
import json
import pandas as pd

class Infrastructure:
    def __init__(self, logger=None):
        self.logger = logger
        self.station_tracks = {} 
        self.connections = {}    
        self.global_order = []   

    def log(self, msg):
        if self.logger: self.logger(msg)
        else: print(msg)

    def load_from_json(self, path, route_id, parser):
        self.log("⏳ 正在讀取實體軌道設施與路網拓樸 (station.json)...")
        self.station_tracks = {}
        self.connections = {}
        
        if parser:
            if parser.stations.get('下行'):
                self.global_order = parser.stations['下行']
            elif parser.stations.get('上行'):
                self.global_order = list(reversed(parser.stations['上行']))

        if not os.path.exists(path):
            self.log("⚠️ 找不到 station.json，將使用虛擬無限軌道進行排班。")
            return
            
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        id_to_name = {k: v.get('name') for k, v in data.items() if v.get('name')}

        for st_id, st_info in data.items():
            st_name = st_info.get("name")
            if not st_name: continue

            valid_tracks = []
            for t in st_info.get("tracks", []):
                routes = t.get("allowed_routes", ["all"])
                if "all" in routes or route_id in routes:
                    valid_tracks.append({
                        'id': t.get('id', f"ST_{st_name}_{len(valid_tracks)}"),
                        'name': t.get('name', '股道'),
                        'left_signal': t.get('left_signal', 'double'),
                        'right_signal': t.get('right_signal', 'double'),
                        'allowed_grades': t.get('allowed_grades', ['all'])
                    })
            self.station_tracks[st_name] = valid_tracks

            for conn in st_info.get("connections", []):
                target_id = conn.get("target_station")
                target_name = id_to_name.get(target_id)
                if not target_name: continue

                side = conn.get("side")
                c_tracks = []
                for idx, ct in enumerate(conn.get("tracks", [])):
                    routes = ct.get("allowed_routes", ["all"])
                    if "all" in routes or route_id in routes:
                        c_tracks.append({
                            'id': ct.get('id', f"CT_{st_id}_{target_id}_{idx}"),
                            'dir': ct.get('dir', 'double'),
                            'allowed_grades': ct.get('allowed_grades', ['all'])
                        })
                
                if side == "right":
                    self.connections[(st_name, target_name)] = c_tracks
                elif side == "left":
                    self.connections[(target_name, st_name)] = c_tracks
                else:
                    idx_a = self.global_order.index(st_name) if st_name in self.global_order else -1
                    idx_b = self.global_order.index(target_name) if target_name in self.global_order else -1
                    if idx_a >= 0 and idx_b >= 0:
                        if idx_a < idx_b: self.connections[(st_name, target_name)] = c_tracks
                        else: self.connections[(target_name, st_name)] = c_tracks
                        
        self.log(f"✅ 成功載入 {len(self.station_tracks)} 座車站的實體軌道資源。")

    def get_valid_st_tracks(self, st_name, grade, prev_st, next_st):
        if st_name not in self.station_tracks or not self.station_tracks[st_name]:
            return [f"MOCK_ST_{st_name}"], "無實體設定，採用虛擬軌道"

        valid = []
        reasons = []
        for t in self.station_tracks[st_name]:
            grades = t.get('allowed_grades', ['all'])
            if 'all' not in grades and grade not in grades: 
                reasons.append(f"{t['name']}(等級不符)")
                continue
            
            ls = t.get('left_signal', 'double')
            rs = t.get('right_signal', 'double')
            
            can_enter = True
            can_exit = True
            
            if prev_st:
                if (prev_st, st_name) in self.connections:
                    if ls not in ['double', 'right', 'cross']: can_enter = False
                elif (st_name, prev_st) in self.connections:
                    if rs not in ['double', 'left', 'cross']: can_enter = False
                    
            if next_st:
                if (st_name, next_st) in self.connections:
                    if rs not in ['double', 'right', 'cross']: can_exit = False
                elif (next_st, st_name) in self.connections:
                    if ls not in ['double', 'left', 'cross']: can_exit = False
                
            if can_enter and can_exit:
                valid.append(t['id'])
            else:
                reasons.append(f"{t['name']}(號誌阻擋 L:{ls} R:{rs})")
                
        if valid:
            return valid, "OK"
        return [], " | ".join(reasons)

    def get_valid_conn_tracks(self, st_A, st_B, grade):
        tracks = []
        is_moving_l_to_r = True
        
        if (st_A, st_B) in self.connections:
            tracks = self.connections[(st_A, st_B)]
            is_moving_l_to_r = True
        elif (st_B, st_A) in self.connections:
            tracks = self.connections[(st_B, st_A)]
            is_moving_l_to_r = False
        else:
            return [f"MOCK_CT_{st_A}_{st_B}"], "無實體設定，採用虛擬軌道"
            
        if not tracks: 
            return [f"MOCK_CT_{st_A}_{st_B}"], "無實體設定，採用虛擬軌道"
            
        valid = []
        reasons = []
        for t in tracks:
            grades = t.get('allowed_grades', ['all'])
            if 'all' not in grades and grade not in grades: 
                reasons.append(f"連接軌(等級不符)")
                continue
                
            d = t.get('dir', 'double')
            if is_moving_l_to_r:
                if d in ['double', 'right', 'cross']: valid.append(t['id'])
                else: reasons.append(f"連接軌(方向阻擋:{d})")
            else:
                if d in ['double', 'left', 'cross']: valid.append(t['id'])
                else: reasons.append(f"連接軌(方向阻擋:{d})")
        
        if valid: return valid, "OK"
        return [], " | ".join(reasons)


class TimetableBuilder:
    def __init__(self, parser, infra, direction, schedule_type="weekdays", global_ledger=None, logger=None):
        self.parser = parser
        self.infra = infra
        self.direction = direction
        self.schedule_type = schedule_type
        self.sch_zh = "平日" if schedule_type == "weekdays" else "假日"
        self.schedule = []
        self.counters = {} 
        
        self.logger = logger or getattr(parser, 'logger', None)
        if not self.infra.logger:
            self.infra.logger = self.logger

        self.line_id = os.path.basename(self.parser.project_path) if self.parser and hasattr(self.parser, 'project_path') and self.parser.project_path else "UNKNOWN_LINE"

        if global_ledger is None:
            from core.global_ledger import GlobalLedger
            self.global_ledger = GlobalLedger(logger=self.logger)
        else:
            self.global_ledger = global_ledger

        if hasattr(self.parser, 'project_path') and self.parser.project_path:
            st_json = os.path.join(os.path.dirname(self.parser.project_path), "station.json")
            self.infra.load_from_json(st_json, self.line_id, self.parser)

    def log(self, msg):
        if self.logger: self.logger(msg)
        else: print(msg)

    def attempt_route(self, grade, start_sec, buffer_sec, allow_stretch, shift_step):
        pattern = self.parser.patterns[self.direction].get(grade)
        
        if not pattern: 
            for k, v in self.parser.level_mapping.items():
                if v.get('name') == grade and v.get('direction') == self.direction:
                    grade = k
                    pattern = self.parser.patterns[self.direction].get(k)
                    break

        if not pattern: 
            return "IMPOSSIBLE", f"在基準時刻表 (CSV) 中完全找不到等級 [{grade}] 的行駛時間網格！", None, None, None
        
        full_sts = self.parser.stations[self.direction]
        proj_off = {}
        has_any = False
        
        for st in full_sts:
            p = pattern.get(st, {})
            a = p.get('到')
            d = p.get('發')
            if a is not None or d is not None: has_any = True
            if a is None and d is not None: a = d
            if d is None and a is not None: d = a
            proj_off[st] = {'arr': a, 'dep': d, 'real_a': p.get('到'), 'real_d': p.get('發')}
            
        if not has_any: 
            return "IMPOSSIBLE", f"等級 [{grade}] 的行駛時間網格全為空白", None, None, None

        last_k = -1
        for i, st in enumerate(full_sts):
            if proj_off[st]['arr'] is not None:
                if last_k == -1: 
                    last_k = i 
                else:
                    miss = i - last_k - 1
                    if miss > 0:
                        t0 = proj_off[full_sts[last_k]]['dep']
                        t1 = proj_off[st]['arr']
                        step = (t1 - t0) / (miss + 1)
                        for j in range(1, miss + 1):
                            t_interp = t0 + step * j
                            proj_off[full_sts[last_k + j]]['arr'] = t_interp
                            proj_off[full_sts[last_k + j]]['dep'] = t_interp
                    last_k = i

        first_idx = next(i for i, st in enumerate(full_sts) if proj_off[st]['arr'] is not None)
        last_idx = next(i for i in range(len(full_sts)-1, -1, -1) if proj_off[full_sts[i]]['dep'] is not None)
        visited_sts = full_sts[first_idx:last_idx+1]
        
        actual_times = {}
        assigned_st_tracks = {}
        assigned_conn_tracks = {}
        
        for i, st in enumerate(visited_sts):
            is_first = (i == 0)
            is_last = (i == len(visited_sts) - 1)
            
            arr_off = proj_off[st]['arr']
            dep_off = proj_off[st]['dep']
            real_a = proj_off[st]['real_a']
            real_d = proj_off[st]['real_d']
            
            if is_first:
                arr_calc = start_sec + arr_off
            else:
                prev_st = visited_sts[i-1]
                prev_dep_calc = actual_times[prev_st]['_calc_dep']
                travel_sec = arr_off - proj_off[prev_st]['dep']
                arr_calc = prev_dep_calc + travel_sec
                
            min_dwell = dep_off - arr_off
            base_dep_calc = arr_calc + min_dwell
            
            prev_st_name = visited_sts[i-1] if not is_first else None
            next_st_name = visited_sts[i+1] if not is_last else None
            
            valid_st_tracks, st_reason = self.infra.get_valid_st_tracks(st, grade, prev_st_name, next_st_name)
            if not valid_st_tracks: 
                return "IMPOSSIBLE", f"車站 [{st}] 無可用股道，診斷結果: {st_reason}", None, None, None
            
            valid_conn_tracks = []
            if next_st_name:
                valid_conn_tracks, conn_reason = self.infra.get_valid_conn_tracks(st, next_st_name, grade)
                if not valid_conn_tracks: 
                    return "IMPOSSIBLE", f"連接軌 [{st}]->[{next_st_name}] 無可用路線，診斷結果: {conn_reason}", None, None, None

            found_slot = False
            max_delay = 3600 if allow_stretch else 0 
            
            for delay in range(0, max_delay + 1, shift_step):
                test_dep_calc = base_dep_calc + delay
                
                chosen_st = next((t for t in valid_st_tracks if self.global_ledger.is_st_track_free(st, t, arr_calc, test_dep_calc, buffer_sec)), None)
                if not chosen_st: break 

                if is_last:
                    assigned_st_tracks[st] = chosen_st
                    actual_times[st] = {'到': arr_calc if real_a is not None else None, '發': test_dep_calc if real_d is not None else None, '_calc_arr': arr_calc, '_calc_dep': test_dep_calc}
                    found_slot = True
                    break
                    
                travel_to_next = proj_off[next_st_name]['arr'] - dep_off
                test_next_arr = test_dep_calc + travel_to_next
                
                chosen_conn = next((ct for ct in valid_conn_tracks if self.global_ledger.is_conn_track_free(st, next_st_name, ct, test_dep_calc, test_next_arr, buffer_sec)), None)
                        
                if chosen_conn:
                    next_st_next = visited_sts[i+2] if i+2 < len(visited_sts) else None
                    next_st_valid, _ = self.infra.get_valid_st_tracks(next_st_name, grade, st, next_st_next)
                    next_st_ok = any(self.global_ledger.is_st_track_free(next_st_name, nt, test_next_arr, test_next_arr, buffer_sec) for nt in next_st_valid)
                    
                    if next_st_ok:
                        assigned_st_tracks[st] = chosen_st
                        assigned_conn_tracks[(st, next_st_name)] = {'track': chosen_conn, 'enter': test_dep_calc, 'leave': test_next_arr}
                        actual_times[st] = {'到': arr_calc if real_a is not None else None, '發': test_dep_calc if real_d is not None else None, '_calc_arr': arr_calc, '_calc_dep': test_dep_calc}
                        found_slot = True
                        break
                        
                if not allow_stretch: break 
                    
            if not found_slot: 
                return False, f"在時間視窗內皆與其他車次發生衝突", None, None, None 
                
        return True, "OK", actual_times, assigned_st_tracks, assigned_conn_tracks

    def insert_train(self, grade, ideal_start_sec, min_start_sec, params, is_seed=False, source_train_id=None, source_line=None, is_revenue=True):
        shift_step = params.get('shift_step', 5)
        allow_stretch = params.get('stretch', params.get('allow_stretch', False))
        buffer_sec = params.get('buffer_time', params.get('buffer_sec', 45))
        test_sec = max(ideal_start_sec, min_start_sec)
        
        max_test_sec = test_sec + 7200 
        
        while test_sec <= max_test_sec:
            status, reason, actual_times, st_assignments, conn_assignments = self.attempt_route(
                grade, test_sec, buffer_sec, allow_stretch, shift_step
            )
            if status is True:
                break
            elif status == "IMPOSSIBLE":
                self.log(f"⚠️ 放棄排定 [{self.direction}] {grade}。原因: {reason}")
                return None
                
            test_sec += shift_step 
        else:
            self.log(f"⚠️ 放棄排定 [{self.direction}] {grade}。原因: 2小時內找不到可用空隙(持續衝突)")
            return None
            
        prio = self.parser.priorities[self.direction].get(grade, 9)
        if prio not in self.counters:
            base = 500 if self.schedule_type == "weekends" else 0
            self.counters[prio] = base + (1 if self.direction == '下行' else 2)
            
        train_id_str = f"{prio}{self.counters[prio]:03d}"
        self.counters[prio] += 2 
            
        new_train = {
            'id': train_id_str, 
            'grade': grade,
            'direction': self.direction,
            'times': {},
            'connections': conn_assignments,
            'is_seed': is_seed,                  
            'source_train_id': source_train_id,  
            'source_line': source_line if source_line else self.line_id,
            'is_revenue': is_revenue
        }
        
        for st, times in actual_times.items():
            new_train['times'][st] = {
                '到': times['到'], 
                '發': times['發'],
                'track': st_assignments.get(st),
                '_calc_arr': times['_calc_arr'],
                '_calc_dep': times['_calc_dep']
            }
            
        self.schedule.append(new_train)
        
        for st, times in actual_times.items():
            t_id = st_assignments.get(st)
            if t_id:
                self.global_ledger.book_st_track(st, t_id, times['_calc_arr'], times['_calc_dep'], self.line_id, train_id_str)
                
        for (stA, stB), conn_info in conn_assignments.items():
            ct_id = conn_info['track']
            if ct_id:
                self.global_ledger.book_conn_track(stA, stB, ct_id, conn_info['enter'], conn_info['leave'], self.line_id, train_id_str)

        return test_sec

    # 🌟 修改：支援接收並傳遞幽靈種子資訊
    def insert_deadhead(self, start_st, end_st, ideal_start_sec, params, is_seed=False, source_train_id=None, source_line=None):
        """動態向 Parser 請求回送網格並插入全域帳本，支援跨線種子交接"""
        dh_id = self.parser.get_or_create_deadhead_pattern(start_st, end_st, self.direction)
        if not dh_id:
            self.log(f"⚠️ 無法生成從 {start_st} 到 {end_st} 的回送網格，請檢查車站名稱或順序。")
            return None
            
        self.log(f"   💨 開始安插回送車 [{dh_id}] 於 {self.parser.to_str(ideal_start_sec)}")
        return self.insert_train(
            grade=dh_id, 
            ideal_start_sec=ideal_start_sec, 
            min_start_sec=ideal_start_sec, 
            params=params, 
            is_revenue=False,
            is_seed=is_seed,
            source_train_id=source_train_id,
            source_line=source_line
        )

    def _distribute_evenly(self, grades_with_counts, start_sec, cycle_sec):
        total_trains = sum(grades_with_counts.values())
        if total_trains <= 0: return []

        temp_list = []
        for g, count in grades_with_counts.items():
            if count <= 0: continue
            for i in range(count):
                rel_pos = (i + 0.5) / count 
                temp_list.append((g, rel_pos))

        temp_list.sort(key=lambda x: x[1])

        interval = cycle_sec / total_trains
        result = []
        for i, (g, _) in enumerate(temp_list):
            ideal_time = start_sec + (i + 0.5) * interval
            result.append((g, ideal_time))

        return result

    def build_period(self, start_sec, end_sec, grade_counts, cycle_mins, params, ghost_seeds=None, through_counts_per_hour=None):
        if cycle_mins <= 0: return
        
        from core.timetable_parser import TimetableParser
        
        cycle_sec = cycle_mins * 60
        cycles = math.ceil((end_sec - start_sec) / cycle_sec)

        active_grades = {g: c for g, c in grade_counts.items() if c > 0}
        through_counts = {g: c for g, c in (through_counts_per_hour or {}).items() if c > 0}
        
        if not active_grades and not ghost_seeds and not through_counts: 
            return

        through_accumulators = {g: 0.0 for g in through_counts}

        for c in range(cycles):
            c_start = start_sec + c * cycle_sec
            c_end = c_start + cycle_sec

            current_cycle_through = {}
            for g, tph in through_counts.items():
                through_accumulators[g] += tph * (cycle_mins / 60.0)
                int_count = int(math.floor(through_accumulators[g] + 1e-5)) 
                if int_count > 0:
                    current_cycle_through[g] = int_count
                    through_accumulators[g] -= int_count
            
            combined_counts = dict(active_grades)
            for g, count in current_cycle_through.items():
                combined_counts[g] = combined_counts.get(g, 0) + count

            if not combined_counts and not ghost_seeds:
                continue

            max_prio = -1
            superior_counts = {}
            inferior_counts = {}
            
            if combined_counts:
                for g in combined_counts.keys():
                    p = self.parser.priorities[self.direction].get(g, 99)
                    if p > max_prio:
                        max_prio = p

                for g, c_cnt in combined_counts.items():
                    p = self.parser.priorities[self.direction].get(g, 99)
                    if p == max_prio: inferior_counts[g] = c_cnt
                    else: superior_counts[g] = c_cnt

                sup_trains = self._distribute_evenly(superior_counts, c_start, cycle_sec)
                inf_trains = self._distribute_evenly(inferior_counts, c_start, cycle_sec)
                all_planned = sup_trains + inf_trains
                all_planned.sort(key=lambda x: self.parser.priorities[self.direction].get(x[0], 99))
            else:
                all_planned = []

            if ghost_seeds:
                cycle_seeds = [s for s in ghost_seeds if c_start <= s['min_dep'] < c_end]
                for seed in cycle_seeds:
                    s_grade = seed['grade']
                    
                    if s_grade not in self.parser.level_mapping:
                        for k, v in self.parser.level_mapping.items():
                            if v.get('name') == s_grade and v.get('direction') == self.direction:
                                s_grade = k
                                break

                    s_min = seed['min_dep']
                    s_max = seed['max_dep']
                    
                    best_slot_idx = -1
                    min_diff = float('inf')
                    
                    for idx, (p_grade, p_time) in enumerate(all_planned):
                        if p_grade == s_grade:
                            if s_min <= p_time <= s_max:
                                diff = abs(p_time - (s_min + s_max) / 2)
                                if diff < min_diff:
                                    min_diff = diff
                                    best_slot_idx = idx
                    
                    if best_slot_idx != -1:
                        hijacked_time = all_planned[best_slot_idx][1]
                        self.log(f"   🔗 直通車 [{s_grade}] 成功鳩佔鵲巢：鎖定完美網格 {TimetableParser.to_str(hijacked_time)}")
                        self.insert_train(s_grade, hijacked_time, s_min, params, is_seed=True, source_train_id=seed.get('source_train_id'), source_line=seed.get('source_line'))
                        all_planned.pop(best_slot_idx) 
                    else:
                        closest_idx = -1
                        min_distance = float('inf')
                        
                        for idx, (p_grade, p_time) in enumerate(all_planned):
                            if p_grade == s_grade:
                                if p_time < s_min:
                                    dist = s_min - p_time
                                else:
                                    dist = p_time - s_max
                                    
                                if dist < min_distance:
                                    min_distance = dist
                                    closest_idx = idx
                        
                        if closest_idx != -1:
                            snapped_time = all_planned[closest_idx][1]
                            self.log(f"   🧲 直通車 [{s_grade}] 啟動磁吸演算法：消耗相鄰網格 {TimetableParser.to_str(snapped_time)} (差距 {int(min_distance)} 秒)")
                            self.insert_train(s_grade, s_min, s_min, params, is_seed=True, source_train_id=seed.get('source_train_id'), source_line=seed.get('source_line'))
                            all_planned.pop(closest_idx)
                        else:
                            self.log(f"   ⚠️ 直通車 [{s_grade}] 無網格可吸附，強行於邊界開啟時間 {TimetableParser.to_str(s_min)} 擠入。")
                            self.insert_train(s_grade, s_min, s_min, params, is_seed=True, source_train_id=seed.get('source_train_id'), source_line=seed.get('source_line'))

            for grade, ideal_time in all_planned:
                self.insert_train(grade, ideal_time, c_start, params)

    def filter_by_operating_hours(self, first_train_sec, last_train_sec):
        """
        過濾營運時間外的車次 (去頭去尾功能)。
        確保車次的首站發車時間，嚴格落在首末班車的設定區間內。
        """
        def get_first_time(train):
            for st in self.parser.stations[self.direction]:
                if st in train['times']:
                    if train['times'][st]['發'] is not None: 
                        return train['times'][st]['發']
                    if train['times'][st]['到'] is not None: 
                        return train['times'][st]['到']
            return 0
        
        self.schedule = [t for t in self.schedule if first_train_sec <= get_first_time(t) <= last_train_sec]

    def export_to_csv(self, filepath, linkage_registry=None):
        if not self.schedule: return False
        
        self.log(f"📄 產出 [{self.sch_zh}][{self.direction}] 時刻表報表...")

        def get_sort_time(train):
            for st in self.parser.stations[self.direction]:
                if st in train['times'] and train['times'][st]['發'] is not None:
                    return train['times'][st]['發']
            return 0
        self.schedule.sort(key=get_sort_time)

        stations = self.parser.stations[self.direction]
        header_id = ['車站', '到發'] + [str(t['id']) for t in self.schedule]
        
        # UI端可以根據這個名字或內部邏輯辨識回送車
        header_grade = ['', ''] + [self.parser.level_mapping.get(t['grade'], {}).get("name", t['grade']) for t in self.schedule]
        rows = [header_id, header_grade]

        for st in stations:
            row_arr = [st, '到']
            row_dep = ['', '發']
            for t in self.schedule:
                times = t['times'].get(st, {})
                row_arr.append(self.parser.to_str(times.get('到')))
                row_dep.append(self.parser.to_str(times.get('發')))
            rows.append(row_arr)
            rows.append(row_dep)

        row_next_line = ['接續路線', '']
        row_next_grade = ['接續等級', '']
        row_next_id = ['接續車次', '']

        for t in self.schedule:
            link = linkage_registry.get((self.line_id, t['id'])) if linkage_registry else None
            
            if link:
                row_next_line.append(str(link['next_line']))
                row_next_grade.append(str(link['next_grade']))
                row_next_id.append(str(link['next_id']))
            else:
                row_next_line.append('')
                row_next_grade.append('')
                row_next_id.append('')

        rows.append(row_next_line)
        rows.append(row_next_grade)
        rows.append(row_next_id)

        df = pd.DataFrame(rows)
        df.to_csv(filepath, index=False, header=False, encoding='utf-8-sig')
        return True