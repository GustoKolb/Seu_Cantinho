#liga broker e server, uso: bash run.sh
#vai rodar os dois juntos, bom pra testar, ruim de debugar
#pra desenvolver eh melhor rodar em terminais separados
#lembrar de matar o processo e reexecutar dps de mudar o codigo!!!
uvicorn broker:app --host 0.0.0.0 --port 8000 &
uvicorn server:app --host 0.0.0.0 --port 8001 &
wait
