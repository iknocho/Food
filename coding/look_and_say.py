from itertools import groupby

def next_term(seq: str) -> str:
    result = ''
    for digit, group in groupby(seq):
        group_list = list(group)       
        count = len(group_list)
        result += str(count) + digit
    return result

def nth_term(n: int) -> str:
    term = '1'
    for _ in range(1, n):
        term = next_term(term)
    return term

def center_two_digits(n: int) -> str:
    if not 4 <= n <= 99:
        raise ValueError('n은 4 이상 99 이하이어야 합니다.')

    term = nth_term(n)           # 최적화된 생성
    mid  = len(term) // 2
    return term[mid-1:mid+1]