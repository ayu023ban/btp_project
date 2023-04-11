function visualize_output(data)
global max_vel Nd Nr max_range no_of_sensors
temp = size(data);
temp = temp(2:4);
sensors_count = size(data);
sensors_count = min(sensors_count(1),no_of_sensors);

for sensor = 1:sensors_count
    output = reshape(data(sensor,:,:,:),temp);
    signal_fft3 = fftn(output);
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
end