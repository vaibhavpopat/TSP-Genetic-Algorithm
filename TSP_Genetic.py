import random


# Function that provides the evaluation value for each state
def fitness_function(path,cost_matrix,N):
    cost=0
    for i in range(1,N):
        cost+=cost_matrix[path[i-1]][path[i]]
    cost+=cost_matrix[path[N-1]][path[0]]
    return(1/cost)


# Driver Code
if __name__ == '__main__':

    with open("input.txt",'r') as f:
        lines = f.readlines()
        
    N = int(lines[0])               # Input number of cities
    cost_matrix = [[int(x) for x in line.split()] for line in lines[1:]]        # Cost between different cities stored

    k=50                            # Defining the population size
    maxvalue=-1                     # Initialized maxvalue variable (stores max {1/cost} value)
    generations=5000                # Initializing the number of times we need to repeat evolution

    arr=[[] for i in range(k)]      # Initialized array to store first generation parents
    
    for i in range(0,k):
        for j in range(0,N):
            arr[i].append(j)
        random.shuffle(arr[i])      # Shuffling parent states randomly to get different parents

    counter=0
    ans=[]                          # Stores minimal cost

    while counter<generations:

        fitness=[]
        fitness_percent=[]
        fitness_sum=0
    
        # Selection of parents for the next operation - crossover

        for i in range(0,k):
            cost=fitness_function(arr[i],cost_matrix,N)
            fitness_sum+=cost
            fitness.append(cost)
            if cost>maxvalue:                       # If greater maxvalue obtained - updates it and optimal path
                maxvalue=cost
                ans=arr[i]
        
        for i in range(0,k):
            fitness_percent.append((fitness[i]/fitness_sum)*100)    #Stores fitness percent value for each parent

        selection=[[] for i in range(k)]
        selection.clear()
        for i in range(0,k):
            rand=random.uniform(0.0,100.0)
            maxl=0
            found=0
            for j in range(0,k):
                if found==0:
                    maxl+=fitness_percent[j]
                    if(rand<=maxl):
                        found=1
                        selection.append(arr[j])    #Selection now contains the parents for next operation - crossover
        

        # Crossover Starts from here
        crossover=[[] for i in range(k)]
        for i in range(0,k,2):
            a1,b1=random.sample(range(0,N),2)
            a=min(a1,b1)
            b=max(a1,b1)
            crossover[i]=selection[i][a:b+1]
            temp = [item for item in selection[i+1] if item not in crossover[i]]
            ptr=0
            for j in range(0,N):
                if(j<a):
                    crossover[i].insert(j,temp[ptr])
                    ptr=ptr+1
                if(j>b):
                    crossover[i].insert(j,temp[ptr])
                    ptr=ptr+1

            a1,b1=random.sample(range(0,N),2)
            a=min(a1,b1)
            b=max(a1,b1)
            crossover[i+1]=selection[i+1][a:b+1]
            temp = [item for item in selection[i] if item not in crossover[i+1]]
            ptr=0
            for j in range(0,N):
                if(j<a):
                    crossover[i+1].insert(j,temp[ptr])
                    ptr=ptr+1
                if(j>b):
                    crossover[i+1].insert(j,temp[ptr])
                    ptr=ptr+1
        # Crossover list now contains parents for next operation - Mutation
        


        # Mutation starts from here
        mutation = crossover
        for i in range(0,k):
            rand=random.randint(0,N-1)
            a,b=random.sample(range(0,N),2)
            
            temp=crossover[i][a]
            mutation[i][a]=crossover[i][b]
            mutation[i][b]=temp

            cost=fitness_function(mutation[i],cost_matrix,N)
            if(cost>maxvalue):                      # If greater maxvalue obtained - updates it and optimal path
                maxvalue=cost       
                ans=mutation[i]
                print("mutation")

        arr=mutation            # The mutated state of parents form the next generation selection parents
        print("Generation " + str(counter) + " ends -------------------- Min Cost ",1/maxvalue," Path ",ans)
        counter=counter+1
