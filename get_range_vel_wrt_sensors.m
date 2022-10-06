function output = get_range_vel_wrt_sensors(sensors_coordinates, target_coordinates, target_velocities)
global no_of_sensors no_of_targets
no_of_sensors = size(sensors_coordinates,1);
no_of_targets = size(target_coordinates,1);
output = zeros(no_of_sensors,no_of_targets,2);
for sensor = 1:no_of_sensors
    for target = 1:no_of_targets
        range_vel = get_r_v(target_coordinates(target,:),target_velocities(target,:),sensors_coordinates(sensor,:));
        output(sensor,target,:) = range_vel;
    end
end
end
function r_v =  get_r_v(target_coordinate,target_velocity,sensor_coordinate)
r_v = zeros(1,2);
r_v(1) = sqrt(sum((target_coordinate - sensor_coordinate) .^ 2));
R = target_coordinate - sensor_coordinate;
costheta = max(min(dot(target_velocity,R)/(norm(R)*norm(target_velocity)),1),-1);
r_v(2) = norm(target_velocity)*costheta;
end