%This uses functions from the SLMtools and helpers folders to run the
%calculate the profits from sales under different assortments of products
%with hypothetical mergers not being included. The output produced is a
%table that is used in python subscript for output as a LaTeX
%figure.
addpath(fullfile(cd,'SLMtools'))
addpath(fullfile(cd,'helpers'))

tic;

% Grab the correct parameter and setup the filenames
fname_out=fullfile('../Table Output/',strcat('threshold_figure.mat'));
fn1=fullfile('../Output/',strcat('SalesHM-mle.mat'));
fn2=fullfile('../Output/',strcat('SalesHH-mle.mat'));
fn3=fullfile('../Output/',strcat('SalesMM-mle.mat'));

% Do the work
[profitsHM]=calc_profits(fn1,0);
disp(['HM Success'])
[profitsHH]=calc_profits(fn2,0);
disp(['HH Success'])
[profitsMM]=calc_profits(fn3,0)
disp(['MM Success'])

% save the (small) profit and policy tables
save(fname_out,'profitsHM','profitsHH','profitsMM');
toc
