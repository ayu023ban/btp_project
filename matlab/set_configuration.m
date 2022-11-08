function set_configuration()

global c max_vel max_range Nd Nr range_res B Tchirp slope fc 
global no_of_targets d no_of_channels snr_db TRRI vel_res 
global sensors_coordinates sensor_directions target_coordinates target_velocities no_of_sensors


%% chip limits
c = 3e8;
max_range = 100;
range_res = 1;

%% chirp using the requirements above.
B = c / (2*range_res);
Tchirp = 20 * 2 * (max_range/c);
TRRI = Tchirp;
slope = B/Tchirp;


fc= 77e9;             %carrier freq
                                                          
%The number of chirps in one sequence.
Nd=128;

%The number of samples on each chirp. 
Nr=256;

vel_res = c/(2*fc*TRRI*Nd);
max_vel = Nd/(2*vel_res);

snr_db = -9;


sensors_coordinates = [0,0,0;30,0,0];
sensor_directions = [0,1,0;0,1,0];
target_coordinates = [50,0,0;10,20,0];
target_velocities = [40,0,0;10,0,0];
no_of_sensors = size(sensors_coordinates,1);
no_of_targets = size(target_coordinates,1);
no_of_channels = 10;
d = 2e-3;

end