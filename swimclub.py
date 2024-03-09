import statistics
import os
import hfpy_utils

FOLDER = "ch5/swimdata/"
CHARTS = "Charts/"

def get_swim_data(filename):
    filename.rstrip(".txt").split("-")
    name, age, distance, style = filename.removesuffix(".txt").split("-")
    with open(FOLDER + filename) as file:
        records = file.readline().rstrip("\n").split(",")
        mili_sceond_list = [] 
        times_list =[]
    for record in records:
        if ':' in record:
            values = record.split(".")[0].split(":") + [record.split(".")[1]]
        else:
            values = [0] + record.split(".")
        numbers = [ int(x) for x in values ]
        times_list.append(record)
        mili_sceond_list.append((numbers[0]*60+numbers[1])*100+numbers[2])
    av = statistics.mean(mili_sceond_list)
    min = int(av/100/60)
    sec = int(av/100)-min*60
    mili = int((av-(min*60+sec)*100)*10)
    av_formatted = f"{min}:{sec}.{mili}"    
    return name, age, distance, style, times_list, av_formatted, mili_sceond_list

def produce_bar_chart(filename, location=CHARTS):
    svgs = ""
    *_, times, average, converts = get_swim_data(filename)
    from_max=max(converts)
    title = f"{_[0]} (Under {_[1]}) {_[2]} {_[3]}"

    for n,t in enumerate(reversed(converts),1):
        bar_width = hfpy_utils.convert2range(t, 0, from_max, 0,350)
        svgs += f"""<svg height="30" width="400">
    <rect height="30" width="{bar_width}" style="fill:rgb(0, 0, 255);" />
    </svg>{times[-n]}<br />
    """
    path = os.path.abspath(f"{location}{filename.rstrip('.txt')}.html")
    
    save_to = f"{location}{filename.rstrip('.txt')}.html"
    header = f"""<!DOCTYPE html>
    <html>
        <head>
            <link rel="stylesheet" href="static/style.css">
            <title>
                {title}
            </title>
        </head><h2>{title}</h2>"""
    body = f"""
        <p>Avreage time: {average:0>2}</p>
        </body>
        </html>"""
    site = f"{header} {svgs} {body} "

    with open(path,"w") as hf:
        print(site,file=hf)
    save_to= path

    return save_to

