import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import numpy as np
import matplotlib.animation as animation


class App(tk.Tk):

    outer_left_menu_frame = None
    outer_main_frame = None

    inner_left_menu_frame = None
    inner_main_frame = None

    array_entry = None
    array_entry_value = None

    array_size_label = None
    array_size_slider = None
    size_value = None

    sorting_speed_label = None
    sorting_speed_slider = None
    sorting_speed = None

    sorting_algo_label = None
    sorting_algo_value = None
    sorting_algo_selection_sort_rb = None
    sorting_algo_bubble_sort_rb = None
    sorting_algo_insertion_sort_rb = None
    sorting_algo_merge_sort_rb = None
    sorting_algo_quick_sort_rb = None

    graph_type_label = None
    graph_type_value = None
    scatter_graph_rb = None
    bar_graph_rb = None
    stem_graph_rb = None

    button_frame = None
    create_button = None
    start_button = None
    pause_resume_button = None
    reset_button = None

    unsorted_array = []
    compared_indices = []
    sorted_indices = []

    graph_canvas = None
    animation = None

    is_animation_paused = False

    comparison_counter_value = None
    comparison_counter_label = None
    best_time_complexity_label = None
    avarage_time_complexity_label = None
    worst_time_complexity_label = None
    space_complexity_label = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=1650, height=900)
        self.title("Sıralama Algoritmaları Görselleştiricisi")

        self.outer_left_menu_frame = ttk.Frame(self)
        self.outer_left_menu_frame.place(
            relheight=1.0, relwidth=0.25, relx=0.0, rely=0.0)

        self.style1 = ttk.Style()
        self.style1.configure("label2.TFrame", background="blue")

        self.outer_main_frame = ttk.Frame(
            self)
        self.outer_main_frame.place(
            relheight=1.0, relwidth=0.75, relx=0.25, rely=0.0)

        self.inner_main_frame = self.inner_left_menu_frame = ttk.Frame(
            self.outer_main_frame)
        self.inner_main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.inner_left_menu_frame = ttk.Frame(self.outer_left_menu_frame)
        self.inner_left_menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.size_value = tk.IntVar(value=1)
        self.array_size_label = ttk.Label(
            self.inner_left_menu_frame, text=f"Boyut: {self.size_value.get()}", anchor="center", font=("Segoe UI", 16, "bold"))
        self.array_size_label.pack(padx=5, pady=5)
        self.array_size_slider = ttk.Scale(self.inner_left_menu_frame, from_=1.0, to=30.0,
                                           variable=self.size_value, command=self.size_slider_change, length=250)
        self.array_size_slider.pack(padx=5, pady=5)
        tk.Label(self.inner_left_menu_frame, text="Manuel Değerler", font=(
            "Segoe UI", 10, "bold"), anchor="center").pack(padx=5, pady=5)
        self.array_entry_value = tk.StringVar(value="")
        self.array_entry = ttk.Entry(self.inner_left_menu_frame, textvariable=self.array_entry_value,
                                     width=50, validate="key", validatecommand=(self.register(self.validate_entry), '%S'))
        self.array_entry.pack(padx=5, pady=5)

        self.sorting_speed = tk.IntVar(value=1)
        self.sorting_speed_label = ttk.Label(
            self.inner_left_menu_frame, text=f"Hız: {self.sorting_speed.get()}", anchor="center", font=("Segoe UI", 16, "bold"))
        self.sorting_speed_label.pack(padx=5, pady=5)
        self.sorting_speed_slider = ttk.Scale(self.inner_left_menu_frame, from_=1.0, to=10.0,
                                              variable=self.sorting_speed, command=self.speed_slider_change, length=250)
        self.sorting_speed_slider.pack(padx=5, pady=5)

        self.sorting_algo_value = tk.StringVar(value="selection_sort")
        self.sorting_algo_label = ttk.Label(
            self.inner_left_menu_frame, text="Sıralama Algoritmaları", anchor="center", font=("Segoe UI", 16, "bold"))
        self.sorting_algo_label.pack(padx=5, pady=5)

        self.sorting_algo_selection_sort_rb = ttk.Radiobutton(
            self.inner_left_menu_frame, text='Seçme Sıralaması (Selection Sort)', value='selection_sort', variable=self.sorting_algo_value)
        self.sorting_algo_selection_sort_rb.pack(padx=5, pady=5)

        self.sorting_algo_bubble_sort_rb = ttk.Radiobutton(
            self.inner_left_menu_frame, text='Kabarcık Sıralaması (Bubble Sort)', value='bubble_sort', variable=self.sorting_algo_value)
        self.sorting_algo_bubble_sort_rb.pack(padx=5, pady=5)

        self.sorting_algo_insertion_sort_rb = ttk.Radiobutton(
            self.inner_left_menu_frame, text='Ekleme Sıralaması (Insertion Sort)', value='insertion_sort', variable=self.sorting_algo_value)
        self.sorting_algo_insertion_sort_rb.pack(padx=5, pady=5)

        self.sorting_algo_merge_sort_rb = ttk.Radiobutton(
            self.inner_left_menu_frame, text='Birleştirme Sıralaması (Merge Sort)', value='merge_sort', variable=self.sorting_algo_value)
        self.sorting_algo_merge_sort_rb.pack(padx=5, pady=5)

        self.sorting_algo_quick_sort_rb = ttk.Radiobutton(
            self.inner_left_menu_frame, text='Hızlı Sıralama (Quick Sort)', value='quick_sort', variable=self.sorting_algo_value)
        self.sorting_algo_quick_sort_rb.pack(padx=5, pady=5)

        self.graph_type_value = tk.StringVar(value="scatter_graph")
        self.graph_type_label = ttk.Label(
            self.inner_left_menu_frame, text="Grafik Tipleri", anchor="center", font=("Segoe UI", 16, "bold"))
        self.graph_type_label.pack(padx=5, pady=5)

        self.scatter_graph_rb = ttk.Radiobutton(
            self.inner_left_menu_frame, text='Dağılım (Scatter) Grafiği', value='scatter_graph', variable=self.graph_type_value)
        self.scatter_graph_rb.pack(padx=5, pady=5)

        self.bar_graph_rb = ttk.Radiobutton(
            self.inner_left_menu_frame, text='Sütun (Bar) Grafiği', value='bar_graph', variable=self.graph_type_value)
        self.bar_graph_rb.pack(padx=5, pady=5)

        self.stem_graph_rb = ttk.Radiobutton(
            self.inner_left_menu_frame, text='Kök (Stem) Grafiği', value='stem_graph', variable=self.graph_type_value)
        self.stem_graph_rb.pack(padx=5, pady=5)

        self.button_frame = ttk.Frame(self.inner_left_menu_frame)
        self.button_frame.pack(padx=5, pady=5)
        self.create_button = ttk.Button(
            self.button_frame, text="Oluştur", command=self.create)
        self.create_button.pack(side="left")
        self.start_button = ttk.Button(
            self.button_frame, text="Başla", command=self.start)
        self.start_button.pack(side="left")
        self.pause_resume_button = ttk.Button(
            self.button_frame, text="Dur", command=self.pause_resume)
        self.pause_resume_button.pack(side="left")
        self.reset_button = ttk.Button(
            self.button_frame, text="Sıfırla", command=self.reset)
        self.reset_button.pack(side="left")

        self.comparison_counter_value = tk.IntVar(value=0)
        self.start_button.config(state=tk.DISABLED)
        self.pause_resume_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

    def destroy(self):
        return super().destroy()
    
    def validate_entry(self, text):
        return all(c.isdigit() or c.isspace() or c == "-" for c in text)

    def size_slider_change(self, event):
        self.array_size_label.config(text=f"Boyut: {self.size_value.get()}")

    def speed_slider_change(self, event):
        self.sorting_speed_label.config(
            text=f"Hız: {self.sorting_speed.get()}")

    def create(self):
        print(self.sorting_algo_value.get())
        if self.array_entry_value.get() != "":
            self.unsorted_array = np.fromstring(
                self.array_entry_value.get(), dtype=int, sep=' ')
        else:
            self.unsorted_array = np.random.randint(
                0, 100, self.size_value.get())
        print(self.unsorted_array)
        if self.graph_canvas is None:
            self.fig, self.ax = plt.subplots(figsize=(12, 6))
            self.graph_canvas = FigureCanvasTkAgg(
                self.fig, master=self.inner_main_frame)
            self.graph_canvas.get_tk_widget().pack(side=tk.TOP, expand=1)

        self.draw_graph()
        self.start_button.config(state=tk.ACTIVE)
        self.array_entry_value.set("")

    def start(self):

        if self.sorting_algo_value.get() == "selection_sort":
            self.animation = animation.FuncAnimation(self.fig, self.draw_animation, frames=self.selection_sort(self.unsorted_array),
                                                     interval=1000/self.sorting_speed.get(),
                                                     repeat=False)
            self.graph_canvas.draw()

            self.best_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En İyi Zaman : O(n*n)", font=("Segoe UI", 16, "bold"))
            self.best_time_complexity_label.pack(pady=5)
            self.worst_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En Kötü Zaman : O(n*n)", font=("Segoe UI", 16, "bold"))
            self.worst_time_complexity_label.pack(pady=5)
            self.avarage_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Ortalama Zaman : O(n*n)", font=("Segoe UI", 16, "bold"))
            self.avarage_time_complexity_label.pack(pady=5)
            self.space_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Alan Karmaşıklığı : O(1)", font=("Segoe UI", 16, "bold"))
            self.space_complexity_label.pack(pady=5)
        elif self.sorting_algo_value.get() == "bubble_sort":
            self.animation = animation.FuncAnimation(self.fig, self.draw_animation, frames=self.bubble_sort(self.unsorted_array),
                                                     interval=1000/self.sorting_speed.get(),
                                                     repeat=False)
            self.graph_canvas.draw()

            self.best_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En İyi Zaman : O(n*n)", font=("Segoe UI", 16, "bold"))
            self.best_time_complexity_label.pack(pady=5)
            self.worst_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En Kötü Zaman : O(n*n)", font=("Segoe UI", 16, "bold"))
            self.worst_time_complexity_label.pack(pady=5)
            self.avarage_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Ortalama Zaman : O(n*n)", font=("Segoe UI", 16, "bold"))
            self.avarage_time_complexity_label.pack(pady=5)
            self.space_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Alan Karmaşıklığı : O(1)", font=("Segoe UI", 16, "bold"))
            self.space_complexity_label.pack(pady=5)

        elif self.sorting_algo_value.get() == "insertion_sort":
            self.animation = animation.FuncAnimation(self.fig, self.draw_animation, frames=self.insertion_sort(self.unsorted_array),
                                                     interval=1000/self.sorting_speed.get(),
                                                     repeat=False)
            self.graph_canvas.draw()

            self.best_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En İyi Zaman : O(n)", font=("Segoe UI", 16, "bold"))
            self.best_time_complexity_label.pack(pady=5)
            self.worst_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En Kötü Zaman : O(n*n)", font=("Segoe UI", 16, "bold"))
            self.worst_time_complexity_label.pack(pady=5)
            self.avarage_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Ortalama Zaman : O(n*n)", font=("Segoe UI", 16, "bold"))
            self.avarage_time_complexity_label.pack(pady=5)
            self.space_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Alan Karmaşıklığı : O(1)", font=("Segoe UI", 16, "bold"))
            self.space_complexity_label.pack(pady=5)
        elif self.sorting_algo_value.get() == "merge_sort":
            self.animation = animation.FuncAnimation(self.fig, self.draw_animation, frames=self.mergesort(self.unsorted_array, 0, len(self.unsorted_array)-1),
                                                     interval=1000/self.sorting_speed.get(),
                                                     repeat=False)
            self.graph_canvas.draw()

            self.best_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En İyi Zaman : O(n*logn)", font=("Segoe UI", 16, "bold"))
            self.best_time_complexity_label.pack(pady=5)
            self.worst_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En Kötü Zaman : O(n*logn)", font=("Segoe UI", 16, "bold"))
            self.worst_time_complexity_label.pack(pady=5)
            self.avarage_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Ortalama Zaman : O(n*logn)", font=("Segoe UI", 16, "bold"))
            self.avarage_time_complexity_label.pack(pady=5)
            self.space_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Alan Karmaşıklığı : O(n)", font=("Segoe UI", 16, "bold"))
            self.space_complexity_label.pack(pady=5)
        elif self.sorting_algo_value.get() == "quick_sort":
            self.animation = animation.FuncAnimation(self.fig, self.draw_animation, frames=self.quicksort(self.unsorted_array, 0, len(self.unsorted_array)-1),
                                                     interval=1000/self.sorting_speed.get(),
                                                     repeat=False)
            self.graph_canvas.draw()

            self.best_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En İyi Zaman : O(n*logn)", font=("Segoe UI", 16, "bold"))
            self.best_time_complexity_label.pack(pady=5)
            self.worst_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="En Kötü Zaman : O(n*n)", font=("Segoe UI", 16, "bold"))
            self.worst_time_complexity_label.pack(pady=5)
            self.avarage_time_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Ortalama Zaman : O(n*logn)", font=("Segoe UI", 16, "bold"))
            self.avarage_time_complexity_label.pack(pady=5)
            self.space_complexity_label = tk.Label(
                master=self.inner_main_frame, text="Alan Karmaşıklığı : O(logn)", font=("Segoe UI", 16, "bold"))
            self.space_complexity_label.pack(pady=5)

        self.create_button.config(state=tk.DISABLED)
        self.pause_resume_button.config(state=tk.ACTIVE)
        self.reset_button.config(state=tk.ACTIVE)
        self.start_button.config(state=tk.DISABLED)

    def pause_resume(self):
        if self.animation is not None:
            if(self.is_animation_paused):
                self.pause_resume_button.config(text="Dur")
                self.animation.resume()
                self.is_animation_paused = False
            else:
                self.pause_resume_button.config(text="Devam Et")
                self.animation.pause()
                self.is_animation_paused = True

    def reset(self):
        for child in self.inner_main_frame.winfo_children():
            child.destroy()

        self.start_button.config(state=tk.DISABLED)
        self.pause_resume_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.create_button.config(state=tk.ACTIVE)
        self.ax = None
        self.fig = None
        self.graph_canvas = None
        self.animation = None
        self.is_animation_paused = False
        self.pause_resume_button.config(text="Dur")
        self.unsorted_array = []
        self.compared_indices = []
        self.sorted_indices = []
        self.comparison_counter_value.set(0)
        self.array_entry_value.set("")

    def draw_graph(self):
        self.ax.clear()  # clear the previous plot
        if self.graph_type_value.get() == "scatter_graph":
            self.create_scatter_plot()
        elif self.graph_type_value.get() == "bar_graph":
            self.create_bar_chart()
        elif self.graph_type_value.get() == "stem_graph":
            self.create_stem_plot()
        self.ax.set_xticks(np.arange(0, len(self.unsorted_array), 1))
        self.ax.set_yticks(np.arange(min(self.unsorted_array),
                           max(self.unsorted_array) + 5, 5))
        self.ax.set_ylabel("Dizi Elemanı")
        self.ax.set_xlabel("İndeks")
        self.graph_canvas.draw()

    def draw_animation(self, values):
        self.ax.clear()  # clear the previous plot
        if self.graph_type_value.get() == "scatter_graph":
            self.create_scatter_plot()
        elif self.graph_type_value.get() == "bar_graph":
            self.create_bar_chart()
        elif self.graph_type_value.get() == "stem_graph":
            self.create_stem_plot()
        self.ax.set_xticks(np.arange(0, len(self.unsorted_array), 1))
        self.ax.set_yticks(np.arange(min(self.unsorted_array),
                           max(self.unsorted_array) + 5, 5))
        self.ax.set_ylabel("Dizi Elemanı")
        self.ax.set_xlabel("İndeks")
        self.ax.set_title(
            f"Karşılaştırma Sayısı : {self.comparison_counter_value.get()}")
        self.graph_canvas.draw()

    def create_scatter_plot(self):
        x = np.arange(len(self.unsorted_array))
        y = self.unsorted_array
        colors = []
        for i in range(len(self.unsorted_array)):
            if i in self.compared_indices:
                colors.insert(i, "green")
            elif i in self.sorted_indices:
                colors.insert(i, "blue")
            else:
                colors.insert(i, "red")
        self.ax.scatter(x, y, color=colors)

    def create_bar_chart(self):
        x = np.arange(len(self.unsorted_array))
        y = self.unsorted_array
        colors = []
        for i in range(len(self.unsorted_array)):
            if i in self.compared_indices:
                colors.insert(i, "green")
            elif i in self.sorted_indices:
                colors.insert(i, "blue")
            else:
                colors.insert(i, "red")
        self.ax.bar(x, y, color=colors)

    def create_stem_plot(self):
        x = np.arange(len(self.unsorted_array))
        y = self.unsorted_array
        colors = []
        for i in range(len(self.unsorted_array)):
            if i in self.compared_indices:
                colors.insert(i, "green")
            elif i in self.sorted_indices:
                colors.insert(i, "blue")
            else:
                colors.insert(i, "red")
        self.ax.vlines(x, min(y), y, colors=colors, linestyles='solid')
        self.ax.plot(x, y, 'o', ms=5, c='darkorange')

    def bubble_sort(self, array):

        for i in range(len(array)):
            for j in range(len(array)-i-1):
                self.compared_indices.extend([j, j+1])
                if array[j] > array[j+1]:
                    array[j], array[j+1] = array[j+1], array[j]
                self.comparison_counter_value.set(
                    self.comparison_counter_value.get() + 1)
                yield array
                self.compared_indices = []
            self.sorted_indices.append(len(array)-i-1)
            yield array

    def selection_sort(self, array):
        for i in range(len(array)):
            min_idx = i
            for j in range(i+1, len(array)):
                self.compared_indices.extend([j, min_idx])
                if array[j] < array[min_idx]:
                    min_idx = j
                self.comparison_counter_value.set(
                    self.comparison_counter_value.get() + 1)
                yield array
                self.compared_indices = []
            array[i], array[min_idx] = array[min_idx], array[i]
            self.sorted_indices.append(i)
            yield array
        return array

    def insertion_sort(self, array):
        sorted_array = np.sort(array)
        for i in range(1, len(array)):
            key = array[i]
            new_array = np.insert(array, len(array), key)
            j = i - 1
            while j >= 0 and array[j] > key:
                self.compared_indices.extend(
                    [j, np.where(new_array == key)[0][0]])
                self.comparison_counter_value.set(
                    self.comparison_counter_value.get() + 1)
                yield array
                self.compared_indices = []
                array[j+1] = array[j]
                j -= 1

            array[j+1] = key
            yield array
        return array
    
    # https://www.geeksforgeeks.org/visualization-of-merge-sort-using-matplotlib/ 'den alınmıştır.
    def mergesort(self, array, start, end):
        if end <= start:
            return

        mid = start + ((end - start + 1) // 2) - 1

        yield from self.mergesort(array, start, mid)
        yield from self.mergesort(array, mid + 1, end)
        yield from self.merge(array, start, mid, end)

    def merge(self, array, start, mid, end):
        merged = []
        leftIdx = start
        rightIdx = mid + 1

        while leftIdx <= mid and rightIdx <= end:
            self.compared_indices.extend([leftIdx, rightIdx])
            self.comparison_counter_value.set(
                self.comparison_counter_value.get() + 1)
            yield array
            if array[leftIdx] < array[rightIdx]:
                merged.append(array[leftIdx])
                leftIdx += 1
            else:
                merged.append(array[rightIdx])
                rightIdx += 1
            self.compared_indices = []

        while leftIdx <= mid:
            merged.append(array[leftIdx])
            leftIdx += 1

        while rightIdx <= end:
            merged.append(array[rightIdx])
            rightIdx += 1

        for i in range(len(merged)):
            array[start + i] = merged[i]
            self.sorted_indices.append(start + i)
            yield array

    def quicksort(self, array, start, end):
        if start < end:
            pivot = array[end]
            boundry = start - 1
            for i in range(start, end+1):
                self.compared_indices.extend([i, end])
                self.comparison_counter_value.set(
                    self.comparison_counter_value.get() + 1)
                if array[i] <= pivot:
                    boundry += 1
                    (array[boundry], array[i]) = (array[i], array[boundry])
                yield array
                self.compared_indices = []
            self.sorted_indices.append(boundry)
            yield array

            yield from self.quicksort(array=array, start=start, end=boundry-1)
            yield from self.quicksort(array=array, start=boundry+1, end=end)
            return array

    """ def partition(self, array, start, end):
        pivot = array[end]
        boundry = start - 1
        for i in range(start, end+1):
            self.compared_indices.extend([i, end])
            if array[i] <= pivot:
                boundry += 1
                (array[boundry], array[i]) = (array[i], array[boundry])
            yield array
            self.compared_indices = []
        return boundry """


app = App()
app.mainloop()
