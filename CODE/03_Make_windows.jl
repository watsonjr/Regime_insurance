
# optimal insurnace coverage assumign income lost = 1 in low regime
# gamma is the strength of risk aversion, rho is the correlation between 
# insurance claims and losses, p is the pobability of a loss and cv are variable
# insurance preimum costs
coverage(p,λ,ρ,cv) = max((ρ*λ*p*(1-p)-p*(cv/(1-cv)))/(λ*p*(1-p)),0)

# Utility with insruance 
function utils(p,λ,ρ,cv,cf,y_high,y_low) 
    δ = coverage(p,λ,ρ,cv)
    μY = p*y_low+(1-p)*y_high
    μX = p 
    σ2 = p*(1-p)*(y_high-y_low)^2
    μY - δ*μX*(cv/(1-cv)) - cf/(1-cv) - 0.5*λ*((1+δ)*σ2-2*ρ*δ*σ2)
end

# Utility without insuracne 
function utils(p,λ,y_high,y_low) 
    μY = p*y_low+(1-p)*y_high
    σ2 = p*(1-p)*(y_high-y_low)^2
    μY - 0.5*λ*σ2
end

# optimal coverge level 
function coverage(p,λ,ρ,cv,y_high,y_low,Ū )
    if utils(p,λ,ρ,cv,cf,y_high,y_low)  < utils(p,λ,y_high,y_low)
        return 0
    elseif utils(p,λ,ρ,cv,cf,y_high,y_low) < Ū 
        return 0
    end
    return coverage(p,λ,ρ,cv)
end 

include("../CODE/parameters_windows.jl")

using CSV
using DataFrames
data = ARGS[1]
# load probabilities 
df = CSV.read("DATA/$data.csv",DataFrame)
println(names(df))
print(occursin.("income_high_sliding",names(df)))
income_high = df[:,occursin.("income_high_sliding",names(df))][:,1]
income_low = df[:,occursin.("income_low_sliding",names(df))][:,1]
prob = df[1:end,occursin.("probability_low_sliding",names(df))][:,1]


# # calcualte utility 
utils_with = broadcast(i -> utils(prob[i],λ,ρ,cv,cf,income_high[i],income_low[i]), 1:length(prob)) 
utils_without = broadcast(i -> utils(prob[i],λ,income_high[i],income_low[i]), 1:length(prob))  

# add utility to data frame
df.utils_with .= utils_with
df.utils_without .= utils_without
df.utility_alternative .= Ū 

# save data frame 
CSV.write("DATA/Data_utils.csv",df)
