#sobe broker, server e host pra clientes simulados
uvicorn broker:app --host 0.0.0.0 --port 8000 &
BROKER_PID=$!
uvicorn server:app --host 0.0.0.0 --port 8001 &
SERVER_PID=$!

trap "kill $BROKER_PID $SERVER_PID ; exit 0" SIGINT
wait
