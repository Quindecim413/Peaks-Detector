from PyQt5.QtWidgets import QFileDialog
from IPython.display import display

from ipywidgets import interact
from ipywidgets import Button
import ipywidgets as widgets
from IPython.display import clear_output
import os, re, pandas as pd, numpy as np

def select_upload_files(dir=None):
    """Select a file via a dialog and return the file name."""
    if dir is None: dir ='./'
    fname = QFileDialog.getOpenFileNames(None, "Select data file...", 
                dir, filter="Column data files (*.csv *.txt)")
    return fname[0]

def select_save_dir():
    return str(QFileDialog.getExistingDirectory(None, "Select Directory"))



files = []
def files_selection():
    def update():
        clear_output()
        display(buttons)

        files_masks = list(filter(lambda el: '*' in el, files))
        files_others = list(filter(lambda el: '*' not in el, files))

        from glob import glob
        childs = []
        titles = []
        for ind, file in enumerate(files_masks):
            title = file
            if check_mask(file):
                fls = glob(file)
                t = widgets.VBox([widgets.Label(value=f) for f in fls])

                title = title + ' (Найлено {})'.format(len(fls))

                if not t:
                    t = widgets.Label(value='Ничего не найдено')
            else:
                title = title + ' (Не верная маска)'
                t = widgets.Label(value='Не верная маска. На конце должно быть .csv или .txt')

            def wrap_delete():
                f_ind = ind
                def delete_file(b):
                    global files
                    del files_masks[f_ind]
                    files = [*files_masks, *files_others]
                    update()
                return delete_file
            delete_btn = widgets.Button(description='Удалить')
            delete_btn.on_click(wrap_delete())
            t = widgets.VBox([delete_btn, t])
            childs.append(t)
            titles.append(title)

        display(widgets.Label(value="Файлы найденные по маскам"))
        masked = widgets.Accordion(children=childs)
        for ind, file in enumerate(titles):
            masked.set_title(ind, file)
        display(masked)

        display(widgets.Label(value='Иные файлы'))
        for ind, file in enumerate(files_others):
            delete_btn = widgets.Button(description='Удалить')
            text = widgets.Text(value=file, layout=widgets.Layout(width='80%'))
            l = widgets.HBox([text, delete_btn])

            def wrap_delete():
                f_ind = ind
                def delete_file(b):
                    global files
                    del files_others[f_ind]
                    files = [*files_masks, *files_others]
                    update()
                return delete_file

            def wrap_edit():
                f_ind = ind
                text_el = text
                def edit_file(change):
                    if '*' in change['new']:
                        change['owner'].value = change['old'] 
                    else:
                        files[f_ind] = change['new']
                return edit_file

            text.observe(wrap_edit(), names='value')

            delete_btn.on_click(wrap_delete())

            display(l)

    def add_file(b):
        add_btn.disabled = True
        file = select_upload_files()
        add_btn.disabled = False 
        if file:
            files.extend(file)
        update()

    def add_empty_file(b):
        files.append('')
        update()

    def add_mask(b):
        clear_output()
        display(widgets.Label(value='Введите маску'))

        text = widgets.Text(layout=widgets.Layout(width='80%'))
        submit_mask = widgets.Button(description='Создать маску')
        display(widgets.HBox([text, submit_mask]))
        def submit(b):
            inserted = text.value
            files.append(inserted)
            update()

        submit_mask.on_click(submit)

    add_btn = widgets.Button(description="Добавить файл", layout=widgets.Layout(width='auto'))
    add_text_btn = widgets.Button(description="Добавить файл вручную", layout=widgets.Layout(width='auto'))

    add_mask_btn = widgets.Button(description="Добавить маску", layout=widgets.Layout(width='auto'))

    box_layout = widgets.Layout(display='flex',
                        flex_flow='row',
                        border='solid')
    buttons = widgets.HBox([add_btn, add_text_btn, add_mask_btn], layout=box_layout)
    display(buttons)

    add_btn.on_click(add_file)
    add_text_btn.on_click(add_empty_file)
    add_mask_btn.on_click(add_mask)

def check_mask(mask):
    return mask.endswith('.csv') or mask.endswith('.txt')

