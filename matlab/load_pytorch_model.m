function net = load_pytorch_model(input)
    mydir  = pwd;
    idcs   = strfind(mydir,'\');
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