/*
 * Program for simulating diffraction patterns
 */
#include <iostream>
#include <iomanip>
#include <sys/time.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <gsl/gsl_spline.h>
#include <gsl/gsl_errno.h>
#include <algorithm>
#include <fstream>
#include <string>
//SHM for local rank
#include <sys/ipc.h>
#include <sys/stat.h>
#include <sys/shm.h>
// Armadillo library
#include <armadillo>
// Boost library
#include <boost/tokenizer.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/mpi.hpp>
#include <boost/serialization/string.hpp>
#include <boost/program_options.hpp>
// HDF5 library
#include "hdf5.h"
#include "hdf5_hl.h"
// SingFEL library
#include "detector.h"
#include "beam.h"
#include "particle.h"
#include "diffraction.h"
#include "toolbox.h"
#include "io.h"

#ifdef COMPILE_WITH_CUDA
#include "diffraction.cuh"
#endif

namespace mpi = boost::mpi;
namespace opt = boost::program_options;
using namespace std;
using namespace arma;
using namespace detector;
using namespace beam;
using namespace particle;
using namespace diffraction;
using namespace toolbox;

#define QTAG 1	// quaternion
#define DPTAG 2	// diffraction pattern
#define DIETAG 3 // die signal
#define DONETAG 4 // done signal

#define MPI_SHMKEY 0x6FB1407
//#define MPI_SHMKEY 0x6FB10407

const int master = 0; // Process with rank=0 is the master
const int msgLength = 4; // MPI message length
int localRank=0;
#ifdef COMPILE_WITH_CUDA
int deviceCount=cuda_getDeviceCount();
#endif

static void master_diffract(mpi::communicator* comm, opt::variables_map vm);
static void slave_diffract(mpi::communicator* comm, opt::variables_map vm);
opt::variables_map parse_input(int argc, char* argv[], mpi::communicator* comm);
void generateRotations(const bool uniformRotation, \
                       const string rotationAxis, const int numQuaternions, \
                       fmat* myQuaternions);
void loadParticle(const opt::variables_map vm, const string filename, \
                  const int timeSlice, CParticle* particle);
void setTimeSliceInterval(const int numSlices, int* sliceInterval, \
                          int* timeSlice, int* done);
void rotateParticle(fvec* quaternion, CParticle* particle);
void setFluenceFromFile(const string filename, const int timeSlice, \
                        const int sliceInterval, CBeam* beam);
void setEnergyFromFile(const string filename, CBeam* beam);
void setFocusFromFile(const string filename, CBeam* beam);
void getComptonScattering(const opt::variables_map vm, CParticle* particle, \
                          CDetector* det, fmat* Compton);
void savePhotonField(const string filename, const int isFirstSlice, \
                     const int timeSlice, fmat* photon_field);
void saveAsDiffrOutFile(const string outputName, umat* detector_counts, \
                        fmat* detector_intensity, fvec* quaternion, \
                        CDetector* det, CBeam* beam, double total_phot);

int main( int argc, char* argv[] ){

	// Initialize MPI
  	mpi::environment env;
  	mpi::communicator world;
	mpi::communicator* comm = &world;

	// All processes parse the input
	opt::variables_map vm = parse_input(argc, argv, comm);
	// Set random seed
	//srand( vm["pmiStartID"].as<int>() + world.rank() + (unsigned)time(NULL) );
	srand( 0x01333337);
	int shmid;
	key_t shmkey = (key_t)MPI_SHMKEY;
	static int *shmval;
	if (world.rank() != master){
		shmid = shmget(shmkey,sizeof(int),0666 | IPC_CREAT);
		if ( 0 > shmid )
			perror("shmget");
		shmval = (int*)shmat(shmid,NULL,0);
		if ( 0 > shmval )
			perror("shmval");
		*shmval=0;
	}

	world.barrier();
	if (world.rank() != master){
		//printf("Local %d\n",localRank);fflush(NULL);
		localRank = __sync_fetch_and_add( shmval,1);
		//printf("Local %d\n",localRank);fflush(NULL);
	}
	wall_clock timerMaster;

	timerMaster.tic();


	// Main program
	if (world.rank() == master) {
		master_diffract(comm, vm);
	} else {
		slave_diffract(comm, vm);
	}

	world.barrier();
	if (world.rank() != master) {
		shmdt(shmval);
		shmctl(shmid, IPC_RMID, 0);
	}


	if (world.rank() == master) {
		cout << "Finished: " << timerMaster.toc() <<" seconds."<<endl;
	}

  	return 0;
}

