# emslade23's Video Assignment

Run the example code on: https://stackoverflow.com/questions/3044580/multiprocessing-vs-threading-python

- running: python3 threadsVprocess.py 10
(10 being the number of iterations)

        nthreads CpuThread CpuProcess IoThread IoProcess
        1.000000e+00 3.359318e-04 2.189016e-02 1.003167e+00 1.008976e+00
        2.000000e+00 9.989738e-04 9.231806e-03 1.005150e+00 1.009247e+00
        3.000000e+00 1.423120e-03 1.195335e-02 1.007330e+00 1.013715e+00
        4.000000e+00 1.843929e-03 1.476407e-02 1.003240e+00 1.016916e+00
        5.000000e+00 2.140045e-03 1.893687e-02 1.004509e+00 1.020476e+00
        6.000000e+00 2.423048e-03 2.284694e-02 1.003871e+00 1.020572e+00
        7.000000e+00 1.770020e-03 1.690698e-02 1.002155e+00 1.022617e+00 

## Conclusions:

### Multiprocessing

    - higher overhead
    - used for tasks that require high CPU computational resources
    - avoids GIL limitations in CPython
    - takes advantage of multiple CPUs and cores

### Multi-threading

    - Used for Input/Output tasks
    - make responsive UIs
    - light weight
    - shared memory
