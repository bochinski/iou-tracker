function [stateInfo, speed] = run_tracker(curSequence, baselinedetections)
%% tracker configuration

%% Mask R-CNN (frcnn)
sigma_l = 0;
sigma_h = 0.95;
sigma_iou = 0.6;
t_min = 7;

% %% R-CNN
% sigma_l = 0;
% sigma_h = 0.7;
% sigma_iou = 0.5;
% t_min = 2;

% %% ACF
% sigma_l = 0;
% sigma_h = 0.3;
% sigma_iou = 0.5;
% t_min = 3;

% %% CompACT
% sigma_l = 0;
% sigma_h = 0.2;
% sigma_iou = 0.4;
% t_min = 2;

% %% EB
% sigma_l = 0;
% sigma_h = 0.8;
% sigma_iou = 0.5;
% t_min = 2;

%% running tracking algorithm
try
    ret = py.iou_tracker.track_iou_matlab_wrapper(py.numpy.array(baselinedetections(:).'), sigma_l, sigma_h, sigma_iou, t_min);
    
catch exception
    disp('error while calling the python tracking module: ')
    disp(' ')
    disp(getReport(exception))
end
speed = ret{1};
track_result = cell2mat(reshape(ret{2}.cell.', 6, []).');

%% convert and save the mot style track_result
stateInfo = saveStateInfo(track_result, numel(curSequence.frameNums));