static void master_diffract(mpi::communicator* comm, opt::variables_map vm) {

	int pmiStartID = vm["pmiStartID"].as<int>();
	int pmiEndID = vm["pmiEndID"].as<int>();
	int numDP = vm["numDP"].as<int>();
	int sliceInterval = vm["sliceInterval"].as<int>();
	string rotationAxis = vm["rotationAxis"].as<string>();
	bool uniformRotation = vm["uniformRotation"].as<bool>();

  	int ntasks, rank, numProcesses, numSlaves;
  	int numTasksDone = 0;
  	boost::mpi::status status;

	ntasks = (pmiEndID-pmiStartID+1)*numDP;
	numProcesses = comm->size();
	numSlaves = comm->size()-1;

	if (numSlaves > ntasks) {
		cout << "Reduce number of slaves and restart" << endl;
		for (rank = 1; rank < numProcesses; ++rank) {
			comm->send(rank, DIETAG, 1);
			cout << "Killing: " << rank << endl;
		}
		return;
	}

	// Send
	// 1) pmiID
	// 2) diffrID
	// 3) sliceInterval

	int diffrID = (pmiStartID-1)*numDP+1;
	int pmiID = pmiStartID;
	int dpID = 1;
	fvec quaternion(4);

	// Setup rotations
	fmat myQuaternions;
	generateRotations(uniformRotation, rotationAxis, ntasks, \
	                  &myQuaternions);

	int counter = 0;
	int done = 0;
	float lastPercentDone = 0.;
	for (rank = 1; rank < numProcesses; ++rank) {
		if (pmiID > pmiEndID) {
			cout << "Error!!" << endl;
			return;
		}
		// Tell the slave how to rotate the particle
		quaternion = trans(myQuaternions.row(counter));
		counter++;
		float* quat = &quaternion[0];
		comm->send(rank, QTAG, quat,4);
		// Tell the slave to compute DP
		fvec id;
		id << pmiID << diffrID << sliceInterval << endr;
		float* id1 = &id[0];
		comm->send(rank, DPTAG, id1, 3);

		diffrID++;
		dpID++;
		numTasksDone++;
		if (dpID > numDP) {
			dpID = 1;
			pmiID++;
		}
	}

	// Listen for slaves
	int msgDone = 0;

	if (numTasksDone >= ntasks) done = 1;
	while (!done) {
		status = comm->recv(boost::mpi::any_source, DONETAG, msgDone);
		// Tell the slave how to rotate the particle
		quaternion = trans(myQuaternions.row(counter));
		float* quat = &quaternion[0];
		counter++;
		comm->send(status.source(), QTAG, quat, 4);
		// Tell the slave to compute DP
		fvec id;
		id << pmiID << diffrID << sliceInterval << endr;
		float* id1 = &id[0];
		comm->send(status.source(), DPTAG, id1, 3);

		diffrID++;
		dpID++;
		numTasksDone++;
		if (dpID > numDP) {
			dpID = 1;
			pmiID++;
		}
		if (numTasksDone >= ntasks) {
			done = 1;
		}
		// Display status
		CToolbox::displayStatusBar(numTasksDone,ntasks,&lastPercentDone);
	}

  	// Wait for status update of slaves.
	for (rank = 1; rank < numProcesses; ++rank) {
		status = comm->recv(rank, DONETAG, msgDone);
	}

	// KILL SLAVES
  	// Tell all the slaves to exit by sending an empty message with the DIETAG.
	for (rank = 1; rank < numProcesses; ++rank) {
		comm->send(rank, DIETAG, 1);
	}
}

