function [stateInfo, speed] = run_tracker(curSequence, baselinedetections)
%% tracker configuration
ttl = 0;
tracker_type = '';

%% v-iou tracker configurations
% %% Mask R-CNN (frcnn)
sigma_l = 0;
sigma_h = 0.98;
sigma_iou = 0.6;
t_min = 13;
ttl=6;
tracker_type='KCF2';

% %% CompACT
%sigma_l = 0;
%sigma_h = 0.3;
%sigma_iou = 0.5;
%t_min = 3;
%ttl=12;
%tracker_type='KCF2';

%% iou tracker configurations
% %% Mask R-CNN (frcnn)
%sigma_l = 0;
%sigma_h = 0.95;
%sigma_iou = 0.6;
%t_min = 7;

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
    if strcmp(tracker_type, '')
        ret = py.iou_tracker.track_iou_matlab_wrapper(py.numpy.array(baselinedetections(:).'), sigma_l, sigma_h, sigma_iou, t_min);
    else
        ret = py.viou_tracker.track_viou_matlab_wrapper(curSequence.imgFolder, py.numpy.array(baselinedetections(:).'), sigma_l, sigma_h, sigma_iou, t_min, ttl, tracker_type);
    end
catch exception
    disp('error while calling the python tracking module: ')
    disp(' ')
    disp(getReport(exception))
end
speed = ret{1};
track_result = cell2mat(reshape(ret{2}.cell.', 6, []).');

%% convert and save the mot style track_result
stateInfo = saveStateInfo(track_result, numel(curSequence.frameNums));
