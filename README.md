# fastapi_rate_limiter_ws
Experiment - Naive rate limiter on websocket protocol

    # To run the app
    cd app
    uvicorn app:app --reload --port 8080

After that, execute a websocket connection into:

    ws://127.0.0.1:8080/car/{id}

    where id could be brand car {Ferrari, Masserati, Tesla} or any string
