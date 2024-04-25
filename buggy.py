import xtrack as xt
line = xt.Line.from_json('buggy.json')
print(line.get_length())
for i, (s1, s2) in enumerate(zip(line.metadata['s_insertions'], line.metadata['s_end'])):
    line.insert_element(name=f'insertion_{i}', element=xt.Drift(length=s2-s1), at_s=s1)
    print(line.get_length())

