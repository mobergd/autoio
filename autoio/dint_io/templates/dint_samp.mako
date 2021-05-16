${potflag}						##Record 1	
${nsurf0} ${nsurft} ${methflag} ${repflag}		##Record 2
${intflag}						##Record 3
elif intflag == 1:	##Rung-Kutta 4th order
    ${hstep} ${nprint}					##Record 3.1
${ranseed}						##Record 4
${ntraj} ${tflag1} ${tflag2} ${tflag3} ${tflag4}	##Record 5
${nmol} ${ezero}					##Record 6

    ${natom} ${initx} ${initp} ${initj} ${ezero_i}	##Record 7
    if initx == 0:					##Record 8.0
        for j in range(natom):
            ${target_mass_xyz} (${sym} ${mass} ${xx}
    elif initp == 0:					##Record 9.0
        ${temp0im} ${escale0im}
    elif initj == 1:					##Record 10.1
        ${samptarg} ${sampjmin} ${sampjmax} ${sampjtemp1} ${samptjemp2} ${sampbrot1} ${sampbrot2}
        if samptarg == 0:
            #do nothing
        elif samptarg < 0:				##Record 10.1.2
            ${ejsc}
        elif samptarg > 0:
            #scale vib momenta

${termflag} ${tnstep}				##Record 12
    if termflag == 0:
        #run for ${tnstep}
${ioutput} ${ilist1} ${ilist2} ..
