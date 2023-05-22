% Util Function to Run Python Model from matlab itself. 
% Set to run both on Windows and Unix based environments 
% Need to set python virtual environment file path here
function net = load_pytorch_model(input)
    mydir  = pwd;
    idcs = 0;
    if isunix
        idcs   = strfind(mydir,'/');
    else
        idcs = strfind(mydir,'\');
    end
    newdir = mydir(1:idcs(end)-1);
    input_file = fullfile(newdir,'dataset',"temp_input");
    output_file = fullfile(newdir,'dataset',"temp_output");

    % For pip based environment
    venv = fullfile(newdir,'venv','bin','python');

    % For Anaconda based environment
    %venv = '\Users\Admin\anaconda3\envs\py39\python.exe';
    python = fullfile(newdir,'python','run_model.py');
    save(input_file,"input");
    system(venv + " "+python);
    net = load(output_file).output;
    delete(input_file+'.mat');
    delete(output_file+'.mat');
end