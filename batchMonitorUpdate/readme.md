# Batch Monitor Update

These two scripts are for batch updating monitors over a single account.

Provide both your **API** key and your **APP** key.

The scripts differ slightly in the endpoints used because of the structure the data is returned. 
---
The first script **batchUpdate.py** takes a number of optional parameters.

| variable | type | description
| ----------- | ----------- |-------|
| query      | str       |Can     contain any number of space-separated monitor  attributes, for instance `query=\"type:metric status:alert\"`.
| page   | int        | Page to start paginating from. Default value of 0
| per_page | int | Number of monitors to return per page. Default value of 30

This script takes applies a query to your monitors and returns a selection of `<class 'datadog_api_client.v1.model.monitor_search_result.MonitorSearchResult'>`

 https://github.com/DataDog/datadog-api-client-java/blob/8d53fa2bb4174147d12b17353473bc35042a7182/api_docs/v1/MonitorSearchResult.md
                
 https://github.com/DataDog/datadog-api-client-java/blob/72ca579bcd71cd9254563927254bb9c79d4b5cf6/src/main/java/com/datadog/api/v1/client/model/MonitorSearchResult.java

---

The second script ***batchUpdateReturnAll.py** returns a list of all monitors definitions which are stored as dictionaries. You can then get the key of whatever attribute you are interested in and make any changes necessary.

---

There are a number of examples for use in the scripts to provide a basis of how to utilise them.