import pymc as mc


challenger_data = np.genfromtxt("../../Chapter2_MorePyMC/data/challenger_data.csv", skip_header = 1, usecols=[1,2], missing_values="NA", delimiter=",")
#drop the NA values
challenger_data = challenger_data[ ~np.isnan(challenger_data[:,1]) ]


temperature = challenger_data[:,0]
D = challenger_data[:,1] #defect or not?

beta = mc.Normal( "beta", 0, 0.001, value = 0 )
alpha = mc.Normal( "alpha", 0, 0.001, value = 0 )

@mc.deterministic
def p( temp = temperature, alpha = alpha, beta = beta):
    return 1.0/( 1. + np.exp( beta*temperature + alpha) ) 


observed = mc.Bernoulli( "bernoulli_obs", p, value = D, observed=True)

model = mc.Model( [observed, beta, alpha] )

#mysterious code to be explained in Chapter 3
map_ = mc.MAP(model)
map_.fit()
mcmc = mc.MCMC( model )
mcmc.sample( 260000, 220000, 2 )
