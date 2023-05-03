
%% Baseband Signal Generation
function Mix = baseband_signal_generation(range_vector, vel_vector,theta_vector,channel_index)
global c range Nd Nr Tchirp slope fc no_of_targets temp d snr_db data_collection_start_time TRRI Ts
% Timestamp for running the displacement scenario for every sample on each
% chirp
t = zeros(Nr*Nd);
for chirp = 1:Nd
    per_chirp_sample_times = (0:Nr-1)*Ts +data_collection_start_time +(chirp-1)*TRRI;
    start_index = (chirp-1)*Nr +1;
    end_index = start_index +Nr-1;
    t(start_index:end_index) = per_chirp_sample_times;
end

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
Mix = Mix + complex(randn(1,length(t))*sqrt(noise_pow/2),randn(1,length(t))*sqrt(noise_pow/2));
end




