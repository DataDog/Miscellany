from datadog import initialize, api


def delete_dashboards_by_text_in_title():

    api_key = input("Please enter your API key: ")
    app_key = input("Please enter your APPLICATION key: ")

    options = {"api_key": api_key, "app_key": app_key}

    initialize(**options)

    text_to_search_in_dashboard = input(
        "Please enter the text to search in your dashboard titles: "
    )

    dashboards = api.Dashboard.get_all()["dashboards"]

    dashboards_to_delete = {}

    for dashboard in dashboards:
        if text_to_search_in_dashboard in dashboard["title"]:
            dashboards_to_delete[dashboard["id"]] = dashboard["title"]

    dashboard_list = dashboards_to_delete.values()

    if len(dashboard_list) == 0:
        print("There were no dashboards found for this query.")
    else:
        print("Dashboards to delete:\n" + "\n".join(dashboard_list))

        delete_or_not = input(
            "These dashboards will be deleted. Do you want to continue? [Y/n]: "
        )

        if delete_or_not.lower() == "y":
            for dash_id in dashboards_to_delete.keys():
                api.Dashboard.delete(dash_id)
            print("The dashboards in the list were deleted.")
        else:
            print("No dashboards were deleted.")


if __name__ == "__main__":
    delete_dashboards_by_text_in_title()
