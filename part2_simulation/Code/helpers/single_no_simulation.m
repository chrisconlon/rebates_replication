%This function is a simulation which generates optimal effort policies and
%profits levels under them. It takes in 5 parameters, a function, a level
%of elasticity, a a fixed cost and two booleans which induce the usage of
%interquartile ranges and whether to calculate consumer surplus, The ouput
%of this simulation function is a matrix of optimal effort policies and
%corresponding profits. 
function [profits,policies] = single_no_simulation(fn,elas,fcvec,use_iqr,do_cs,mc_0)
if use_iqr,
    load('../Output/statevars_iqr.mat');
else,
    load('../Output/statevars.mat');
end
load(fn,'sales','CSVec');

% fix the magic number here(!) -- I fixed this but check that it works
payoffs = smoothprofits(sales,CSVec,mc_0);

if do_cs,
    [profits,policies]=compute_long_run_profits_cs(payoffs,ads,fcvec,elas,mc_0);
else
    [profits,policies]=compute_long_run_profits(payoffs,ads,fcvec,elas,mc_0);

end