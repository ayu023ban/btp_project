
function set_random_target()
    global target_coordinates target_velocities max_range max_vel
    target_coordinates = rand(2,3).*(max_range/2);
    target_velocities = rand(2,3).*(max_vel/2);
    target_coordinates(:,3)=0;
    target_velocities(:,3)=0;
end