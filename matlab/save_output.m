function save_output(output,file_name)
    global max_vel max_range Nr Nd
    mydir  = pwd;
    idcs   = strfind(mydir,'/');
    newdir = mydir(1:idcs(end)-1);
    Folder = fullfile(newdir,'dataset',file_name);
    save(Folder,'output',"max_range","max_vel","Nd", "Nr");
end