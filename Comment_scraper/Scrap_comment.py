import pytchat 


def start_scrapping():
    chat = pytchat.create(video_id = "YM51YthgzPk")
    while chat.is_alive(): 
        for c in chat.get().sync_items(): 
            print(f"{c.author}, {c.message}")
start_scrapping()