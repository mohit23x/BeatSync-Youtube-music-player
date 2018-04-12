import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import vlc
import pafy
import re
import requests
import threading
import pprint
import time
import datetime
import sqlite3



class Application(tk.Frame):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        #variables
        self.top_vids = []
        self.top_vids_title = []
        self.title_var = tk.StringVar()
        self.playlist_dict = {}
        self.music_progress = tk.StringVar()
        self.btn_hlder = []
        self.frame_5_show = 0
        self.toop = None
        self.var_for_scale= tk.StringVar()

  
        self.master.title("beatsync testing")
        self.pack(fill='both', expand=1)

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Open Track", command=self.onopen, accelerator="Ctrl+O")
        fileMenu.add_separator()
        fileMenu.add_command(label="Add favorite Channel", command=self.add_favorite_channel, accelerator="Ctrl+A")
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.onexit, accelerator="Ctrl+Q")
        menubar.add_cascade(label='File', menu=fileMenu)


        channel = tk.Menu(menubar)
        channel.add_command(label="Add favorite Channel", command=self.add_favorite_channel)
        channel.add_separator()
        channel.add_command(label="show favorite Channel", command=self.show_favorite_channel)
        menubar.add_cascade(label='Channel', menu=channel)

        discover = tk.Menu(menubar)
        discover.add_command(label="Discover New Music", command=self.discover_new_music_function)
        discover.add_separator()
        discover.add_command(label="show favorite Channel", command=self.show_favorite_channel)
        menubar.add_cascade(label='discover', menu=discover)


        frame0 = ttk.Frame(self)
        frame0.pack(fill='x', expand=False)

        f0_lbl1 = ttk.Label(frame0, textvariable= self.title_var, background='yellow', justify='center')
        f0_lbl1.pack(fill='x')


        frame1 = ttk.Frame(self)
        frame1.pack(fill='x', expand=False, pady=15)
        
        ent0_label = ttk.Label(frame1, text='Entry Bar : ')
        ent0_label.pack(side='left', padx=5, pady=5)


        self.name =  tk.StringVar()

        ent2_entry = ttk.Entry(frame1, font = "Helvetica 13 bold")
        ent2_entry.pack(side='left', fill='x', padx=5, expand=True)
        ent2_entry['textvariable'] = self.name
        ent2_entry.bind('<Key-Return>', self.print_contents)
    
        ent3_button = ttk.Button(frame1, text='Playlist', command=lambda: self.ournewwindow(self.playlist_dict, self.top_vids))
        ent3_button.pack(pady=2, padx=2)


        frame2 = ttk.Frame(self)
        frame2.pack(side='top', fill = 'x', expand=False, pady=5)        

        self.progress_ba = ttk.Progressbar(frame2, orient="horizontal", length=300, mode="determinate")
        self.progress_ba.pack(side = 'top', fill='x', padx=3)

        f2_progress_lbl = ttk.Label(frame2, textvariable=self.music_progress)
        f2_progress_lbl.pack(side='top')

        
        frame3 = ttk.Frame(self, border=5)
        frame3.pack(side='top', fill='x')
        
        ent2_button = ttk.Button(frame3, text='play', command=self.playbutclick)
        ent2_button.pack(side='left', padx=5, pady=5)

        ent3_button = ttk.Button(frame3, text='pause', command=self.pausebutclick)
        ent3_button.pack(side='left', padx=5, pady=5)

        ent4_button = ttk.Button(frame3, text='mute on-off', command=self.mutebutclick)
        ent4_button.pack(side='left', padx=5, pady=5)

        ent5_button = ttk.Button(frame3, text='next', command=self.next_track)
        ent5_button.pack(side='left', padx=5, pady=5)

        ent6_button = ttk.Button(frame3, text='forward', command=lambda: self.forwbutclick(5))
        ent6_button.pack(side='left', padx=5, pady=5)

        ent7_button = ttk.Button(frame3, text='backward', command=lambda: self.backwbutclick(5))
        ent7_button.pack(side='left', padx=5, pady=5)

        self.ent8_slider = ttk.Scale(frame3, from_ = 0, to=100, orient='horizontal',variable=self.var_for_scale, command=self.slidervol)
        self.ent8_slider.pack(side='right')


        frame4 = ttk.Frame(self, border=5)
        frame4.pack(side='top', expand=False, pady=10, fill='x')


        self.f4_tree = ttk.Treeview(frame4, columns=("size", "modified"))
        scrollbar_vertical = ttk.Scrollbar(frame4, orient='vertical', command=self.f4_tree.yview)
        scrollbar_vertical.pack(side='right', fill='y')
        self.f4_tree.configure(yscrollcommand=scrollbar_vertical.set)

        frame5 = ttk.Frame(self, border=5)
        frame5.pack(side='top', expand=True, pady=10, fill='x')

        self.f5_tree = ttk.Treeview(frame5, columns=("size", "modified"))

        self.popup  = tk.Menu(self, tearoff=0)
        self.popup.add_command(label="Next", command=self.selextion)
        self.popup.add_separator()
        self.popup.add_command(label="Show Music", command=self.show_music_favorite_channel)
        self.popup.add_separator()
        self.popup.add_command(label="Remove Channel", command=self.remove_one_favorite_channel)


        self.master.bind('m', self.mutebutclick)
        self.master.bind('f', self.forwbutclick)
        self.master.bind('b', self.backwbutclick)
        self.master.bind('x', self.up_increase_volume)
        self.master.bind('z', self.down_decrease_volume)
        self.master.bind('<space>', self.pausebutclick)
        self.master.bind('u', self.up_increase_volume)
        self.master.bind('d', self.down_decrease_volume)
        self.master.bind('n', self.next_track)
        self.master.bind('p', self.previous_track)



    def playbutclick(self):
        self.player.play()        
        var1 = self.media.get_meta(0)
        var2 = self.media.get_meta(1)


    def pausebutclick(self, event=''):
        self.player.pause()

    def forwbutclick(self, event):
        self.player.set_time(self.player.get_time() + 5000)

    def backwbutclick(self, event):
        self.player.set_time(self.player.get_time() - 5000)

    def next_track(self, event=''):
        cur_item = self.f4_tree.focus()
        curr_ = self.f4_tree.next(cur_item)
        v = self.f4_tree.item(curr_)
        self.link_offline_player(v['values'][1])
        self.f4_tree.focus(curr_)
        self.f4_tree.selection_set(curr_)

        
    def previous_track(self, event=''):
        cur_item = self.f4_tree.focus()
        curr_ = self.f4_tree.prev(cur_item)
        v = self.f4_tree.item(curr_)
        self.link_offline_player(v['values'][1])
        self.f4_tree.focus(curr_)
        self.f4_tree.selection_set(curr_)
        

    def mutebutclick(self, event):
        self.player.audio_toggle_mute()


    def up_increase_volume(self, event):
        try:
            var = int(self.player.audio_get_volume())
            var = var + 5
            self.player.audio_set_volume(int(var))
            self.ent8_slider.set(var)

        except:
            print('i will not fail!')

        
    def down_decrease_volume(self, event):
        try:
            var = int(self.player.audio_get_volume())
            var = var - 5
            self.player.audio_set_volume(int(var))
            self.ent8_slider.set(var)

        except:
            print('i will not fail!')
        
        


    def slidervol(self, value):
        self.player.audio_set_volume(int(float(value)))


    def link_offline_player(self, location):
        #vlc things ------------------>
        try:
            self.player.stop()
            try:
                self.player.release()
                self.instance.release()
            
            except:
                print('')
        except:
            print('')
        
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        #print('\nthe file is -> {}'.format(location))
        self.media = self.instance.media_new(location)
        self.player.set_media(self.media)
        self.media.parse()
        #print(self.media.parse())
        var1 = self.media.get_meta(0)
        #print('var1 -> {}'.format(var1))
        var2 = self.media.get_meta(1)
        #print('ASEI')
        #print('var 2 -> {}'.format(var2))
        self.title_var.set('{} - - - {}'.format(var1, var2))
        #print('\nmedia playe set')
        self.player.play()
        self.var_for_scale.set(int(self.player.audio_get_volume()))
        self.progress_bar_func()



    def linkplayer(self, location):
        #vlc things ------------------>
        try:
            self.player.stop()
            try:
                self.player.release()
                self.instance.release()
            except:
                print('')
        except:
            print('')
        
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(location)
        self.player.set_media(self.media)
        self.player.play()
        self.var_for_scale.set(int(self.player.audio_get_volume()))
        
        self.progress_bar_func()


        

    def progress_bar_func(self):
        progress_percent = int(self.player.get_position() * 100)
        label_text = '{}%'.format(progress_percent)
        self.music_progress.set(label_text)
        self.progress_ba["value"] = progress_percent
        if (self.player.get_position() * 100) > 99:
            self.next_track()
        self.after(100, self.progress_bar_func)



    def pafy_function_direct_play(self, para):

        #variables - global
        self.title_var.set('BLANK ')
        #variables - local
        vid = ''
        aud = ''

        vid = pafy.new(para)
        aud = vid.getbestaudio()
        self.title_var.set(vid.title)
        self.linkplayer(aud.url)
        self.name.set('')



    def pafy_function_fetch_and_show(self, para):

        #variables - local
        top_vids_temp = []
        #variables - global
        self.top_vids = []
        self.playlist_dict = {}

        r = requests.get(para)
        page_source = r.text

        temp_reg = re.compile(r'/watch\?v=.{11}')
        mat = re.findall(temp_reg, page_source)
        #pprint.pprint(mat)
        for m in mat:
            if m not in top_vids_temp:
                top_vids_temp.append(m)
                if len(top_vids_temp) > 2:
                    break
        #pprint.pprint(top_vids_temp)
        for v in top_vids_temp:
                x = 'https://www.youtube.com' + v
                if x not in self.top_vids:
                    self.top_vids.append(x)
        #pprint.pprint(self.top_vids)


        my_thread1 = threading.Thread(target=self.pafy_function_returns_list, args=(self.top_vids,))
        my_thread1.start()
        


    def pafy_function_returns_list(self, para):

        for p in para:
            if p not in self.playlist_dict:
                vid = pafy.new(p)
                time.sleep(3)
                self.playlist_dict[p] = vid.title
        self.ournewwindow(self.playlist_dict, self.top_vids)
        self.name.set('Showing top3 new stuff . . .')        


    def print_contents(self, event):

        #local variables
        temp_self_name = self.name.get()
        
        if 'www.youtube.com/watch?v=' in temp_self_name:
            self.pafy_function_direct_play(temp_self_name)


        elif 'www.youtube.com/user/' in temp_self_name:
            self.pafy_function_fetch_and_show(temp_self_name)

        elif 'www.youtube.com/channel/' in temp_self_name:
            self.pafy_function_fetch_and_show(temp_self_name)
        
        elif temp_self_name.endswith('.mp3'):
            self.link_offline_player(self.name.get())

        else:
            self.name.set('try again')




    def onopen(self):
        dlg = filedialog.askopenfilenames()
        fl = list(dlg)

        #variables - local
        top_vids_temp = []
        #variables - global
        self.top_vids = []
        self.playlist_dict = {}

        if len(fl) > 0:
            
            for f in fl:
                if f not in self.top_vids:
                    self.top_vids.append(f)
                    self.playlist_dict[f] = f
            self.ournewwindow(self.playlist_dict, self.top_vids)
            



    def ournewwindow(self, para_dict, ek_list):
        
        for k, v in para_dict.items():
            if k == v:

                self.f4_tree['selectmode'] = 'browse'
                self.f4_tree['show'] = 'headings'
                self.f4_tree["columns"]=("one","two")
                self.f4_tree.column("one", width=5)
                self.f4_tree.column("two", width=500)
                self.f4_tree.heading("one", text="Count")
                self.f4_tree.heading("two", text="Name")

                self.f4_tree.delete(*self.f4_tree.get_children())

                for i in range(len(ek_list)):

                    self.f4_tree.insert("" , i, text='Track {}'.format(i), values=(i, ek_list[i]))
                
                self.f4_tree.pack(side='left', fill='both', expand=True)
                self.f4_tree.bind("<<TreeviewSelect>>", self.select_item)

                break
                
            else:
            
                self.f4_tree['selectmode'] = 'browse'
                self.f4_tree["columns"]=("one","two")
                self.f4_tree.column("one", width=5)
                self.f4_tree.column("two", width=100)
                self.f4_tree.heading("one", text="Count")
                self.f4_tree.heading("two", text="Name")

                self.f4_tree.delete(*self.f4_tree.get_children())


                for i in range(len(ek_list)):

                    self.f4_tree.insert("" , i, text=i, values=(ek_list[i], para_dict[ek_list[i]]))

                
                self.f4_tree.pack(side='left', fill='both', expand=True)
                self.f4_tree.bind('<<TreeviewSelect>>', self.select_item_online)
           
                break



    def select_item_online(self, b):
        cur_item = self.f4_tree.focus()
        v = self.f4_tree.item(cur_item)
        #self.pafy_function_direct_play(v['values'][0])
        
        thread0001 = threading.Thread(target=self.pafy_function_direct_play(v['values'][0]))
        thread0001.start()



    def select_item(self, a):
        cur_item = self.f4_tree.focus()
        v = self.f4_tree.item(cur_item)
        #self.link_offline_player(v['values'][1])

        thread0010 = threading.Thread(target=self.link_offline_player(v['values'][1]))
        thread0010.start()
        

    
    def add_favorite_channel(self):

        #local variables
        link = tk.StringVar()
        name = tk.StringVar()

        ttk.Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        #inner function
        def add_but_click():
            link_var = link.get()
            name_var = name.get()
            self.add_to_fav_button_click(name_var, link_var)
            top.destroy()
            top.grab_release()

        self.columnconfigure(0, pad=2)
        self.columnconfigure(1, pad=2)
        self.columnconfigure(2, pad=2)
        self.columnconfigure(3, pad=2)
        self.columnconfigure(4, pad=2)
        self.columnconfigure(5, pad=2)
        self.columnconfigure(6, pad=2)

        self.rowconfigure(0, pad=2)
        self.rowconfigure(1, pad=2)
        self.rowconfigure(2, pad=2)
        self.rowconfigure(3, pad=2)
        self.rowconfigure(4, pad=2)
        self.rowconfigure(5, pad=2)
        self.rowconfigure(6, pad=2)

        top = tk.Toplevel()
        top.title('Add Favorite Channel')

        top.grab_set()

        afc_fill1 = ttk.Label(top, text=' ')
        afc_fill1.grid(row=0)

        afc_lable1 = ttk.Label(top, text='URL of channel - video page : ')
        afc_lable1.grid(row=1)

        afc_entry1 = ttk.Entry(top, width=70)
        afc_entry1["textvariable"] = link
        afc_entry1.grid(row=1, column=2, columnspan=4)

        afc_fill2 = ttk.Label(top, text='Channel Name : ')
        afc_fill2.grid(row=3, ipady=10, sticky='e')

        afc_entry2 = ttk.Entry(top, width=70)
        afc_entry2["textvariable"] = name
        afc_entry2.grid(row=3, column=2, columnspan=4)

        afc_button1 = ttk.Button(top, text='DONE', command= add_but_click)
        afc_button1.grid(row=5, column=4, sticky='e')

        afc_button2 = ttk.Button(top, text='CANCEL', command=top.destroy)
        afc_button2.grid(row=5, column=5)
        
        afc_fill3 = ttk.Label(top, text=' ')
        afc_fill3.grid(row=6, column=6)

        top.resizable(width=False, height=False)



    def show_favorite_channel(self):
        
        self.f4_tree['selectmode'] = 'browse'
        self.f4_tree['show'] = 'headings'
        self.f4_tree["columns"]=("one","two")
        self.f4_tree.column("one", width=100)
        self.f4_tree.column("two", width=500)
        self.f4_tree.heading("one", text="Channel Name")
        self.f4_tree.heading("two", text="Channel Link")

        self.f4_tree.delete(*self.f4_tree.get_children())

        var = show_fav_table()

        for v in var:
            self.f4_tree.insert("" , v[0], text='item {}'.format(v[0]), values=(v[2], v[3]))

        self.f4_tree.bind("<Button-3>", self.do_popup)
        self.f4_tree.pack(side='left', fill='both', expand=True)


    def add_to_fav_button_click(self, name, link):
        insert_in_fav_table(datetime.datetime.now(), name, link)


    def discover_new_music_function(self):
        
        if not self.toop:
            self.toop = tk.Toplevel()
            self.toop.title('New Music from All Channels')

            self.a_lbl_holder_list = []

            self.toop_frame1 = ttk.Frame(self.toop, border=5)
            self.toop_frame1.pack(side='top', expand=True, fill='both')

            self.toop_f1_tree = ttk.Treeview(self.toop_frame1, columns=("size", "modified"))
            scrollbar_vertical = ttk.Scrollbar(self.toop_frame1, orient='vertical', command=self.toop_f1_tree.yview)
            scrollbar_vertical.pack(side='right', fill='y')
            self.toop_f1_tree.configure(yscrollcommand=scrollbar_vertical.set)
            self.toop_f1_tree.pack(side='left', expand=True, fill='both')


            self.toop_f1_tree['show'] = 'headings'
            self.toop_f1_tree['selectmode'] = 'browse'
            self.toop_f1_tree["columns"]=("one","two", "three")
            self.toop_f1_tree.column("one", width=5)
            self.toop_f1_tree.column("two", width=100)
            self.toop_f1_tree.heading("one", text="Count")
            self.toop_f1_tree.heading("two", text="Name")
            self.toop_f1_tree.heading("three", text="Views")

            self.toop_f1_tree.bind('<<TreeviewSelect>>', self.select_item_online_discover)



            thread00 = threading.Thread(target=self.discover_new_music_fetch_and_show)
            thread00.start()

            self.toop.protocol("WM_DELETE_WINDOW", self.on_exit_toop_helper)
        


    def discover_new_music_fetch_and_show(self):
       
        discover_channel_links = select_channel_link_from_fav_table()

        for link in discover_channel_links:
    
           #variables - local
            top_vids_temp = []
            top_vids_temp2 = []
       
            r = requests.get(link[3])
            time.sleep(3)
            page_source = r.text

            temp_reg = re.compile(r'/watch\?v=.{11}')
            mat = re.findall(temp_reg, page_source)
            #pprint.pprint(mat)

            for m in mat:
                if m not in top_vids_temp:
                    top_vids_temp.append(m)
                    if len(top_vids_temp) > 2:
                        break
            #pprint.pprint(top_vids_temp)
            for v in top_vids_temp:
                    x = 'https://www.youtube.com' + v
                    if x not in top_vids_temp2:
                        top_vids_temp2.append(x)
            #pprint.pprint(self.top_vids)

            my_thread11 = threading.Thread(target=self.pafy_function_returns_list_discover_music, args=(top_vids_temp2,))
            my_thread11.start()
            
            time.sleep(13)



    def pafy_function_returns_list_discover_music(self, para):

        #local variable
        title = ''

        for p in para:
            vid = pafy.new(p)
            time.sleep(3)
            title = vid.title
            self.toop_f1_tree.insert("" , 0, text=p, values=(vid.author, vid.duration, title))



    def select_item_online_discover(self, b):
        
        cur_item = self.toop_f1_tree.focus()
        v = self.toop_f1_tree.item(cur_item)
        self.pafy_function_direct_play(v['text'])




    def on_exit_toop_helper(self):
        self.toop.destroy()
        self.toop = None


    def onexit(self):
        self.quit()


    
    def do_popup(self, event):
        try:
            self.popup.selection = self.f4_tree.set(self.f4_tree.identify_row(event.y))
            self.popup.post(event.x_root, event.y_root)

        finally:
            self.popup.grab_release()


    def selextion(self):
        pass


    def remove_one_favorite_channel(self):
        var = self.popup.selection
        link = var['two']
        delete_from_favorites(link)
        self.show_favorite_channel()

    def show_music_favorite_channel(self):
        var = self.popup.selection
        link = var['two']
        my_thread0 = threading.Thread(target=self.pafy_function_fetch_and_show, args=(link,))
        my_thread0.start()
        self.name.set('showing music from "{}" in 10 seconds . . . '.format(var['one']))



