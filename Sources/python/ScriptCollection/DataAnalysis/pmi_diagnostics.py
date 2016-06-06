#!/usr/bin/python2.6

import sys
import os
import commands

import datetime
import time

import string
import copy

import shelve
import cPickle
import h5py

import select
import numpy
import scipy.interpolate

import scipy

import matplotlib
matplotlib.use('Agg')
import pylab

#try:
#    import plot_disp
#except:
#    print 'plot_disp not loaded.'


global g_s2e_setup

##############################################################################


def f_hdf5_simple_read( a_file , a_dataset ) :
    xfp  = h5py.File( a_file , "r" )
    xxx = xfp.get( a_dataset ).value
    xfp.close()
    return xxx


##############################################################################


def f_load_snp_content( a_fp , a_snp ) :
    global g_s2e_setup
    dbase_root = "/data/snp_" + str( a_snp ).zfill(g_s2e_setup['num_digits']) + "/"
    xsnp = dict()
    xsnp['Z']   = a_fp.get( dbase_root + 'Z' )   .value
    xsnp['T']   = a_fp.get( dbase_root + 'T' )   .value
    xsnp['ff']  = a_fp.get( dbase_root + 'ff' )  .value
    xsnp['xyz'] = a_fp.get( dbase_root + 'xyz' ) .value
    xsnp['r']   = a_fp.get( dbase_root + 'r' )   .value
    xsnp['Nph']   = a_fp.get( dbase_root + 'Nph' )   .value
    N = xsnp['Z'].size
    xsnp['q'] = numpy.array( [ xsnp['ff'][ pylab.find( xsnp['T'] == x ) , 0 ]  for x in xsnp['xyz'] ] ) .reshape(N,)
    xsnp['snp'] = a_snp ;

    return xsnp


##############################################################################


def f_load_snp( a_real , a_snp ) :
    global g_s2e_setup
    xfp  = h5py.File( g_s2e_setup['prj'] + '/pmi/pmi_out_' + str( a_real ).zfill(g_s2e_setup['num_digits'])  + '.h5' , "r" )
    xsnp = f_load_snp_content( xfp , a_snp )
    xfp.close()
    return xsnp


##############################################################################


def f_load_sample( ) :
    global g_s2e_setup
    sample = dict()

    xfp = h5py.File( g_s2e_setup['prj'] + '/sample/sample.h5' , "r" )
    xxx = xfp.get( 'Z' )   ;  sample['Z']   = xxx.value
    xxx = xfp.get( 'r' )   ;  sample['r']   = xxx.value
    xfp.close()
    sample['selZ'] = dict()
    for sel_Z in numpy.unique( sample['Z'] ) :
        sample['selZ'][sel_Z] = pylab.find( sel_Z == sample['Z'] )

    return sample


##############################################################################


def f_num_snp( all_real ) :
    global g_s2e_setup
    xfp  = h5py.File( g_s2e_setup['prj'] + '/pmi/pmi_out_' + str( all_real[0] ).zfill(g_s2e_setup['num_digits'])  + '.h5' , "r" )
    cc = 1
    while 1 :
        if not  xfp.get( "/data/snp_" + str( cc ).zfill(g_s2e_setup['num_digits']) )  :
            xfp.close()
            return cc - 1
        cc = cc + 1

#        try:
#            if type( a_fp.get( "/data/snp_" + str( cc ).zfill(NUM_DIGITS) + '/Nph' ) ) == 'NoneType' :
#                print 'N'
#            else :
#                print 1
#
#        except:
#            return cc


##############################################################################


def f_eval_disp( a_snp , a_r0 , a_sample ) :

    num_Z = len( a_sample['selZ'].keys() )
    all_disp = numpy.zeros( ( num_Z , ) )
    cc = 0 ;
    for sel_Z in a_sample['selZ'].keys() :
        dr = a_snp['r'][a_sample['selZ'][sel_Z],:] - a_r0[a_sample['selZ'][sel_Z],:]
        all_disp[cc] = numpy.mean( numpy.sqrt( numpy.sum( dr * dr , axis = 1 ) ) ) / 1e-10
        cc = cc + 1
    return all_disp


##############################################################################


