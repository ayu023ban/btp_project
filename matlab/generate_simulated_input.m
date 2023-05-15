function single_output = generate_simulated_input()
    global Nd Nr no_of_channels no_of_sensors
    res = get_range_vel_wrt_sensors();
    single_output = zeros(no_of_sensors,Nr,Nd,no_of_channels);
    for sensor =1:no_of_sensors
        range_vector = res(sensor,:,1);
        vel_vector = res(sensor,:,2);
        theta_vector =res(sensor,:,3);
        Mix = zeros(no_of_channels,Nr*Nd);
        for channel_index = 1:no_of_channels
            Mix(channel_index,:) = baseband_signal_generation(range_vector, vel_vector,theta_vector,channel_index);
            single_output(sensor,:,:,channel_index) = reshape(Mix(channel_index,:),[Nr,Nd]);
        end
    end
end