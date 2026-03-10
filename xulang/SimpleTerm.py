import string

class SimpleTerm:
    def __init__(self) -> None:
        self.content = "simple_term" # 具体内容名称
        self.has_star = False        # 前缀 star

    @classmethod
    def init(cls, msg:str, has_star:bool) -> 'SimpleTerm':
        if not isinstance(has_star, bool):
            raise TypeError()
        if not isinstance(msg, str) or len(msg) == 0:
            raise TypeError()
        if msg == "_":
            raise ValueError() # 不能只留一个下划线
        for i in range(len(msg)):
            if msg[i] not in (["_"] + [
                    char_now for char_now in string.ascii_letters
                ] + [
                    str(num_now) for num_now in range(10)
                ]):
                raise ValueError() # 字母数字下划线
            
        new_item = SimpleTerm()
        new_item.content = msg
        new_item.has_star = has_star
        return new_item
    
    def serialize(self) -> str:
        head = "*" if self.has_star else ""
        return head + self.content

    def json_obj(self) -> dict:
        return {
            "type": "SimpleTerm",
            "content": self.content,
            "has_star": self.has_star
        }

    @classmethod
    def deserialize(cls, s:str) -> 'SimpleTerm':
        s = s.strip()
        has_star = s.startswith("*")
        if has_star:
            s = s[1:] # 分离开头的 star
        return SimpleTerm.init(s, has_star)

    @classmethod
    def from_json_obj(cls, json_obj:dict) -> 'SimpleTerm':
        if json_obj.get("type") != "SimpleTerm":
            raise TypeError()
        if not isinstance(json_obj.get("content"), str):
            raise TypeError()
        if not isinstance(json_obj.get("has_star"), bool):
            raise TypeError()
        return SimpleTerm.init(
            json_obj["content"], json_obj["has_star"])
    
    # 由下划线和大写字母、数字构成，且至少包含一个大写字母或者数字
    # 这样的元素强制匹配，不能当变量名
    @classmethod
    def is_upper(cls, s:str) -> bool:
        cnt_cap = 0
        for c in s:
            if c in string.ascii_uppercase or c in string.digits:
                cnt_cap += 1
            elif c != "_":
                if c not in string.ascii_lowercase and c != "*":
                    raise AssertionError()
                return False
        return cnt_cap >= 1

if __name__ == "__main__":
    term = SimpleTerm.init("hello", False)
    print(term.serialize())
    print(term.json_obj())
    print(SimpleTerm.deserialize(term.serialize()).json_obj())
