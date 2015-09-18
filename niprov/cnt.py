from struct import unpack
from datetime import datetime, time
from niprov.basefile import BaseFile


class NeuroscanFile(BaseFile):
    """ Support for the Neuroscan .cnt format.
    """

    _datatypes = {'char':1, 'uchar':1, 'long':4,'ulong':4,'short':2,'ushort':2,
        'float':4, 'double':8,'int':4}

    def __init__(self, location, **kwargs):
        super(NeuroscanFile, self).__init__(location, **kwargs)

    def inspect(self):
        provenance = super(NeuroscanFile, self).inspect()
        header = self._read()
        provenance['subject'] = header.patient.translate(None, '\x00')
        nchannels = unpack('H',header.nchannels)[0]
        numsamples = unpack('I',header.numsamples)[0]
        provenance['dimensions'] = [nchannels, numsamples]
        acqstring = (header.date+' '+header.time).translate(None, '\x00')
        dtformat = '%d/%m/%y %H:%M:%S'
        provenance['acquired'] = datetime.strptime(acqstring, dtformat)
        return provenance

    def _fread(self, fhandle, size, dtype):
        """ Read bytes from file at current cursor position.

        Emulates MATLAB fread().
        """
        precision = self._datatypes[dtype]
        nbytes = size*precision
        return fhandle.read(nbytes)
 
    def _read(self):
        """
        Read the Neuroscan CNT file header.

        This code is loosely based on the MATLAB function loadcnt.m by
        Sean Fitzgibbon and Arnaud Delorme which is available under the GPLv2 
        license. Part of the original copyright statement and license are 
        reproduced below (in the source code).
        """
        # Copyright (C) 2000 Sean Fitzgibbon, <psspf@id.psy.flinders.edu.au>
        # Copyright (C) 2003 Arnaud Delorme, Salk Institute, arno@salk.edu
        #
        # This program is free software; you can redistribute it and/or modify
        # it under the terms of the GNU General Public License as published by
        # the Free Software Foundation; either version 2 of the License, or
        # (at your option) any later version.
        #
        # This program is distributed in the hope that it will be useful,
        # but WITHOUT ANY WARRANTY; without even the implied warranty of
        # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        # GNU General Public License for more details.
        #
        # You should have received a copy of the GNU General Public License
        # along with this program; if not, write to the Free Software
        # Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
        #
        # Revision 1.21  2005/08/16 22:46:55  arno
        # allowing to read event type 3
        class CntHeader(object):
            pass
        h = CntHeader()
        with self.filesystem.open(self.path,'rb') as fid:
            h.rev               = self._fread(fid,12,'char')
            h.nextfile          = self._fread(fid,1,'long')
            h.prevfile          = self._fread(fid,1,'ulong')
            h.type              = self._fread(fid,1,'char')
            h.id                = self._fread(fid,20,'char')
            h.oper              = self._fread(fid,20,'char')
            h.doctor            = self._fread(fid,20,'char')
            h.referral          = self._fread(fid,20,'char')
            h.hospital          = self._fread(fid,20,'char')
            h.patient           = self._fread(fid,20,'char')
            h.age               = self._fread(fid,1,'short')
            h.sex               = self._fread(fid,1,'char')
            h.hand              = self._fread(fid,1,'char')
            h.med               = self._fread(fid,20, 'char')
            h.category          = self._fread(fid,20, 'char')
            h.state             = self._fread(fid,20, 'char')
            h.label             = self._fread(fid,20, 'char')
            h.date              = self._fread(fid,10, 'char')
            h.time              = self._fread(fid,12, 'char')
            h.mean_age          = self._fread(fid,1,'float')
            h.stdev             = self._fread(fid,1,'float')
            h.n                 = self._fread(fid,1,'short')
            h.compfile          = self._fread(fid,38,'char')
            h.spectwincomp      = self._fread(fid,1,'float')
            h.meanaccuracy      = self._fread(fid,1,'float')
            h.meanlatency       = self._fread(fid,1,'float')
            h.sortfile          = self._fread(fid,46,'char')
            h.numevents         = self._fread(fid,1,'int')
            h.compoper          = self._fread(fid,1,'char')
            h.avgmode           = self._fread(fid,1,'char')
            h.review            = self._fread(fid,1,'char')
            h.nsweeps           = self._fread(fid,1,'ushort')
            h.compsweeps        = self._fread(fid,1,'ushort')
            h.acceptcnt         = self._fread(fid,1,'ushort')
            h.rejectcnt         = self._fread(fid,1,'ushort')
            h.pnts              = self._fread(fid,1,'ushort')
            h.nchannels         = self._fread(fid,1,'ushort')
            h.avgupdate         = self._fread(fid,1,'ushort')
            h.domain            = self._fread(fid,1,'char')
            h.variance          = self._fread(fid,1,'char')
            h.rate              = self._fread(fid,1,'ushort')
            h.scale             = self._fread(fid,1,'double')
            h.veogcorrect       = self._fread(fid,1,'char')
            h.heogcorrect       = self._fread(fid,1,'char')
            h.aux1correct       = self._fread(fid,1,'char')
            h.aux2correct       = self._fread(fid,1,'char')
            h.veogtrig          = self._fread(fid,1,'float')
            h.heogtrig          = self._fread(fid,1,'float')
            h.aux1trig          = self._fread(fid,1,'float')
            h.aux2trig          = self._fread(fid,1,'float')
            h.heogchnl          = self._fread(fid,1,'short')
            h.veogchnl          = self._fread(fid,1,'short')
            h.aux1chnl          = self._fread(fid,1,'short')
            h.aux2chnl          = self._fread(fid,1,'short')
            h.veogdir           = self._fread(fid,1,'char')
            h.heogdir           = self._fread(fid,1,'char')
            h.aux1dir           = self._fread(fid,1,'char')
            h.aux2dir           = self._fread(fid,1,'char')
            h.veog_n            = self._fread(fid,1,'short')
            h.heog_n            = self._fread(fid,1,'short')
            h.aux1_n            = self._fread(fid,1,'short')
            h.aux2_n            = self._fread(fid,1,'short')
            h.veogmaxcnt        = self._fread(fid,1,'short')
            h.heogmaxcnt        = self._fread(fid,1,'short')
            h.aux1maxcnt        = self._fread(fid,1,'short')
            h.aux2maxcnt        = self._fread(fid,1,'short')
            h.veogmethod        = self._fread(fid,1,'char')
            h.heogmethod        = self._fread(fid,1,'char')
            h.aux1method        = self._fread(fid,1,'char')
            h.aux2method        = self._fread(fid,1,'char')
            h.ampsensitivity    = self._fread(fid,1,'float')
            h.lowpass           = self._fread(fid,1,'char')
            h.highpass          = self._fread(fid,1,'char')
            h.notch             = self._fread(fid,1,'char')
            h.autoclipadd       = self._fread(fid,1,'char')
            h.baseline          = self._fread(fid,1,'char')
            h.offstart          = self._fread(fid,1,'float')
            h.offstop           = self._fread(fid,1,'float')
            h.reject            = self._fread(fid,1,'char')
            h.rejstart          = self._fread(fid,1,'float')
            h.rejstop           = self._fread(fid,1,'float')
            h.rejmin            = self._fread(fid,1,'float')
            h.rejmax            = self._fread(fid,1,'float')
            h.trigtype          = self._fread(fid,1,'char')
            h.trigval           = self._fread(fid,1,'float')
            h.trigchnl          = self._fread(fid,1,'char')
            h.trigmask          = self._fread(fid,1,'short')
            h.trigisi           = self._fread(fid,1,'float')
            h.trigmin           = self._fread(fid,1,'float')
            h.trigmax           = self._fread(fid,1,'float')
            h.trigdir           = self._fread(fid,1,'char')
            h.autoscale         = self._fread(fid,1,'char')
            h.n2                = self._fread(fid,1,'short')
            h.dir               = self._fread(fid,1,'char')
            h.dispmin           = self._fread(fid,1,'float')
            h.dispmax           = self._fread(fid,1,'float')
            h.xmin              = self._fread(fid,1,'float')
            h.xmax              = self._fread(fid,1,'float')
            h.automin           = self._fread(fid,1,'float')
            h.automax           = self._fread(fid,1,'float')
            h.zmin              = self._fread(fid,1,'float')
            h.zmax              = self._fread(fid,1,'float')
            h.lowcut            = self._fread(fid,1,'float')
            h.highcut           = self._fread(fid,1,'float')
            h.common            = self._fread(fid,1,'char')
            h.savemode          = self._fread(fid,1,'char')
            h.manmode           = self._fread(fid,1,'char')
            h.ref               = self._fread(fid,10,'char')
            h.rectify           = self._fread(fid,1,'char')
            h.displayxmin       = self._fread(fid,1,'float')
            h.displayxmax       = self._fread(fid,1,'float')
            h.phase             = self._fread(fid,1,'char')
            h.screen            = self._fread(fid,16,'char')
            h.calmode           = self._fread(fid,1,'short')
            h.calmethod         = self._fread(fid,1,'short')
            h.calupdate         = self._fread(fid,1,'short')
            h.calbaseline       = self._fread(fid,1,'short')
            h.calsweeps         = self._fread(fid,1,'short')
            h.calattenuator     = self._fread(fid,1,'float')
            h.calpulsevolt      = self._fread(fid,1,'float')
            h.calpulsestart     = self._fread(fid,1,'float')
            h.calpulsestop      = self._fread(fid,1,'float')
            h.calfreq           = self._fread(fid,1,'float')
            h.taskfile          = self._fread(fid,34,'char')
            h.seqfile           = self._fread(fid,34,'char')
            h.spectmethod       = self._fread(fid,1,'char')
            h.spectscaling      = self._fread(fid,1,'char')
            h.spectwindow       = self._fread(fid,1,'char')
            h.spectwinlength    = self._fread(fid,1,'float')
            h.spectorder        = self._fread(fid,1,'char')
            h.notchfilter       = self._fread(fid,1,'char')
            h.headgain          = self._fread(fid,1,'short')
            h.additionalfiles   = self._fread(fid,1,'int')
            h.unused            = self._fread(fid,5,'char')
            h.fspstopmethod     = self._fread(fid,1,'short')
            h.fspstopmode       = self._fread(fid,1,'short')
            h.fspfvalue         = self._fread(fid,1,'float')
            h.fsppoint          = self._fread(fid,1,'short')
            h.fspblocksize      = self._fread(fid,1,'short')
            h.fspp1             = self._fread(fid,1,'ushort')
            h.fspp2             = self._fread(fid,1,'ushort')
            h.fspalpha          = self._fread(fid,1,'float')
            h.fspnoise          = self._fread(fid,1,'float')
            h.fspv1             = self._fread(fid,1,'short')
            h.montage           = self._fread(fid,40,'char')
            h.eventfile         = self._fread(fid,40,'char')
            h.fratio            = self._fread(fid,1,'float')
            h.minor_rev         = self._fread(fid,1,'char')
            h.eegupdate         = self._fread(fid,1,'short')
            h.compressed        = self._fread(fid,1,'char')
            h.xscale            = self._fread(fid,1,'float')
            h.yscale            = self._fread(fid,1,'float')
            h.xsize             = self._fread(fid,1,'float')
            h.ysize             = self._fread(fid,1,'float')
            h.acmode            = self._fread(fid,1,'char')
            h.commonchnl        = self._fread(fid,1,'uchar')
            h.xtics             = self._fread(fid,1,'char')
            h.xrange            = self._fread(fid,1,'char')
            h.ytics             = self._fread(fid,1,'char')
            h.yrange            = self._fread(fid,1,'char')
            h.xscalevalue       = self._fread(fid,1,'float')
            h.xscaleinterval    = self._fread(fid,1,'float')
            h.yscalevalue       = self._fread(fid,1,'float')
            h.yscaleinterval    = self._fread(fid,1,'float')
            h.scaletoolx1       = self._fread(fid,1,'float')
            h.scaletooly1       = self._fread(fid,1,'float')
            h.scaletoolx2       = self._fread(fid,1,'float')
            h.scaletooly2       = self._fread(fid,1,'float')
            h.port              = self._fread(fid,1,'short')
            h.numsamples        = self._fread(fid,1,'ulong')
            h.filterflag        = self._fread(fid,1,'char')
            h.lowcutoff         = self._fread(fid,1,'float')
            h.lowpoles          = self._fread(fid,1,'short')
            h.highcutoff        = self._fread(fid,1,'float')
            h.highpoles         = self._fread(fid,1,'short')
            h.filtertype        = self._fread(fid,1,'char')
            h.filterdomain      = self._fread(fid,1,'char')
            h.snrflag           = self._fread(fid,1,'char')
            h.coherenceflag     = self._fread(fid,1,'char')
            h.continuoustype    = self._fread(fid,1,'char')
            h.eventtablepos     = self._fread(fid,1,'ulong')
            h.continuousseconds = self._fread(fid,1,'float')
            h.channeloffset     = self._fread(fid,1,'long')
            h.autocorrectflag   = self._fread(fid,1,'char')
            h.dcthreshold       = self._fread(fid,1,'uchar')
        return h



