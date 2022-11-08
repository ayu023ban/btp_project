%% Generate Simulated Data of Sensors
% Output is 6D data with following information:
% 1st Index: Index of sample
% 2nd Index: Sensor Index
% 3rd Index: Dimension for storing real and imaginary values
% 4rd Index: Number of samples in one chirp
% 5th Index: chirps in one sequence
% 6th Index: Channel Index
function output = generate_simulated_data()
    global Nd Nr Tchirp no_of_channels target_velocities no_of_sensors
    global sensors_coordinates sensor_directions target_coordinates
    res = get_range_vel_wrt_sensors(sensors_coordinates,target_coordinates,target_velocities,sensor_directions);
    no_of_samples = 100;
    output = zeros(no_of_samples,no_of_sensors,2,Nr,Nd,no_of_channels);
    for row = 1:no_of_samples
        set_random_target()
        for sensor =1:no_of_sensors
            range_vector = res(sensor,:,1);
            vel_vector = res(sensor,:,2);
            theta_vector = res(sensor,:,3);
            t = linspace(0,Nd*Tchirp,Nr*Nd);
            Mix = zeros(no_of_channels,length(t));
            for channel_index = 1:no_of_channels
                Mix(channel_index,:) = baseband_signal_generation(range_vector, vel_vector,theta_vector,channel_index);
                output(row,sensor,1,:,:,channel_index) = reshape(real(Mix(channel_index,:)),[Nr,Nd]);
                output(row,sensor,2,:,:,channel_index) = reshape(imag(Mix(channel_index,:)),[Nr,Nd]);
            end
        end
    end
end