########################################
# Standard ANN example written in PYTHON
########################################

import numpy as np
###########################
# ACTIVATION FUNCTIONS
###########################

# sigmoid function
def sigmoid(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

# gaussian function
def gaussian(x, deriv=False):
    if(deriv==True):
        return -2*x*np.exp(-x**2)
    return np.exp(-x**2)

# binary step function
def binary_step(x,deriv=False):
    if(deriv==True):
        return np.array([[1 if z == 0 else 0 for z in y] for y in x])
    return np.array([[0 if z < 0 else 1 for z in y] for y in x])

###########################
# DEFINE ANN AND IO
###########################

for i in range(3):
    # input dataset converges
    X = np.array([[0,0,1],[1,1,1],[1,0,1],[0,1,1]])
    # input dataset fails to coverge
    #X = np.array([[0,0,1],[0,1,1],[1,0,1],[1,1,1]])
    # output dataset
    y = np.array([[0,1,1,0]]).T

    ###########################
    # INTIALISE AND SEED ANN
    ###########################

    np.random.seed(1)

    # initialize weights randomly with mean 0
    syn0 = 2*np.random.random((3,1)) - 1

    ############################
    # SEEK CONVERGENCE (TRAIN)
    ############################

    for iter in range(1000):
        # forward propagation
        l0 = X
        l1 = [sigmoid(np.dot(l0,syn0)),
              gaussian(np.dot(l0,syn0)),
              binary_step(np.dot(l0,syn0))][i]
        
        # how much did we miss?
        l1_error = y - l1
        
        # multiply how much we missed by the
        # slope of the activation function at the values in l1
        l1_delta = l1_error * [sigmoid(l1,True),
                               gaussian(l1,True),
                               binary_step(l1,True)][i]
        
        # update weights
        syn0 += np.dot(l0.T,l1_delta)

    ###########################
    # REPORT RESULTS
    ###########################

    print (["sigmoid", "gaussian", "binary_step"][i])
    print ("Output After Training:")
    print (l1)
    print ()

