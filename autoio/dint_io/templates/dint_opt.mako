${potflag}						##Record 1	
${nsurf0} ${nsurft} ${methflag} ${repflag}		##Record 2
${intflag}						##Record 3
${hstep0} ${eps} ${nprint}				##Record 3.0
${ranseed}						##Record 4
${ntraj} ${tflag1} ${tflag2} ${tflag3} ${tflag4}	##Record 5
${nmol} ${ezero}					##Record 6
${natom} ${initx} ${initp} ${initj} ${ezeroi}		##Record 7
${geom}
${temp0im} ${escale0im}

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
