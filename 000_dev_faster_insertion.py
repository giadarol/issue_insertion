import xtrack as xt
import numpy as np

line = xt.Line.from_json('buggy.json')
print(line.get_length())
s_insert = np.array(line.metadata['s_insertions'])
l_insert = np.array(line.metadata['s_end']) - s_insert

ele_insert = [xt.Drift(length=l) for l in l_insert]
name_insert = [f'insertion_{i}' for i in range(len(s_insert))]

end_insert = np.array(s_insert) + np.array(l_insert)

line.cut_at_s(list(s_insert) + list(end_insert))

i_sorted = np.argsort(s_insert)
s_insert_sorted = s_insert[i_sorted]
ele_insert_sorted = [ele_insert[i] for i in i_sorted]
name_insert_sorted = [name_insert[i] for i in i_sorted]
end_insert_sorted = end_insert[i_sorted]

assert np.all(s_insert_sorted[:-1] < end_insert_sorted[1:]), (
              'Overlapping insertions')

old_element_names = line.element_names

s_tol = 1e-6

s_vect_upstream = np.array(line.get_s_position(mode='upstream'))

i_replace = np.zeros(len(s_vect_upstream), dtype=int)
mask_remove = np.zeros(len(s_vect_upstream), dtype=bool)

i_replace[:] = -1

for ii in range(len(s_insert_sorted)):
    ss_start = s_insert_sorted[ii]
    ss_end = end_insert_sorted[ii]

    i_first_removal = np.where(np.abs(s_vect_upstream - ss_start) < s_tol)[0][-1]
    i_last_removal = np.where(np.abs(s_vect_upstream - ss_end) < s_tol)[0][0] - 1

    i_replace[i_first_removal] = ii
    mask_remove[i_first_removal+1:i_last_removal+1] = True

new_element_names = []
for ii, nn in enumerate(old_element_names):
    if mask_remove[ii]:
        continue
    if i_replace[ii] != -1:
        new_element_names.append(name_insert_sorted[i_replace[ii]])
    else:
        new_element_names.append(nn)

for new_nn, new_ee in zip(name_insert_sorted, ele_insert_sorted):
    line.element_dict[new_nn] = new_ee

line.element_names = new_element_names

# for i, (s1, s2) in enumerate(zip(line.metadata['s_insertions'], line.metadata['s_end'])):
#     line.insert_element(name=f'insertion_{i}', element=xt.Drift(length=s2-s1), at_s=s1)
#     print(line.get_length())

