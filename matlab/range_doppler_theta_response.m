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

