class RLPolicyAdapter:
    def __init__(self, checkpoint: str):
        self.path = checkpoint
        # TODO: 載入 SB3 模型

    def plan(self, ts_state):
        # TODO: 轉 obs → model.predict → 決策 dict
        return None
