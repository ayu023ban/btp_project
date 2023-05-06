%% Generate Simulated Data of Sensors
% Output is 6D data with following information:
% 1st Index: Index of sample
% 2nd Index: Sensor Index
% 3rd Index: Number of samples in one chirp
% 4th Index: chirps in one sequence
% 5th Index: Channel Index
function output = generate_grid_simulated_data()
    global Nd Nr no_of_channels no_of_sensors target_coordinates target_velocities
    velocity_combinations = get_velocity_combinations();
    position_combinations = get_position_combinations();
    target_coordinates = transpose(reshape(position_combinations(1,:),2,[]));

    no_of_samples = length(velocity_combinations)*length(position_combinations);
    output = zeros(no_of_samples,no_of_sensors,Nr,Nd,no_of_channels);
    row = 1;
    for position_index = 1:length(position_combinations)
        for velocity_index = 1:length(velocity_combinations)
            target_coordinates = transpose(reshape(position_combinations(position_index,:),2,[]));
            target_coordinates(:,3) = 0;
            target_velocities = transpose(reshape(velocity_combinations(velocity_index,:),2,[]));
            target_velocities(:,3) = 0;
            output(row,:,:,:,:) = generate_simulated_input(); 
            row = row+1;
        end
    end
end

function position_combinations = get_position_combinations()
    global max_range no_of_targets
    position_grid_size = [3,3];
    x_positions = (1:position_grid_size(1)-1)/position_grid_size(1)*max_range;
    y_positions = (1:position_grid_size(2)-1)/position_grid_size(2)*max_range;
    positions_available = get_possible_pairs(x_positions,y_positions,max_range);
    position_combinations = choosek(positions_available,no_of_targets);
end

function velocity_combinations = get_velocity_combinations()
    global max_vel no_of_targets
    velocity_grid_size = [3,3];
    x_velocity = (-(velocity_grid_size(1)-1):velocity_grid_size(1)-1)/velocity_grid_size(1)*max_vel;
    y_velocity = (-(velocity_grid_size(2)-1):velocity_grid_size(2)-1)/velocity_grid_size(2)*max_vel;
    velocities_available = get_possible_pairs(x_velocity,y_velocity,max_vel);
    velocity_combinations = choosek(velocities_available,no_of_targets);
end

function output = choosek(v,k)
sz = length(v);
indices = 1:sz;
choices = nchoosek(indices,k);
sz = size(choices);
output = [];
for x = 1:sz(2)
    output = [output,v(choices(:,x),:)];
end
end


function output =  get_possible_pairs(a,b,max_value)
    [A,B] = meshgrid(a,b);
    c=cat(2,A',B');
    output = reshape(c,[],2);
    norm_values = vecnorm(output,2,2);
    output(norm_values>max_value,:) = [];
end