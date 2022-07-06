lst = [(0,22), (23,61), (1000,3721)]


def searchProblem(self,lst):
    isValid = False
    init_problem = -1
    final_problem = -1
    for i in range(3722):
        isValid = False
        for t in lst:
            if i - t[0] >= 0 and i - t[1] <= 0:
                isValid = True
                #print(i,"safe in", t)
                break
        if not isValid and init_problem == -1:
            init_problem = i
        
        if isValid and init_problem != -1:
            final_problem = i-1
            break

    return init_problem, final_problem

se = 0

print(searchProblem(se,lst))