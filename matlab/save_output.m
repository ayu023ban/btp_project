function save_output(data,file_name)
    mydir  = pwd;
    idcs   = strfind(mydir,'/');
    newdir = mydir(1:idcs(end)-1);
    Folder = fullfile(newdir,'dataset',file_name);
    save(Folder,'data')
end