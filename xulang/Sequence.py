try:
    from .SimpleTerm import SimpleTerm
except:
    from SimpleTerm import SimpleTerm

def flush(buffer:str, arr:list) -> str:
    if buffer != "":
        arr.append(buffer)
    return ""

def smart_split(s:str) -> list[str]:
    arr = []
    buffer = ""
    for i in range(len(s)):
        if s[i].isspace():
            buffer = flush(buffer, arr)
        elif s[i] in ["(", ")"]:
            buffer = flush(buffer, arr)
            arr.append(s[i])
        else:
            buffer += s[i]
    buffer = flush(buffer, arr)
    return arr

def find_match(str_list:list[str], index:int):
    cnt = 0
    pos = -1
    for j in range(index, len(str_list)):
        if str_list[j] == "(":
            cnt += 1
        elif str_list[j] == ")":
            cnt -= 1
        if cnt == 0 and j > index:
            pos = j
            break
    if pos == -1:
        raise ValueError() # 没有找到匹配的括号
    return pos

BRACE_SEQUENCE_CLASS_META_OBJECT = [None]

class Sequence:
    def __init__(self) -> None:
        self.objects = []
    
    @classmethod
    def init(cls, objects:list) -> 'Sequence':
        for term in objects:
            if type(term).__name__ not in ["SimpleTerm", "BraceSequence"]:
                raise TypeError()
        new_item = Sequence()
        new_item.objects = objects
        return new_item
    
    def serialize(self) -> str:
        return " ".join([
            term.serialize() for term in self.objects
        ])
    
    def json_obj(self) -> dict:
        return {
            "type": "Sequence",
            "objects": [
                term.json_obj() for term in self.objects
            ]
        }
    
    @classmethod
    def deserialize(cls, s:str) -> 'Sequence':
        if BRACE_SEQUENCE_CLASS_META_OBJECT[0] is None:
            raise AssertionError()
        str_list = smart_split(s)
        object_list = []
        index = 0
        while index < len(str_list):
            if str_list[index] == ")":
                raise ValueError("Unexpected closing parenthesis.")
            elif str_list[index] == "(":
                pos = find_match(str_list, index)
                object_list.append(
                    BRACE_SEQUENCE_CLASS_META_OBJECT[0].deserialize(
                        " ".join(str_list[index: pos+1])
                    )
                )
                index = pos + 1
            else:
                object_list.append(
                    SimpleTerm.deserialize(str_list[index])
                )
                index += 1
        return Sequence.init(object_list)

    @classmethod
    def from_json_obj(cls, json_obj:dict) -> 'Sequence':
        if BRACE_SEQUENCE_CLASS_META_OBJECT[0] is None:
            raise AssertionError()
        if json_obj.get("type") != "Sequence":
            raise TypeError()
        if not isinstance(json_obj.get("objects"), list):
            raise TypeError()
        object_list = []
        for term in json_obj["objects"]:
            if term.get("type") not in ["SimpleTerm", "BraceSequence"]:
                raise TypeError()
            if term["type"] == "SimpleTerm":
                object_list.append(
                    SimpleTerm.from_json_obj(term)
                )
            else:
                object_list.append(
                    BRACE_SEQUENCE_CLASS_META_OBJECT[0].from_json_obj(term)
                )
        return Sequence.init(object_list)
    
    def has_sub_brace(self) -> bool:
        if BRACE_SEQUENCE_CLASS_META_OBJECT[0] is None:
            raise AssertionError()
        for item in self.objects:
            if isinstance(item, BRACE_SEQUENCE_CLASS_META_OBJECT[0]):
                return True
        return False

    # 检查一个序列是不是完全由常量构成
    def all_const(self) -> bool:
        ans = True
        for term in self.objects:
            ans = ans and term.all_const()
        return ans
