import numpy as np

binaries3 = ['000', '001', '010', '011', '100', '101', '110','111']
get_bin = lambda x: format(x, 'b').zfill(5)
binaries5 = [get_bin(i) for i in np.arange(2**5)] # get a list of all 5-bit binaries


def postselect(s1,s2,s3, data, measurement_basis, shots):
    counts = np.zeros(2) # empty array. counts[0] stores the number of measured |0> results
    # and counts[1] stores the |1> counts
    
    # data is an array of probabibilities. The first entry data[0] corresponds to the probability of 
    # getting |00000>, the second entry to |00001>, then |00010> and so on...
    
    data *= shots # multiply with the number of experiments to convert probabilities to absolute number of occurances
    
    for i,b in zip(np.arange(len(binaries5)), binaries5):
        # b is the binary string corresponding to an outcome, i.e. the first iteration of the loop it is
        # '00000', then '00001', `00010`,...
        
        # the s1_,s2_, ... are the actual measurement outcomes of the qubits 0 to 4
        s1_ = int(b[0])
        s2_ = int(b[1])
        s3_ = int(b[2])
        s4_ = int(b[3])
        s5_ = int(b[4])
        
        # apply the Pauli correction
        # they depend on the measurement basis:
        # in the x-basis Z^{s_1+s_3} flips (|+> <-> |->) the outcome for s_1 + s_3 odd
        # in the z-basis X^{s_2+s_4} flips the outcomes (|0> <-> |1>) for s_2 + s_4 odd
        # in the y-basis both of above terms flip the outcomes
        
        if (measurement_basis == 'x' or measurement_basis == 'y') and (s1_ + s3_) == 1:
            s5_ = 1 - s5_ # flip roles of |0> and |1>
        if (measurement_basis == 'z' or measurement_basis == 'y') and (s2_ + s4_) == 1:
            s5_ = 1 - s5_
        
        # post select the data, only count it when guess of s1, s2, s3 matches the actual measurement 
        if s1_ == s1 and s2_ == s2 and s3_ == s3:
            counts[s5_] += data[i]
  
    return counts         