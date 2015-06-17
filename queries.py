import pprint


def get_db():
    from pymongo import MongoClient
    client = MongoClient()
    db = client.users
    return db


def user_entries_count(collection):
    """Print the top 5 contributing users in collection."""
    db = get_db()
    collection = db[collection]
    top_entries = collection.aggregate([{"$group" : {"_id" : "$created.user", "count" : {"$sum" : 1}}},
	                                {"$sort" : {"count" : -1}},
	                                {"$limit" : 5}])
    return top_entries


def user_count(collection):
    """Print the number of unique users in collection."""
    db = get_db()
    collection = db[collection]
    users = collection.aggregate([{"$group" : {"_id" : "$created.user"}},
		                          {"$group" : {"_id" : "$created.user",
		                                       "count" : {"$sum" : 1}}}])
    return users


def node_count(collection):
    """Print the number of elements of type node and way in collection."""
    db = get_db()
    collection = db[collection]
    nodes = collection.find({"element_type": "node"})
    ways = collection.find({"element_type": "way"})
    return nodes.count(), ways.count()


def park_count(collection):
    """Print the number of national parks in collection."""
    db = get_db()
    collection = db[collection]
    parks = collection.find({"boundary": "national_park"})
    return parks.count()


def univ_count(collection):
    """Print all universities in collection."""
    db = get_db()
    collection = db[collection]
    univ = collection.aggregate([{"$match" : {"amenity" : "university"}},
		                         {"$group" : {"_id" : "$address.street",
		                                      "count" : {"$sum" : 1}}},
		                         {"$sort" : {"count" : -1}}])
    return univ


def embassy_count(collection):
    """Print all embassies in collection."""
    db = get_db()
    collection = db[collection]
    embassy = collection.aggregate([{"$match" : {"amenity" : "embassy"}},
		                         {"$group" : {"_id" : "$address.street",
		                                      "count" : {"$sum" : 1}}},
		                         {"$sort" : {"count" : -1}}])
    return embassy

if __name__ == "__main__":
    #print "Top 5 users by entry count:"
    #pprint.pprint(user_entries_count("dc"))
    #print "Number of users contributing to map:"
    #pprint.pprint(user_count("dc"))
    #print "Number of nodes in map: %i\nNumber of ways in map: %i" % node_count("dc")
    print "Number of National Park boundaries:"
    pprint.pprint(park_count("dc"))
    #print "Number of universities:"
    #pprint.pprint(univ_count("dc"))
    print "Number of embassies:"
    pprint.pprint(embassy_count("dc"))
