from app.agent.vendor_agent import route_query

def main():

    print("=== Vendor Analytics Agent ===")

    while True:

        query = input("\n> ")

        if query.lower() in ["exit", "quit"]:
            break

        result = route_query(query)

        print("\nResult:\n", result)


if __name__ == "__main__":
    main()