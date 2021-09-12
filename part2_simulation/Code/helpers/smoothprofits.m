%
% Use the simulated sales (nsims x nconsumers)
% and compute smoothed chebyshev profits
%The function takes in two parameters, surplus and simulated sales
%It then outputs smoothed profits 
function [profits] = smoothprofits(sales,surplus,mc)
    loadProductData;
    
    sales(sales==0)=J+1;
    % incorporate outside good
    margins=[margins;0];
    cost1=[cost1;0];

    % Retailer profits
    profits.retail= quicksmooth(mean(margins(sales))',1);
    profits.onlychoc= quicksmooth(mean(margins(sales).*ismember(sales,chocolate)),1);

    % consumer surplus
    profits.surplus= quicksmooth(surplus',1);

    % Chocolate Sales
    profits.marsQ = quicksmooth(mean(ismember(sales,mars)),1);
    profits.marsExtraQ = quicksmooth(mean(ismember(sales,marsextra)),0);
    profits.hersheyQ = quicksmooth(mean(ismember(sales,hershey)),0);
    profits.nestleQ = quicksmooth(mean(ismember(sales,nestle)),0);
   
    % Chocolate Profits
    profits.mars = mean(cost1(mars)-mc)*profits.marsQ;
    profits.marsExtra = mean(cost1(mars)-mc)*profits.marsExtraQ;
    profits.hershey = mean(cost1(hershey)-mc)*profits.hersheyQ; 
    profits.nestle = mean(cost1(nestle)-mc)*profits.nestleQ;
    
    % Chocolate Profits
    %profits.mars = mean(cost1(mars)-.15)*profits.marsQ;
    %profits.hershey = mean(cost1(hershey)-.15)*profits.hersheyQ; 
    %profits.nestle = mean(cost1(nestle)-.15)*profits.nestleQ;
    
    % Chocolate Profits
    %profits.mars = mean(cost1(mars))*profits.marsQ;
    %profits.hershey = mean(cost1(hershey))*profits.hersheyQ; 
    %profits.nestle = mean(cost1(nestle))*profits.nestleQ;

    %profits.nestle = quicksmooth(mean(cost1(sales).*ismember(sales,nestle)),0);
end
