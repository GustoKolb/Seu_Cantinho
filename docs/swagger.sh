docker run -p 8080:8080 -e SWAGGER_JSON=/tmp/openapi.yaml -v $(pwd)/openapi.yaml:/tmp/openapi.yaml swaggerapi/swagger-ui &
open http://localhost:8080