static void slave_diffract(mpi::communicator* comm, opt::variables_map vm) {

	string inputDir = vm["inputDir"].as<std::string>();
	string outputDir = vm["outputDir"].as<string>();
	string configFile = vm["configFile"].as<string>();
	string beamFile = vm["beamFile"].as<string>();
	string geomFile = vm["geomFile"].as<string>();
	int numSlices = vm["numSlices"].as<int>();
	int saveSlices = vm["saveSlices"].as<int>();
	bool calculateCompton = vm["calculateCompton"].as<bool>();

	wall_clock timer;
	boost::mpi::status status;


	string filename;
	string outputName;

	// Set up beam and detector from file
	CDetector det = CDetector();
	CBeam beam = CBeam();
	beam.readBeamFile(beamFile);
	det.readGeomFile(geomFile);

	bool givenFluence = false;
	if (beam.get_photonsPerPulse() > 0) {
		givenFluence = true;
	}
	bool givenPhotonEnergy = false;
	if (beam.get_photon_energy() > 0) {
		givenPhotonEnergy = true;
	}
	bool givenFocusRadius = false;
	if (beam.get_focus() > 0) {
		givenFocusRadius = true;
	}

	int px = det.get_numPix_x();
	int py = px;
	float msg[msgLength];

	fvec quaternion(4);
	fmat photon_field(py,px);
	fmat detector_intensity(py,px);
	umat detector_counts(py,px);
	fmat F_hkl_sq(py,px);
	fmat Compton(py,px);
	fmat myPos;

	while (1) {
		// Receive a message from the master
    	status = comm->recv(master, boost::mpi::any_tag, msg, msgLength);

    	if (status.tag() == QTAG) {
    		quaternion << msg[0] << msg[1] << msg[2] << msg[3] << endr;
    	}

		// Receive how many slices assigned to this slave
		if (status.tag() == DPTAG) {

			timer.tic();

    		int pmiID = (int) msg[0];
    		int diffrID = (int) msg[1];
    		int sliceInterval = (int) msg[2];

			// input file
			stringstream sstm;
			sstm << inputDir << "/pmi_out_" << setfill('0') << setw(7) \
			     << pmiID << ".h5";
			filename = sstm.str();
			if ( !boost::filesystem::exists( filename ) ) {
				cout << filename << " does not exist!" << endl;
				exit(0);
			}

			// output file
			sstm.str("");
			sstm << outputDir << "/diffr_out_" << setfill('0') << setw(7) \
			      << diffrID << ".h5";
			outputName = sstm.str();
			if ( boost::filesystem::exists( outputName ) ) {
				boost::filesystem::remove( outputName );
			}

			// Run prepHDF5
			string scriptName;
			sstm.str("");
			sstm << inputDir << "/prepHDF5.py";
			scriptName = sstm.str();
			string myCommand = string("python ") + scriptName + " " \
			                   + filename + " " + outputName + " " + configFile;
			int i = system(myCommand.c_str());
			assert(i == 0);

			// Set up diffraction geometry
			if (givenPhotonEnergy == false) {
				setEnergyFromFile(filename, &beam);
			}
			if (givenFocusRadius == false) {
				setFocusFromFile(filename, &beam);
			}
			det.init_dp(&beam);

			double total_phot = 0;
			photon_field.zeros(py,px);
			detector_intensity.zeros(py,px);
			detector_counts.zeros(py,px);
			int done = 0;
			int timeSlice = 0;
			int isFirstSlice = 1;
			while(!done) {	// sum up time slices
				setTimeSliceInterval(numSlices, &sliceInterval, &timeSlice, \
				                     &done);
				// Particle //
				CParticle particle = CParticle();
				loadParticle(vm, filename, timeSlice, &particle);
				// Apply random rotation to particle
				rotateParticle(&quaternion, &particle);
				// Beam // FIXME: Check that these fields exist
				if (givenFluence == false) {
					setFluenceFromFile(filename, timeSlice, sliceInterval, \
					                   &beam);
				}
				total_phot += beam.get_photonsPerPulse();

				// Coherent contribution
				CDiffraction::calculate_atomicFactor(&particle, &det);

				// Incoherent contribution
				if (calculateCompton) {
					getComptonScattering(vm, &particle, &det, &Compton);
				}
				#ifdef COMPILE_WITH_CUDA
				if (localRank < 2*deviceCount){
					float* F_mem = F_hkl_sq.memptr();
					// f_hkl: py x px x numAtomTypes
					float* f_mem = CDiffraction::f_hkl.memptr();
					float* q_mem = det.q_xyz.memptr();
					float* p_mem = particle.atomPos.memptr();
					int*   i_mem = particle.xyzInd.memptr();
					cuda_structureFactor(F_mem, f_mem, q_mem, p_mem, i_mem, \
					               det.numPix, particle.numAtoms,  \
					               particle.numAtomTypes,localRank%deviceCount);
					if (calculateCompton) {
						photon_field += (F_hkl_sq+Compton) % det.solidAngle \
						                % det.thomson \
						                * beam.get_photonsPerPulsePerArea();
					} else {
						photon_field += F_hkl_sq % det.solidAngle \
						                % det.thomson \
						                * beam.get_photonsPerPulsePerArea();
					}
				}else
				#endif
				{
					F_hkl_sq = CDiffraction::calculate_molecularFormFactorSq(&particle, &det);
					if (calculateCompton) {
						photon_field = (F_hkl_sq + Compton) % det.solidAngle \
						               % det.thomson \
						               * beam.get_photonsPerPulsePerArea();
					} else {
						photon_field = F_hkl_sq % det.solidAngle \
						               % det.thomson \
						               * beam.get_photonsPerPulsePerArea();
					}
				}
				detector_intensity += photon_field;

				if (saveSlices) {
					savePhotonField(outputName, isFirstSlice, timeSlice, \
					                &photon_field);
				}
				isFirstSlice = 0;
			}// end timeSlice

			// Apply badpixelmap
			CDetector::apply_badPixels(&detector_intensity);
			// Poisson noise
			detector_counts = CToolbox::convert_to_poisson(&detector_intensity);

			// Save to HDF5
			saveAsDiffrOutFile(outputName, &detector_counts, \
			                   &detector_intensity, &quaternion, &det, &beam, \
			                   total_phot);

    		comm->send(master, DONETAG, 1);
    	}

		if (status.tag() == DIETAG) {
			return;
		}
	} // end of while

	if (comm->rank() == 1) {
		CDiffraction::displayResolution(&det, &beam);
	}
}// end of slave_diffract

