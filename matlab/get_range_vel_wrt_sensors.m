%% This Function gives range and velocity with respect to each sensor
% Output is 3d array in which 1st index denotes sensor, second index denote
% target and 3rd index have 2 elements- first range and second velocity
function output = get_range_vel_wrt_sensors()
global sensors_coordinates target_coordinates target_velocities no_of_sensors no_of_targets
output = zeros(no_of_sensors,no_of_targets,3);
for sensor = 1:no_of_sensors
    for target = 1:no_of_targets
        range_vel_theta = get_r_v(target_coordinates(target,:),target_velocities(target,:),sensors_coordinates(sensor,:));
        output(sensor,target,:) = range_vel_theta;
    end
end
end



function r_v =  get_r_v(target_coordinate,target_velocity,sensor_coordinate)
r_v = zeros(3,1);
r_v(1) = floor(sqrt(sum((target_coordinate - sensor_coordinate) .^ 2)));
R = target_coordinate - sensor_coordinate;
costheta = max(min(dot(target_velocity,R)/(norm(R)*norm(target_velocity)),1),-1);
r_v(2) = norm(target_velocity)*costheta;
TanTheta = R(1)/R(2);
r_v(3) = real(atand(TanTheta))*pi/180;
end