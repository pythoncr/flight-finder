FUNCTION_NAME=static-cache-valuations-ecr
LOG_STREAM_NAME=$(aws logs describe-log-streams --log-group-name "/aws/lambda/${FUNCTION_NAME}" | jq -r '.logStreams | sort_by(.creationTime) | .[-1].logStreamName')
aws logs get-log-events \
    --log-group-name "/aws/lambda/${FUNCTION_NAME}" \
    --log-stream-name "${LOG_STREAM_NAME}" | jq -r '.events[] | select(has("message")) | .message'
