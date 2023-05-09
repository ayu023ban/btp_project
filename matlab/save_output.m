function save_output(output,file_name)
    global max_vel max_range Nr Nd no_of_channels vel_res range_res
    global ground_target_coordinates ground_target_velocities
    mydir  = pwd;
    if isunix
        idcs   = strfind(mydir,'/');
    else
        idcs = strfind(mydir,'\');
    end
    newdir = mydir(1:idcs(end)-1);
    Folder = fullfile(newdir,'dataset',file_name);
    save(Folder,'output','ground_target_coordinates','ground_target_velocities',"max_range","max_vel","Nd", "Nr", "no_of_channels","vel_res","range_res",'-v7.3','-nocompression');
end