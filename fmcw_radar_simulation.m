clear all;
close all;
clc;

global c range max_vel max_range Nd Nr range_res B Tchirp slope fc no_of_targets

%% chip limits
c = 3e8;
max_range = 200;
range_res = 1;
max_vel = 100; % m/s

%% chirp using the requirements above.
B = c / (2*range_res);
Tchirp = 5.5 * 2 * (max_range/c);
slope = B/Tchirp;

fc= 77e9;             %carrier freq
                                                          
%The number of chirps in one sequence.
Nd=128;

%The number of samples on each chirp. 
Nr=1024;


sensors_coordinates = [0,0,0];
target_coordinates = [110,0,0;0,80,0];
target_velocities = [20,0,0;0,40,0];
no_of_sensors = size(sensors_coordinates,1);
no_of_targets = size(target_coordinates,1);


%% Calling of Functions
 res = get_range_vel_wrt_sensors(sensors_coordinates,target_coordinates,target_velocities);
 for sensor =1:no_of_sensors
     range_vector = res(sensor,:,1);
     vel_vector = res(sensor,:,2);
     Mix = baseband_signal_generation(range_vector, vel_vector); 
     RDM = range_doppler_response(Mix);
     visualize_fmcw_radar_baseband_signals(RDM)
 end

%% Baseband Signal Generation
function Mix = baseband_signal_generation(range_vector, vel_vector)
global c range Nd Nr Tchirp slope fc no_of_targets
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

for target_index= 1:no_of_targets
    range = range_vector(target_index);
    vel = vel_vector(target_index);
    weight = weights(target_index);

    for i=1:length(t)         
      r_t(i) = range + (vel*t(i));
      td(i) = (2 * r_t(i)) / c;
    
      Tx(i)   = cos(2*pi*(fc*t(i) + (slope*t(i)^2)/2 ) );
      Rx(i)   = cos(2*pi*(fc*(t(i) -td(i)) + (slope * (t(i)-td(i))^2)/2 ) );
        
      Mix(i) = Mix(i) + Tx(i) .* Rx(i);
    end
end
end

%% RANGE DOPPLER RESPONSE
function RDM = range_doppler_response(Mix)
global Nd Nr
Mix=reshape(Mix,[Nr,Nd]);

signal_fft2 = fft2(Mix,Nr,Nd);

% Taking just one side of signal from Range dimension.
signal_fft2 = signal_fft2(1:Nr/2,1:Nd);
signal_fft2 = fftshift (signal_fft2);

RDM = abs(signal_fft2);
% RDM = 10*log10(RDM) ;
end

%% Visualize fmcw range doppler response
function visualize_fmcw_radar_baseband_signals(RDM)
global max_vel Nd Nr max_range 
doppler_axis = linspace(-max_vel,max_vel,Nd);
range_axis = linspace(-max_range,max_range,Nr/2)*((Nr/2)/(max_range*2));

figure,surf(doppler_axis,range_axis,RDM);
title('Amplitude and Range From FFT2');
xlabel('Speed');
ylabel('Range');
zlabel('Amplitude');

end

