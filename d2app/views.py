from django.shortcuts import render
from django.http import HttpResponseRedirect
from d2app import pkg_db
from d2app import model_unpacker
import os
import numpy as np

# Create your views here.

"""
Helper functions
"""


def get_buttons_html():
    model_files = []

    folder = 'city_tower_d2_0369'

    pkg_db.start_db_connection('2_9_0_1')
    entries_refid = {x: y for x, y in pkg_db.get_entries_from_table(folder, 'FileName, RefID') if y == '0x11A7'}
    entries_refpkg = {x: y for x, y in pkg_db.get_entries_from_table(folder, 'FileName, RefPKG') if y == '0x0003'}

    for file in entries_refid:
        if file in entries_refpkg.keys():
            model_files.append(file)

    new_html = ''
    for i in range(5):
        model_data_file = model_unpacker.get_model_data_file(model_files[i])
        if model_data_file.split('-')[0] != folder.split('_')[-1]:
            continue
        new_html += f'<div><button class="model-button" type="submit" onclick="unpackModel()" name="{model_files[i]}">{model_data_file}</button></div>\n'

    return new_html


"""
Webpage-related views
"""


def index(request):
    """The default webpage of the website"""
    buttons_html = get_buttons_html()
    template_data = {
        'buttons_html': buttons_html,
    }
    return render(request, 'd2app/index.html', context=template_data)


def submit(request):
    """Functioned invoked by the user when they submit which song they prefer.
    Uses the assigned name of the button to determine which song they chose, and
    returns the ids of both songs involved"""
    try:
        info = request.POST
        # Extracts the song IDs from the "name" values of the button that was pressed
        model_file_name = list(info.items())[-1][0]
        model_file_hash = model_unpacker.get_hash_from_file(model_file_name).upper()
        print(f'Info: {model_file_name} {model_file_hash}')
        model_unpacker.get_model(model_unpacker.get_flipped_hex(model_file_hash, 8))
        # Model has been sent to d2app/unpacked_objects/model.obj
        os.system('obj2gltf -i static/d2app/models/model.obj -o static/d2app/models/model.glb')


    except Exception as e:
        print(e)

    return HttpResponseRedirect(f'/?ignore={np.random.randint(1, 99999)}')
