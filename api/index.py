from fastapi import FastAPI
import api.utils as utils

app = FastAPI()

@app.get("/")
async def root():
    # Only turn this on when new data should be created
    # utils.create_json_from_csv()
    # print(utils.get_best_lifts(data))
    
    # json_data = utils.get_json_file()
    
    # print(json_data)
    
    
    return {"message": "Nothing to see here. Bye! "}

@app.get("/api/lifters/{lifter_id}")
async def get_lifters_by_id(lifter_id):
    json_data = utils.get_json_file()
    occurrences = []
    
    for row in json_data:
        name = row.get("name")
        hyphenated_name = "-".join(name.split()).lower()
        
        if hyphenated_name == lifter_id:
            occurrences.append(row)
       
    if occurrences:
        return {"data": occurrences}
    else:
        return {"data": "No lifters found with the given ID"}
    
@app.get("/api/lifters/{lifter_id}/best")
async def get_lifters_by_id_with_best_lifts(lifter_id):
    json_data = utils.get_json_file()
    occurrences = []
    
    for row in json_data:
        name = row.get("name")
        hyphenated_name = "-".join(name.split()).lower()
        
        if hyphenated_name == lifter_id:
            occurrences.append(row)
       
    if occurrences:
        return {"data": utils.get_best_lifts(occurrences)}
    else:
        return {"data": "No lifters found with the given ID"}


