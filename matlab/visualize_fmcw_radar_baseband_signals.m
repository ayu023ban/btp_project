%% Visualize fmcw range doppler response
function visualize_fmcw_radar_baseband_signals(RDM)
global max_vel Nd Nr max_range 
doppler_axis = linspace(-max_vel,max_vel,Nd);
range_axis = linspace(-max_range,max_range,Nr)*((Nr/2)/(max_range));
figure;
s = surf(doppler_axis,range_axis,RDM);
s.EdgeColor = 'none';
view(2);
title('Amplitude and Range From FFT2');
xlabel('Speed');
ylabel('Range');
zlabel('Amplitude');

end