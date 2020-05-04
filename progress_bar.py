"""Modulo responsavel por imprimir uma barra de progresso no console"""

def printProgressBar (iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """Call in a loop to create terminal progress bar"""

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()
