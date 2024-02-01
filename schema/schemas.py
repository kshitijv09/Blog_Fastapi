def individual_serial(blog)->dict:
    return{
        "id":str(blog["_id"]),
        "title":blog["title"],
        "tag":blog["tag"],
        "content":blog["content"],
        "date":blog["date"],
        "author":blog["author"],
    }


def list_serial(blogs)->list:
    return [individual_serial(blog) for blog in blogs]

""" def individual_serial(user)->dict:
    return{
        "id":str(user["_id"]),
        "title":blog["title"],
        "tag":blog["tag"],
        "content":blog["content"],
        "date":blog["date"],
        "author":blog["author"],
    } """