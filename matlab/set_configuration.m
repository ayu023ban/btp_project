function set_configuration()

global c max_vel max_range Nd Nr range_res B Tchirp slope fc 
global no_of_targets d no_of_channels snr_db TRRI vel_res 
global sensors_coordinates sensor_directions target_coordinates target_velocities no_of_sensors
global data_collection_start_time Ts Fs
%% chip limits
c = 3e8;

%% chirp using the requirements above.
% B = c / (2*range_res);
% Tchirp = 200 * 2 * (max_range/c)
% TRRI = Tchirp;
% slope = B/Tchirp

slope = 30e12;
Tchirp = 15e-6;
Fs = 20e6;
Ts = 1/Fs;
TRRI = 20e-6;
B = slope*Tchirp;
B/1e9
fc= 77e9;             

%carrier freq                                                      
%The number of chirps in one sequence.
Nd=32;

%The number of samples on each chirp. 
Nr=256;
range_res = c*Tchirp/(2*B*Ts*Nr);  
max_range = Nr/2*range_res;
vel_res = c/(2*fc*TRRI*Nd);
max_vel = vel_res*Nd/(2);
data_collection_start_time = 2*max_range/c*3;


data_collection_time = Nr*Ts;
total_measurement_time = Nd*TRRI;

max_t_prop = 2*max_range/c;
max_freq = slope*max_t_prop;
max_phase_change = 2*pi*max_freq*TRRI;

if(data_collection_time > Tchirp)
   fprintf('Error Data collection period exceeding Chirp duration time');
end

snr_db = 0;



sensors_coordinates = [0,0,0;10,0,0];
sensor_directions = [0,1,0;0,1,0];
target_coordinates = [-20,-20,0;-5,10,0];
target_velocities = [10,10,0;-10,20,0];
no_of_sensors = size(sensors_coordinates,1);
no_of_targets = size(target_coordinates,1);
no_of_targets = 1;
no_of_channels = 4;
d = 2e-3;

end