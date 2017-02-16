clear all; close all; clc; 
tic;
%timestep:
timestep = 8000;

%Input file names
filename000 = strcat('simData_',int2str(timestep),'.h5');
inf0 = strcat('/data/',int2str(timestep),'/particles/e/position/');
inf1 = strcat('/data/',int2str(timestep),'/particles/e/momentum/');

x_data = h5read(filename000,strcat(inf0,'x'));
x_data_unit = hdf5read(filename000,strcat(inf0,'x'),'unitSI');
x = x_data*x_data_unit;

y_data = h5read(filename000,strcat(inf0,'y'));
y_data_unit = hdf5read(filename000,strcat(inf0,'y'),'unitSI');
y = y_data*y_data_unit;

z_data = h5read(filename000,strcat(inf0,'z'));
z_data_unit = hdf5read(filename000,strcat(inf0,'z'),'unitSI');
z = z_data*z_data_unit;

px_data = h5read(filename000,strcat(inf1,'x'));
px_data_unit = hdf5read(filename000,strcat(inf1,'x'),'unitSI');
px = px_data*px_data_unit;

py_data = h5read(filename000,strcat(inf1,'y'));
py_data_unit = hdf5read(filename000,strcat(inf1,'y'),'unitSI');
py = py_data*py_data_unit;

pz_data = h5read(filename000,strcat(inf1,'z'));
pz_data_unit = hdf5read(filename000,strcat(inf1,'z'),'unitSI');
pz = pz_data*pz_data_unit;

me = 9.1E-27;
c0 = 3e8;
psquare = px.^2 + py.^2 + pz.^2;
gamma = sqrt( 1 + psquare./((me*c0)^2));

thetax = atan(px./py);
thetaz = atan(pz./py);
timey = y./c0;
Energy = 0.511*gamma;


DATA = cat( 6, timey, x, thetax, z, thetaz, gamma);


dlmwrite('Data_PIC2Simplex.txt',DATA,'delimiter','\t');

toc
