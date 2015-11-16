#!/usr/bin/env python2.7
"""
prepHDF5.py:
Prepares hdf5 in S2E format
"""
import os
import sys
import h5py

def prepS2E( src , dest , config ) :

    file_in  = h5py.File( src , "r")
    file_out =  h5py.File( dest , "w")

    grp_hist = file_out.create_group( "history" )
    grp_hist_parent = file_out.create_group( "history/parent" )
    grp_hist_parent_detail = file_out.create_group( "history/parent/detail" )

    pre_s2e_module = os.path.basename( os.path.dirname( os.path.abspath( src ) ) )
    #print 'Previous module: ' , pre_s2e_module
    
    # Add attribute to history/parent
    grp_hist_parent.attrs['name'] =  "_" + pre_s2e_module
    
    grp_srchist = file_in.get( "history/parent" ) ;
    file_out.copy( grp_srchist , grp_hist_parent )

    # Copy everything to history except "data" & "history"  
    for objname in file_in.keys() :
        if   objname != "data" \
             and   objname != "history" :
            x = file_in.get( objname )
            if file_in.get( objname , getclass = True )  == h5py.highlevel.Dataset :
                mygroup = file_in['/']
                #print mygroup.name # print name of group
                #print mygroup.keys() # print keys
                #print mygroup[objname] # print dataset description
                #print mygroup[objname].name # print name
                #print mygroup[objname].shape # print shape
                #print mygroup[objname].dtype # print datatype
                #print mygroup[objname][...] # print value
                file_out["history/parent/detail/"+objname] = mygroup[objname][...]
            elif file_in.get( objname , getclass = True )  == h5py.highlevel.Group :
                file_out.copy( x , "history/parent/detail/" + objname )
            else:
                print objname  , " has been SKIPPED!!"
        #else :
        #    print '  NOT:', objname

    #print file_in['data'].keys()
    #print file_in['data'].items()    

    # Create external link to parent's data
    #file_out['history/parent/detail/data'] = h5py.ExternalLink(src,'/data')
    parent_module = os.path.basename( src ) [ : os.path.basename( src ) .find( '_out' ) ]
    file_out['history/parent/detail/data'] = h5py.ExternalLink( '../' + parent_module + '/' + os.path.basename( src ) , '/data' )
    
	# Create your own groups
    grp_data = file_out.create_group( "data" )
    grp_param = file_out.create_group( "params" )
    grp_param = file_out.create_group( "misc" )
    grp_param = file_out.create_group( "info" )

    str_type = h5py.new_vlen(str)
	# Interface version  
    dataset = file_out.create_dataset("version", (1,), dtype='f')
    dataset[...] = 0.1
    # Populate /info
    dataset = file_out.create_dataset("info/package_version",(1,), dtype=str_type)
    data = ("SingFEL v0.1.0")
    dataset[...] = data
    dataset = file_out.create_dataset("info/contact",(2,), dtype=str_type)
    data = ("Name: Chunhong Yoon", "Email: chun.hong.yoon@desy.de")
    dataset[...] = data
    dataset = file_out.create_dataset("info/data_description",(1,), dtype=str_type)
    data = ("This dataset contains a diffraction pattern generated using SingFEL.")
    dataset[...] = data
    dataset = file_out.create_dataset("info/method_description",(1,), dtype=str_type)
    data = ("Form factors of the radiation damaged molecules are calculated in time slices. At each time slice, the coherent scattering is calculated and incoherently added to the final diffraction pattern. Finally, Poissonian noise is added to the diffraction pattern.")
    dataset[...] = data
    # Populate /params
    dataset = file_out.create_dataset("params/info",(1,), dtype=str_type)
    data = open(config)
    dataset[...] = data.read()
     
    file_out.close()
    file_in.close()

def valid_file(x):
    if not os.path.exists(x):
        raise argparse.ArgumentError("{0} does not exist".format(x))
    return x

def valid_name(x):
    # Should check the outfile should be overwritten
    if os.path.exists(x):
        var = raw_input("Overwrite %s? [y/N]: " %x)
        if var == 'Y' or var == 'y':
            return x
        else:
            sys.exit(0)
    else:
        return x

# inputs to the script
if __name__ == '__main__':
    if len( sys.argv ) > 1 :

        src  = sys.argv[1]
        dest = sys.argv[2]
        config = sys.argv[3]        
        prepS2E( src , dest , config ) 
                        
# inputs to the script
#if __name__ == '__main__':
#    import argparse
#    parser = argparse.ArgumentParser(description='Preparing S2E format hdf5.')
#    parser.add_argument("-i", "--input", dest="filename", required=True,
#                        help='input hdf5 filename', metavar="FILE",
#                        type=valid_file)
#    parser.add_argument("-o", "--output", dest="outfilename", required=False,
#                        help='output text filename', metavar="FILE",
#                        type=valid_name, default="out.h5")                  
#    args = parser.parse_args()
#    prepS2E( args.filename, args.outfilename )

