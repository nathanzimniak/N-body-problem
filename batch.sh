#!/bin/bash

# OAR job configuration.
#OAR -n n_body_solver
#OAR -l /nodes=3/core=15,walltime=00:10:00
#OAR -t besteffort

# Parameters.
N_MPI_PROCS=3
N_OMP_THREADS=15
SETUP=galaxy

# Set number of OpenMP threads per MPI process.
export OMP_NUM_THREADS=$N_OMP_THREADS

# Display allocated nodes/cores, and MPI/OpenMP configuration.
WIDTH=34
SEP=$(printf '%*s' "$WIDTH" '' | tr ' ' '=')
SUBSEP=$(printf '%*s' "$WIDTH" '' | tr ' ' '-')

printf "\n%s\n" "$SEP"

printf "%-18s %s\n" "Allocated nodes" "Allocated cores"
printf "%s\n" "$SUBSEP"

sort "$OAR_NODE_FILE" | uniq -c | awk '{
    node=$2
    gsub(/\.u-ga\.fr|\.univ-savoie\.fr/, "", node)
    printf "%-18s %s\n", node, $1
}'

printf "%s\n" "$SEP"

printf "%-18s %s\n" "MPI processes" "$N_MPI_PROCS"
printf "%-18s %s\n" "OpenMP threads" "$N_OMP_THREADS"

printf "%s\n\n" "$SEP"

# Launch the job.
#
# --hostfile $OAR_NODE_FILE:
# Provides the list of allocated nodes (one entry per core) given by OAR.
# MPI uses this file to know where to launch processes.
#
# -mca plm_rsh_agent "oarsh":
# Tells OpenMPI to use 'oarsh' (instead of ssh) to start processes on remote nodes.
# Required on OAR clusters for proper job launching.
#
mpirun -np $N_MPI_PROCS --hostfile $OAR_NODE_FILE -mca plm_rsh_agent "oarsh" ./main --setup $SETUP
