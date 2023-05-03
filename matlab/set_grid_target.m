function set_grid_target
    global target_coordinates target_velocities max_range max_vel grid_index grid_size no_of_targets

    
    target_coordinates(1,1:2) = grid_index./grid_size.*(max_range);
    target_velocities(1,1:2) = grid_index./grid_size.*(max_vel/2);
    no_of_targets = size(target_coordinates,1);
    target_coordinates(:,3)=0;
    target_velocities(:,:)=0;
    grid_index = mod(grid_index,grid_size)+[1,1]
end