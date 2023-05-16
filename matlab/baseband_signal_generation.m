
%% Baseband Signal Generation
function Mix = baseband_signal_generation(range_vector, vel_vector,theta_vector,channel_index)
global c Nd Nr slope fc no_of_targets  d snr_db data_collection_start_time TRRI Ts
% Timestamp for running the displacement scenario for every sample on each
% chirp
% t = zeros(Nr*Nd,1);

%Creating the vectors for Tx, Rx and Mix based on the total samples input.
Mix = zeros(Nr*Nd,1);%beat signal




%% Signal generation and Moving Target simulation
% Running the radar scenario over the time. 
weights = rand(no_of_targets,1);
weights = weights/sum(weights);

snr = 10^(snr_db/10);
sig_pow = 1;
noise_pow = sig_pow/snr;

for target_index= 1:no_of_targets
    r = range_vector(target_index);
    vel = vel_vector(target_index);
    theta = theta_vector(target_index);    
    weight =1;% weights(target_index);

    for chirp = 1:Nd
        t = (0:1:Nr-1)'*Ts +data_collection_start_time +(chirp-1)*TRRI;
        
        r_t = r + (vel*t);
        td = (2 * r_t - (channel_index-1)*d*sin(theta)) / c;
    
        phase_tx = 2*pi*(fc*(t-(chirp-1)*TRRI) + (slope*(t-(chirp-1)*TRRI).^2)*0.5);
        phase_rx = 2*pi*(fc*(t-td-(chirp-1)*TRRI) + (slope*(t-td-(chirp-1)*TRRI).^2)*0.5);
        phase_diff = phase_tx-phase_rx;
        start_index = (chirp-1)*Nr +1;
        end_index = start_index +Nr-1;
        Mix(start_index:end_index) = Mix(start_index:end_index) + weight*complex(cos(phase_diff),sin(phase_diff));
        % t(start_index:end_index) = %er_chirp_sample_times;
    end
    

    %phase_tx = 2*pi*(fc*t + (slope*t.*t)/2 );
    %phase_rx = 2*pi*(fc*(t-td) + (slope * (t-td).*(t-td))/2 ) ;
    %phase_diff = phase_tx-phase_rx;
    %Mix = Mix + weight*complex(cos(phase_diff),sin(phase_diff));
end
% Adding AWGN Noise
Mix = Mix + complex(randn(Nr*Nd,1)*sqrt(noise_pow/2),randn(Nr*Nd,1)*sqrt(noise_pow/2));
end




