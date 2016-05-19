from niprov.dependencies import Dependencies
import webbrowser


class Polaroid(object):

    def __init__(self, dependencies):
        pass

    def view(img, dependencies=Dependencies()):
        libs = dependencies.getLibraries()
        plt = libs.pyplot
        nibabel = libs.nibabel
        data = nibabel.load(img.path).get_data()

        ## 3D
        ndims = len(data.shape)
        sliceOrder = [1, 0, 2]

        fig, axs = plt.subplots(nrows=1, ncols=ndims)

        for d in range(ndims):
            slicing = [slice(None)]*ndims
            slicing[sliceOrder[d]] = int(data.shape[d]/2)
            axs[d].matshow(data[slicing].T, origin='lower', 
                cmap = plt.get_cmap('gray'), vmin = 0, vmax = data.max())
            axs[d].locator_params(nbins=3)
            axs[d].tick_params(axis='both', which='major', labelsize=8)

        plt.tight_layout()

        fname = 'myplot.png'
        plt.savefig(fname)
        webbrowser.open(fname)
