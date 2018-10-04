#!/usr/bin/env python

##########################################################################
#                                                                        #
# Copyright (C) 2015-2018 Carsten Fortmann-Grote                         #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

from argparse import ArgumentParser

def   pmi_diagnostics_help() :
    print("""
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

    """)
import periodictable as pte
XCOLORS = [ 'b', 'r', 'g', 'k', 'm', 'c',  'b--', 'r--', 'g--', 'k--', 'm--', 'c--'  ]
ELEMENT_SYMBOL = ['-'] + [e.symbol for e in pte.elements()]

def main(args) :

    #OPT_real_test    = numpy.array([1]) ; OPT_num_snp_test  = numpy.array( [50] )
    #OPT_real_quick   = numpy.arange(1,6) ; OPT_num_snp_quick = numpy.array( [10] )
    #OPT_real_default = numpy.arange(1,21) ;



    if os.path.isdir( args[0] ) :
        self.__prj  = args[0] ; args = args[1:]
    if  len(args) > 0 :
        a_comm = args[0] ; args = args[1:]


#-------------------------------------------------------------------------

    if a_comm == 'help' :
        f_pmi_diagnostics_help()



#-------------------------------------------------------------------------
    if a_comm == 'load' :



#-------------------------------------------------------------------------

    if a_comm == 'plot-disp':
        data = args[0] ;

        if args[1] == 'all' :
            all_Z = list(data['sample']['selZ'].keys())
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

            #pylab.legend( legendtxt , 2 )
            return

        sel_Z = args[1]
        xcolor = args[2]
        pylab.plot( data['time'] , data['disp'][ : , pylab.find( sel_Z == pylab.array( list(data['sample']['selZ'].keys()) ) ) ] , xcolor  )
        ha = pylab.gca()
        ha.set_xlabel( 'Time [fs]' )
        ha.set_ylabel( 'Average displacement [$\AA$]' )


    if a_comm == 'plot-numE':
        data = args[0] ;

        if args[1] == 'all' :
            all_Z = list(data['sample']['selZ'].keys())
            legendtxt = []
            pylab.figure()
            cc = 0
            for sel_Z in all_Z :
                pmi_diagnostics( 'plot-numE' , data , sel_Z , xcolors[cc] ) ;
                legendtxt.append( str( sel_Z ) )
                cc += 1

            #pylab.legend( legendtxt , 1 )
            return

        sel_Z = args[1]
        xcolor = args[2]
        pylab.plot( data['time'] , data['numE'][ : , pylab.find( sel_Z == pylab.array( list(data['sample']['selZ'].keys()) ) ) ] , xcolor  )
        ha = pylab.gca()
        ha.set_xlabel( 'Time [fs]' )
        ha.set_ylabel( 'Number of bound electrons' )



#-------------------------------------------------------------------------

    if a_comm == 'plot-combined':
        lw = 4 ; fs = 20 ; inset_bgcolor = 'Yellow'
        data = args[0] ;
        allZ = pylab.array( list(data['sample']['selZ'].keys()) )

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
        print(legendtxt)
        pylab.legend( legendtxt , loc=(0.65 , 0.6) )
        pylab.draw() ; pylab.show() ;
        print(os.getcwd())
        try:
            import plot_disp
        except:
            print('plot_disp not loaded.')
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
        allZ = pylab.array( list(data['sample']['selZ'].keys()) )

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
        print(legendtxt)
        #pylab.legend( legendtxt , loc=(0.65 , 0.6) )
        pylab.legend( legendtxt , loc=(0.1 , 0.55) )
        pylab.draw() ; pylab.show() ;
        print(os.getcwd())
        try:
            import plot_disp
        except:
            print('plot_disp not loaded.')
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
            data = pmi_diagnostics( self.__prj  , 'load' , OPT_real_default )
        if  a_comm == 'quick' :
            data = pmi_diagnostics( self.__prj  , 'load' , OPT_real_quick , OPT_num_snp_quick )
        if  a_comm == 'test' :
            data = pmi_diagnostics( self.__prj  , 'load' , OPT_real_test  , OPT_num_snp_test  )

        pylab.figure()
        pmi_diagnostics( 'plot-disp' , data , 'all' ) ;
        for ext in [ 'png' ,  'eps' ] :
            pic_file = './pmi_diag-' + data['__prj'] + '-disp.' + ext
            pylab.savefig( pic_file , dpi=200 )
        print('Saved image: ' + pic_file)

        pylab.figure()
        pmi_diagnostics( 'plot-numE' , data , 'all' ) ;
        for ext in [ 'png' ,  'eps' ] :
            pic_file = './pmi_diag-' + data['__prj'] + '-numE.' + ext
            pylab.savefig( pic_file , dpi=200 )
        print('Saved image: ' + pic_file)

        combined_version = '2' ;
        pylab.figure()
        pmi_diagnostics( 'plot-combined' + combined_version , data ) ;
        for ext in [ 'png' ,  'eps' ] :
            pic_file = './pmi_diag-' + data['__prj'] + '-combined' + combined_version + '.' + ext
            pylab.savefig( pic_file , dpi=200 )
        print('Saved image: ' + pic_file)

        return data

if __name__ == '__main__':
    # Setup argument parser.
    parser = ArgumentParser()

    # Add arguments.
    parser.add_argument("input_path",
                        metavar="input_path",
                        help="Name (path) of input file (dir).",
                        default=None)

    parser.add_argument(
            "-q",
            "--quick",
            action="store_true",
            dest="quick",
            default=True,
            help="Quick analysis selecting only few random snapshots.",
            )

    parser.add_argument(
            "-c",
            "--charge",
            action="store_true",
            dest="charge",
            default=True,
            help="Calculate and plot average ion charge.",
            )

    parser.add_argument(
            "-d",
            "--displacement",
            action="store_true",
            dest="disp",
            default=True,
            help="Calculate and plot average displacement.",
            )

    parser.add_argument(
            "-s",
            "--snapshots",
            dest=snapshot_indices,
            default=None,
            help="Select which snapshots to include in the analysis.",
            )

    parser.add_argument(
            "-a",
            "--animation",
            dest="animation_filename",
            default="",
            help="Animate the trajectory.",
            )


    args = parser.parse_args()

    main(args)

