import json
import boto3
from responseManager import manageReponse

client = boto3.client('resourcegroupstaggingapi')

_TAG_FILTERS = "TagFilters"
_TAGS_TO_APPLY = "TagsToApply"
_RESOURCE_TYPE_FILTERS = "ResourceTypeFilters"
_RESOURCE_TAG_MAPPING_LIST = "ResourceTagMappingList"
_FAILED_RESOURCES_MAP = "FailedResourcesMap"

def bulk_tagger(event, context):
    # check request's arguments
    if _TAG_FILTERS not in event or _RESOURCE_TYPE_FILTERS not in event or _TAGS_TO_APPLY not in event:
        return manageReponse(400,"Missing arguments in your request. View README file to rectify your request payload.")

    try:
        # get all resources with specified tags
        resources = client.get_resources(
            ResourceTypeFilters = event[_RESOURCE_TYPE_FILTERS],
            TagFilters = event[_TAG_FILTERS]
        )
        # print(json.dumps(resources))
    except KeyError as err:
        return manageReponse(204,"KeyError: {0}".format(err))
    except:
        return manageReponse(500,"Unexpected error: {0}".format(sys.exc_info()[0]))

    if len(resources[_RESOURCE_TAG_MAPPING_LIST]) == 0:
        return manageReponse(204,"No resource to tag")

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

    if count_FailedResourcesMap > 0:
        return manageReponse(500,json.dumps(FailedResourcesMap))

    return manageReponse(200,json.dumps(FailedResourcesMap), False)