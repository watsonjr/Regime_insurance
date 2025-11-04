
# optimal insurnace coverage assumign income lost = 1 in low regime
# gamma is the strength of risk aversion, rho is the correlation between 
# insurance claims and losses, p is the pobability of a loss and cv are variable
# insurance preimum costs
coverage(p,λ,ρ,cv) = max((ρ*λ*p*(1-p)-p*(cv/(1-cv)))/(λ*p*(1-p)),0)

# Utility with insruance 
function utils(p,λ,ρ,cv,cf,ϕ) 
    δ = coverage(p,λ,ρ,cv)
    μY = (1/ϕ-p)
    μX = p 
    σ2 = p*(1-p)
    μY - δ*μX*(cv/(1-cv)) - cf/(1-cv) - 0.5*λ*((1+δ)*σ2-2*ρ*δ*σ2)
end

# Utility without insuracne 
function utils(p,λ,ϕ) 
    μY = (1/ϕ-p)
    σ2 = p*(1-p)
    μY - 0.5*λ*σ2
end

# optimal coverge level 
function coverage(p,λ,ρ,cv,ϕ,Ū )
    if utils(p,λ,ρ,cv,cf,ϕ)  < utils(p,λ,ϕ)
        return 0
    elseif utils(p,λ,ρ,cv,cf,ϕ) < Ū 
        return 0
    end
    return coverage(p,λ,ρ,cv)
end 

include("../CODE/jack_parameters.jl")

using CSV
using DataFrames

# load probabilities 
df = CSV.read("DATA/Data_prob.csv",DataFrame)

# calcualte utility 
utils_with = broadcast(p -> utils(p,λ,ρ,cv,cf,ϕ), df.p) 
utils_without = broadcast(p -> utils(p,λ,ϕ), df.p)  

# add utility to data frame
df.utils_with .= utils_with
df.utils_without .= utils_without
df.utility_alternative .= Ū 

# save data frame 
CSV.write("DATA/Data_utils.csv",df)