def confirmation(intermidiate_printing=True):
    global do_itermidiate_print
    do_itermidiate_print = intermidiate_printing
    delta_upper = widgets.BoundedFloatText(
        value=1,
        min=0,
        max=1000.0,
        step=0.001,
        disabled=False
    )
    delta_upper_label = widgets.Label(value='Дельта +')
    mean_val = widgets.BoundedFloatText(
        value=0,
        min=0,
        max=1000.0,
        step=0.001,
        disabled=False
    )
    mean_val_label = widgets.Label(value='Среднее значение')

    delta_lower = widgets.BoundedFloatText(
        value=1,
        min=0,
        max=1000.0,
        step=0.001,
        disabled=False
    )
    delta_lower_label = widgets.Label(value='Дельта -')

    grid = widgets.GridBox([
        delta_upper_label, delta_upper,
        mean_val_label, mean_val,
        delta_lower_label, delta_lower
    ], layout=widgets.Layout(widht='auto',grid_template_columns="repeat(2, 200px)"))
    display(grid)

    check_index_from_1 = widgets.Checkbox(
        description='Индексировать с 1', 
        value=False,
        disabled=False,
        indent=False)

    check_add_headers = widgets.Checkbox(
        description='Добавлять заголовки', 
        value=True,
        disabled=False,
        indent=False)
    display(check_index_from_1)
    display(check_add_headers)

    def select_save_dir_event(b):
        button_select_save_dir.disabled = True
        save_dir = select_save_dir()
        button_select_save_dir.disabled = False
        if save_dir:
            text_save_dir.value = save_dir

    text_save_dir = widgets.Text(layout=widgets.Layout(width='60%'))
    
    def check_text_in_save_dir_changed(changed):
        if os.path.exists(changed['new']) and os.path.isdir(changed['new']):
            
            button_start.description = 'Начать обработку'
            button_start.disabled = False
        else:
            button_start.description = 'Перед началом обработки установите папку сохранени'
            button_start.disabled = True
    
    text_save_dir.observe(check_text_in_save_dir_changed, names='value')
    
    button_select_save_dir = widgets.Button(description='...')
    button_select_save_dir.on_click(select_save_dir_event)
    save_box = widgets.HBox([widgets.Label('Папка сохранения'), text_save_dir, button_select_save_dir])
    display(save_box)

    button_start = widgets.Button(description='Перед началом обработки установите папку сохранения', layout=widgets.Layout(width='80%', height='50px'), disabled=True)
    display(button_start)

    def start_process(b):
        b.disabled=True
        
        clear_output()
        display(grid)
        display(check_index_from_1)
        display(check_add_headers)
        display(save_box)
        display(button_start)
        
        delta_max = delta_upper.value
        delta_min = delta_lower.value
        mean = mean_val.value
        index_from_1 = check_index_from_1.value
        add_headers = check_add_headers.value
        save_dir = text_save_dir.value
        
        min_val = mean - delta_min
        max_val = mean + delta_max
        
        stat = process_selected_files(files, save_dir, 
                                      min_val, max_val,
                                      index_from_1, add_headers)
        display(stat)
        b.disabled = False

    button_start.on_click(start_process)

# Статистические методы
def fisher_test(data1, data2):
    import scipy.stats as stats
    oddsratio, pvalue = stats.fisher_exact([data1, data2])
    return {
        'Fisher stat': oddsratio,
        'Fisher p-value': pvalue
    }

def mann_whitney_test(data1, data2):
    import scipy.stats as stats
    statistic, pvalue = stats.mannwhitneyu(data1, data2)
    return {
        'Mann-Whitney stat': statistic,
        'Mann-Whitney pvalue': pvalue
    }

def chi_square_test(data1, data2):
    from scipy.stats import chi2_contingency
    try:
        chi2, pvalue, _, _ =chi2_contingency([data1, data2])
        flag = 'OK' if len(data1) >=5 and len(data2) >= 5 else "Some less than 5"
    except:
        chi2 = None
        pvalue = None
        flag = 'Error'
    finally:
        return {
            'ChiSquare stat': chi2,
            'ChiSquare pvalue': pvalue,
            'ChiSquare flag': flag
        }
    
def mean_and_std_error(data):
    return{
        'mean': np.mean(data) if len(data) else None,
        'std error': np.std(data)/np.sqrt(len(data)) if len(data) else None
    }

def agg_stats(df, min_val, max_val):
    df_greater = df[df['Y'] >= max_val]
    df_lower = df[df['Y'] <= min_val]
    
    
    initial_len = len(df) + 1
    first_part_mask = df['X'] < initial_len//2 
    
    data = \
        [
            len(df_greater.loc[first_part_mask]), len(df_greater.loc[~first_part_mask])
        ],\
        [
            len(df_lower.loc[first_part_mask]), len(df_lower.loc[~first_part_mask])
        ]
    
    mann_whitney = mann_whitney_test(df_greater['amplitude_abs'], df_lower['amplitude_abs'])
    chi_square = chi_square_test(*data)
    fisher = fisher_test(*data)
    mean_and_std_error_above = mean_and_std_error(df_greater['amplitude_abs'])
    mean_and_std_error_under = mean_and_std_error(df_lower['amplitude_abs'])
    res = {
        **mann_whitney,
        **chi_square,
        **fisher
    }
    res['Above: mean'] = mean_and_std_error_above['mean']
    res['Above: std error'] = mean_and_std_error_above['std error']
    res['Under: mean'] = mean_and_std_error_under['mean']
    res['Under: std error'] = mean_and_std_error_under['std error']
    return res
    
