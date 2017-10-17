load("http://garsia.math.yorku.ca/~zabrocki/superpartitions.py")

#wait is this the same thing as in the first file?
#  lets just do a load("The first Pieri rule") so that we aren't editing two copies of the same thing
# which is the add_horizontal_super_border_strip?

def add_horizonal_border_strip(sp, h):
    r"""
    a list of super partitions that differ from ``self`` by a horizontal strip
    
    INPUT:
    - ``sp`` -- a super partition
    - ``h`` -- number of addition cells 

    OUPUT:

    - a list of super partitions
    
    EXAMPLES::

        sage: add_horizonal_border_strip([[4,1],[3]], 3)
        [[4, 1; 3, 3],
         [4, 1; 4, 2],
         [3, 1; 5, 2],
         [4, 1; 5, 1],
         [3, 1; 6, 1],
         [4, 0; 4, 3],
         [3, 0; 5, 3],
         [4, 0; 5, 2],
         [3, 0; 6, 2],
         [4, 1; 6],
         [3, 1; 7]]
        sage: add_horizonal_border_strip([[2,1],[3]], 2)
        [[2, 1; 3, 2], [2, 1; 4, 1], [2, 0; 3, 3], [2, 0; 4, 2], [2, 1; 5]]
    """
    (sp1, circ_list) = SuperPartition(sp).to_circled_diagram()
    nsp=[list(la)+[0] for la in sp1.add_horizontal_border_strip(h)]
    sp1= sp1+[0]
    out=[]
    rows_with_circle=[a[0] for a in circ_list]
    for elt in nsp:
        row_changed = [row1-row2 for row1,row2 in zip(elt,sp1)]
        new_sp = [elt,[(i[0]+1,elt[i[0]+1]) for i in circ_list if row_changed[i[0]]!=0]+\
                            [(i) for i in circ_list if row_changed[i[0]]==0]]
        if len(uniq([k for (j,k) in new_sp[1]]))==len(new_sp[1]): 
            out+=[SuperPartition.from_circled_diagram(*new_sp)]
    return out



def locate_cells(first_superpartition):
    r"""
     compares two partitions to find locations of the added cells
     
    
    
    
    INPUT: 
     -``first_superpartition``-- self[0] and superpartition from first rule
     
     
    
     
     OUTPUT: 
     - a list of locations of cells
     
     
     
     
     EXAMPLES::
        sage:([4, 3, 1], [[[4, 3, 3, 1], [(0, 4), (3, 1)]], [[4, 4, 2, 1], [(0, 4), (3, 1)]], etc.]
        [[(2, 2), (2, 1), (3, 0)],[(1, 3), (2, 1), (3, 0)],etc.]
     
    """
    o1,o2=first_superpartition[0],first_superpartition[1]
    cell_location=[[] for i in range(len(o2)) ]
     
    for k in range(len(o2)):

        old_partition,new_partition=o1,o2[k][0]

        for i in range(len(old_partition)):
            if old_partition[i]!=new_partition[i]:
                for j in range(new_partition[i]-old_partition[i]):
                    cell_location[k].append((i,new_partition[i]-j-1))
        if len(new_partition)>len(old_partition):
            for i in range(new_partition[-1]):
                cell_location[k].append((len(new_partition)-1,i))
    return(cell_location)

def second_pieri_rule(self,h):
    r"""
     gives legal locations of the unique circle described in second pieri rule
     
     
     INPUT: 
     
     -``h``-- number of addition cells 
     
     
     OUTPUT:
     
     
     - a list superpartition of legal locations of unique circles
     
    EXAMPLE::
        sage:([4, 3, 1], [[[4, 3, 3, 1], [(0, 4), (3, 1)]], [[4, 4, 2, 1], [(0, 4), (3, 1)]],etc])
        [[-1, [4, 3, 1; 3]],
         [-1, [4, 2, 1; 4]],
         etc.]
    """
    to_diagram = [SuperPartition([la[0],la[1]]).to_circled_diagram() for la in add_horizonal_border_strip(self, h)]
    output_from_last_function = [SuperPartition(self).to_circled_diagram()[0],to_diagram]
    cell_location=locate_cells(output_from_last_function)
    circle_location=[a[1] for a in output_from_last_function[1]]
    partition=[a[0] for a in output_from_last_function[1]]

    legal_unique_circle_locations=[[] for i in range(len(partition)) ]
    for j in range(len(partition)):

        partition[j]=list(partition[j])+[0]
        row_with_cir=[circle_location[j][i][0] for i in(range(len(circle_location[j])))]
        col_with_cir=[circle_location[j][i][1] for i in(range(len(circle_location[j])))]
        col_with_cel=[cell_location[j][i][1] for i in(range(len(cell_location[j])))]
        for col in range(partition[j][0]+1):
            if col not in col_with_cir:
                if col not in col_with_cel:
                    for row in range(len(partition[j])):
                        if row not in row_with_cir:
                            l=list(range(col))
                            if set(l) <= set(col_with_cel):
                                roww=0
                                for i in partition[j]:
                                    if i>col:
                                        roww+=1
                                if roww==0:
                                    legal_unique_circle_locations[j].append((roww,col))
                                else:
                                     if partition[j][roww]<partition[roww-1]:
                                        legal_unique_circle_locations[j].append((roww,col))
    
    for i in range(len(legal_unique_circle_locations)):
        legal_unique_circle_locations[i]=list(set(legal_unique_circle_locations[i]))
    l=[] 
    for i in range(len(legal_unique_circle_locations)):
        if legal_unique_circle_locations[i]!=[]:
            l.append(sign_superpartition([output_from_last_function[1][i],legal_unique_circle_locations[i]]))
    return l


# recommendation : write a function that computes the sign for a single
# then apply this to the list in one line
# [sign_superpartition(x) for x in list_of_things]
def sign_superpartition(x):
    r"""
    determine the sign given by the by the second pieri rule for a list

    INPUT:

    - ``x`` -- a list of circle diagram and circle location converted by the second pieri rule.
    OUTPUT:
    - a list of superpartitions with plus or minus sign

    EXAMPLES::
    
        sage: sign_superpartition([[[4, 3, 3, 1], [(0, 4), (3, 1)]], [(1, 3)]])
        [-1, [4, 3, 1; 3]]

    """
    

    sign_sp=[]
    count_circle = 0
    og = x[0]
    og[1].append(x[1][0]) 
    for j in range(len(og[1])-1):
        if og[1][j][0] > og[1][len(og[1])-1][0]:
            count_circle+=1      
    sign_sp.append((-1)**count_circle)
    sign_sp.append( SuperPartition.from_circled_diagram(og[0],og[1]))   
    return sign_sp

    
#second_pieri_rule([[4,1],[3]],3)
