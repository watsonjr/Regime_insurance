using ComponentArrays, Roots, DataFrames, CSV

coverage(p,λ,ρ,cv) = max((ρ*λ*p*(1-p)-p*(cv/(1-cv)))/(λ*p*(1-p)),0)
function utils(p,λ,ρ,cv,cf,ϕ) 
    δ = coverage(p,λ,ρ,cv)
    μY = (1/ϕ-p)
    μX = p 
    σ2 = p*(1-p)
    μY - δ*μX*(cv/(1-cv)) - cf/(1-cv) - 0.5*λ*((1+δ)*σ2-2*ρ*δ*σ2)
end

function utils(p,λ,ϕ) 
    μY = (1/ϕ-p)
    σ2 = p*(1-p)
    μY - 0.5*λ*σ2
end


function window_of_opportunity(pars)
    U(p) = utils(p,pars.λ,pars.ρ,pars.cv,pars.cf,pars.ϕ) 
    U0(p) = utils(p,pars.λ,pars.ϕ) 
    p0 = find_zero(p-> U(p)-U0(p),[0.001,0.5])
    pend = find_zero(p-> U(p)-pars.Ū,[0.001,0.75])
    return p0, pend
end

include("./parameters_windows.jl")
pars = ComponentArray((λ = λ, ρ = ρ, cv = cv, cf = cf, ϕ = ϕ , Ū = Ū ))

open = ComponentArray((λ = 1.0,ρ = 0.9,cv = 0.0,cf = 0.02,ϕ = 0.5, Ū = 1.5 ))
close = ComponentArray((λ = 1.0,ρ = 0.9,cv = 0.0,cf = 0.02,ϕ = 0.5,Ū = 1.5 ))

t0, tend= window_of_opportunity(pars)
δ = 1e-4
for par in keys(open)
    pars[par] += δ
    t0_δ, tend_δ = window_of_opportunity(pars)
    pars[par] += -δ
    open[par] = pars[par]*(t0_δ-t0)/δ
    close[par] = pars[par]*(tend_δ-tend)/δ
end


open = DataFrame(param = [k for k in keys(open)], sensetivity = open)
close = DataFrame(param = [k for k in keys(close)], sensetivity = close)
CSV.write("../DATA/sensetivity_window_open_prob.csv",open)
CSV.write("../DATA/sensetivity_window_close_prob.csv",close)
