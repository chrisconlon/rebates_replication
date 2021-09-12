%The function takes in a multidimensional dataframe as a parameter 
%which contains information on sales data and the ds3 dataset structure.
%The function outputs calculations for smoothed chebyshev
%profits including retail amounts with and without the rebate as well as
%for machines stocked with mars bars by solving appropriate dynamic
%programming problems
function [profits] = calc_profits(fn,mc_0)
load('../Raw Data/main-short.mat');
%Load State Variables
load('../Output/statevars.mat');
load(fn,'sales','CSVec');
%Set base parameters
fcvec=10; xx=ads;

% for mc=0
if mc_0 == 0
    rebsize = 0.16;
% for mc=15
elseif mc_0 == 0.15
    rebsize = .222;
else
    error("Marginal Cost not Properly Specified")
end

%Obtain Smopth Chebyshev payoffs
payoffs = smoothprofits(sales,CSVec,0.15);

if fn == '../Output/SalesHM-mle.mat'
    save('../Table Output/payoffs-mc15.mat','payoffs')
end

%Retail Rebate amount with mars bars payoffs
retailerrebate= payoffs.retail+payoffs.mars.*rebsize;

%Solve dynamic programming for retailer rebate, mars bars payoffs and
%retail payoffs
[resRReb]=solveDP(xx,retailerrebate,fcvec, 1, 600);
[resNReb]=solveDP(xx,payoffs.retail,fcvec, 1, 600);
[resMars]=solveDP(xx,payoffs.mars,0, 1, 600);

%Return the optimal policy for profits according to retailer payoffs,
%retailer rebates and mars bars
profits.Retail =resNReb.Vbar';
profits.RetailR =resRReb.Vbar';
profits.Mars =resMars.Vbar';

end
