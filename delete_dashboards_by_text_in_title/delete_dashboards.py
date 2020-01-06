import os
from datadog import initialize, api


def file_output(dashboard, title):
    if os.path.exists("datadog_dashboards_backup.txt"):
        mode = "a"
    else:
        mode = "w"

    print(f"Writing backup for {title} on file datadog_dashboards_backup.txt.")
    with open("datadog_dashboards_backup.txt", mode) as f:
        f.write(f"Dashboard Title: {title}\n\n{dashboard}\n\n\n")


def get_search_text():
    while True:
        text = input(
            "Please enter the text to search in your dashboard titles: "
        ).strip()
        if len(text) >= 3:
            return text
        print("Search text must be at least 3 characters!")


def confirm_delete(dash_id, dash_title):
    confirm = input(f'Delete dashboard entitled "{dash_title}"? [Y/n]: ')
    if confirm.lower() == "y":
        try:
            api.Dashboard.delete(dash_id)
            print(f'Dashboard entitled "{dash_title}" was deleted.')
        except Exception as e:
            print(e)
    else:
        print(f'Dashboard entitled "{dash_title}" was NOT deleted.')


def initialize_options():
    if "DD_API_KEY" in os.environ:
        api_key = os.getenv("DD_API_KEY")
    else:
        api_key = input("Please enter your API key: ")

    if "DD_APP_KEY" in os.environ:
        app_key = os.getenv("DD_APP_KEY")
    else:
        app_key = input("Please enter your APPLICATION key: ")

    options = {"api_key": api_key, "app_key": app_key}

    initialize(**options)


def delete_dashboards_by_text_in_title():

    initialize_options()

    search_text = get_search_text()

    try:
        dashboards = api.Dashboard.get_all()
    except:
        raise RuntimeError("Your API or APPLICATION key may be invalid.")

    to_delete = {}

    for d in dashboards["dashboards"]:
        if search_text.lower() in d["title"].lower():
            to_delete[d["id"]] = d["title"]
            result = api.Dashboard.get(d["id"])
            file_output(result, d["title"])

    if not to_delete:
        print("There were no dashboards found for this query.")
    else:
        print("Dashboards to delete:")
        for i, dashboard in enumerate(to_delete.values()):
            print(f"  {i + 1}. {dashboard}")

        delete_or_not = input(
            "These dashboards will be deleted. Do you want to continue? [Y/n]: "
        )

        if delete_or_not.lower() == "y":
            for dash_id, dash_title in to_delete.items():
                confirm_delete(dash_id, dash_title)
            print("Dashboard deletion completed.")
        else:
            print("Dashboard deletion aborted.")


if __name__ == "__main__":
    delete_dashboards_by_text_in_title()
