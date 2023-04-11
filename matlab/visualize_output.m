function visualize_output(data)
global max_vel Nd Nr max_range 
signal_fft3 = fftn(data);
signal_fft3 = fftshift (signal_fft3);
signal_fft3 = abs(signal_fft3);
signal_fft3 = signal_fft3(:,:,1);
doppler_axis = linspace(-max_vel,max_vel,Nd);
range_axis = linspace(-max_range,max_range,Nr)*((Nr/2)/(max_range));
figure;
s = surf(doppler_axis,range_axis,signal_fft3);
s.EdgeColor = 'none';
% view(2);
title('Amplitude and Range From FFT3');
xlabel('Speed');
ylabel('Range');
zlabel('Amplitude');
end