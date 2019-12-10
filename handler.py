import json
import boto3

client = boto3.client('resourcegroupstaggingapi')

_TAG_FILTERS = "TagFilters"
_TAGS_TO_APPLY = "TagsToApply"
_RESOURCE_TYPE_FILTERS = "ResourceTypeFilters"
_RESOURCE_TAG_MAPPING_LIST = "ResourceTagMappingList"
_FAILED_RESOURCES_MAP = "FailedResourcesMap"

_STATUS_CODE = "statusCode"
_BODY = "body"

def bulk_tagger(event, context):
    # check request's arguments
    if _TAG_FILTERS not in event or _RESOURCE_TYPE_FILTERS not in event or _TAGS_TO_APPLY not in event:
        response = {
            _STATUS_CODE: 400,
            "body": "Missing arguments in your request. View README file to rectify your request payload."
        }
        return response

    # get all resources with specified tags
    try:
        resources = client.get_resources(
            ResourceTypeFilters = event[_RESOURCE_TYPE_FILTERS],
            TagFilters = event[_TAG_FILTERS]
        )
        # print(json.dumps(resources))
    except KeyError as err:
        response = {
            _STATUS_CODE: 204,
            _BODY: "KeyError: {0}".format(err)
        }
        return response
    except:
        response = {
            _STATUS_CODE: 500,
            _BODY: "Unexpected error: {0}".format(sys.exc_info()[0])
        }
        return response
    

    if len(resources[_RESOURCE_TAG_MAPPING_LIST]) == 0:
        response = {
            _STATUS_CODE: 204,
            _BODY: "No resource to tag"
        }
        return response

    # create a list off all resources ARNs
    arns_list = []
    for resource in resources[_RESOURCE_TAG_MAPPING_LIST]:
        arns_list.append(resource['ResourceARN'])
    
    # Tag resources with the new tags
    tagging_result = client.tag_resources(
        ResourceARNList=arns_list,
        Tags=event[_TAGS_TO_APPLY]
    )
    FailedResourcesMap = tagging_result[_FAILED_RESOURCES_MAP]
    count_FailedResourcesMap = len(FailedResourcesMap)

    statusCode=200
    if count_FailedResourcesMap > 0:
        statusCode=500
        # TODO send a email

    response = {
        _STATUS_CODE: statusCode,
        _BODY: json.dumps(FailedResourcesMap)
    }

    return response