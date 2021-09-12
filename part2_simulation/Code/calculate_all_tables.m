
%%% Constructs tables (for Python)
%%% Inputs the long-run average profit computations
%% This is the last file to be run

% Base case MC=15
do_tables('../Output/Profits_mc15.mat','../Table Output/mc15-tables.mat',0.15)

% IQR
do_tables('../Output/Profits_mc15-iqr.mat','../Table Output/mc15-iqr-tables.mat',0.15)

% Consumer Surplus
do_tables('../Output/Profits_mc15-cs.mat','../Table Output/mc15-cs-tables.mat',0.15)

% FC=15
do_tables('../Output/Profits_mc15-fc15.mat','../Table Output/mc15-fc15-tables.mat',0.15)

% FC=5
do_tables('../Output/Profits_mc15-fc5.mat','../Table Output/mc15-fc5-tables.mat', 0.15)

% MC=0
do_tables('../Output/Profits_mc0.mat','../Table Output/mc0-tables.mat', 0)
%% 
 