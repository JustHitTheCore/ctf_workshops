from decimal import *
from math import ceil, floor, log
from subprocess import PIPE, Popen


if __name__ == "__main__":
    """
    http://secgroup.dais.unive.it/wp-content/uploads/2012/11/Practical-Padding-Oracle-Attacks-on-RSA.html
    """

    
    n = 120357855677795403326899325832599223460081551820351966764960386843755808156627131345464795713923271678835256422889567749230248389850643801263972231981347496433824450373318688699355320061986161918732508402417281836789242987168090513784426195519707785324458125521673657185406738054328228404365636320530340758959
    e = 65537

    c = 2201077887205099886799419505257984908140690335465327695978150425602737431754769971309809434546937184700758848191008699273369652758836177602723960420562062515168299835193154932988833308912059796574355781073624762083196012981428684386588839182461902362533633141657081892129830969230482783192049720588548332813
    
    enctwo = pow(2, e, n)

    lb = Decimal(0)
    ub = Decimal(n)

    k = int(ceil(log(n, 2)))  # n. of iterations
    getcontext().prec = k     # allows for 'precise enough' floats

    p = Popen(["F:\ida_re\lsb_oracle.vmp.exe", "/decrypt"], stdin=PIPE, stdout=PIPE, bufsize=1)

    for i in range(1, k + 1):
        c = (c * enctwo) % n  # Adapting c...
        
        nb = (lb + ub) / 2
        
        print p.stdout.readline()
        print >>p.stdin, str(c)
        p.stdin.flush()
        parity = int(p.stdout.readline())
        
        if not parity:
            ub = nb
        else:
            lb = nb

        print("{:>4}: [{}, {}]".format(i, int(lb), int(ub)))
