% The function returns a probability matrix and a corresponding matrix of
% consumer surpluses. It takes in 4 parameters including a dataset vector
% containing the product characteristics, the arrival of "likely
% consumers", the set of available products and a defined "hypothetical
% full machine" which contains a set of the 29 most-commonly stocked products
% 
function [pmat,CS] = rcprobs(ds3,t,avail,xi)
if nargin < 3,
	avail = ds3.avail;
end

[J K] = size(ds3.Xmat);
nmkt = size(avail,1);

dj = t(1:J)+xi;
sigma = t(J+1:J+K);
utils=exp(bsxfun(@plus,bsxfun(@times,ds3.Xmat,sigma')*ds3.v',dj));

CS =zeros(nmkt,1);
pmat=zeros(J,nmkt);
for i=1:nmkt,
	av=avail(i,:);
	d = 1./(1+utils'*av');
    CS(i) = log(1+av*utils)*ds3.w;
	p=utils.*repmat(d',[J 1])*ds3.w;
	pmat(:,i) = p.*av';
end
pmat = full(pmat)';

end