def f_eval_numE( a_snp , a_sample ) :

    num_Z = len( a_sample['selZ'].keys() )
    all_numE = numpy.zeros( ( num_Z , ) )
    cc = 0 ;
    for sel_Z in a_sample['selZ'].keys() :
        all_numE[cc] = numpy.mean( a_snp['q'][a_sample['selZ'][sel_Z]] )
        cc = cc + 1
    return all_numE


##############################################################################


def   f_pmi_diagnostics_help() :
    print """
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Usage - Detailed:
    * I.  open (i)python session [ipython -pylab] and run:
        >> run  your_path_to/pmi_diagnostics.py
    * II.  load and process data:
        >> data = pmi_diagnostics( <PROJ_FOLDER> , 'quick' )
      or
        >> data = pmi_diagnostics( <PROJ_FOLDER> , 'default' )
      or
        >> data = pmi_diagnostics( <PROJ_FOLDER> , 'load' , <pmi_out_instances> [ , <snapshots> ] )
      or if current folder is the project folder:
        >> data = pmi_diagnostics( 'load' , <pmi_out_instances> [ , <snapshots> ] )
    * III.  plot displacements and number of electrons
        >> figure()
        >> pmi_diagnostics( 'plot-disp' , data , <Z> ,  <color> ) ;
        >> pmi_diagnostics( 'plot-numE' , data , <Z> ,  <color> ) ;
      Data used above:
        Time:
          >> data['time']
        Data:
          >> data['disp']
          >> data['numE']
        Columns correspond to Z in
          >> xdata['sample']['selZ'].keys()



E.g.:
    # Average over realizations 1..20, all timeslices:
        >> data = pmi_diagnostics( './PROJ_9fs' , 'load' , arange(1,21) )
    # or e.g. in project folder,  with snp selection 1,25,50,100:
    # data = pmi_diagnostics( 'load' , array([1,2,3,4,5]) , arange(1,25,101) )
        >> figure()
        >> pmi_diagnostics( 'plot-disp' , data , 1 ,  'b' ) ;
        >> pmi_diagnostics( 'plot-disp' , data , 6 ,  'r' ) ;
        >> figure()
        >> pmi_diagnostics( 'plot-numE' , data , 1 ,  'b' ) ;
        >> pmi_diagnostics( 'plot-numE' , data , 6 ,  'r' ) ;

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

More:
    * help:  pmi_diagnostics()   or   pmi_diagnostics('help')
    * TODO: 'dose'

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Usage - Quick (predefined):
    The following commands (executed in linux shell) will save files:
        ./pmi_diag-<PROJECT_FOLDER>-disp.png
        ./pmi_diag-<PROJECT_FOLDER>-numE.png
    Default based on 20 realizations, all snapshots:
        $ pmi_diag.py  <PROJECT_FOLDER>  default
    Quick  based on 5 realizations, 10 snapshots:
        $ pmi_diag.py  <PROJECT_FOLDER>  quick

    """


##############################################################################
##############################################################################
##############################################################################


