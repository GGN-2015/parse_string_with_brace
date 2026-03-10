try:
    from .Sequence import Sequence, BRACE_SEQUENCE_CLASS_META_OBJECT
except:
    from Sequence import Sequence, BRACE_SEQUENCE_CLASS_META_OBJECT

class BraceSequence:
    def __int__(self):
        self.inner_sequence = Sequence.init([])
    
    @classmethod
    def init(cls, inner_sequence: Sequence) -> 'BraceSequence':
        if not isinstance(inner_sequence, Sequence):
            raise TypeError()
        new_obj = BraceSequence()
        new_obj.inner_sequence = inner_sequence
        return new_obj
    
    def serialize(self) -> str:
        return f"({self.inner_sequence.serialize()})"
    
    
    def json_obj(self) -> dict:
        return {
            "type": "BraceSequence",
            "inner_sequence": self.inner_sequence.json_obj()
        }
    
    @classmethod
    def deserialize(cls, s:str) -> 'BraceSequence':
        s = s.strip()
        if not s.startswith("("):
            raise ValueError()
        if not s.endswith(")"):
            raise ValueError("Unterminated parenthetical expression.")
        new_obj = BraceSequence()
        new_obj.inner_sequence = Sequence.deserialize(s[1:-1])
        return new_obj
    
    @classmethod
    def from_json_obj(cls, json_obj:dict) -> 'BraceSequence':
        if json_obj.get("type") != "BraceSequence":
            raise TypeError()
        if json_obj.get("inner_sequence") is None:
            raise ValueError()
        new_obj = BraceSequence()
        new_obj.inner_sequence = Sequence.from_json_obj(
            json_obj["inner_sequence"]
        )
        return new_obj
    
    def has_sub_brace(self) -> bool:
        return self.inner_sequence.has_sub_brace()
    
    # 检查一个序列是不是完全由常量构成
    def all_const(self) -> bool:
        return self.inner_sequence.all_const()

# 传参方式传递类型对象
BRACE_SEQUENCE_CLASS_META_OBJECT[0] = BraceSequence # type: ignore

if __name__ == "__main__":
    item = BraceSequence.deserialize("(a (b (*c) *f d) e)")
    print(item.serialize())
    print(BraceSequence.from_json_obj(item.json_obj()).serialize())
