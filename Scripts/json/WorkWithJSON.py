from enum import Flag
import json

def main():
    try:
        with open("sample.json") as f:
            j = json.load(f)
    except json.JSONDecodeError as err:
        print("Json load/parce error" + err)
        return
    print(type(j), j)
    print("----------------------------")
    for k in j:
        print(k, j[k], type(j[k]),sep='    ')
    print("----------------------------")
    for v in j.values():
        print(v)
    print("----------------------------")
    for k, v in j.items():
        print(k,v, sep=": ")
    print("----------------------------")
    j['newItem']='New item 1'
    j['d']=123
    j['newItem2']='Привет'
    print(json.dumps(j, indent=4, ensure_ascii=False))
    try:
        with open('sample2.json', 'w') as f:
            json.dump(j, f, indent=4)
    except:
        print("File write error")
    else:
        print("File write ok")


if __name__ == "__main__":
    main()