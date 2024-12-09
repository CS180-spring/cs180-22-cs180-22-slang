def editDistance(search, result, m, n):
    if m == 0:
        return n
    
    if n == 0:
        return m
    
    if search[m-1] == result[n-1]:
        return editDistance(search, result, m-1, n-1)
    
    return 1 + min(editDistance(search, result, m, n-1), editDistance(search, result, m-1, n), editDistance(search, result, m-1, n-1))