try:
    from .BraceSequence import BraceSequence
    from .Sequence import Sequence
    from .ValueTerm import ValueTerm
except:
    from BraceSequence import BraceSequence
    from Sequence import Sequence
    from ValueTerm import ValueTerm

class ValueMap:
    def __init__(self) -> None:
        self.left = BraceSequence.init(Sequence.init([]))
        self.right = ValueTerm.init(Sequence.init([]))

    @classmethod
    def init(cls, left:BraceSequence, right:ValueTerm) -> 'ValueMap':
        if not isinstance(left, BraceSequence):
            raise TypeError()
        if not isinstance(right, ValueTerm):
            raise TypeError()
        new_item = ValueMap()
        new_item.left = left
        new_item.right = right
        return new_item
    
    # 这里右侧序列化的时候不使用中括号，但需要牢记右侧是 ValueTerm
    def serialize(self) -> str:
        return f"{self.left.serialize()} => {self.right.serialize()[1:-1]}"
    
    def json_obj(self) -> dict:
        return {
            "type": "ValueMap",
            "left": self.left.json_obj(),
            "right": self.right.json_obj()
        }
    
    @classmethod
    def deserialize(cls, s:str) -> 'ValueMap':
        if s.find("=>") == -1:
            raise ValueError()
        left_str, right_str = s.split("=>", maxsplit=1)
        new_item = ValueMap()
        new_item.left = BraceSequence.deserialize(left_str)
        new_item.right = ValueTerm.deserialize(f"[{right_str}]")
        return new_item
    
    @classmethod
    def from_json_obj(cls, json_obj:dict) -> 'ValueMap':
        if json_obj.get("type") != "ValueMap":
            raise TypeError()
        if json_obj.get("left") is None:
            raise ValueError()
        if json_obj.get("right") is None:
            raise ValueError()
        new_item = ValueMap()
        new_item.left = BraceSequence.from_json_obj(json_obj["left"])
        new_item.right = ValueTerm.from_json_obj(json_obj["right"])
        return new_item
    
if __name__ == "__main__":
    
    test_list = [
        "() => a b c",
        "(a (b c d) e) => (a (b) c)",
        "(a b) => a"
    ]
    for value in test_list:
        print(ValueMap.deserialize(value).serialize())
        print(ValueMap.from_json_obj(ValueMap.deserialize(value).json_obj()).serialize())