#-------------------sql functions ------------------



def create_fav_table():
    conn = sqlite3.connect('beatsync.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS favorites_table(favid INTEGER PRIMARY KEY, dateadded TEXT, channelname TEXT, channelink TEXT)")
    conn.commit()
    conn.close()

def insert_in_fav_table(date, name, link):
    conn = sqlite3.connect('beatsync.db')
    cur = conn.cursor()
    data = cur.execute('SELECT channelink FROM favorites_table')
    #data contains number of tuples
    temp_list = []
    for d in data:
        temp_list.append(d[0])

    if link not in temp_list:
        cur.execute('INSERT INTO favorites_table VALUES(NULL, ?, ?, ?)',(date, name, link))
        conn.commit()
        conn.close()
    else:        
        print('this data is already present in database')

        
def select_channel_link_from_fav_table():
    conn = sqlite3.connect('beatsync.db')
    cur = conn.cursor()
    data = cur.execute('SELECT * FROM favorites_table')
    return data

def show_fav_table():
    conn = sqlite3.connect('beatsync.db')
    cur = conn.cursor()
    var = cur.execute('SELECT * FROM favorites_table')
    return var


def delete_from_favorites(link):
    conn = sqlite3.connect('beatsync.db')
    cur = conn.cursor()
    
    cur.execute("DELETE FROM favorites_table WHERE channelink=?", (link,))
    conn.commit()
    conn.close()



    


#-----------------------------------------if name == main
root = tk.Tk()
root.geometry("700x400")
app = Application()

app.mainloop()
