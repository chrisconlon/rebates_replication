%
% This is the main routine to simulate arrivals of consumers
%
% should be called by allprofitsimulations.m
%
% Calls: None
% Depends: None
%The function takes in an initial inventory vector, a number of simulated
%chains, the dataset vector containing product characteristics, theta
%(which is the vector of demand parameters (product intercepts plus random
%coefficients on product characteristics), the total number of consumer
%arrivals to simulate, and a paramenter representing a hypothetical full
%machine which contains all supersets of the considered products.
%The function then outputs a matrix of simulated sales (the product id of each sale)
%and a similarly sized matrix containing
%the expected consumer surplus at each level of m in M.
function [sales,CSVec]=simulateforward(inventory, nsims, ds, theta,M,inventory0)
    xi=0.75;
    J = length(inventory);
    P0 = rcprobs(ds,theta,inventory0>0,xi);
    igshare=sum(P0)+eps;
    %num2str(igshare)
    currentinv = repmat(inventory',[nsims 1]);

    % initialize simulated vends -- save as uint8 to keep size small!
    sales = zeros(nsims,M,'uint8');
    CSmat = zeros(nsims,M);
    [P,CS] = rcprobs(ds,theta,currentinv>0,xi);
    P=P./(max(sum(P,2))+eps);
    for t=1:M,
        Q=sparse(mnrnd(1,[P 1-sum(P,2)]));
        [i,~,~]=find(Q');
        sales(:,t) = i;
        [P,currentinv,CS] = updateprobs(currentinv,Q,P,CS);
        CSmat(:,t) = CS;
    end
    sales(sales==J+1) = 0;
    
    function [P,newinv,CS]=updateprobs(oldinv,Q,P,CS)
                newinv=oldinv-Q(:,1:end-1);
                [i,~]=find((newinv>0)-(oldinv>0));
                if(~isempty(i)),
                     [P2,CSX]= rcprobs(ds,theta,newinv(i,:)>0,xi);
                     P2=P2./igshare;
                     P(i,:) = P2;
                     CS(i,:) = CSX;
                end
    end
    CSVec = mean(CSmat);
end