### if to be called as a function:
def pmi_diagnostics( *args ) :
    global g_s2e_setup

    xcolors = [ 'b', 'r', 'g', 'k', 'm', 'c',  'b--', 'r--', 'g--', 'k--', 'm--', 'c--'  ]
    element_symbol = [ '-' , 'H' , 'He' , 'Li' , 'Be' , 'B' , 'C' , 'N' , 'O' , 'F' , 'Ne' , 'Na' , 'Mg' , 'Al' , 'Si' , 'P' , 'S' , 'Cl' , 'Ar' , 'K' , 'Ca' , 'Sc' , 'Ti' , 'V' , 'Cr' , 'Mn' , 'Fe' , 'Co' , 'Ni' , 'Cu' , 'Zn' , 'Ga' , 'Ge' , 'As' , 'Se' , 'Br' , 'Kr' , 'Rb' , 'Sr' , 'Y' , 'Zr' , 'Nb' , 'Mo' , 'Tc' , 'Ru' , 'Rh' , 'Pd' , 'Ag' , 'Cd' , 'In' , 'Sn' , 'Sb' , 'Te' , 'I' , 'Xe' , 'Cs' , 'Ba' , 'La' , 'Ce' , 'Pr' , 'Nd' , 'Pm' , 'Sm' , 'Eu' , 'Gd' , 'Tb' , 'Dy' , 'Ho' , 'Er' , 'Tm' , 'Yb' , 'Lu' , 'Hf' , 'Ta' , 'W' , 'Re' , 'Os' , 'Ir' , 'Pt' , 'Au' , 'Hg' , 'Tl' , 'Pb' , 'Bi' , 'Po' , 'At' , 'Rn' , 'Fr' , 'Ra' , 'Ac' , 'Th' , 'Pa' , 'U' , 'Np' , 'Pu' , 'Am' , 'Cm' , 'Bk' , 'Cf' , 'Es' , 'Fm' , 'Md' , 'No' , 'Lr' , 'Rf' , 'Db' , 'Sg' , 'Bh' , 'Hs' , 'Mt' , 'Ds' , 'Rg' , 'Cp' , 'Uut' , 'Uuq' , 'Uup' , 'Uuh' , 'Uus' , 'Uuo' ]

    OPT_real_test    = numpy.arange(1,2) ; OPT_num_snp_test  = numpy.array( [5] )
    OPT_real_quick   = numpy.arange(1,6) ; OPT_num_snp_quick = numpy.array( [10] )
    OPT_real_default = numpy.arange(1,21) ;

    a_comm = 'default'

    if len( args ) == 0 :
        f_pmi_diagnostics_help()
        return

### if to be called from command line:
#    if __name__ == '__main__':
#        if len( sys.argv ) > 1 :
#            #a_comm = sys.argv[1]
#            #sys.argv = sys.argv[2:]
#            args = sys.argv[1:]
    if isinstance( args[0] , list ) :
        args = args[0]


    g_s2e_setup = dict()
    g_s2e_setup['prj'] = '.'
    g_s2e_setup['num_digits'] = 7


    if os.path.isdir( args[0] ) :
        g_s2e_setup['prj']  = args[0] ; args = args[1:]
    if  len(args) > 0 :
        a_comm = args[0] ; args = args[1:]


#-------------------------------------------------------------------------

    if a_comm == 'help' :
        f_pmi_diagnostics_help()



#-------------------------------------------------------------------------

    if a_comm == 'load' :

        ref_prop_out = g_s2e_setup['prj'] + '/prop/prop_out_' + str( 1 ).zfill(g_s2e_setup['num_digits'])  + '.h5'

        data = dict() ;
        data['prj'] = os.path.abspath(  g_s2e_setup['prj'] ).split('/')[-1]

        if  len(args) > 0 :
            data['real'] = numpy.array( args[0] )

        if  len(args) > 1 :
            data['snp'] = args[1]
        else :
            data['snp'] = numpy.arange( 1 ,  f_num_snp( data['real'] ) + 1 )

        if len( data['snp'] ) == 1 :
                data['snp'] = numpy.around( numpy.linspace( 1 ,  f_num_snp( data['real'] ) ,  data['snp'] ) ) .astype(int)

        data['sample']   = f_load_sample()
        data['num_real'] = data['real'].size
        data['num_snp'] = data['snp'].size
        data['time'] = ( data['snp'] \
                * ( f_hdf5_simple_read( ref_prop_out , '/params/Mesh/sliceMax' ) - f_hdf5_simple_read( ref_prop_out , '/params/Mesh/sliceMin' ) ) \
                / f_num_snp( data['real'] ) +  f_hdf5_simple_read( ref_prop_out , '/params/Mesh/sliceMin' ) )  \
                / 1e-15
        print 'Project:    ' , data['prj']
        print "Num. real.: " , data['num_real']
        print "Num. snp:   " , data['num_snp']


        data['disp'] = numpy.zeros( ( data['num_snp'] , len( data['sample']['selZ'].keys() ) ) )
        data['numE'] = numpy.zeros( ( data['num_snp'] , len( data['sample']['selZ'].keys() ) ) )
        data['Nph']  = numpy.zeros( ( data['num_snp'] ,  ) )

        for x_real in data['real'] :
            #print 'Real: %0' + str(NUM_DIGITS) + 'd' % ( x_real ) ,
            print '%07d  ' % ( x_real ) ,
            sys.stdout.flush()


            data_snp0 = f_load_snp( x_real , 1 )
            cc = 0
            for xsnp in data['snp'] :
                #print '.',
                sys.stdout.write('.')
                sys.stdout.flush()
                data_snp = f_load_snp( x_real , xsnp )
                data['disp'][cc,:] += f_eval_disp( data_snp , data_snp0['r'] , data['sample'] ) / data['num_real']
                data['numE'][cc,:] += f_eval_numE( data_snp , data['sample'] ) / data['num_real']
                data['Nph'][cc]    += data_snp['Nph'] / data['num_real']
                cc = cc + 1

            print

        return data
        #return data_snp



