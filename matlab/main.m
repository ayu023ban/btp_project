clear all;
close all;
clc;

global c max_vel max_range Nd Nr range_res B Tchirp slope fc 
global no_of_targets d no_of_channels snr_db TRRI vel_res 
global sensors_coordinates sensor_directions target_coordinates target_velocities no_of_sensors
tic;
set_configuration()

% output = generate_random_simulated_data(10);

output = generate_grid_simulated_data();
size(output)
save_output(output,"training_dataset.mat");
toc
