import sqlite3

#this program deletes items from Zotero collections if the items are also present in child collections
#used to eliminate duplicate filing of items in parent collections after import of library from Papers3
#
#you must add the correct path to Zotero database on line 40
#
#Note: Back-up Zotero library before running this!
#

def existsInChild(collectionID, itemID):
    #if itemID exists in a child collection of collection ID: returns True
    #else: returns false
    #(this function operates recursively, see line 24)

    #find direct children
    children = []
    for childID, parentID in collectionMap.items():
        if parentID == collectionID:
            children.append(childID)

    #does itemID occur in direct children?
    found_in_child = False
    for child in children:
        SQL_query = "SELECT itemID FROM collectionItems WHERE collectionID = %d" % child
        res = cur.execute(SQL_query)
        itemIDs_inChild_results = res.fetchall()
        itemIDs_inChild = [item[0] for item in itemIDs_inChild_results]
        if itemID in itemIDs_inChild:   #if the direct child has the item
            found_in_child = True
            break
        else:    #check to see if children of the direct child have the item
            found_in_child = existsInChild(child, itemID) #call the same function recursively
            if found_in_child:
                break

    return found_in_child


con = sqlite3.connect("/Users/user/Zotero/zotero.sqlite")  #add path to zotero database here
cur = con.cursor()

#get distinct collectionsIDs in collections table
SQL_query = "SELECT DISTINCT collectionID FROM collections"
res = cur.execute(SQL_query)
collectionID_results = res.fetchall()
collectionIDs = [item[0] for item in collectionID_results]

#make a map of collection structure
# {childID : parentID}
collectionMap = {}
for collectionID in collectionIDs:   #iterate through collectionIDs
    # get parent ID
    SQL_query = "SELECT parentCollectionID FROM collections WHERE collectionID = %d" % collectionID
    res = cur.execute(SQL_query)
    parentID_results = res.fetchone()
    parentID = parentID_results[0]
    collectionMap[collectionID] = parentID

for collectionID in collectionIDs:
    #get list of itemIDs in this collectionID
    SQL_query = "SELECT itemID FROM collectionItems WHERE collectionID = %d" % collectionID
    res = cur.execute(SQL_query)
    itemID_results = res.fetchall()
    itemIDs = [item[0] for item in itemID_results]

    for itemID in itemIDs:
        if existsInChild(collectionID, itemID):
            #item exists in a child collection
            #remove item from this collectionID
            SQL_query = "DELETE FROM collectionItems WHERE itemID = %d AND collectionID = %d" % (itemID, collectionID)
            res = cur.execute(SQL_query)
            con.commit()

