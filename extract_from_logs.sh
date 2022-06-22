#!/bin/bash

set -e

# $1 must match the path to the logs directory
if [ -z $4 ]
then
    echo "Usage: bash extract_from_logs.sh PATH_TO_LOGS_DIRECTORY ARTIFACT_PATH OUT CPUS TOPI" ;
    echo "If you don't know what to set this to, set OUT to benches/ CPUs to 8 and topI to 300" ;
    echo "Ex: ./extract_from_logs.sh dreamcoder_logs ~/proj/stitch/experiments/artifact benches/ 8 300" ;
    exit 1 ;
fi


ARTIFACT_PATH=$2
LOGS_DIR=$1
ARTIFACT_BIN_PATH="${ARTIFACT_PATH}/bin"  # Note: this directory must contain a copy of the "data_extractor.py" script
OUT=$3
CPUS=$4
TOPI=$5


echo "copying log_extractor.py to $ARTIFACT_BIN_PATH"
cp log_extractor.py $ARTIFACT_BIN_PATH

for DOMAIN in `ls $LOGS_DIR` ; do
    echo "Started extracting data from $DOMAIN"

    # we skip rational bc the data is messy
    if [[ $DOMAIN == "rational" ]]; then continue; fi

    for RUN in `ls $LOGS_DIR/$DOMAIN` ; do
        # if [[ $RUN != "list_hard_test_ellisk_2019-02-15T11.26.41" ]]; then continue; fi

        echo "Started extracting data from $DOMAIN/$RUN"
        OUT_DIR="$OUT/${DOMAIN}_${RUN}"
        mkdir -p $OUT_DIR


        # echo "Logging extraction process to $OUT_DIR/$DOMAIN/$RUN/.log"
        # echo "$LOG_FILE" > "data/$DOMAIN/$RUN/.log"
        # python3 "$ARTIFACT_BIN_PATH/log_extractor.py" "$EXP_OUTS_PATH/$LOG_FILE" "data/$DOMAIN/$RUN" "8" >> "data/$DOMAIN/$RUN/.log" 2>&1
        python3 "$ARTIFACT_BIN_PATH/log_extractor.py" "$LOGS_DIR/$DOMAIN/$RUN" "$DOMAIN" "$RUN" "$OUT_DIR" "$CPUS" "$TOPI"

    done
    echo "Finished extracting data from $DOMAIN"

done

echo "done"

# add info.json to all data folders
# echo "analyzing all run data"
# python3 analyze.py all_run_info
# echo "done"
