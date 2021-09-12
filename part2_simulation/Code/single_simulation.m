%This function is a simulation which generates optimal effort policies from
%simulating consumer arrivals to obtain consumer surplus and simulated
%sales
%It takes in 7 parameters, a fixed cost, a vector of demand parameters, an initial
%inventory vector, a hypothetical full machine which a paramenter 
%representing a hypothetical full machine which contains all supersets of 
%the considered products, an elasticity level and a and a file to output to
%and a boolean for a marginal cost of zero.
%The ouput of this simulation function is a matrix of optimal 
%effort policies and corresponding profits. 
function [profits,policies] = single_simulation(fcvec,theta,inventory,inventory0,elas,fn,mc)
%load 
load('../Raw Data/main-short.mat');
%Load State Variables
load('../Output/statevars.mat');

N=800; nsims=1e5; NN=300;

% Do forward simulation
% no dependencies
[sales,CSVec]=simulateforward(inventory, nsims, ds3, theta,N,inventory0);
save(fn,'sales','CSVec');


%%% Can we eliminate below this?
% Do the Chebyshev smoothing
% depends: loadProductdata
payoffs = smoothprofits(sales,CSVec,mc);

% Now we can compute long-run stationary profits at the ergodic
% distribution of consumer arrivals
[profits,policies]=compute_long_run_profits(payoffs,ads,fcvec,elas,mc);

end