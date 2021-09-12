% [res]=solveDP(tprobs,f,FC,powers)
% Tprobs is a stationary vector of incremental sales
% f is an N x 1 vector of payoffs
% FC: is the fixed cost

%% This implements Algorithm 3 from the Appendix
function [res]=solveDP(tprobs,f,FC,effort_min,effort_max)
if nargin < 5,
    effort_min=130;
    effort_max=260;
end
N = length(f);
% intialize to a constant to prevent dependence on Fin Inst Toolbox
%rho=rate2disc(365,.05,1);
%Chosen Discount Rate
rho= 0.999863032461307;

% Step 1
%Summing up the payoff vector
profits=cumsum(f(1:N));

% Initialize the pre-decision transitions
B=create_tpm(tprobs,N); % This is the TPM (without decision)
res.Vzero=zeros(1,N);
res.Vbar =zeros(1,N);

    % grid of possible effort values (limit to those near the optimum)
    for effort=effort_min:effort_max,
        % Steps 2 and 3
        [P,u] = set_critical(B,profits-FC,effort);
        % Step 4
        V=(speye(N)-rho*P)\u;
        % Step 5
        a=stochastic_inverse(P);
        res.Vzero(effort)  = V(1);
        res.Vbar(effort) = a(1,:)*V;
    end
    % Solve optimal policy by PI algorithm
    [res.optimum,res.policy]=max(res.Vbar);
% This constructs a TPM from vector xx for N states
    function B=create_tpm(xx,N)
        a=histc(xx,[0:max(xx)])'./length(xx);
        a=a./sum(a);
        B=spdiags(repmat(a,[N 1]),1:length(a),zeros(N,N));
        adj=B(:,end) + 1-full(sum(B,2));
        B(adj>1e-14,end) = adj(adj>1e-14);
    end

% Given a choice of cutoff x* this updates the post-decision TPM (A)
% and the post-decision payoff (y)
% Updated Mar 2019: don't send reset to zero send it to 0 + 1 period.
    function [A,y]=set_critical(A,y,x)
        M=size(A(x:end,:),1);
        A(x:end,:)=0;
        A(x:end,:)=repmat(A(1,:),[M 1]);
        y(1:x-1)=0;
    end

% This finds the inverse of a valid stochastic TPM X
% when X need not be full rank
    function Y=stochastic_inverse(X)
        N=size(X,2);
        Y=mrdivide(augmentF(sparse(zeros(N))),augmentF(X-speye(N)));
        function Y=augmentF(Y)
            Y(:,end) = ones(N,1);
            Y=sparse(Y);
        end
    end
end
