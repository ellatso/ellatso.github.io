from typing import List, Tuple, Dict, Any, Optional

class Arbiter:
    def __init__(self, priority: List[str]):
        self.priority = priority

    def choose(self, decisions: List[Tuple[str, Dict[str, Any]]]) -> Optional[Tuple[str, Dict[str, Any]]]:
        # 依 priority 取第一個可執行；（可擴：同 phase extend 合併 duration）
        for key in self.priority:
            for name, d in decisions:
                if name == key and d is not None:
                    return (name, d)
        return None