void generateRotations(const bool uniformRotation, const string rotationAxis, \
                       const int numQuaternions, fmat* myQuaternions) {
	fmat& _myQuaternions = myQuaternions[0];

	_myQuaternions.zeros(numQuaternions,4);
	if (uniformRotation) { // uniform rotations
		if (rotationAxis == "y" || rotationAxis == "z") {
			_myQuaternions = CToolbox::pointsOn1Sphere(numQuaternions, \
			                                           rotationAxis);
		} else if (rotationAxis == "xyz") {
			_myQuaternions = CToolbox::pointsOn4Sphere(numQuaternions);
		}
	} else { // random rotations
		for (int i = 0; i < numQuaternions; i++) {
			_myQuaternions.row(i) = trans( \
			                         CToolbox::getRandomRotation(rotationAxis));
		}
	}
}

void setTimeSliceInterval(const int numSlices, int* sliceInterval, \
                          int* timeSlice, int* done) {
	if (*timeSlice + *sliceInterval >= numSlices) {
		*sliceInterval = numSlices - *timeSlice;
		*done = 1;
	}
	*timeSlice += *sliceInterval;
}

void loadParticle(const opt::variables_map vm, const string filename, \
                  const int timeSlice, CParticle* particle) {
	bool calculateCompton = vm["calculateCompton"].as<bool>();

	string datasetname;
	stringstream ss;
	ss << "/data/snp_" << setfill('0') << setw(7) << timeSlice;
	datasetname = ss.str();
	// rowvec atomType
	particle->load_atomType(filename,datasetname+"/T");
	// mat pos
	particle->load_atomPos(filename,datasetname+"/r");
	// rowvec ion list
	particle->load_ionList(filename,datasetname+"/xyz");
	// mat ffTable (atomType x qSample)
	particle->load_ffTable(filename,datasetname+"/ff");
	// rowvec q vector sin(theta)/lambda
	particle->load_qSample(filename,datasetname+"/halfQ");
	// Particle's inelastic properties
	if (calculateCompton) {
		// rowvec q vector sin(theta)/lambda
		particle->load_compton_qSample(filename,datasetname+"/Sq_halfQ");
		// rowvec static structure factor
		particle->load_compton_sBound(filename,datasetname+"/Sq_bound");
		// rowvec Number of free electrons
		particle->load_compton_nFree(filename,datasetname+"/Sq_free");
	}
}

void rotateParticle(fvec* quaternion, CParticle* particle) {
	fvec& _quat = quaternion[0];

	// Rotate particle
	fmat rot3D = CToolbox::quaternion2rot3D(_quat);
	fmat myPos = particle->get_atomPos();
	myPos = myPos * trans(rot3D); // rotate atoms
	particle->set_atomPos(&myPos);
}

