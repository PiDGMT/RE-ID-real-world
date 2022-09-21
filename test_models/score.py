"""
Calculates scores with which to evaluate the model
"""

def true_target_rate(Nt2t, Nt):
    """
    True Target Rate

    Nt2t: the number of correctly verified probe sets of target people
    Nt: number of probe sets from target people
    """
    return Nt2t / Nt

def false_target_rate(Nnt2t, Nnt):
    """
    False Target Rate

    Nn2t: number of probe sets of non-targets but verified as target people
    Nnt: number of probe sets from non-target people

    """
    return Nnt2t / Nnt

#TODO: Figure out below
def roc():
    """
    Obtain various FDR/TTR combinations by varying theta
    """
    pass

def mAP():
    """
    Evaluate the holistic ranking performance

    For each probe
    """
    pass