#-------------------------------------------------------------------------

    if a_comm == 'plot-disp':
        data = args[0] ;

        if args[1] == 'all' :
            all_Z = data['sample']['selZ'].keys()
            legendtxt = []
            fig = pylab.figure()
            a1 = pylab.axes( ) ;
#            a1.plot( data['time'] ,  data['Nph'][:] )
#            fig.add_axes( a1.get_position(), frameon=False  )
            cc = 0
            for sel_Z in all_Z :
                pmi_diagnostics( 'plot-disp' , data , sel_Z , xcolors[cc] ) ;
                legendtxt.append( element_symbol[sel_Z] )   #  legendtxt.append( str( sel_Z ) )
                cc += 1

            pylab.legend( legendtxt , 2 )
            return

        sel_Z = args[1]
        xcolor = args[2]
        pylab.plot( data['time'] , data['disp'][ : , pylab.find( sel_Z == pylab.array( data['sample']['selZ'].keys() ) ) ] , xcolor  )
        ha = pylab.gca()
        ha.set_xlabel( 'Time [fs]' )
        ha.set_ylabel( 'Average displacement [$\AA$]' )




#-------------------------------------------------------------------------

    if a_comm == 'plot-numE':
        data = args[0] ;

        if args[1] == 'all' :
            all_Z = data['sample']['selZ'].keys()
            legendtxt = []
            pylab.figure()
            cc = 0
            for sel_Z in all_Z :
                pmi_diagnostics( 'plot-numE' , data , sel_Z , xcolors[cc] ) ;
                legendtxt.append( str( sel_Z ) )
                cc += 1

            pylab.legend( legendtxt , 1 )
            return

        sel_Z = args[1]
        xcolor = args[2]
        pylab.plot( data['time'] , data['numE'][ : , pylab.find( sel_Z == pylab.array( data['sample']['selZ'].keys() ) ) ] , xcolor  )
        ha = pylab.gca()
        ha.set_xlabel( 'Time [fs]' )
        ha.set_ylabel( 'Number of bound electrons' )



#-------------------------------------------------------------------------

    if a_comm == 'plot-combined':
        lw = 4 ; fs = 20 ; inset_bgcolor = 'Yellow'
        data = args[0] ;
        allZ = pylab.array( data['sample']['selZ'].keys() )

        pmi_diagnostics( 'plot-disp' , data , 'all' ) ;
        ha = pylab.gca()
        ha.get_xaxis() .get_label() .set_fontsize( fs )
        ha.get_yaxis() .get_label() .set_fontsize( fs )
	for hh in ha.lines:
	    hh.set_linewidth( lw )
	for hh in ha.get_xticklabels():
	    hh.set_fontsize( fs )
	for hh in ha.get_yticklabels():
	    hh.set_fontsize( fs )
        pylab.axis( [ min( data['time'] ) ,  max( data['time'] ) , ha.get_ylim()[0] , ha.get_ylim()[1] ] )
#	ha.axhline(linewidth=lw, color='k')
#	ha.axvline(linewidth=lw, color='k')
        legendtxt = []
        for sel_Z in allZ :
            legendtxt.append( element_symbol[sel_Z] )   # legendtxt.append( str( sel_Z ) )
        print legendtxt
        pylab.legend( legendtxt , loc=(0.65 , 0.6) )
        pylab.draw() ; pylab.show() ;
        print os.getcwd()
        try:
            import plot_disp
        except:
            print 'plot_disp not loaded.'
        pylab.ylim( [0,18] )


        cc = 0


        a1 = pylab.axes([.2, .58, .3, .3], axisbg = inset_bgcolor ) ;
        for sel_Z in allZ[ pylab.find( allZ  <= 10 ) ] :
