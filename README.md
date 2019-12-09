# aws-bulk-tagging
 A tool for tagging AWS resources massively

### Goal
Apply a list of tags to a set of AWS resources.

### Use case:
You want to add or update the following tags:
                    
| Key  | Value |
| ------------- | ------------- |
| Entity  | SALES  |
                    

To all EC2 instances tagged with:
                    
| Key  | Value |
| ------------- | ------------- |
| Stage  | PROD  |
| App  | AWESOME_SALES_APP  |
                    

In this case, the request payload will be:
```json
{
  "TagFilters": [
    {
      "Key": "lookForResourcesWithTagKey",
      "Values": [
        "lookForResourcesWithTagValue"
      ]
    }
  ],
  "TagsToApply": {
      "tagKeyToAddOrUpdate": "tagValueToAddOrUpdate"
   },
  "ResourceTypeFilters": [
    "ec2:instance"
  ]
}
```