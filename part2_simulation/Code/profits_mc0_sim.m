%This file uses functions from the SLMtools and helpers folders to run the
%needed siumations for creating the appropriate profit and policy tables.
%This is similar to run_one_simulation_mle.m but does not use interquartile
%range sales data, instead it uses the maximum likelihood estimator for
%predicting sales in order to optimize effort policies and profit levels
%accordingly
addpath(fullfile(cd,'SLMtools'))
addpath(fullfile(cd,'helpers'))

elas=-2;
tic;
load('../Raw Data/inventory-new.mat');
load('../Raw Data/mle-estimates.mat');

% Grab the correct parameter and setup the filenames
fname_main=fullfile('../Output/',strcat('Profits_mc0.mat'));
fn1=fullfile('../Output/',strcat('SalesHM-mle.mat'));
fn2=fullfile('../Output/',strcat('SalesHH-mle.mat'));
fn3=fullfile('../Output/',strcat('SalesMM-mle.mat'));
fn4=fullfile('../Output/',strcat('SalesNN-mle.mat'));

% Do the work
[profitsHM,policyHM]=single_simulation(10,theta,inv_mat(:,1),inventory0,elas,fn1,0);
disp(['HM Success'])
[profitsHH,policyHH]=single_simulation(10,theta,inv_mat(:,2),inventory0,elas,fn2,0);
disp(['HH Success'])
[profitsMM,policyMM]=single_simulation(10,theta,inv_mat(:,3),inventory0,elas,fn3,0);
disp(['MM Success'])
[profitsNN,policyNN]=single_simulation(10,theta,inv_mat(:,4),inventory0,elas,fn4,0);
disp(['NN Success'])

% save the (small) profit and policy tables
save(fname_main,'profitsNN','profitsHM','profitsHH','profitsMM','policyHM','policyHH','policyMM','policyNN');
toc
