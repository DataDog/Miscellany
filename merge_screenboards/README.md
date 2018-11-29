# How to Merge Screenboards

## Steps to merge screenboards

1. Retrieve the ID of each of screenboard (the ID is located in the URL of the screenboard).

2. Use [merge_screenboards.py][1], which relies on the Datadog API [get][2] and [push][3] for screenboards.

3. Update [merge_screenboards.py][1] with your Datadog API and APP keys.

4. Run the following (**orientation** is a number, use 0 to merge screenboards vertically or 1 for horizontally):  
    ```
    python merge_screenboard.py [screenboard1,screenboard2...,screenboardN] 
    orientation
    ```

5. The output of the script is the URL of your merged screenboard.

## Items of note
- By default, template variables are added uniquely to the new dashboard. To add new template variables, list them in `dict_tem_var` (examples are in the code comments).

- The default screenboard title is **Merged Screenboard**, but you can change it in the `title` variable.

- Integration screenboards must be cloned before merging. The default screenboards don't have IDs.

[1]: ./merge_screenboards.py
[2]: https://docs.datadoghq.com/api/#screenboards-get
[3]: https://docs.datadoghq.com/api/#screenboards-post
