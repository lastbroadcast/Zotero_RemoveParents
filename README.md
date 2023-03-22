# Zotero_RemoveParents

This program deletes items from Zotero collections if the items are also present in child collections (sub-collections).

It therefore eliminates duplicate filing of items in parent collections after an import of library from Papers3 (I found this to be a problem with my library when I transfered my collections with the python scripts).

Run this script after transfering the collections from Papers3 to Zotero using the scripts FromPapers and ToZotero.


Instructions:

-Back-up Zotero library before running this!! (See readme of ToZotero for instructions).

-Make sure the path to the Zotero database ('zotero.sqlite') is correct (line 40 of script).

-Make sure Zotero is closed.

-Run script.

