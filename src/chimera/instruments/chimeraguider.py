import threading
import os

import numpy as np

try:
    from astropy.io import fits
except:
    import pyfits as fits

from chimera.core.chimeraobject import ChimeraObject
from chimera.core.lock import lock
from chimera.core.event import event

from chimera.interfaces.guider import Guider

from chimera.instruments.telescope import TelescopeBase
from chimera.instruments.filterwheel import FilterWheelBase

from chimera.util.filenamesequence import FilenameSequence


class ChimeraGuider(Guider):
    def __init__(self):
        ChimeraObject.__init__(self)

    def __start__(self):
        """
        Initialization stuff for the guider:

        """
        pass

    def getTelescope(self):
        """
        Get the telescope we are guiding either from the __config__
        or from the running Manager, if needed. The latter should
        take precedence if different from the former (possible?).
        """
        pass


    def correctTelPos(self, pos):
        """
        Send direction and distance (in arcseconds?) to the telescope
        for correction, if the guiding algorithm does not deliver them
        directly (hence this method might prove unnecessary, except for
        decoupling).
        @param pos: list of tuples (dir, dist); e.g.:
        [('S', 1.2), ('E', 0.4)]
        Constraints:
        - At most 2 elements in the list;
        - Cannot have opposing cardinals: N-S, or E-W, in the same list.
        Hint: use the SlewRate.GUIDE Enum
        """
        pass

    def getCorrections(self, img):
        """
        We implement a SIMPLE, lightweight, guiding technique; for the purpose of
        keeping the scope aligned with the target, we don't need astrometry, photometry,
        nor field ID and WCS. We only need a clear point source of photons...
        """
        # Assume the data is in the primary header unit.
        # NOTE: need to hook an event here to know when the image is updated.

        gdrarray = fits.getdata(img)
        bg = np.nanmean(img)

        # Get the brightest candidate guiding source.

        trans = np.array(
            [[i, np.argmax(self.gdrarray[i]), np.nanmax(gdrarray[i])] for i in range(0, gdrarray.shape[1])],
            dtype='float32')

        # Coords and value of the highest pixel value
        ctr = trans[np.argmax(trans[0:1023, 2])]

        # Finally, the guiding box is:
        gbox = gdarray[ctr[0] - 5:ctr[0] + 5, ctr[1] - 5:ctr[1] + 5]

        n = fits.PrimaryHDU(gbox)
        nunits = fits.HDUList(n)
        nunits.writeto(os.path.join(self['gdrimagesdir'], "box.fits"))