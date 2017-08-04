function stateInfo = saveStateInfo(track_result, frame_num)

try
     sorted_result = sortrows(track_result,6);
     detect_num = size(sorted_result,1);
catch
    detect_num = 0;
    
    stateInfo.X(:,1) = zeros(frame_num,1);
    stateInfo.Y(:,1) = zeros(frame_num,1);
    stateInfo.Xi(:,1) = zeros(frame_num,1);
    stateInfo.Yi(:,1) = zeros(frame_num,1);
    stateInfo.W(:,1) = zeros(frame_num,1);
    stateInfo.H(:,1) = zeros(frame_num,1);
end

stateInfo.F = frame_num;
stateInfo.frameNums = 1:frame_num;
index = 0;
cur_id = -1;

for i = 1:detect_num
    if (cur_id ~= sorted_result(i,6))
        cur_id = sorted_result(i,6);
        index = index + 1;
        stateInfo.X(:,index) = zeros(frame_num,1);
        stateInfo.Y(:,index) = zeros(frame_num,1);
        stateInfo.Xi(:,index) = zeros(frame_num,1);
        stateInfo.Yi(:,index) = zeros(frame_num,1);
        stateInfo.W(:,index) = zeros(frame_num,1);
        stateInfo.H(:,index) = zeros(frame_num,1);
    end
    bbox = sorted_result(i,:);
    n = bbox(1,5);
    stateInfo.X(n,index) = bbox(1,1)+0.5*bbox(1,3);
    stateInfo.Y(n,index) = bbox(1,2)+bbox(1,4);
    stateInfo.Xi(n,index) = stateInfo.X(n,index);
    stateInfo.Yi(n,index) = stateInfo.Y(n,index);
    stateInfo.W(n,index) = bbox(1,3);
    stateInfo.H(n,index) = bbox(1,4);   
end
