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
