${potflag}						##Record 1	
${nsurf0} ${nsurft} ${methflag} ${repflag}		##Record 2
${intflag}						##Record 3
${hstep0} ${eps} ${nprint}				##Record 3.0
${ranseed}						##Record 4
${ntraj} ${tflag1} ${tflag2} ${tflag3} ${tflag4}	##Record 5
${nmol} ${ezero}					##Record 6

    ${natom} ${initx} ${initp} ${initj} ${ezero_i}	##Record 7
    if initx == 0:					##Record 8.0
        for j in range(natom):
            ${target_mass_xyz} (${sym} ${mass} ${xx}
    elif initp == 0:					##Record 9.0
        ${temp0im} ${escale0im}
    if initj == 0:
        #nothing

${termflag} ${tnstep}				##Record 12
    if termflag == 0:
        #run for ${tnstep}
    elif termflag == 1:				##Record 12.1
        ${tstime}
    elif termflag == 2:				##Record 12.2
        ${tgradmag}
    elif termflag == 3:				##Record 12.3
        ${tnoutcome}
        ${tsymb1} ${tsymb2} ${distcut}
${ioutput} ${ilist1} ${ilist2} ..
