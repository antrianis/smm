# dnov: bash-autocomplete

# complete group options -- BEGIN
_smg_completion() {
    local cur prev opts base prev_prev
    COMPREPLY=()  # nothing
    cur="${COMP_WORDS[COMP_CWORD]}"           # current
    prev="${COMP_WORDS[COMP_CWORD-1]}"        # previous
    prev_prev=""                              # previous previous

    #  options + groups
    base_opts=$(for x in `smg`; do echo ${x} ; done )
    opts="-c --create -d --delete "${base_opts}

    # if deleting give options
    if [ $COMP_CWORD -eq 2 ]; then
        if [ "${#prev}" -gt "1"  ] && [ "${prev:0:2}" == "-d" ]
    	then
            COMPREPLY=( $(compgen -W "${base_opts}" -- ${cur}) )
            return 0
    	fi
    fi
   COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
   return 0
}
complete -F _smg_completion -o default smg;
# complete group options -- END


# complete last command from history while adding -- BEGIN
_smn_completion() {
    local cur prev opts base prev_prev
    COMPREPLY=()  # nothing
    cur="${COMP_WORDS[COMP_CWORD]}"           # current
    prev="${COMP_WORDS[COMP_CWORD-1]}"        # previous
    prev_prev=""                              # previous previous

    #  The Basics
    opts=$(for x in `smg`; do echo ${x} ; done )

    if [ $COMP_CWORD -eq 2 ]; then
        local running="'\"!!\"'"
        COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
        return 0

    fi

   COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
   return 0
}

complete -F _smn_completion -o default smn;
# complete last command from history while adding -- END