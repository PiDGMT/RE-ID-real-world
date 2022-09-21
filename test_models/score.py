"""
Calculates scores with which to evaluate the model
"""

def true_target_rate(Nt2t, Nt):
    """
    True Target Rate

    Nt2t: the number of correctly verified gallery sets of probe people
    Nt: number of gallery sets from target people
    """
    return Nt2t / Nt

def false_target_rate(Nnt2t, Nnt):
    """
    False Target Rate

    Nn2t: number of gallery sets of non-targets but verified as probe people
    Nnt: number of gallery sets from non-target people

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
