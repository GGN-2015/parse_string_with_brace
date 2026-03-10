from typing import Optional

try:
    from .ValueMap import ValueMap
    from .ValueTerm import ValueTerm
    from .MatchBraceSequence import match_brace_sequence
    from .FillValueTerm import fill_value_term
    from .Sequence import Sequence
    from .BraceSequence import BraceSequence
except:
    from ValueMap import ValueMap
    from ValueTerm import ValueTerm
    from MatchBraceSequence import match_brace_sequence
    from FillValueTerm import fill_value_term
    from Sequence import Sequence
    from BraceSequence import BraceSequence

class RuleSet:
    def __init__(self) -> None:
        self.value_map_list = []
        self.latest_used_rule:Optional[ValueMap] = None
    
    def add_rule(self, value_map: ValueMap): # 新增规则
        if not isinstance(value_map, ValueMap):
            raise TypeError()
        self.value_map_list.append(value_map)

    # 执行一次所有简单规则
    def execute_simple_rules(self, value_term:ValueTerm) -> tuple[bool, ValueTerm]:
        if not isinstance(value_term.value, BraceSequence):
            return False, value_term
    
        for value_map in self.value_map_list:

            # 检查是否还能替换
            if isinstance(value_term.value, Sequence):
                break

            assert isinstance(value_map.left, BraceSequence)
            if value_map.left.has_sub_brace(): # 跳过复杂规则
                continue

            dic = dict()
            flag = match_brace_sequence(
                value_map.left, value_term.value, dic)
            
            if flag:
                value_term = fill_value_term(
                    value_map.right, dic
                )
                self.latest_used_rule = value_map
                return True, value_term

        # 返回最终结果
        return False, value_term

    def try_match_sons(self, value_term:ValueTerm) -> tuple[bool, ValueTerm]:
        if isinstance(value_term.value, BraceSequence):
            sub_obj_list = value_term.value.inner_sequence.objects
            value_type = BraceSequence
        else:
            sub_obj_list = value_term.value.objects
            value_type = Sequence

        suc = False
        new_sub_obj_list = []
        for i in range(len(sub_obj_list)):
            if type(sub_obj_list[i]) not in [BraceSequence, Sequence] or suc:
                new_sub_obj_list.append(sub_obj_list[i])
                continue
            flag, new_obj = self.calc(ValueTerm.init(sub_obj_list[i]))

            if isinstance(new_obj.value, BraceSequence):
                new_sub_obj_list.append(new_obj.value)
            else:
                assert isinstance(new_obj.value, Sequence)
                new_sub_obj_list += new_obj.value.objects # 追加模式

            if flag:
                suc = True # 至少进行了一次替换

        if value_type is BraceSequence:
            return suc, ValueTerm.init(BraceSequence.init(
                Sequence.init(new_sub_obj_list)
            ))
        else:
            return suc, ValueTerm.init(
                Sequence.init(new_sub_obj_list)
            )

    # 使用当前规则集合进行必要的计算
    def calc(self, value_term:ValueTerm) -> tuple[bool, ValueTerm]:

        if type(value_term.value) not in [Sequence, BraceSequence]:
            raise TypeError()

        # 先考虑外层是括号的情况
        if isinstance(value_term.value, BraceSequence):
            
            # 先枚举无嵌套规则并执行
            # 此时当前层已经不再能执行
            flag, value_term = self.execute_simple_rules(value_term)
            if flag:
                return True, value_term

            # 试图递归对所有成员执行算法
            flag, value_term = self.try_match_sons(value_term)
            if flag:
                return True, value_term
            
            # 试图对当前层进行复杂规则替换
            for value_map in self.value_map_list:
                assert isinstance(value_map, ValueMap)
                assert isinstance(value_term.value, BraceSequence)

                if value_map.left.has_sub_brace(): # 复杂规则
                    dic = dict()
                    flag = match_brace_sequence(
                        value_map.left, value_term.value, dic)
                    
                    if flag:
                        value_term = fill_value_term(value_map.right, dic)
                        self.latest_used_rule = value_map
                        return True, value_term
            
            return False, value_term
        
        else:

            # 直接对子元素进行递归即可
            if not isinstance(value_term.value, Sequence):
                raise AssertionError()
            
            # 试图递归对所有成员执行算法
            flag, value_term = self.try_match_sons(value_term)
            if flag:
                return True, value_term

            return False, value_term

if __name__ == "__main__":
    rule_set = RuleSet()
    rule_set.add_rule(ValueMap.deserialize("""
        (IF TRUE a b) => a"""))
    rule_set.add_rule(ValueMap.deserialize("""
        (IF FALSE a b) => b"""))
    rule_set.add_rule(ValueMap.deserialize("""
        (HEAD ()) => """))
    rule_set.add_rule(ValueMap.deserialize("""
        (HEAD (a *b)) => a"""))
    rule_set.add_rule(ValueMap.deserialize("""
        (REV ()) => ()"""))    
    rule_set.add_rule(ValueMap.deserialize("""
        (REV (a)) => (a)"""))
    rule_set.add_rule(ValueMap.deserialize("""
        (REV (a *b)) => (MERGE (REV (*b)) (a))"""))
    rule_set.add_rule(ValueMap.deserialize("""
        (MERGE (*a) (*b)) => (*a *b)"""))
    rule_set.add_rule(ValueMap.deserialize("""
        (TAIL (*a)) => (HEAD (REV (*a)))"""))
    
    for value_term_str in [
        "(IF TRUE 1 (TAIL (A B C D E)))",
        "(IF FALSE X (TAIL (A B C D E)))"
    ]:
        print("=" * 40)
        value_term = ValueTerm.deserialize(f"[{value_term_str}]")
        
        print(value_term.serialize()[1:-1])
        while True:
            flag, value_term = rule_set.calc(value_term)
            if flag == False:
                break
            if rule_set.latest_used_rule is not None:
                print("\nRULE:", rule_set.latest_used_rule.serialize())
            print("OUTP:", value_term.serialize()[1:-1])
