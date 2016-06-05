from niprov.dependencies import Dependencies


class Camera(object):

    def __init__(self, dependencies):
        self.film = dependencies.getPictureCache()
        self.libs = dependencies.getLibraries()

    def saveSnapshot(self, data, for_):
        """Plot an overview of the image and store it.

        Uses :class:`.PictureCache` as service that provides a file-like 
                handle to save the plotted picture to.
        Calls takeSnapshot() to do the actual plotting.

        Args:
            data (numpy.ndarray): Array of 2, 3 or 4 dimensions with image data.
        """
        newPicture = self.film.new()
        success = self.takeSnapshot(data, on=newPicture)
        if success:
            self.film.keep(newPicture, for_)

    def takeSnapshot(self, data, on):
        """Plot an overview of the image using matplotlib.pyplot.

        Args:
            data (numpy.ndarray): Array of 2, 3 or 4 dimensions with image data.
            on (str or file-like object): Where to save figure to.
        """
        if not self.libs.hasDependency('pyplot'):
            return False
        plt = self.libs.pyplot

        try:
            ndims = len(data.shape)
            sliceOrder = [1, 0, 2]
            fig, axs = plt.subplots(nrows=1, ncols=ndims, figsize=(8, 3), dpi=100)
            for d in range(ndims):
                slicing = [slice(None)]*ndims
                slicing[sliceOrder[d]] = int(data.shape[d]/2)
                axs[d].matshow(data[slicing].T, origin='lower', 
                    cmap = plt.get_cmap('gray'), vmin = 0, vmax = data.max())
                axs[d].locator_params(nbins=3)
                axs[d].tick_params(axis='both', which='major', labelsize=8)
            plt.tight_layout()
            plt.savefig(on)
        except Exception as e:
            return False
        return True
