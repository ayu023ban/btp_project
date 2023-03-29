function single_output = generate_simulated_input()
    global Nd Nr Tchirp no_of_channels target_velocities no_of_sensors
    global sensors_coordinates sensor_directions target_coordinates
    res = get_range_vel_wrt_sensors(sensors_coordinates,target_coordinates,target_velocities,sensor_directions);
    single_output = zeros(no_of_sensors,2,Nr,Nd,no_of_channels);
    for sensor =1:no_of_sensors
        range_vector = res(sensor,:,1);
        vel_vector = res(sensor,:,2);
        theta_vector = res(sensor,:,3);
        t = linspace(0,Nd*Tchirp,Nr*Nd);
        Mix = zeros(no_of_channels,length(t));
        for channel_index = 1:no_of_channels
            Mix(channel_index,:) = baseband_signal_generation(range_vector, vel_vector,theta_vector,channel_index);
            % output(row,sensor,1,:,:,channel_index) = reshape(real(Mix(channel_index,:)),[Nr,Nd]);
            % output(row,sensor,2,:,:,channel_index) = reshape(imag(Mix(channel_index,:)),[Nr,Nd]);
            single_output(sensor,1,:,:,channel_index) = reshape(real(Mix(channel_index,:)),[Nr,Nd]);
            single_output(sensor,2,:,:,channel_index) = reshape(imag(Mix(channel_index,:)),[Nr,Nd]); 
        end
    end
    set_random_target()
end