import requests
import PySimpleGUI as sg

aniList = {}
rating, rank, status, episodes, genre, indx, search = "?","?","?","?",["?"],0,""

def TopAnime():
    global x , aniList, search
    aniList = {}
    search = "https://api.jikan.moe/v4/top/anime"
    response = requests.get(search)
    top = response.json()
    for x, i in enumerate(top["data"]):
        aniList[(top["data"][x]["titles"][0]["title"])] = x

def SeasonNow():
    global x, aniList, search
    aniList = {}
    search = "https://api.jikan.moe/v4/seasons/now"
    response = requests.get(search)
    top = response.json()
    for x, i in enumerate(top["data"]):
        aniList[(top["data"][x]["titles"][0]["title"])]= x

def SearchResult():
    global x, aniList, search
    aniList = {}
    search = "https://api.jikan.moe/v4/anime?q="+x+"&sfw"

    response = requests.get(search)
    searched = response.json()

    for x, i in enumerate(searched["data"]):
        aniList[(searched["data"][x]["title"])] = x

    if aniList == {}:
        aniList = ["No Results"]

    else:
        return aniList

def DisplayResult():
    global x, rating, rank, status, episodes, aniList, search, genre
    genre = []

    response = requests.get(search)
    searched = response.json()

    indx = aniList.get(x)
    print (indx)
    print (aniList)
    print(searched["data"][1]["title"])

    if searched["data"][indx]["score"] is None:
        rating = "?"

    else:
        rating = searched["data"][indx]["score"]

    if searched["data"][indx]["rank"] is None:
        rank = "?"
    else: rank = searched["data"][indx]["rank"]

    if searched["data"][indx]["status"] is None:
        status = "?"
    else:
        status = searched["data"][indx]["status"]

    if searched["data"][indx]["episodes"] is None:
        episodes = "?"
    else:
        episodes = searched["data"][indx]["episodes"]

    if searched["data"][indx]["genres"] is None:
        genre = "?"
    else:
        for i, n in enumerate(searched["data"][indx]["genres"]):
            genre.append(searched["data"][indx]["genres"][i]["name"])



    if aniList == []:
        aniList = ["No Results"]

    else:
        return
#------------------------------------------------------------------------------------------------

layout = [
    [sg.Text("Search: ", key = "-SearchText-"), sg.Input(key= "-SearchBar-")],
    [sg.Button("Search", key = "-Button1-"), sg.Button("Top Anime", key = "-TopAnime-"), sg.Button("This Season", key = "-SeasonNow-")],
    [sg.Listbox(values = aniList, select_mode = "extended", key= "-Results-", size = (100,30))],
    [sg.Button("Display", key= "-Button2-")],
    [sg.Text("Name", key='-Name-')],
    [sg.Text("Rating: ", key='-RatingTxt-'),sg.Text("?", key='-Rating-')],
    [sg.Text("Rank: ", key='-RankTxt-'), sg.Text("?", key='-Rank-')],
    [sg.Text("Status: ", key='-StatusTxt-'), sg.Text("?", key='-Status-')],
    [sg.Text("Episodes: ", key='-EpTxt-'),sg.Text("?", key='-Ep-')],
    [sg.Text("Genre: ", key='-GenreTxt-'),sg.Text("?", key='-Genre-')]


]

#------------------------------------------------------------------------------------------------


window = sg.Window("Anime App", layout, size= (600,600))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-TopAnime-": #Top anime Button
        aniList = []
        TopAnime()
        window["-Results-"].update(aniList)

    if event == "-SeasonNow-":#Season Now Button
        aniList = []
        SeasonNow()
        window["-Results-"].update(aniList)

    if event == "-Button1-": #Search Button
        aniList = []
        x = values["-SearchBar-"]
        print("Searching for", x)
        print("-----------------------")
        SearchResult()
        window["-Results-"].update(aniList)
        print(aniList)

    if event == "-Button2-": #Display Button
        print(values)
        if values["-Results-"] == []:
            window["-Name-"].update("Please Select a Anime")
        else:
            window["-Name-"].update(values["-Results-"][0])
            x = values["-Results-"][0]
            DisplayResult()
            window["-Rating-"].update(rating)
            window["-Rank-"].update(rank)
            window["-Status-"].update(status)
            window["-Ep-"].update(episodes)
            window["-Genre-"].update(genre)


window.close()