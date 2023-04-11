function visualize_output(data)
global max_vel Nd Nr max_range no_of_sensors
dims = ndims(data);
if(dims==5)
    temp = size(data);
    new_data = zeros(temp(1),temp(3),temp(4),temp(5));
    for sensor = 1:no_of_sensors
        new_data(sensor,:,:,:) = complex(data(sensor,1,:,:,:),data(sensor,2,:,:,:));
    end
data = new_data;
% else
%     temp = data(1,:,:,:);
%     sz = size(data);
%     last_index = sz(1);
%     data(1,:,:,:) = data(last_index,:,:,:);
%     data(last_index,:,:,:) = temp;
end
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