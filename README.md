```
# If you want to tag a bunch of documents, organized under a "tagging_push_2023" dataset name:
mkdir -p to_be_tagged/pdfs/tagging_push_2023

docker-compose up

# In another terminal or in Finder, copy the pdfs into to_be_tagged/pdfs/tagging_push_2023. This will kick off some mild processing in the background to split the PDF into page-level images, and add them to the backend for processing. After a few minutes, they should be visible when you select the "Tag" option on localhost:8080.

```

Data is persisted in ./pg_data, but can be dumped in XML+PNG format for model training by:

```
docker cp dump_to_xml.py cosmos-tagger_import_data_1:/src/
docker exec cosmos-tagger_import_data_1 python dump_to_xml.py /data/pngs/ /data/dump
```

Now the annotations are sitting in your local host in `to_be_tagged/dump`. Improvements for this step to come soon.




# Database changes
The following functions are possible, but require database changes for which there are no easy interfaces yet:
 
- Adding users
- Adding tag classes.

Both are self-explanatory within the postgres database, and changes should be immediately apparent within the app.

**NOTE**: because complete annotations are tied to the tag_id within `tag`
table, do not re-use ids if you have both annotated documents AND delete tag
classes. 

