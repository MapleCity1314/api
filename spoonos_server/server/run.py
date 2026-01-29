import uvicorn


def main() -> None:
    uvicorn.run("spoonos_server.server.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
