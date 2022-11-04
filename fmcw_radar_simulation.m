clear all;
close all;
clc;

global c max_vel max_range Nd Nr range_res B Tchirp slope fc no_of_targets d no_of_channels snr_db


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
target_velocities = [40,0,0;1,0,0];
no_of_sensors = size(sensors_coordinates,1);
no_of_targets = size(target_coordinates,1);
no_of_channels = 4;
d = 2e-3;

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
%           RDM = range_doppler_response(Mix(channel_index,:));
%           visualize_fmcw_radar_baseband_signals(RDM)
     end
     RDTM = range_doppler_theta_response(Mix);
     for channel_index = 1:no_of_channels
         visualize_fmcw_radar_baseband_signals(RDTM(:,:,channel_index));
     end
 end

%% Baseband Signal Generation
function Mix = baseband_signal_generation(range_vector, vel_vector,theta_vector,channel_index)
global c range Nd Nr Tchirp slope fc no_of_targets temp d snr_db
% Timestamp for running the displacement scenario for every sample on each
% chirp
t=linspace(0,Nd*Tchirp,Nr*Nd); %total time for samples

%Creating the vectors for Tx, Rx and Mix based on the total samples input.
Tx=zeros(1,length(t)); %transmitted signal
Rx=zeros(1,length(t)); %received signal
Mix = zeros(1,length(t)); %beat signal

%Similar vectors for range_covered and time delay.
r_t=zeros(1,length(t));
td=zeros(1,length(t));

%% Signal generation and Moving Target simulation
% Running the radar scenario over the time. 
weights = rand(1, no_of_targets);
weights = weights/sum(weights);

snr = 10^(snr_db/10);
sig_pow = 1;
noise_pow = sig_pow/snr;

for target_index= 1:no_of_targets
    range = range_vector(target_index);
    vel = vel_vector(target_index);
    theta = theta_vector(target_index);
    weight = weights(target_index);
    for i=1:length(t)         
      r_t(i) = range + (vel*t(i)) + (channel_index-1)*d*sin(theta);
      td(i) = (2 * r_t(i)) / c;
      new_time = t(i)-td(i);

      Tx(i) = 2*pi*(fc*t(i) + (slope*t(i)^2)/2 );
      Rx(i) = 2*pi*(fc*(new_time) + (slope * (new_time)^2)/2 ) ;
      temp = Tx(i)-Rx(i);
      Mix(i) = Mix(i) + weight .* complex(cos(temp),sin(temp));
    end
end
% Adding AWGN Noise
Mix = Mix + randn(1,length(t))*sqrt(noise_pow);
end


%% 3D- Range Doppler Theta Response
function RDTM = range_doppler_theta_response(Mix)
global Nd Nr no_of_channels
a = zeros(Nr,Nd,no_of_channels);
for channel_index = 1:no_of_channels
    a(:,:,channel_index) = reshape(Mix(channel_index,:),[Nr,Nd]);
end
signal_fft3 = fftn(a);
signal_fft3 = fftshift (signal_fft3);

RDTM = abs(signal_fft3);
end


%% RANGE DOPPLER RESPONSE
function RDM = range_doppler_response(Mix)
global Nd Nr
Mix=reshape(Mix,[Nr,Nd]);

signal_fft2 = fft2(Mix,Nr,Nd);

% Taking just one side of signal from Range dimension.
signal_fft2 = fftshift (signal_fft2);

RDM = abs(signal_fft2);
% RDM = 10*log10(RDM) ;
end

%% Visualize fmcw range doppler response
function visualize_fmcw_radar_baseband_signals(RDM)
global max_vel Nd Nr max_range 
doppler_axis = linspace(-max_vel,max_vel,Nd);
range_axis = linspace(-max_range,max_range,Nr)*((Nr/2)/(max_range));

figure;
s = surf(doppler_axis,range_axis,RDM);
s.EdgeColor = 'none';
view(2);
title('Amplitude and Range From FFT2');
xlabel('Speed');
ylabel('Range');
zlabel('Amplitude');

end

