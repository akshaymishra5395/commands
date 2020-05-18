from datetime import datetime, timedelta

from mongoengine.queryset.visitor import Q

from .models import UserMobileAction, UserMobileTopActions, HistoricalUserMobileAction, HistoricalUserMobileTopActions, SignInUser


def getParamsFromRequest(request):
    if request.method == "GET":
        params = request.query_params
    if request.method == "POST":
        params = request.data.get('params')
    return params


def query_generator(filters):

    # getting all the filters:
    start_date = filters.get("fromDate")
    end_date = filters.get("endDate")

    state = filters.get("state") or filters.get("state_code")

    district = filters.get("district")
    block = filters.get("block")
    title = filters.get("title")
    user_id = filters.get("username")

    query = Q()
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        query = Q(week_start_date__gte=start_date) & Q(
            week_start_date__lte=end_date)
        start_return_date = start_date - timedelta(days=30)

    if state and state != 'ALL':
        query &= Q(state__iexact=state)
    if district and district != 'ALL':
        query &= Q(district__iexact=district)
    if block and block != 'ALL':
        query &= Q(block__iexact=block)
    if title and title != 'ALL':
        query &= Q(title__iexact=title)
    if user_id and user_id != 'ALL':
        query &= Q(user_id=user_id)

    return query


def get_returing_users(request, times=[]):
    """
    operation:  fetch records from signin_user collection and get the count of signin users equal to the requested counts(times)
    input:      request(obj), times(list)
    ouput:      dict with key=> occurence value, value=>num of records having the same occurence value
    ex:
    input: request, [1,3,7]
    output: {1:50, 3:21, 7:2} or None if input = (request, [])
    """
    params = getParamsFromRequest(request)
    # getting all the filters:
    start_date = params.get("fromDate")
    end_date = params.get("endDate")

    state = params.get("state") or params.get("state_code")

    district = params.get("district")
    block = params.get("block")
    title = params.get("title")
    user_id = params.get("username")

    query = Q()
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        query = Q(signin_date__gte=start_date) & Q(signin_date__lte=end_date)

    if state and state != 'ALL':
        query &= Q(state__iexact=state)
    if district and district != 'ALL':
        query &= Q(district__iexact=district)
    if block and block != 'ALL':
        query &= Q(block__iexact=block)
    if title and title != 'ALL':
        query &= Q(title__iexact=title)
    if user_id and user_id != 'ALL':
        query &= Q(user_id=user_id)

    if len(times):
        result = {}
        for t in times:
            result[int(t)] = 0

        pipeline = []
        # group by username and count the occurance of usernames
        groupby_pipe = {
            "$group": {
                "_id": "$username",
                "count": {
                    "$sum": 1
                }
            }
        }
        # filter the records having count equal to the times
        having_pipe = {
            "$match": {
                "$or": []
            }
        }
        #  adding the or clause for count dynamically
        for t in times:
            having_pipe["$match"]["$or"].append({"count": {"$eq": int(t)}})
        # select username and count
        select_pipe = {
            "$project": {
                "username": "$_id",
                "_id": 0,
                "count": "$count"
            }
        }

        pipeline = [groupby_pipe, having_pipe, select_pipe]
        qs = SignInUser.objects.filter(query).aggregate(*pipeline)

        # update the occurance of count for every value of times
        for q in qs:
            for t in times:
                if q["count"] == int(t):
                    result[int(t)] += 1
        return result

def get_average_users(request):
    params = getParamsFromRequest(request)
    query = query_generator(params)
    pipeline = [
        {
            "$group": {
                "_id": "$week_start_date",
                "count": {
                    "$sum": 1
                }
            }
        },
        {
            "$project": {
                "dates": "$_id",
                "_id": 0,
                "count": 1
            }
        }
    ]
    agg_data = list(UserMobileAction.objects.filter(
        query).aggregate(*pipeline))
    num_of_weeks = len(agg_data)
    user_count_list = [i["count"] for i in agg_data]
    total_user_count = sum(user_count_list)
    try:
        average_user_count = total_user_count / num_of_weeks
    except ZeroDivisionError:
        print("Got  time interval as 0, please check")
        average_user_count = 0
    return {
        "count": average_user_count
    }


