clear all;
close all;
clc;

global c max_vel max_range Nd Nr range_res B Tchirp slope fc 
global no_of_targets d no_of_channels snr_db TRRI vel_res 
global sensors_coordinates sensor_directions target_coordinates target_velocities no_of_sensors
global ground_target_coordinates ground_target_velocities
tic;
set_configuration()

% output = generate_random_simulated_data(10);

%output= generate_grid_simulated_data();
%size(output,1)
output = generate_simulated_input();
visualize_output(output);
%save_output(output,"training_dataset.mat");
toc
