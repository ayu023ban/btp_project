clear all;
close all;
clc;

global c max_vel max_range Nd Nr range_res B Tchirp slope fc 
global no_of_targets d no_of_channels snr_db TRRI vel_res 
global sensors_coordinates sensor_directions target_coordinates target_velocities no_of_sensors
tic;
set_configuration()
% 
% %% Calling of Functions
%  res = get_range_vel_wrt_sensors(sensors_coordinates,target_coordinates,target_velocities,sensor_directions);
% 
%  for sensor =1:1
%      range_vector = res(sensor,:,1);
%      vel_vector = res(sensor,:,2);
%      theta_vector = res(sensor,:,3);
%      t = linspace(0,Nd*Tchirp,Nr*Nd);
%      Mix = zeros(no_of_channels,length(t));
%      for channel_index = 1:no_of_channels
%          Mix(channel_index,:) = baseband_signal_generation(range_vector, vel_vector,theta_vector,channel_index); 
% %          figure;
% %          plot(t(1:Nr),real(Mix(channel_index,1:Nr)));
% %          hold on;
% %          plot(t(1:Nr),imag(Mix(channel_index,1:Nr)));
% %          legend('Real part','Imaginary part')
% %          title('Timeseries Base-band signal');
% %          xlabel('time (in s)');
% %          ylabel('Amplitude');
%      end
%      RDTM = range_doppler_theta_response(Mix);
%      for channel_index = 1:no_of_channels
%         visualize_fmcw_radar_baseband_signals(RDTM(:,:,channel_index));
%      end
%  end
%output = generate_simulated_data();
%save_output(output,"output.mat");
input = generate_simulated_input();
net = load_pytorch_model(input);
temp = size(net);
temp = temp(2:4);
first_sensor_output = reshape(net(1,:,:,:),temp);
visualize_output(first_sensor_output);
toc