#            print sel_Z
            pmi_diagnostics( 'plot-numE' , data , sel_Z , xcolors[cc] ) ;
            cc += 1
        pylab.ylabel( 'Num. of bound el.' )
        pylab.axis( [ min( data['time'] ) ,  max( data['time'] ) , 0 , a1.get_ylim()[1] * 1.05 ] )


        #a2 = pylab.axes([.2, .19, .3, .3], axisbg = inset_bgcolor) ;
        a2 = pylab.axes([.2, .17, .3, .3], axisbg = inset_bgcolor) ;
        for sel_Z in allZ[ pylab.find( allZ  > 10 ) ] :
#            print sel_Z
            pmi_diagnostics( 'plot-numE' , data , sel_Z , xcolors[cc] ) ;
            cc += 1
        pylab.ylabel( 'Num. of bound el.' )
        pylab.axis( [ min( data['time'] ) ,  max( data['time'] ) , 0 , a2.get_ylim()[1] * 1.05 ] )
        a2.xaxis.set_ticks_position('top')
        a2.set_xlabel( '' )


	for hh in a1.lines:
	    hh.set_linewidth( lw )
	for hh in a2.lines:
	    hh.set_linewidth( lw )



#-------------------------------------------------------------------------

    if a_comm == 'plot-combined2':

        lw = 4 ; fs = 20 ; inset_bgcolor = 'White' # 'Yellow'
        data = args[0] ;
        allZ = pylab.array( data['sample']['selZ'].keys() )

        pmi_diagnostics( 'plot-disp' , data , 'all' ) ;

        F = pylab.gcf()
        F.set_size_inches( [9,6], forward=True ) ; pylab.show() ;

        ha = pylab.gca()
        #ha .set_position([0.1,  0.1 ,  0.9 * 0.6 ,  0.85 ]) ;
        ha .set_position([0.12,  0.12 ,  0.35 ,  0.83 ]) ;
        ha.get_xaxis() .get_label() .set_fontsize( fs )
        ha.get_yaxis() .get_label() .set_fontsize( fs )
	for hh in ha.lines:
	    hh.set_linewidth( lw )
	for hh in ha.get_xticklabels():
	    hh.set_fontsize( fs )
	for hh in ha.get_yticklabels():
	    hh.set_fontsize( fs )
        pylab.axis( [ min( data['time'] ) ,  max( data['time'] ) , ha.get_ylim()[0] , ha.get_ylim()[1] ] )
#	ha.axhline(linewidth=lw, color='k')
#	ha.axvline(linewidth=lw, color='k')
        legendtxt = []
        for sel_Z in allZ :
            legendtxt.append( element_symbol[sel_Z] )   # legendtxt.append( str( sel_Z ) )
        print legendtxt
        #pylab.legend( legendtxt , loc=(0.65 , 0.6) )
        pylab.legend( legendtxt , loc=(0.1 , 0.55) )
        pylab.draw() ; pylab.show() ;
        print os.getcwd()
        try:
            import plot_disp
        except:
            print 'plot_disp not loaded.'
        pylab.ylim( [0,18] )
        # EXTRA, TO BE COMMENTED OUT:
        # pylab.gca() .set_xticks( [-30, -15, 0, 15 ,30] )


        cc = 0
        #a1 = pylab.axes( [.75, .1, .2, .85] , axisbg = inset_bgcolor ) ;
        a1 = pylab.axes( [.6, .12, .35, .83] , axisbg = inset_bgcolor ) ;
        a1.get_xaxis() .get_label() .set_fontsize( fs )
        a1.get_yaxis() .get_label() .set_fontsize( fs )
        for sel_Z in allZ[ pylab.find( allZ  <= 99 ) ] :
