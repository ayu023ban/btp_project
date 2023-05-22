%% Generate Simulated Data of Sensors
% Output is 5D data with following information:
% 1st Index: Index of sample
% 2nd Index: Sensor Index
% 3rd Index: Number of samples in one chirp
% 4th Index: chirps in one sequence
% 5th Index: Channel Index
function output = generate_random_simulated_data(no_of_samples)
    global Nd Nr no_of_channels no_of_sensors
    output = zeros(no_of_samples,no_of_sensors,Nr,Nd,no_of_channels);
    for row = 1:no_of_samples
        set_random_target()
        output(row,:,:,:,:) = generate_simulated_input(); 
    end
end