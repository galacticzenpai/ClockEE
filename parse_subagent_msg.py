import json

with open(r'C:\Users\Kunal\.gemini\antigravity\brain\121f81ef-e6cd-4e90-a4b0-71f7139b16f4\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        for tc in obj.get('tool_calls', []):
            if tc.get('name') == 'send_message':
                sidx = obj.get('step_index')
                print(f"send_message found at step {sidx}")
                msg = tc.get('args', {}).get('Message', '')
                print(f"Message length: {len(msg)}")
                pos = msg.find('```json')
                if pos != -1:
                    end = msg.find('```', pos + 7)
                    json_str = msg[pos+7:end].strip()
                    try:
                        qs = json.loads(json_str)
                        print(f"Total questions parsed from JSON block: {len(qs)}")
                        with open('pw_physical_world_cycle2_raw.json', 'w', encoding='utf-8') as out:
                            json.dump(qs, out, indent=2, ensure_ascii=False)
                        print("Successfully saved pw_physical_world_cycle2_raw.json")
                    except Exception as e:
                        print(f"Error parsing json block: {e}")
                        with open('pw_pw_c2_dump.txt', 'w', encoding='utf-8') as out:
                            out.write(json_str)
