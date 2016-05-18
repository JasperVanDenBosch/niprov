from niprov.dependencies import Dependencies
import webbrowser

def view(img, dependencies=Dependencies()):
    libs = dependencies.getLibraries()
    plt = libs.pyplot
    plt.ion()
    plt.plot(range(10))
    fname = 'myplot.png'
    plt.savefig(fname)
    webbrowser.open(fname)
