%This function takes in two parameters and returns an evaluated hermite function. 
%The first parameter is a set of data used for the estimate. The second
%parameter is a boolean that determines whether the data is decreasing
function [y]=quicksmooth(x,decreasing)
    n=length(x);
    %Estimating a spline function from the provided data and boolean
    if decreasing,
        slm = slmengine([1:n],x,'decreasing','on');
    else
        slm = slmengine([1:n],x);
    end
    %Using the spline function to evaluate the Hermite function
    y=slmeval([1:n],slm)';
end