void setFluenceFromFile(const string filename, const int timeSlice, \
                        const int sliceInterval, CBeam* beam) {
	double n_phot = 0;
	for (int i = 0; i < sliceInterval; i++) {
		string datasetname;
		stringstream ss;
		ss << "/data/snp_" << setfill('0') << setw(7) << timeSlice-i;
		datasetname = ss.str();
// SY: new format for fluence
//		double myNph = hdf5readConst<double>(filename,datasetname+"/Nph");
		vec vecNph;
		vecNph = hdf5read<vec>(filename,datasetname+"/Nph");
		if (vecNph.n_elem !=1)
		{
			cerr << "setFluenceFromFile: Wrong fluence format in : " << filename << endl;
			exit(0);
		}
		beam->set_photonsPerPulse(vecNph[0]);
		n_phot += beam->get_photonsPerPulse();	// number of photons per pulse
	}
	beam->set_photonsPerPulse(n_phot);
}

void setEnergyFromFile(const string filename, CBeam* beam) {
	// Read in photon energy
	double photon_energy = double(hdf5readScalar<float>(filename, \
	                             "/history/parent/detail/params/photonEnergy"));
	beam->set_photon_energy(photon_energy);
}

void setFocusFromFile(const string filename, CBeam* beam) {
	// Read in focus size
	double focus_xFWHM = double(hdf5readScalar<float>(filename,\
	                                      "/history/parent/detail/misc/xFWHM"));
	double focus_yFWHM = double(hdf5readScalar<float>(filename,\
	                                      "/history/parent/detail/misc/yFWHM"));
	beam->set_focus(focus_xFWHM, focus_yFWHM, "ellipse");
}

void getComptonScattering(const opt::variables_map vm, CParticle* particle, \
                          CDetector* det, fmat* Compton) {
	bool calculateCompton = vm["calculateCompton"].as<bool>();

	if (calculateCompton) {
		CDiffraction::calculate_compton(particle, det, Compton); // get S_hkl
	} else {
		Compton->zeros(det->py,det->px);
	}
}

void savePhotonField(const string filename, const int isFirstSlice, \
                     const int timeSlice, fmat* photon_field) {
	fmat& _photon_field = photon_field[0];

	int createSubgroup;
	if (isFirstSlice == 1) {
		createSubgroup = 1;
	} else {
		createSubgroup = 0;
	}
	std::stringstream ss;
	ss << "/misc/photonField/photonField_" << setfill('0') << setw(7) \
	   << timeSlice;
	string fieldName = ss.str();
	int success = hdf5writeVector(filename, "misc", "/misc/photonField", \
	                              fieldName, _photon_field, createSubgroup);
	assert(success == 0);
}

void saveAsDiffrOutFile(const string outputName, umat* detector_counts, \
                        fmat* detector_intensity, fvec* quaternion, \
                        CDetector* det, CBeam* beam, double total_phot) {
			int createSubgroup = 0;
			// FIXME: groupname and subgroupname are redundant
			int success = hdf5writeVector(outputName,"data","","/data/data", \
			                                  *detector_counts, createSubgroup);
			success = hdf5writeVector(outputName,"data","","/data/diffr", \
			                               *detector_intensity, createSubgroup);
			createSubgroup = 0;
			success = hdf5writeVector(outputName,"data","","/data/angle", \
			                                       *quaternion, createSubgroup);
			createSubgroup = 1;
			double dist = det->get_detector_dist();
			success = hdf5writeScalar(outputName,"params","params/geom",\
			                  "/params/geom/detectorDist", dist,createSubgroup);
			createSubgroup = 0;
			double pixelWidth = det->get_pix_width();
			success = hdf5writeScalar(outputName,"params","params/geom",\
			              "/params/geom/pixelWidth", pixelWidth,createSubgroup);
			double pixelHeight = det->get_pix_height();
			success = hdf5writeScalar(outputName,"params","params/geom",\
			            "/params/geom/pixelHeight", pixelHeight,createSubgroup);
			fmat mask = ones<fmat>(det->py,det->px); // FIXME: why is this needed?
			success = hdf5writeVector(outputName,"params","params/geom",\
			                          "/params/geom/mask", mask,createSubgroup);
			createSubgroup = 1;
			double photonEnergy = beam->get_photon_energy();
			success = hdf5writeScalar(outputName,"params","params/beam",\
			          "/params/beam/photonEnergy", photonEnergy,createSubgroup);
			createSubgroup = 0;
			success = hdf5writeScalar(outputName,"params","params/beam",\
			                 "/params/beam/photons", total_phot,createSubgroup);
			createSubgroup = 0;
			double focusArea = beam->get_focus_area();
			success = hdf5writeScalar(outputName,"params","params/beam",\
			                "/params/beam/focusArea", focusArea,createSubgroup);
}

