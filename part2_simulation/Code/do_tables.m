%The function takes in two parameters and does not have an output. 
%Instead it runs the other files to produce tables will be outputted 
%to tex files using an additional `python script.
function do_tables(fn_in,fn_out, mc)

files = dir('../Simulated Profits/Profits-*.mat');
elas=-2;


%% set the MLE policies here
load(fn_in);
policyHM_fixed=policyHM;
policyHH_fixed=policyHH;
policyMM_fixed=policyMM;

%% For the observed values
policyHM_exp=[policyHM; 137; 144];
policyHH_exp=[policyHH; 137; 144];
policyMM_exp=[policyHM; 137; 144];

elas=-2;

my_table_mle=[ print_pi_ae_table(profitsHM,policyHM_exp,elas,0, mc);... %Table 11%
        print_pi_ae_table(profitsHH,policyHH_exp,elas,0, mc);...
        print_pi_ae_table(profitsMM,policyMM_exp,elas,0, mc);];
policy_table_mle = [policyHM policyHH policyMM]; %Table A8
table9_mle=[payoff_difference(profitsHM,profitsHH,policyHM(2),policyHH(2),-2, mc)...
            payoff_difference(profitsMM,profitsHM,policyMM(2),policyHM(2),-2, mc) ...
            payoff_difference(profitsMM,profitsHH,policyMM(2),policyHH(2),-2, mc)]; %Same Structure as Table 13, older revision table 9
efficiency_mle=[...
        payoff_difference(profitsHH,profitsHH,policyHH(3),policyHH(1),-2, mc)...
        payoff_difference(profitsHM,profitsHM,policyHM(3),policyHM(1),-2, mc)...
        payoff_difference(profitsMM,profitsMM,policyMM(3),policyMM(1),-2, mc)...
        payoff_difference(profitsHH,profitsHH,policyHH(5),policyHH(1),-2, mc)...
        payoff_difference(profitsHM,profitsHM,policyHM(5),policyHM(1),-2, mc)...
        payoff_difference(profitsMM,profitsMM,policyMM(5),policyMM(1),-2, mc)];

my_reb=[payoff_difference(profitsMM,profitsMM,144,144,-2, mc), payoff_difference(profitsMM,profitsMM,137,137,-2, mc)];
observed_mle=[...
        payoff_difference(profitsHH,profitsMM,policyMM_exp(8),policyMM_exp(8),-2, mc)...
        payoff_difference(profitsHM,profitsMM,policyMM_exp(8),policyMM_exp(8),-2, mc)...
        payoff_difference(profitsMM,profitsMM,policyMM_exp(9),policyMM_exp(8),-2, mc)...
        payoff_difference(profitsHH,profitsMM,policyMM_exp(9),policyMM_exp(8),-2, mc)...
        payoff_difference(profitsHM,profitsMM,policyMM_exp(9),policyMM_exp(8),-2, mc)...
];


net_effect_mle=[...
        payoff_difference(profitsMM,profitsHM,policyMM(2),policyHM(1),-2, mc)...
        payoff_difference(profitsMM,profitsHM,policyMM(3),policyHM(1),-2, mc)...
        payoff_difference(profitsMM,profitsHM,policyMM(5),policyHM(1),-2, mc)...
        payoff_difference(profitsMM,profitsHH,policyMM(2),policyHH(1),-2, mc)...
        payoff_difference(profitsMM,profitsHH,policyMM(3),policyHH(1),-2, mc)...
        payoff_difference(profitsMM,profitsHH,policyMM(5),policyHH(1),-2, mc)...
        ];
    
ref_table_mle=[... %Table 12%
        payoff_difference(profitsHH,profitsMM,policyHH(1),policyMM(2),-2, mc),...
        payoff_difference(profitsMM,profitsMM,policyMM(3),policyMM(2),-2, mc),...
        payoff_difference(profitsHM,profitsMM,policyHM(4),policyMM(2),-2, mc),...
        payoff_difference(profitsHM,profitsMM,policyHM(5),policyMM(2),-2, mc)];
merger_table_mle=do_one_merger(profitsMM,profitsHM,profitsHH,profitsNN, mc);


%% uncomment to fix the countermeasures for observed data
% observed_mle(8,:)=[my_reb(end,2),my_reb(end,2),my_reb(end,1),my_reb(end,1),my_reb(end,1)];
[reb_mle,reduced_lambda_mle, cutoff_price_mle]=compute_countermeasures(net_effect_mle,mc);
[reb_obs_mle,reduced_lambda_obs_mle, cutoff_price_obs_mle]=compute_countermeasures(observed_mle,mc);


%%
for i=1:length(files),
    disp(files(i).name)
    load(strcat('../Simulated Profits/',files(i).name))
    my_table(:,:,i)=[ print_pi_ae_table(profitsHM,policyHM,elas,1,mc);...
        print_pi_ae_table(profitsHH,policyHH,elas,1, mc);...
        print_pi_ae_table(profitsMM,policyMM,elas,1, mc);];
    my_table_fixed(:,:,i)=[ print_pi_ae_table(profitsHM,policyHM_exp,elas,1,mc);...
        print_pi_ae_table(profitsHH,policyHH_exp,elas,1, mc);...
        print_pi_ae_table(profitsMM,policyMM_exp,elas,1, mc);];
    policy_table(:,:,i) = [policyHM policyHH policyMM];
    table9(:,:,i)=[payoff_difference(profitsHM,profitsHH,policyHM(2),policyHH(2),-2, mc)...
                payoff_difference(profitsMM,profitsHM,policyMM(2),policyHM(2),-2, mc) ....
                payoff_difference(profitsMM,profitsHH,policyMM(2),policyHH(2),-2, mc)];
    efficiency(:,:,i)=[...
        payoff_difference(profitsHH,profitsHH,policyHH(3),policyHH(1),-2, mc)...
        payoff_difference(profitsHM,profitsHM,policyHM(3),policyHM(1),-2, mc)...
        payoff_difference(profitsMM,profitsMM,policyMM(3),policyMM(1),-2, mc)...
        payoff_difference(profitsHH,profitsHH,policyHH(5),policyHH(1),-2, mc)...
        payoff_difference(profitsHM,profitsHM,policyHM(5),policyHM(1),-2, mc)...
        payoff_difference(profitsMM,profitsMM,policyMM(5),policyMM(1),-2, mc)];
    
    net_effect(:,:,i)=[...
        payoff_difference(profitsMM,profitsHM,policyMM(2),policyHM(1),-2, mc),...
        payoff_difference(profitsMM,profitsHM,policyMM(3),policyHM(1),-2, mc),...
        payoff_difference(profitsMM,profitsHM,policyMM(5),policyHM(1),-2, mc),...
        payoff_difference(profitsMM,profitsHH,policyMM(2),policyHH(1),-2, mc),...
        payoff_difference(profitsMM,profitsHH,policyMM(3),policyHH(1),-2, mc),...
        payoff_difference(profitsMM,profitsHH,policyMM(5),policyHH(1),-2, mc),...
        ];

    observed_table(:,:,i)=[...
        payoff_difference(profitsHH,profitsMM,policyMM_exp(8),policyMM_exp(8),-2, mc)...
        payoff_difference(profitsHM,profitsMM,policyMM_exp(8),policyMM_exp(8),-2, mc)...
        payoff_difference(profitsMM,profitsMM,policyMM_exp(9),policyMM_exp(8),-2, mc)...
        payoff_difference(profitsHH,profitsMM,policyMM_exp(9),policyMM_exp(8),-2, mc)...
        payoff_difference(profitsHM,profitsMM,policyMM_exp(9),policyMM_exp(8),-2, mc)...
        ];

    ref_table(:,:,i)=[...
        payoff_difference(profitsHH,profitsMM,policyHH(1),policyMM(2),-2, mc),...
        payoff_difference(profitsMM,profitsMM,policyMM(3),policyMM(2),-2, mc),...
        payoff_difference(profitsMM,profitsMM,policyMM(3),policyMM(2),-2, mc),...
        payoff_difference(profitsHM,profitsMM,policyHM(5),policyMM(2),-2, mc)];

    merger_table(:,:,i)=do_one_merger(profitsMM,profitsHM,profitsHH,profitsNN, mc);
end

% Feasible rebates (a1)-(c3)
pct_feasible_ub=100*mean(squeeze([table9(2,:,:) > table9(8,:,:)])');
pct_feasible_lb=100*mean(squeeze([-table9(1,:,:) < table9(8,:,:)])');

% these are the condition (a3),(b3),(c3)
pct_cond3=100*mean(squeeze([sum(table9(1:2,:,:),1) > -table9(3,:,:)])');
conditions_table=[pct_feasible_lb; pct_feasible_ub; pct_cond3];

% full profit table
pi_ae_table_se=std(my_table,[],3);

% 95% CI for table 11 
policy_diff_ci = [prctile(policy_table,[0.975],3)]-[prctile(policy_table,[0.025],3)];

% Percent of +/- Surplus Conditions for Table 13
net_effect_surplus_pct=round(100*mean(net_effect(5:7,:,:)< 0,3),2);

% Cutoff price for w_h
[reb,reduced_lambda, cutoff_price]=compute_countermeasures(net_effect,mc);
[reb_obs,reduced_lambda_obs, cutoff_price_obs]=compute_countermeasures(observed_table,mc);


% Actual SE's Table 9
% rebate size and rebate standard error
print_table9=[table9(1:2,:,:);  sum(table9(1:2,:,:),1); table9([3 5 6 7],:,:)];
print_table9_se=std(print_table9,[],3);

%Actual SE's (table 14)
x=[std(cutoff_price,[],3); std(reduced_lambda,[],3)];

% Merger Simulations
load(fn_in);
merger_hat=do_one_merger(profitsMM,profitsHM,profitsHH,profitsNN, mc);
clear policyHH policyHM policyMM policyNN profitsHH profitsHM profitsMM profitsNN
save(fn_out)
end

%[payoff_difference(profitsHM,profitsHH,261,257,-2) payoff_difference(profitsMM,profitsHM,261,259,-2) payoff_difference(profitsMM,profitsHH,259,257,-2)]