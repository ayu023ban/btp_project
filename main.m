Mix = baseband_signal_generation(range_vector, vel_vector);

RDM = range_doppler_response(Mix);

visualize_fmcw_radar_baseband_signals(RDM)