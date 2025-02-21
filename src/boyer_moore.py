def get_shift_match_table(P):
    m = len(P)
    shift_match_table = {}

    for shift in range(m - 1, 0, -1):
        p_1 = m - 1
        p_2 = m - shift - 1

        while p_2 >= 0:
            if P[p_2] == P[p_1]:
                p_1 -= 1
                p_2 -= 1
                if p_2 < 0:
                    shift_match_table[shift] = m - shift
                    break
            else:
                shift_match_table[shift] = m - shift - p_2 - 1
                break
    shift_match_table[m] = 0
    return shift_match_table

def get_good_suffix_table(P):
    m = len(P)

    good_suffix_table = {}
    good_suffix_table[0] = 1

    shift_match_table = get_shift_match_table(P)

    for i in range(1, m + 1):
        good_suffix_table[i] = i + m

    for i in range(m, 0, -1):
        if shift_match_table[i] > 0:
            good_suffix_table[shift_match_table[i]] = i + shift_match_table[i]

    for i in range(m, 0, -1):
        if shift_match_table[i] + i == m:
            for j in range(shift_match_table[i] + 1, m+1):
                good_suffix_table[j] = min(good_suffix_table[j], j + i)
    return good_suffix_table

def get_bad_char_table(P):
    # bad_char_table = {'A':None, 'C':None, 'T':None, 'G':None}
    bad_char_table = {}

    for i in range(len(P)):
        bad_char_table[P[i]] = i

    return bad_char_table

def boyer_moore_search(T, P):
    occurrences = []
    
    n = len(T)
    m = len(P)
    if m == 0 or m > n:
        return []
    
    bc = get_bad_char_table(P)
    gs = get_good_suffix_table(P)

    shift = 0

    while shift <= n-m:

        # last index of P
        i = m - 1

        while i >= 0 and P[i] == T[shift+i]:
            i -= 1
        
        # Occurrence found
        if i < 0:
            occurrences.append(shift)
            shift += gs[0]
        else:
            if T[shift+i] not in bc:
                bc[T[shift+i]] = -1

            bc_shift = i - bc[ T[shift + i] ]

            if i < m - 1:
                gs_shift = gs[i] - m
            else:
                gs_shift = 1

            shift += max(1, gs_shift, bc_shift)

    return occurrences
