from app import app


def main():
    app.run(host='0.0.0.0', port=4000, debug=True)


if __name__ == "__main__":
    main()
