
%% Baseband Signal Generation
function Mix = baseband_signal_generation(range_vector, vel_vector,theta_vector,channel_index)
global c range Nd Nr Tchirp slope fc no_of_targets  d snr_db data_collection_start_time TRRI Ts
% Timestamp for running the displacement scenario for every sample on each
% chirp
t = zeros(Nr*Nd,1);
for chirp = 1:Nd
    per_chirp_sample_times = (0:1:Nr-1)*Ts +data_collection_start_time +(chirp-1)*TRRI;
    start_index = (chirp-1)*Nr +1;
    end_index = start_index +Nr-1;
    t(start_index:end_index) = per_chirp_sample_times;
end

%Creating the vectors for Tx, Rx and Mix based on the total samples input.
Mix = zeros(length(t),1); %beat signal

%% Signal generation and Moving Target simulation
% Running the radar scenario over the time. 
weights = rand(no_of_targets,1);
weights = weights/sum(weights);

snr = 10^(snr_db/10);
sig_pow = 1;
noise_pow = sig_pow/snr;

for target_index= 1:no_of_targets
    range = range_vector(target_index);
    vel = vel_vector(target_index);
    theta = theta_vector(target_index);
    weight = weights(target_index);
    r_t = range + (vel*t) + (channel_index-1)*d*sin(theta);
    td = (2 * r_t) / c;
    phase_tx = 2*pi*(fc*t + (slope*t.*t)/2 );
    phase_rx = 2*pi*(fc*(t-td) + (slope * (t-td).*(t-td))/2 ) ;
    phase_diff = phase_tx-phase_rx;
    Mix = Mix + weight*complex(cos(phase_diff),sin(phase_diff));
end
% Adding AWGN Noise
Mix = Mix + complex(randn(length(t),1)*sqrt(noise_pow/2),randn(length(t),1)*sqrt(noise_pow/2));
end




