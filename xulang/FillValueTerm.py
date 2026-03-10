try:
    from .Sequence import Sequence
    from .BraceSequence import BraceSequence
    from .ValueTerm import ValueTerm
    from .SimpleTerm import SimpleTerm
except:
    from Sequence import Sequence
    from BraceSequence import BraceSequence
    from ValueTerm import ValueTerm
    from SimpleTerm import SimpleTerm

def fill_value_term(right:ValueTerm, dic:dict[str, Sequence]) -> ValueTerm:
    if not isinstance(right, ValueTerm):
        raise TypeError()
    if isinstance(right.value, Sequence):
        new_item = ValueTerm()
        new_item.value = fill_sequence(right.value, dic)
        return new_item
    else:
        if not isinstance(right.value, BraceSequence):
            raise TypeError()
        new_item = ValueTerm()
        new_item.value = fill_brace_sequence(right.value, dic) # type:ignore
        return new_item

def fill_sequence(sequence:Sequence, dic:dict[str, Sequence]) -> Sequence:
    object_list = []
    for term in sequence.objects:
        if isinstance(term, SimpleTerm):
            
            # 遇到变量
            if not SimpleTerm.is_const_val(term.serialize()):
                if dic.get(term.serialize()) is None:
                    raise NameError()
                
                # 追加序列
                object_list += (dic[term.serialize()].objects)

            # 遇到常量
            else:
                object_list.append(term)
        else:
            if not isinstance(term, BraceSequence):
                raise TypeError()
            
            object_list.append(
                fill_brace_sequence(term, dic))
            
    new_item = Sequence.init(object_list)
    return new_item

def fill_brace_sequence(brace_sequence:BraceSequence, dic:dict[str, Sequence]) -> BraceSequence:
    return BraceSequence.init(
        fill_sequence(brace_sequence.inner_sequence, dic))

if __name__ == "__main__":
    print(
        fill_value_term(ValueTerm.init(
            Sequence.deserialize("(a (b A) c)")),
            {
                "a": Sequence.deserialize("A B"),
                "b": Sequence.deserialize(""),
                "c": Sequence.deserialize("(E F) G")
            }).serialize()
    )
