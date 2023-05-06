%% Generate Simulated Data of Sensors
% Output is 6D data with following information:
% 1st Index: Index of sample
% 2nd Index: Sensor Index
% 3rd Index: Dimension for storing real and imaginary values
% 4rd Index: Number of samples in one chirp
% 5th Index: chirps in one sequence
% 6th Index: Channel Index
function output = generate_simulated_data(is_random)
    global Nd Nr no_of_channels no_of_sensors
    no_of_samples = 100;
    output = zeros(no_of_samples,no_of_sensors,2,Nr,Nd,no_of_channels);
    for row = 1:no_of_samples
        output(row,:,:,:,:,:) = generate_simulated_input(is_random); 
    end
end