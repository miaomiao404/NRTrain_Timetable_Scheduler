import os
import shutil
import pandas as pd
import json
import re
import uuid
import datetime
from collections import deque

from core.timetable_parser import TimetableParser
from core.timetable_builder import TimetableBuilder, Infrastructure
from core.train_dispatcher import Dispatcher
from core.global_ledger import GlobalLedger
from core.through_run_manager import ThroughRunManager

class RailwayEngine:
    def __init__(self, workspace_root="save", logger=None):
        self.workspace_root = workspace_root
        self.current_env = "env_default" 
        self.current_project = None
        self.logger = logger
        self.parser = TimetableParser(logger=self.log_msg)
        self.schedules = {}          
        self.vehicles = []           
        self.all_trips = []          
        
        self.global_fleet_state = []
        
        if not os.path.exists(self.workspace_root):
            os.makedirs(self.workspace_root)
            
        self.env_path = os.path.join(self.workspace_root, self.current_env)
        os.makedirs(self.env_path, exist_ok=True)
        
        self.station_file = os.path.join(self.env_path, "station.json")
        if not os.path.exists(self.station_file):
            with open(self.station_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)

    @property
    def project_path(self):
        if not self.current_project: return None
        return os.path.join(self.env_path, self.current_project)

    def log_msg(self, msg):
        if self.logger: 
            self.logger(msg)
        else: 
            try:
                print(msg)
            except Exception:
                pass
            
        try:
            log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_log.txt")
            with open(log_path, "a", encoding="utf-8-sig") as f:
                f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        except Exception:
            pass

    def scan_projects(self):
        if not os.path.exists(self.env_path): return []
        return [d for d in os.listdir(self.env_path) if os.path.isdir(os.path.join(self.env_path, d))]

    def create_project(self, project_name):
        self.current_project = project_name
        os.makedirs(self.project_path, exist_ok=True)
        self.log_msg(f"📁 建立/切換至路線專案: {project_name}")

    def _scan_environment_lines(self):
        lines = []
        if not self.env_path or not os.path.exists(self.env_path): return lines
        for item in os.listdir(self.env_path):
            p = os.path.join(self.env_path, item)
            if os.path.isdir(p) and os.path.exists(os.path.join(p, "information.json")):
                lines.append(item)
        return lines

    def _get_scheduling_order(self, lines, rules):
        nodes = []
        for line in lines:
            nodes.append((line, '上行'))
            nodes.append((line, '下行'))

        adj = {node: set() for node in nodes}
        in_degree = {node: 0 for node in nodes}

        for rule in rules:
            chain = rule.get('chain', [])
            for i in range(len(chain) - 1):
                src_line = chain[i].get('line_id')
                src_dir = chain[i].get('direction', '上行')
                dst_line = chain[i+1].get('line_id')
                dst_dir = chain[i+1].get('direction', '上行')

                src_node = (src_line, src_dir)
                dst_node = (dst_line, dst_dir)

                if src_node in nodes and dst_node in nodes:
                    if dst_node not in adj[src_node]:
                        adj[src_node].add(dst_node)
                        in_degree[dst_node] += 1

        queue = [node for node in nodes if in_degree[node] == 0]
        order = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        for node in nodes:
            if node not in order:
                order.append(node)
                
        return order

    def _build_station_graph(self, builders_store):
        graph = {}
        for b_info in builders_store:
            b = b_info['builder']
            direction = b_info['direction']
            st_list = b.parser.stations.get(direction, [])
            
            for i in range(len(st_list)):
                s_i = st_list[i]
                if s_i not in graph:
                    graph[s_i] = []
                for j in range(i+1, len(st_list)):
                    s_j = st_list[j]
                    graph[s_i].append((s_j, b))
        return graph

    def _plan_deadhead_path(self, from_st, to_st, station_graph):
        queue = deque([(from_st, [])])
        visited = set([from_st])

        while queue:
            curr_st, path = queue.popleft()
            if curr_st == to_st:
                return path

            for next_st, builder in station_graph.get(curr_st, []):
                if next_st not in visited:
                    visited.add(next_st)
                    queue.append((next_st, path + [(builder, curr_st, next_st)]))
        return None

    def run_full_simulation(self, schedule_type="all"):
        self.log_msg(f"🚀 開始執行全環境 [365天 平日+假日] 模擬排班 (啟動方向解耦)...")

        types_to_run = ["weekdays", "weekends"] if schedule_type == "all" else [schedule_type]
        overall_success = True
        
        self.global_fleet_state = []

        for stype in types_to_run:
            self.log_msg(f"\n{'='*50}")
            self.log_msg(f"📅 開始進行 [{stype}] 模式全域排班")
            self.log_msg(f"{'='*50}")
            
            success = self._run_single_simulation(stype)
            if not success:
                overall_success = False
                self.log_msg(f"❌ [{stype}] 模式排班失敗或中斷！")

        if overall_success:
            self.log_msg(f"✅ 模擬排班與派車完成！(全環境 365 天)")
            
        return overall_success

    def _run_single_simulation(self, schedule_type):
        global_ledger = GlobalLedger(logger=self.log_msg)
        through_run_manager = ThroughRunManager(logger=self.log_msg)

        lines = self._scan_environment_lines()
        if not lines:
            self.log_msg("⚠️ 環境中沒有任何路線設定，取消排班。")
            return False

        rules_path = os.path.join(self.env_path, "through_rules.json")
        rules = []
        if os.path.exists(rules_path):
            try:
                with open(rules_path, 'r', encoding='utf-8') as f:
                    rules = json.load(f)
            except Exception as e:
                self.log_msg(f"⚠️ 讀取 through_rules.json 失敗: {e}")

        global_freq_path = os.path.join(self.env_path, "global_through_freq.json")
        global_through_freq = {}
        if os.path.exists(global_freq_path):
            try:
                with open(global_freq_path, 'r', encoding='utf-8') as f:
                    global_through_freq = json.load(f)
            except Exception as e:
                self.log_msg(f"⚠️ 讀取 global_through_freq.json 失敗: {e}")

        scheduling_order = self._get_scheduling_order(lines, rules)
        order_str = ' ➔ '.join([f"{l}({d})" for l, d in scheduling_order])
        self.log_msg(f"📋 [{schedule_type}] 系統排班計算順序決定為: {order_str}")

        all_global_schedules = {line: [] for line in lines}
        builders_store = []

        # ==========================================
        # 🟢 第一階段：常規客運排班 (First-Pass)
        # ==========================================
        for line_id, direction in scheduling_order:
            self.log_msg(f"\n======================================")
            self.log_msg(f"🚂 開始排定路線: {line_id} [{direction}] ({schedule_type})")
            self.log_msg(f"======================================")

            line_path = os.path.join(self.env_path, line_id)
            
            local_parser = TimetableParser(logger=self.log_msg)
            local_parser.project_path = line_path
            
            if hasattr(local_parser, 'load_train_levels'):
                local_parser.load_train_levels()
                
            csv_name = "stb_up.csv" if direction == "上行" else "stb_down.csv"
            csv_path = os.path.join(line_path, csv_name)
            
            if hasattr(local_parser, 'parse_template'):
                if os.path.exists(csv_path): local_parser.parse_template(csv_path, direction)
            elif hasattr(local_parser, 'parse_csv'):
                if os.path.exists(csv_path): local_parser.parse_csv(csv_path, direction)

            try:
                infra = Infrastructure(logger=self.log_msg)
            except TypeError:
                infra = Infrastructure()

            try:
                builder = TimetableBuilder(local_parser, infra, direction, schedule_type, global_ledger, self.log_msg)
            except TypeError:
                builder = TimetableBuilder(local_parser, infra, direction, schedule_type)
                builder.global_ledger = global_ledger
                builder.logger = self.log_msg

            freq_path = os.path.join(line_path, "frequency.json")
            freq_data = {}
            if os.path.exists(freq_path):
                with open(freq_path, 'r', encoding='utf-8') as f:
                    freq_data = json.load(f)

            periods = [
                (['weekday_offpeak'], 3*3600, 6*3600),
                (['weekday_offpeak', 'weekday_morning'], 6*3600, 7*3600), 
                (['weekday_morning'], 7*3600, 9*3600),
                (['weekday_morning', 'weekday_offpeak'], 9*3600, 10*3600), 
                (['weekday_offpeak'], 10*3600, 16*3600),
                (['weekday_offpeak', 'weekday_night'], 16*3600, 17*3600), 
                (['weekday_night'], 17*3600, 20*3600),
                (['weekday_night', 'weekday_offpeak'], 20*3600, 21*3600), 
                (['weekday_offpeak'], 21*3600, 22*3600),
                (['weekday_offpeak', 'weekday_latenight'], 22*3600, 23*3600), 
                (['weekday_latenight'], 23*3600, 27*3600)
            ] if schedule_type == "weekdays" else [
                (['weekend_offpeak'], 3*3600, 22*3600),
                (['weekend_offpeak', 'weekend_latenight'], 22*3600, 23*3600), 
                (['weekend_latenight'], 23*3600, 27*3600)
            ]

            for p_keys, start_sec, end_sec in periods:
                if len(p_keys) == 1:
                    p_key = p_keys[0]
                    f_cfg = freq_data.get(p_key, {})
                    cycle = f_cfg.get('cycle_min', 60)
                    
                    freq_key = 'frequencies_up' if direction == '上行' else 'frequencies_down'
                    f_counts = dict(f_cfg.get(freq_key, {}))

                    through_counts_per_hour = {}
                    for rule in rules:
                        chain = rule.get('chain', [])
                        if not chain: continue
                        for node in chain:
                            if node.get('line_id') == line_id and node.get('direction', '上行') == direction:
                                rule_id = rule.get('id')
                                node_grade = node.get('grade')
                                
                                if rule_id and node_grade:
                                    actual_node_grade = node_grade
                                    if actual_node_grade not in local_parser.level_mapping:
                                        for k, v in local_parser.level_mapping.items():
                                            if v.get('name') == node_grade and v.get('direction') == direction:
                                                actual_node_grade = k
                                                break

                                    through_count = global_through_freq.get(rule_id, {}).get(p_key, 0)
                                    if through_count > 0:
                                        through_counts_per_hour[actual_node_grade] = through_counts_per_hour.get(actual_node_grade, 0) + through_count

                elif len(p_keys) == 2:
                    k1, k2 = p_keys
                    f_cfg1 = freq_data.get(k1, {})
                    f_cfg2 = freq_data.get(k2, {})
                    c1 = f_cfg1.get('cycle_min', 60)
                    c2 = f_cfg2.get('cycle_min', 60)
                    
                    freq_key = 'frequencies_up' if direction == '上行' else 'frequencies_down'
                    fc1 = f_cfg1.get(freq_key, {})
                    fc2 = f_cfg2.get(freq_key, {})
                    
                    tph1 = {g: c * (60.0 / c1) for g, c in fc1.items()} if c1 > 0 else {}
                    tph2 = {g: c * (60.0 / c2) for g, c in fc2.items()} if c2 > 0 else {}
                    
                    f_counts = {}
                    for g in set(tph1.keys()) | set(tph2.keys()):
                        avg_val = (tph1.get(g, 0) + tph2.get(g, 0)) / 2.0
                        int_val = int(round(avg_val))
                        if int_val > 0:
                            f_counts[g] = int_val
                            
                    cycle = 60 
                    
                    through_counts_per_hour = {}
                    for rule in rules:
                        chain = rule.get('chain', [])
                        if not chain: continue
                        for node in chain:
                            if node.get('line_id') == line_id and node.get('direction', '上行') == direction:
                                rule_id = rule.get('id')
                                node_grade = node.get('grade')
                                if rule_id and node_grade:
                                    actual_node_grade = node_grade
                                    if actual_node_grade not in local_parser.level_mapping:
                                        for k, v in local_parser.level_mapping.items():
                                            if v.get('name') == node_grade and v.get('direction') == direction:
                                                actual_node_grade = k
                                                break
                                                
                                    t1_thru = global_through_freq.get(rule_id, {}).get(k1, 0)
                                    t2_thru = global_through_freq.get(rule_id, {}).get(k2, 0)
                                    avg_thru = (t1_thru + t2_thru) / 2.0
                                    int_thru = int(round(avg_thru))
                                    if int_thru > 0:
                                        through_counts_per_hour[actual_node_grade] = through_counts_per_hour.get(actual_node_grade, 0) + int_thru

                seeds = through_run_manager.get_seeds_in_window(line_id, direction, start_sec, end_sec)

                try:
                    params = local_parser.get_shift_params()
                except AttributeError:
                    params = {'shift_step': 5, 'buffer_time': 45, 'stretch': False}

                if f_counts or seeds or through_counts_per_hour:
                    try:
                        builder.build_period(start_sec, end_sec, f_counts, cycle, params, ghost_seeds=seeds, through_counts_per_hour=through_counts_per_hour)
                    except TypeError:
                        builder.build_period(start_sec, end_sec, f_counts, cycle, params)

            info_path = os.path.join(line_path, "information.json")
            info_data = {}
            if os.path.exists(info_path):
                try:
                    with open(info_path, 'r', encoding='utf-8') as f:
                        info_data = json.load(f)
                except Exception: pass
                    
            first_t = TimetableParser.to_seconds(info_data.get('首班車發車時間', '06:00:00'))
            if first_t is None: first_t = 6 * 3600
            
            last_t = TimetableParser.to_seconds(info_data.get('末班車發車時間', '27:00:00'))
            if last_t is None or last_t == 86399 or last_t == 86340: 
                last_t = 27 * 3600
            
            if last_t <= first_t: last_t += 24*3600

            builder.filter_by_operating_hours(first_t, last_t)

            sch_csv_name = f"{schedule_type}_sch_up.csv" if direction == "上行" else f"{schedule_type}_sch_down.csv"
            builders_store.append({
                'line_path': line_path,
                'csv_name': sch_csv_name,
                'builder': builder,
                'line_id': line_id,
                'direction': direction
            })

            if builder.schedule:
                self.log_msg(f"✅ {line_id} [{direction}] 成功排定 {len(builder.schedule)} 班車次！")
            else:
                self.log_msg(f"❌ {line_id} [{direction}] 最終沒有任何車次成功排定。")

            all_global_schedules[line_id].extend(builder.schedule)

            for rule in rules:
                chain = rule.get('chain', [])
                nodes = rule.get('nodes', [])
                for i in range(len(chain) - 1):
                    if chain[i].get('line_id') == line_id and chain[i].get('direction', '上行') == direction:
                        
                        source_grade = chain[i].get('grade')
                        actual_source_grade = source_grade
                        if actual_source_grade not in local_parser.level_mapping:
                            for k, v in local_parser.level_mapping.items():
                                if v.get('name') == source_grade and v.get('direction') == direction:
                                    actual_source_grade = k
                                    break

                        target_line = chain[i+1].get('line_id')
                        target_grade = chain[i+1].get('grade')
                        target_direction = chain[i+1].get('direction', '上行')
                        
                        if i + 1 < len(nodes) and nodes[i+1].get('type') == 'junction':
                            boundary_station = nodes[i+1].get('station')
                            min_buf = nodes[i+1].get('min', 120)
                            max_buf = nodes[i+1].get('max', 300)

                            through_run_manager.extract_seeds_from_schedule(
                                source_schedule=builder.schedule,
                                boundary_station=boundary_station,
                                source_line=line_id,         
                                source_grade=actual_source_grade, 
                                target_line=target_line,
                                target_direction=target_direction, 
                                target_grade=target_grade,
                                min_buffer_sec=min_buf,
                                max_buffer_sec=max_buf
                            )

        # ==========================================
        # 🟢 第二階段：回送車盤點與見縫插針 (Two-Pass Squeeze-in)
        # ==========================================
        all_global_schedules = {line: [] for line in lines}
        for b_info in builders_store:
            all_global_schedules[b_info['line_id']].extend(b_info['builder'].schedule)

        self.log_msg(f"\n======================================")
        self.log_msg(f"🕵️ 啟動派車盤點與 SOS 發報 (Dry-Run)")
        self.log_msg(f"======================================")
        
        dry_dispatcher = Dispatcher(
            env_path=self.env_path, 
            schedule_type=schedule_type, 
            logger=self.log_msg, 
            existing_fleet_state=self.global_fleet_state
        )
            
        dry_dispatcher.run_dispatch(all_global_schedules)
        
        dry_run_assignments = {}
        if hasattr(dry_dispatcher, 'vehicles'):
            for v in dry_dispatcher.vehicles:
                for h in v.history:
                    if h.get('type') == 'trip':
                        dry_run_assignments[h['id']] = v.vid
        
        if hasattr(dry_dispatcher, 'audit_deadhead_requests'):
            sos_requests = dry_dispatcher.audit_deadhead_requests()
            
            if sos_requests:
                self.log_msg(f"\n======================================")
                self.log_msg(f"🚑 啟動第二階段排班：回送車自動見縫插針")
                self.log_msg(f"======================================")
                
                station_graph = self._build_station_graph(builders_store)
                
                for req in sos_requests:
                    req_type = req.get('req_type', 'morning')
                    from_st = req['from_st']
                    to_st = req['to_st']
                    count = req['count']
                    start_sec = req['min_after_sec']
                    
                    req_source_train_id = req.get('source_train_id')
                    req_source_line = req.get('source_line')
                    
                    path_segments = self._plan_deadhead_path(from_st, to_st, station_graph)
                    
                    if path_segments:
                        if len(path_segments) == 1:
                            self.log_msg(f"   👉 委派 [{path_segments[0][0].line_id}]({path_segments[0][0].direction}) 執行 {count} 班回送: {from_st} ➔ {to_st}")
                        else:
                            route_str = " ➔ ".join([f"[{b.line_id}]{s}➔{e}" for b, s, e in path_segments])
                            self.log_msg(f"   🗺️ 觸發全域圖尋徑：拆分 {from_st} ➔ {to_st} 為 {route_str}")

                        for _ in range(count):
                            current_seed_train_id = req_source_train_id
                            current_seed_line = req_source_line
                            current_start_sec = start_sec
                            success = True

                            for seg_idx, (b, s_start, s_end) in enumerate(path_segments):
                                try:
                                    params = b.parser.get_shift_params()
                                except AttributeError:
                                    params = {'shift_step': 5, 'buffer_time': 45, 'stretch': False}

                                if req_type == 'night':
                                    params['max_shift'] = max(0, (27 * 3600) - current_start_sec)
                                else:
                                    params['max_shift'] = 7200

                                is_seed = (current_seed_train_id is not None)

                                try:
                                    inserted_sec = b.insert_deadhead(
                                        s_start, s_end,
                                        current_start_sec,
                                        params,
                                        is_seed=is_seed,
                                        source_train_id=current_seed_train_id,
                                        source_line=current_seed_line
                                    )
                                except Exception as e:
                                    self.log_msg(f"      ❌ 安插回送車發生錯誤: {e}")
                                    inserted_sec = None

                                if inserted_sec is not None:
                                    new_train = b.schedule[-1]
                                    current_seed_train_id = new_train['id']
                                    current_seed_line = b.line_id
                                    
                                    arr_seg_end = new_train['times'][s_end]['_calc_arr']
                                    if arr_seg_end is None: arr_seg_end = new_train['times'][s_end]['_calc_dep']
                                    current_start_sec = arr_seg_end 
                                else:
                                    self.log_msg(f"      ❌ 回送段 ({s_start}➔{s_end}) 安插失敗，取消後續段落。")
                                    success = False
                                    break
                                    
                            start_sec += 300 
                    else:
                        valid_junctions = {}
                        for rule in rules:
                            for node in rule.get('nodes', []):
                                if node.get('type') == 'junction':
                                    valid_junctions[node.get('station')] = node.get('min', 120)
                        
                        split_plan = None
                        for J, min_buf in valid_junctions.items():
                            b1, b2 = None, None
                            for b_info in builders_store:
                                b = b_info['builder']
                                st_list = b.parser.stations.get(b_info['direction'], [])
                                if from_st in st_list and J in st_list and st_list.index(from_st) < st_list.index(J):
                                    b1 = b
                                    break
                            for b_info in builders_store:
                                b = b_info['builder']
                                st_list = b.parser.stations.get(b_info['direction'], [])
                                if J in st_list and to_st in st_list and st_list.index(J) < st_list.index(to_st):
                                    b2 = b
                                    break
                            if b1 and b2:
                                split_plan = (J, b1, b2, min_buf)
                                break
                                
                        if split_plan:
                            J, b1, b2, min_buf = split_plan
                            self.log_msg(f"   🗺️ [Fallback] 觸發跨線尋徑：拆分 {from_st} ➔ {to_st} 為 [{b1.line_id}] {from_st}➔{J} 與 [{b2.line_id}] {J}➔{to_st}")
                            
                            try:
                                params1 = b1.parser.get_shift_params()
                            except AttributeError:
                                params1 = {'shift_step': 5, 'buffer_time': 45, 'stretch': False}
                            try:
                                params2 = b2.parser.get_shift_params()
                            except AttributeError:
                                params2 = {'shift_step': 5, 'buffer_time': 45, 'stretch': False}
                                
                            if req_type == 'night':
                                params1['max_shift'] = max(0, (27 * 3600) - start_sec)
                            else:
                                params1['max_shift'] = 7200
                                
                            for _ in range(count):
                                try:
                                    is_seed_1 = (req_source_train_id is not None)
                                    test_sec_1 = b1.insert_deadhead(
                                        from_st, J, start_sec, params1, 
                                        is_seed=is_seed_1, 
                                        source_train_id=req_source_train_id, 
                                        source_line=req_source_line
                                    )
                                    if test_sec_1 is not None:
                                        train1 = b1.schedule[-1]
                                        arr_J = train1['times'][J]['_calc_arr']
                                        if arr_J is None: arr_J = train1['times'][J]['_calc_dep']
                                        ideal_start_2 = arr_J + min_buf
                                        
                                        # 🌟 核心修正點：動態更新 params2 的跨日推移特權 (動態計算下半場的剩餘時間)
                                        if req_type == 'night':
                                            params2['max_shift'] = max(0, (27 * 3600) - ideal_start_2)
                                        else:
                                            params2['max_shift'] = 7200
                                        
                                        self.log_msg(f"      🔗 準備交接跨線回送種子於 {J} 站 (來源車次: {train1['id']})")
                                        b2.insert_deadhead(J, to_st, ideal_start_2, params2, is_seed=True, source_train_id=train1['id'], source_line=b1.line_id)
                                    else:
                                        self.log_msg(f"      ❌ 前半段回送車 ({from_st}➔{J}) 安插失敗，取消後半段。")
                                except Exception as e:
                                    self.log_msg(f"      ❌ 跨線回送車安插發生錯誤: {e}")
                                start_sec += 300
                        else:
                            self.log_msg(f"   ❌ 找不到任何相容路線(含跨線拓樸)可執行 {from_st} ➔ {to_st} 的回送任務，將被迫流浪。")

        all_global_schedules = {line: [] for line in lines}
        for b_info in builders_store:
            all_global_schedules[b_info['line_id']].extend(b_info['builder'].schedule)

        # ==========================================
        # 🟢 第三階段：最終結算與匯出
        # ==========================================
        self.log_msg(f"\n======================================")
        self.log_msg(f"📜 開始結算「全域直通交接名冊」並匯出 CSV")
        self.log_msg(f"======================================")

        linkage_registry = {}
        for b_line, trips in all_global_schedules.items():
            for t in trips:
                if t.get('is_seed') and t.get('source_train_id') and t.get('source_line'):
                    linkage_registry[(t['source_line'], t['source_train_id'])] = {
                        'next_line': b_line,
                        'next_grade': t['grade'],
                        'next_id': t['id']
                    }

        for b_info in builders_store:
            csv_path = os.path.join(b_info['line_path'], b_info['csv_name'])
            try:
                b_info['builder'].export_to_csv(csv_path, linkage_registry)
            except TypeError:
                b_info['builder'].export_to_csv(csv_path)

        self.log_msg(f"\n======================================")
        self.log_msg(f"🚌 開始執行全境車輛無縫派發 (最終版)")
        self.log_msg(f"======================================")

        dispatcher = Dispatcher(
            env_path=self.env_path, 
            schedule_type=schedule_type, 
            logger=self.log_msg, 
            existing_fleet_state=self.global_fleet_state,
            dry_run_assignments=dry_run_assignments 
        )
            
        self.vehicles = dispatcher.run_dispatch(all_global_schedules)
        
        self.global_fleet_state = []
        for v in self.vehicles:
            self.global_fleet_state.append({
                'vid': v.vid,
                'type_name': v.type_name,
                'home_line': getattr(v, 'home_line', ''),
                'home_base_name': v.home_base.name if getattr(v, 'home_base', None) else None
            })
        
        dispatcher.export_to_csv(os.path.join(self.env_path, f"global_{schedule_type}_tud.csv"))
        dispatcher.export_line_specific_csvs(lines)

        self.log_msg(f"☑️ [{schedule_type}] 模式單項排班與派車結束。")
        return True

    def get_vehicle_roster_df(self):
        rows = []
        for v in sorted(self.vehicles, key=lambda x: x.vid):
            row = [str(v.vid), v.initial_loc]
            for h in v.history:
                if h['type'] == 'trip':
                    row.extend([h['direction'], str(h['id']), h['grade'], h['start_st'], TimetableParser.to_str(h['start_sec']), h['end_st'], TimetableParser.to_str(h['end_sec'])])
                elif h['type'] == 'depot_in':
                    row.extend(["-", "入庫", "-", "-", "-", h['facility_name'], TimetableParser.to_str(h['entry_time'])])
            row.extend([v.end_facility, TimetableParser.to_str(v.end_time)])
            rows.append(row)
        max_cols = max((len(r) for r in rows), default=0)
        header = ['車輛編號', '初始出發地']
        for i in range((max_cols - 4) // 7 + 1):
            header.extend([f'運用{i+1}_方向', f'運用{i+1}_車次', f'運用{i+1}_等級', f'運用{i+1}_起點', f'發車', f'終點', f'到站'])
        header.extend(['最終收班地', '收班時間'])
        
        df = pd.DataFrame(rows)
        if not df.empty and len(df.columns) <= len(header): 
            df.columns = header[:len(df.columns)]
        return df

    # ==========================================
    # 🌟 檔案與專案管理工具
    # ==========================================
    def _sync_stations_to_env(self, stations, project_id):
        if not os.path.exists(self.station_file):
            env_data = {}
        else:
            try:
                with open(self.station_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    env_data = json.loads(content) if content else {}
                    if isinstance(env_data, dict) and "nodes" in env_data:
                        converted = {}
                        for node in env_data.get("nodes", []):
                            if "id" in node:
                                converted[node["id"]] = {
                                    "name": node.get("name", ""),
                                    "type": node.get("type", "station"),
                                    "line_id": "", "tracks": [], "connections": []
                                }
                        env_data = converted
            except Exception:
                env_data = {}

        existing_names = {info.get("name") for info in env_data.values() if isinstance(info, dict)}
        
        prefix = re.sub(r'[^a-zA-Z]', '', str(project_id))[:3].upper()
        if not prefix: prefix = "STN"
        
        max_idx = 0
        for nid in env_data.keys():
            if str(nid).startswith(prefix):
                num_part = str(nid)[len(prefix):]
                if num_part.isdigit():
                    max_idx = max(max_idx, int(num_part))
        
        added_count = 0
        for st in stations:
            if st and st not in existing_names:
                max_idx += 1
                new_id = f"{prefix}{max_idx:02d}"
                env_data[new_id] = {
                    "name": st,
                    "type": "station",
                    "line_id": "",
                    "tracks": [],
                    "connections": []
                }
                existing_names.add(st)
                added_count += 1
                
        if added_count > 0:
            with open(self.station_file, 'w', encoding='utf-8') as f:
                json.dump(env_data, f, ensure_ascii=False, indent=4)
            self.log_msg(f"🚉 已自動將 {added_count} 個新車站同步至全域環境 (station.json)。")

    def create_or_load_project(self, project_id, template_csv_path=None):
        self.current_project = project_id
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)
        if template_csv_path:
            self.process_and_split_timetable(template_csv_path, project_id, self.project_path)
        return True, f"✅ 成功載入/切換路線專案: {project_id}"

    def create_new_project(self, info_data, template_csv_path=None):
        project_id = info_data.get('路線ID')
        self.current_project = project_id
        os.makedirs(self.project_path, exist_ok=True)
        
        info_path = os.path.join(self.project_path, "information.json")
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(info_data, f, ensure_ascii=False, indent=4)
            
        if template_csv_path:
            self.process_and_split_timetable(template_csv_path, project_id, self.project_path)
            
        return True, f"✅ 成功建立路線專案: {project_id}"

    def delete_project(self, project_id):
        target_path = os.path.join(self.env_path, project_id)
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
            if self.current_project == project_id:
                self.current_project = None
            return True, f"🗑️ 路線 [{project_id}] 已成功刪除。"
        return False, "找不到該路線資料夾"

    def clone_project(self, source_id, new_info_data):
        new_id = new_info_data.get('路線ID')
        source_path = os.path.join(self.env_path, source_id)
        target_path = os.path.join(self.env_path, new_id)
        
        shutil.copytree(source_path, target_path)
        
        info_path = os.path.join(target_path, "information.json")
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(new_info_data, f, ensure_ascii=False, indent=4)
            
        return True, f"✅ 成功複製路線至: {new_id}"

    def peek_csv_for_stations(self, file_path):
        try:
            try:
                df = pd.read_csv(file_path, header=None, encoding='utf-8-sig')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, header=None, encoding='big5')
                
            stations = []
            for index, row in df.iterrows():
                val = str(row[0]).strip()
                if val == '下行': break
                if val and val.lower() != 'nan' and val not in ['上行', '車站', '到發']:
                    if val not in stations:
                        stations.append(val)
            if not stations: return "", "", 0
            return stations[0], stations[-1], len(stations)
        except Exception:
            return "", "", 0

    def process_and_split_timetable(self, template_csv_path, project_id, project_path):
        try:
            route_color = "#0033A0"
            info_path = os.path.join(project_path, "information.json")
            if os.path.exists(info_path):
                try:
                    with open(info_path, 'r', encoding='utf-8') as f:
                        info_data = json.load(f)
                        route_color = info_data.get('路線顏色', '#0033A0')
                except Exception:
                    pass

            try:
                df = pd.read_csv(template_csv_path, header=None, encoding='utf-8-sig')
            except UnicodeDecodeError:
                df = pd.read_csv(template_csv_path, header=None, encoding='big5')
            
            up_rows = []
            down_rows = []
            current_target = None
            
            for index, row in df.iterrows():
                val = str(row[0]).strip()
                if val == '上行':
                    current_target = up_rows
                    continue
                elif val == '下行':
                    current_target = down_rows
                    continue
                
                if current_target is not None:
                    current_target.append(row.tolist())
                    
            stations_to_sync = []
            if up_rows:
                for r in up_rows[2:]: 
                    st = str(r[0]).strip()
                    if st and st.lower() != 'nan' and st not in stations_to_sync:
                        stations_to_sync.append(st)
            if down_rows:
                for r in down_rows[2:]:
                    st = str(r[0]).strip()
                    if st and st.lower() != 'nan' and st not in stations_to_sync:
                        stations_to_sync.append(st)
                        
            if stations_to_sync:
                self._sync_stations_to_env(stations_to_sync, project_id)
                    
            def _build_stb(rows, direction, id_prefix, train_levels_dict, default_color):
                if not rows: return pd.DataFrame()
                
                header_row = rows[0]
                priority_row = rows[1] if len(rows) > 1 else None
                
                new_header = ['車站', '到發']
                col_mapping = [] 
                
                for col_idx in range(2, len(header_row)):
                    grade_name = str(header_row[col_idx]).strip()
                    if grade_name and grade_name.lower() != 'nan':
                        tid = f"{project_id}_{id_prefix}{len(col_mapping):02d}"
                        
                        new_header.append(tid)
                        col_mapping.append(col_idx)
                        
                        prio_val = 3
                        if priority_row and col_idx < len(priority_row):
                            try:
                                prio_val = int(float(str(priority_row[col_idx]).strip()))
                            except ValueError:
                                pass
                        
                        train_levels_dict[tid] = {
                            "name": grade_name,
                            "priority": prio_val,
                            "direction": direction,
                            "color": default_color 
                        }
                
                out_rows = [new_header]
                for row_idx in range(2, len(rows)):
                    in_row = rows[row_idx]
                    st_name = str(in_row[0]).strip()
                    arr_dep = str(in_row[1]).strip()
                    
                    if st_name.lower() == 'nan': st_name = ""
                    if arr_dep.lower() == 'nan': arr_dep = ""
                    
                    if not st_name and not arr_dep and all(str(in_row[c]).strip().lower() == 'nan' or str(in_row[c]).strip() == '' for c in col_mapping):
                        continue 
                        
                    out_row = [st_name, arr_dep]
                    for c in col_mapping:
                        val = str(in_row[c]).strip() if c < len(in_row) else ""
                        if val.lower() == 'nan': val = ""
                        out_row.append(val)
                    out_rows.append(out_row)
                    
                return pd.DataFrame(out_rows)

            train_levels = {}
            
            if not up_rows and not down_rows:
                df.to_csv(os.path.join(project_path, "stb_up.csv"), index=False, header=False, encoding='utf-8-sig')
                df.to_csv(os.path.join(project_path, "stb_down.csv"), index=False, header=False, encoding='utf-8-sig')
                return
            
            if up_rows:
                df_up = _build_stb(up_rows, "上行", "", train_levels, route_color)
                df_up.to_csv(os.path.join(project_path, "stb_up.csv"), index=False, header=False, encoding='utf-8-sig')
                
            if down_rows:
                df_down = _build_stb(down_rows, "下行", "5", train_levels, route_color)
                df_down.to_csv(os.path.join(project_path, "stb_down.csv"), index=False, header=False, encoding='utf-8-sig')

            levels_path = os.path.join(project_path, "train_levels.json")
            if os.path.exists(levels_path):
                try:
                    with open(levels_path, 'r', encoding='utf-8') as f:
                        old_levels = json.load(f)
                        for k, v in train_levels.items():
                            if k in old_levels:
                                v['color'] = old_levels[k].get('color', route_color)
                except Exception:
                    pass
                    
            with open(levels_path, 'w', encoding='utf-8') as f:
                json.dump(train_levels, f, ensure_ascii=False, indent=4)
                
            self.log_msg(f"✅ 成功從樣板解析出 {len(train_levels)} 種列車等級並切割時刻表。")

        except Exception as e:
            import traceback
            self.log_msg(f"❌ 切割時刻表失敗: {e}\n{traceback.format_exc()}")