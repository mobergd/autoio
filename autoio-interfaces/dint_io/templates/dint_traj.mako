${potflag}						##Record 1	
${nsurf0} ${nsurft} ${methflag} ${repflag}		##Record 2
${intflag}						##Record 3
if intflag == 0:		##Bulirsch-Stoer
    ${hstep0} ${eps} ${nprint}				##Record 3.0
${ranseed}						##Record 4
${ntraj} ${tflag1} ${tflag2} ${tflag3} ${tflag4}	##Record 5

${nmol} ${ezero}					##Record 6
for i in range(nmol):
    ${natom} ${initx} ${initp} ${initj} ${ezero_i}	##Record 7
    elif initx = 6:					##Record 8.6
        ${samptot} ${lbinsamp} ${sampfilexx} ${sampfilepp}	#Record 8.6.1
        for j in range(natom):
            ${target_mass}				##Record 8.6.3

    if initp == -1:
	##see initx

    elif initj == 1:					##Record 10.1
        ${samptarg} ${sampjmin} ${sampjmax} ${sampjtemp1} ${samptjemp2} ${sampbrot1} ${sampbrot2}
        if samptarg == 0:
            #do nothing
        elif samptarg < 0:				##Record 10.1.2
            ${ejsc}
        elif samptarg > 0:
            #scale vib momenta
##NMOL LOOP

${iorient} ${ldofrag}				##Record 11
    elif iorient == 1:				##Record 11.1
        ${rel0qc} ${ttt} ${bminqc} ${bmaxqc}
${termflag} ${tnstep}				##Record 12
    elif termflag == 3:				##Record 12.3
        ${tnoutcome}
        ${tsymb1} ${tsymb2} ${distcut}
${ioutput} ${ilist1} ${ilist2} ..
