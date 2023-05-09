function visualize_output(data)
global max_vel Nd Nr max_range no_of_sensors target_coordinates no_of_channels range_res vel_res
temp = size(data);
temp = temp(2:4);
sensors_count = min(size(data,1),no_of_sensors);

Fr = dftmtx(Nr)/sqrt(Nr);
Fd = dftmtx(Nd)/sqrt(Nd);
Fa = dftmtx(no_of_channels)/sqrt(no_of_channels);
twodfft_output = zeros(temp);
reshape2dfftoutput = zeros(Nr*Nd,no_of_channels);
fft3doutput = zeros(Nr,Nd,no_of_channels);
effective3dfftout = zeros(Nr/2,Nd,no_of_channels);
dopplershiftoutput = zeros(Nr/2,Nd,no_of_channels);
for sensor = 1:sensors_count
    output = reshape(data(sensor,:,:,:),temp);
    for channel = 1:no_of_channels
        twodfft_output(:,:,channel) = Fr*output(:,:,channel)*transpose(Fd);
    end
    for channel = 1:no_of_channels
        reshape2dfftoutput(:,channel) = reshape(twodfft_output(:,:,channel),Nr*Nd,1);
    end
    reshape3dfftoutput = reshape2dfftoutput*transpose(Fa);
    for channel = 1:no_of_channels
        fft3doutput(:,:,channel) = reshape(reshape3dfftoutput(:,channel),Nr,Nd);
    end
    
    effective3dfftout(:,:,:) = fft3doutput(1:end/2,:,:);
    for channel = 1:no_of_channels
        dopplershiftoutput(:,end/2+1:end,channel) = effective3dfftout(:,1:end/2,channel);
        dopplershiftoutput(:,1:end/2,channel) = effective3dfftout(:,end/2+1:end,channel);
    end
    effective3dfftout = dopplershiftoutput;
    % signal_fft3 = fftn(output);
    % signal_fft3 = fftshift (signal_fft3);

    signal_fft3 = abs(effective3dfftout);
    signal_fft3 = signal_fft3(:,:,1);
    
    range_axis = (0:Nr/2-1)*range_res;
    doppler_axis = (-Nd/2:Nd/2-1)*vel_res;
    % keyboard;
    figure;
    s = surf(doppler_axis,range_axis,signal_fft3);

    s.EdgeColor = 'none';
    title('Amplitude and Range From FFT3');
    xlabel('Speed');
    ylabel('Range');
    zlabel('Amplitude');
    view(2);
    % legend('coordinates:',target_coordinates)
end
end