def get_top_actions(request):
    """
    return list of top 10 actions based on count value
    o/p: [{"name": "ViewPost", "count": 213132}, {}, {}]
    """
    query = query_generator(request.query_params)
    pipeline = [
        {
            "$group": {
                "_id": "$action",
                "count": {
                    "$sum": "$count"
                }
            }
        },
        {
            "$project": {
                "name": "$_id",
                "_id": 0,
                "count": 1
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]
    raw_data = UserMobileTopActions.objects.filter(query)
    agg_data = list(raw_data.aggregate(*pipeline))

    return agg_data


def get_top_users(request):
    """
    return list of top 10 users based on count value
    o/p: [{"name": "7503437728", "count": 213132}, {}, {}]
    """
    params = getParamsFromRequest(request)
    query = query_generator(params)
    pipeline = [
        {
            "$group": {
                "_id": "$user_id",
                "count": {
                    "$sum": "$count"
                }
            }
        },
        {
            "$project": {
                "name": "$_id",
                "_id": 0,
                "count": 1
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]
    raw_data = UserMobileAction.objects.filter(query)
    agg_data = list(raw_data.aggregate(*pipeline))

    return agg_data


def getActiveUserCountListForReport(request):
    params = getParamsFromRequest(request)
    # query = query_generator(request.query_params)
    query = query_generator(params)
    raw_data = UserMobileAction.objects.filter(query)

    state = params.get("state_code")
    district = params.get("district")
    block = params.get("block")

    if state and state != "ALL":
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "state": "$state",
                        "district": "$district",
                        "block": "$block"
                    },
                    "uniqueCount": {
                        "$addToSet": "$user_id"
                    }
                }
            },
            {
                "$project": {
                    "state": "$_id.state",
                    "district": "$_id.district",
                    "block": "$_id.block",
                    "_id": 0,
                    "uniqueActiveUserCount": {
                        "$size": "$uniqueCount"
                    }
                }
            }
        ]

    else:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "state": "$state"
                    },
                    "uniqueCount": {
                        "$addToSet": "$user_id"
                    }
                }
            },
            {
                "$project": {
                    "state": "$_id.state",
                    "_id": 0,
                    "uniqueActiveUserCount": {
                        "$size": "$uniqueCount"
                    }
                }
            }
        ]

    data_list = list(raw_data.aggregate(*pipeline))

    return data_list


##################### api for getting historical data ##########################################


def historical_query_generator(filters):

    # getting all the filters:
    start_date = filters.get("fromDate")
    end_date = filters.get("endDate")
    state = filters.get("state_code")
    district = filters.get("district")
    block = filters.get("block")
    title = filters.get("title")
    user_id = filters.get("username")

    query = Q()
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        query = Q(month_start_date__gte=start_date) & Q(
            month_start_date__lte=end_date)
        start_return_date = start_date - timedelta(days=30)

    if state and state != 'ALL':
        query &= Q(state__iexact=state)
    if district and district != 'ALL':
        query &= Q(district__iexact=district)
    if block and block != 'ALL':
        query &= Q(block__iexact=block)
    if title and title != 'ALL':
        query &= Q(title__iexact=title)
    if user_id and user_id != 'ALL':
        query &= Q(user_id=user_id)
    return query


def get_average_users_historical(request):
    params = getParamsFromRequest(request)
    query = historical_query_generator(params)
    pipeline = [
        {
            "$group": {
                "_id": "$month_start_date",
                "count": {
                    "$sum": 1
                }
            }
        },
        {
            "$project": {
                "dates": "$_id",
                "_id": 0,
                "count": 1
            }
        }
    ]
    raw_data = HistoricalUserMobileAction.objects.filter(query)
    agg_data = list(raw_data.aggregate(*pipeline))
    num_of_months = len(agg_data)
    user_count_list = [i["count"] for i in agg_data]
    total_user_count = sum(user_count_list)
    try:
        average_user_count = total_user_count / num_of_months
    except ZeroDivisionError:
        print("Got  time interval as 0, please check")
        average_user_count = 0
    return {
        "count": average_user_count
    }


def get_top_actions_historical(request):
    """
    return list of top 10 actions based on count value
    o/p: [{"name": "ViewPost", "count": 213132}, {}, {}]
    """
    query = historical_query_generator(request.query_params)
    pipeline = [
        {
            "$group": {
                "_id": "$action",
                "count": {
                    "$sum": "$count"
                }
            }
        },
        {
            "$project": {
                "name": "$_id",
                "_id": 0,
                "count": 1
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]
    agg_data = list(HistoricalUserMobileTopActions.objects.filter(query).aggregate(*pipeline))
    return agg_data


def get_top_users_historical(request):
    """
    return list of top 10 users based on count value
    o/p: [{"name": "7503437728", "count": 213132}, {}, {}]
    """
    params = getParamsFromRequest(request)
    query = historical_query_generator(params)
    pipeline = [
        {
            "$group": {
                "_id": "$user_id",
                "count": {
                    "$sum": "$count"
                }
            }
        },
        {
            "$project": {
                "name": "$_id",
                "_id": 0,
                "count": 1
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]
    raw_data = HistoricalUserMobileAction.objects.filter(query)
    agg_data = list(raw_data.aggregate(*pipeline))

    return agg_data
