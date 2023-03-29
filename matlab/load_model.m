mydir  = pwd
idcs   = strfind(mydir,'\');
newdir = mydir(1:idcs(end)-1);
Folder = fullfile(newdir,'python','model.pt');

net = importNetworkFromPyTorch(Folder)