opt::variables_map parse_input( int argc, char* argv[], \
                                mpi::communicator* comm ) {

    // Constructing an options describing variable and giving it a
    // textual description "All options"
    opt::options_description desc("All options");

    // When we are adding options, first parameter is a name
    // to be used in command line. Second parameter is a type
    // of that option, wrapped in value<> class. Third parameter
    // must be a short description of that option
    desc.add_options()
        ("inputDir", opt::value<std::string>(), \
                     "Input directory for finding /pmi and /diffr")
        ("outputDir", opt::value<string>(), \
                      "Output directory for saving diffraction")
        ("configFile", opt::value<string>(), \
                       "Absolute path to the config file")
        ("beamFile", opt::value<string>(), "Beam file defining X-ray beam")
        ("geomFile", opt::value<string>(), \
                     "Geometry file defining diffraction geometry")
        ("rotationAxis", opt::value<string>()->default_value("xyz"), \
                         "Euler rotation convention")
        ("numSlices", opt::value<int>(), \
                      "Number of time-slices to use from \
                      Photon Matter Interaction (PMI) file")
        ("sliceInterval", opt::value<int>()->default_value(1), \
                          "Calculates photon field at every slice interval")
        ("pmiStartID", opt::value<int>()->default_value(1), \
                       "First Photon Matter Interaction (PMI) file ID to use")
        ("pmiEndID", opt::value<int>()->default_value(1), \
                     "Last Photon Matter Interaction (PMI) file ID to use")
        ("numDP", opt::value<int>()->default_value(1), \
                  "Number of diffraction patterns per PMI file")
        ("calculateCompton", opt::value<bool>()->default_value(0), \
                 "If 1, includes Compton scattering in the diffraction pattern")
        ("uniformRotation", opt::value<bool>()->default_value(0), \
                            "If 1, rotates the sample uniformly in SO(3)")
        ("saveSlices", opt::value<int>()->default_value(0), \
                       "If 1, saves time-slices of the photon field \
                        in hdf5 under /misc/photonField")
        ("gpu", opt::value<int>()->default_value(0), \
                "If 1, uses NVIDIA CUDA for faster calculation")
        ("help", "produce help message")
    ;

    // Variable to store our command line arguments
    opt::variables_map vm;

    // Parsing and storing arguments
    opt::store(opt::parse_command_line(argc, argv, desc), vm);
	opt::notify(vm);

	// Print input arguments
    if (vm.count("help")) {
        std::cout << desc << "\n";
        exit(0);
    }

	if (comm->rank() == master) {
		if (vm.count("inputDir"))
    		cout << "inputDir: " << vm["inputDir"].as<string>() << endl;
		if (vm.count("outputDir"))
    		cout << "outputDir: " << vm["outputDir"].as<string>() << endl;
		if (vm.count("configFile"))
    		cout << "configFile: " << vm["configFile"].as<string>() << endl;
		if (vm.count("beamFile"))
    		cout << "beamFile: " << vm["beamFile"].as<string>() << endl;
		if (vm.count("geomFile"))
    		cout << "geomFile: " << vm["geomFile"].as<string>() << endl;
		if (vm.count("rotationAxis"))
    		cout << "rotationAxis: " << vm["rotationAxis"].as<string>() << endl;
		if (vm.count("numSlices"))
    		cout << "numSlices: " << vm["numSlices"].as<int>() << endl;
		if (vm.count("sliceInterval"))
    		cout << "sliceInterval: " << vm["sliceInterval"].as<int>() << endl;
		if (vm.count("pmiStartID"))
    		cout << "pmiStartID: " << vm["pmiStartID"].as<int>() << endl;
		if (vm.count("pmiEndID"))
    		cout << "pmiEndID: " << vm["pmiEndID"].as<int>() << endl;
		if (vm.count("numDP"))
    		cout << "numDP: " << vm["numDP"].as<int>() << endl;
		if (vm.count("calculateCompton"))
    		cout << "calculateCompton: " << vm["calculateCompton"].as<bool>() \
    		     << endl;
		if (vm.count("uniformRotation"))
    		cout << "uniformRotation: " << vm["uniformRotation"].as<bool>() \
    		     << endl;
		if (vm.count("saveSlices"))
    		cout << "saveSlices: " << vm["saveSlices"].as<int>() << endl;
		if (vm.count("gpu"))
    		cout << "gpu: " << vm["gpu"].as<int>() << endl;
	}
	return vm;
} // end of parse_input

