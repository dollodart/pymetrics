def lcs_length(x,y):
    """See CLRS section 15.4"""
    m = len(x) 
    n = len(y)
    c = [[0]*n]*m
    for i in range(1, m):
        c[i][0] = 0
    for j in range(n):
        c[0][j] = 0

    for i in range(1, m):
        for j in range(1, n):
            if x[i] == y[j]:
                c[i][j] = c[i-1][j-1] + 1
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
            else:
                c[i][j] = c[i][j-1]
    return c[m-1][n-1]

# test case
if __name__ == '__main__':
    l = lcs_length('bdcaba', 'abcdbdab')
    print(l)