#            print sel_Z
            pmi_diagnostics( 'plot-numE' , data , sel_Z , xcolors[cc] ) ;
            cc += 1
        pylab.ylabel( 'Number of bound electrons' )
        #pylab.axis( [ min( data['time'] ) ,  max( data['time'] ) , 0 , a1.get_ylim()[1] * 1.05 ] )
        pylab.axis( [ min( data['time'] ) ,  max( data['time'] ) , 0 , allZ.max() * 1.1  ] )

	for hh in a1.lines:
	    hh.set_linewidth( lw )
	for hh in a1.get_xticklabels():
	    hh.set_fontsize( fs )
	for hh in a1.get_yticklabels():
	    hh.set_fontsize( fs )

        # EXTRA, TO BE COMMENTED OUT:
        # pylab.gca() .set_xticks( [-30, -15, 0, 15 ,30] )


        return

        cc = 0


        #a1 = pylab.axes([.2, .58, .3, .3], axisbg = inset_bgcolor ) ;
        a1 = pylab.axes( [.75, .58, .2, .3] , axisbg = inset_bgcolor ) ;
        for sel_Z in allZ[ pylab.find( allZ  <= 10 ) ] :
#            print sel_Z
            pmi_diagnostics( 'plot-numE' , data , sel_Z , xcolors[cc] ) ;
            cc += 1
        pylab.ylabel( 'Num. of bound el.' )
        pylab.axis( [ min( data['time'] ) ,  max( data['time'] ) , 0 , a1.get_ylim()[1] * 1.05 ] )


        #a2 = pylab.axes([.2, .19, .3, .3], axisbg = inset_bgcolor) ;
        a2 = pylab.axes([.75, .17, .2, .3], axisbg = inset_bgcolor) ;
        for sel_Z in allZ[ pylab.find( allZ  > 10 ) ] :
#            print sel_Z
            pmi_diagnostics( 'plot-numE' , data , sel_Z , xcolors[cc] ) ;
            cc += 1
        pylab.ylabel( 'Num. of bound el.' )
        pylab.axis( [ min( data['time'] ) ,  max( data['time'] ) , 0 , a2.get_ylim()[1] * 1.05 ] )
        a2.xaxis.set_ticks_position('top')
        a2.set_xlabel( '' )


	for hh in a1.lines:
	    hh.set_linewidth( lw )
	for hh in a2.lines:
	    hh.set_linewidth( lw )




#-------------------------------------------------------------------------

    if  a_comm == 'default'   or   a_comm == 'quick'   or   a_comm == 'test' :

        if a_comm == 'default' :
            data = pmi_diagnostics( g_s2e_setup['prj']  , 'load' , OPT_real_default )
        if  a_comm == 'quick' :
            data = pmi_diagnostics( g_s2e_setup['prj']  , 'load' , OPT_real_quick , OPT_num_snp_quick )
        if  a_comm == 'test' :
            data = pmi_diagnostics( g_s2e_setup['prj']  , 'load' , OPT_real_test  , OPT_num_snp_test  )

        pylab.figure()
        pmi_diagnostics( 'plot-disp' , data , 'all' ) ;
        for ext in [ 'png' ,  'eps' ] :
            pic_file = './pmi_diag-' + data['prj'] + '-disp.' + ext
            pylab.savefig( pic_file , dpi=200 )
        print 'Saved image: ' + pic_file

        pylab.figure()
        pmi_diagnostics( 'plot-numE' , data , 'all' ) ;
        for ext in [ 'png' ,  'eps' ] :
            pic_file = './pmi_diag-' + data['prj'] + '-numE.' + ext
            pylab.savefig( pic_file , dpi=200 )
        print 'Saved image: ' + pic_file

        combined_version = '2' ;
        pylab.figure()
        pmi_diagnostics( 'plot-combined' + combined_version , data ) ;
        for ext in [ 'png' ,  'eps' ] :
            pic_file = './pmi_diag-' + data['prj'] + '-combined' + combined_version + '.' + ext
            pylab.savefig( pic_file , dpi=200 )
        print 'Saved image: ' + pic_file

        return data

        #pylab.close() ;  pylab.close() ;



#-------------------------------------------------------------------------

    if a_comm == 'test':
        print 'TEST OPTION'

    return




##############################################################################



### if to be called from command line:
if __name__ == '__main__':

    if len( sys.argv ) > 1 :
        pmi_diagnostics( sys.argv[1:] )
        pylab.draw()
        pylab.show()

    else:
        f_pmi_diagnostics_help()


