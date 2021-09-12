function run_profits(out_fn,elas, FC, use_iqr,do_cs, mc_0)

tic;
% change this block
fname_out=fullfile('../Output/',strcat(out_fn));

% Grab the correct parameter and setup the filenames
fn1=fullfile('../Output/',strcat('SalesHM-mle.mat'));
fn2=fullfile('../Output/',strcat('SalesHH-mle.mat'));
fn3=fullfile('../Output/',strcat('SalesMM-mle.mat'));
fn4=fullfile('../Output/',strcat('SalesNN-mle.mat'));

% Do the work
[profitsHM,policyHM]=single_no_simulation(fn1,elas,FC,use_iqr,do_cs,mc_0);
disp(['HM Success'])
[profitsHH,policyHH]=single_no_simulation(fn2,elas,FC,use_iqr,do_cs,mc_0);
disp(['HH Success'])
[profitsMM,policyMM]=single_no_simulation(fn3,elas,FC,use_iqr,do_cs,mc_0);
disp(['MM Success'])
[profitsNN,policyNN]=single_no_simulation(fn4,elas,FC,use_iqr,do_cs,mc_0);
disp(['NN Success'])

% save the (small) profit and policy tables
save(fname_out,'profitsNN','profitsHM','profitsHH','profitsMM','policyHM','policyHH','policyMM','policyNN');
toc

end



