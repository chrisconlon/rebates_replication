
%%% Outputs the long-run average profit computations

%This uses functions from the SLMtools and helpers folders to run the
%needed simulations for creating the appropriate profit and policy tables.
addpath(fullfile(cd,'SLMtools'))
addpath(fullfile(cd,'helpers'))

% Base Case MC = 15
run_profits('Profits_mc15.mat',-2, 10, 0,0,0.15)

% Alternative Case MC = 0
run_profits('Profits_mc0_alt.mat',-2, 10, 0,0,0.0)

% IQR 
run_profits('Profits_mc15-iqr.mat',-2, 10, 1,0,0.15)

% Consumer Surplus
run_profits('Profits_mc15-cs.mat',-2, 10, 0,1,0.15)

% FC = 15 
run_profits('Profits_mc15-fc15.mat',-2, 15, 0,0,0.15)

% FC = 5
run_profits('Profits_mc15-fc5.mat',-2, 5, 0,0,0.15)
