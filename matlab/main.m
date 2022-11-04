clear all;
close all;
clc;

global c max_vel max_range Nd Nr range_res B Tchirp slope fc 
global no_of_targets d no_of_channels snr_db TRRI vel_res 
global sensors_coordinates sensor_directions target_coordinates target_velocities no_of_sensors

set_configuration()

%% Calling of Functions
 res = get_range_vel_wrt_sensors(sensors_coordinates,target_coordinates,target_velocities,sensor_directions);

 for sensor =1:no_of_sensors
     range_vector = res(sensor,:,1);
     vel_vector = res(sensor,:,2);
     theta_vector = res(sensor,:,3);
     t = linspace(0,Nd*Tchirp,Nr*Nd);
     Mix = zeros(no_of_channels,length(t));
     for channel_index = 1:no_of_channels
         Mix(channel_index,:) = baseband_signal_generation(range_vector, vel_vector,theta_vector,channel_index); 
     end
     RDTM = range_doppler_theta_response(Mix);
     save_output(RDTM,"output.mat");
%      for channel_index = 1:no_of_channels
%          visualize_fmcw_radar_baseband_signals(RDTM(:,:,channel_index));
%      end
 end