# Базовая работа с файлами
def gather_files(files):
    from glob import glob
    found = []
    for file in files:
        found.extend(glob(file))
    return found

def find_start_index(save_dir, app_folder_name):
    save_dir_files = [name for name in os.listdir(save_dir) if os.path.isdir(os.path.join(save_dir, name))]
    pattern = '^' + app_folder_name + r'-[0-9]+'
    start_ind = 1
    for file in save_dir_files:
        found = re.findall(pattern, file)
        if len(found):
            start_ind = max(start_ind + 1, int(file.split('-')[-1]))
    return start_ind
        
def index_files(files, start_index):
    folders = list(set(os.path.split(file)[0] for file in files))

    indexed_files = []
    for ind, folder in enumerate(folders, start=start_index):
        for file in files:
            if file.startswith(folder):
                indexed_files.append((ind, file))

    return indexed_files

do_itermidiate_print = False

# Обработка файлов
def process_selected_files(files, save_files_dir, 
                           min_val, max_val, 
                           index_from_1=False, append_headers=True, ext='.txt',
                           app_folder_name="PeaksDetector"):
    from pathlib import Path
    from datetime import datetime
    gathered = gather_files(files)
    start_ind = find_start_index(save_files_dir, app_folder_name)
    files_indexed = index_files(gathered, start_ind)
    
    date_time_start = datetime.now().strftime("%d.%m.%Y, %H.%M.%S")
    
    stats = []
    from datetime import datetime
    start = datetime.now()
    for num, (ind, file) in enumerate(files_indexed):
        if do_itermidiate_print:
            print(num, file, ' .... ', end='')
        save_dir_indexed = os.path.join(save_files_dir, app_folder_name + '-' + str(ind))
        
        if not os.path.exists(save_dir_indexed):
            Path(save_dir_indexed).mkdir(parents=True, exist_ok=True)
            with open(os.path.join(save_dir_indexed, 'README.txt'), 'w') as f:
                f.write("В этой папке сохранены результаты обработки файлов из папки:\n")
                f.write(os.path.split(file)[0]+'\n')
                f.write('Время начала обработки данных:\n')
                f.write(date_time_start)
        
#         Load data
        try:
            try:
                df = pd.read_csv(file, header=None)
            except Exception as e:
                if not do_itermidiate_print:
                    print(num, file, ' .... ', end='')
                print('fail:', e)
                continue

            df.columns = ['Y']
            df.index.name = 'X'
            df.reset_index(inplace=True)

    #         Compute characteristics
            df['shifted'] = df['Y'].shift(1)
            df = df.iloc[1:].copy()
            df['amplitude'] = df['Y'] - df['shifted']
            df['amplitude_abs'] = df['amplitude'].abs()

    #         Select only outliers
            try:
                st = agg_stats(df, min_val, max_val)
                df = df[(df['Y'] >= max_val)|(df['Y']<=min_val)]
            except Exception as e:
                if not do_itermidiate_print:
                    print(num, file, ' .... ', end='')
                print('fail:', e)
                raise e
        
            
        
    #         display(df)
    #         Save data
            base_save_name = os.path.basename(file)
            base_save_name = os.path.splitext(base_save_name)[0]

            if index_from_1:
                df['X'] = df['X'] + 1
            try:
                df.to_csv(os.path.join(save_dir_indexed, base_save_name + ext), 
                          na_rep='NAN', 
                          sep='\t', 
                          index=False, 
                          header=append_headers)

                st = {**{'FileName': file}, **st}
                stats.append(st)
            except Exception as e:
                if not do_itermidiate_print:
                    print(num, file, ' .... ', end='')
                print('fail:', e)
                continue
            if do_itermidiate_print:
                print('OK')
        except Exception as e:
            if not do_itermidiate_print:
                print(num, file, ' .... ', end='')
            print('fail:', e)
    
    df_stats = pd.DataFrame(stats)
    df_stats.to_csv(os.path.join(save_files_dir, 'stats_' + date_time_start + ext), 
                  na_rep='NAN', 
                  sep='\t', 
                  index=False, 
                  header=append_headers)
    print('elapsed time =', datetime.now()-start)
    return df_stats

