import json
import boto3

client = boto3.client('resourcegroupstaggingapi')

def bulk_tagger(event, context):
    # get all resources with specified tags
    
    resources = client.get_resources(
        ResourceTypeFilters = event["ResourceTypeFilters"],
        TagFilters = event["TagFilters"]
    )
    # print(json.dumps(resources))

    if len(resources['ResourceTagMappingList']) == 0:
        response = {
            "statusCode": 204,
            "body": "No resource to tag"
        }
        return response

    # create a list off all resources ARNs
    arns_list = []
    for resource in resources['ResourceTagMappingList']:
        arns_list.append(resource['ResourceARN'])

    # print(arns_list)
    # print(event["TagsToApply"])
    
    # Tag resources with the new tags
    tagging_result = client.tag_resources(
        ResourceARNList=arns_list,
        Tags=event["TagsToApply"]
    )
    FailedResourcesMap = tagging_result['FailedResourcesMap']
    count_FailedResourcesMap = len(FailedResourcesMap)
    # print(FailedResourcesMap)
    # print(count_FailedResourcesMap)

    statusCode=200
    if count_FailedResourcesMap > 0:
        statusCode=500
        # TODO send a email

    response = {
        "statusCode": statusCode,
        "body": json.dumps(FailedResourcesMap)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
