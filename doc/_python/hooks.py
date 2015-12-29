def process_info(info, site):
    if 'layout' not in info:
        if info['components'][-1] == 'index':
            info['layout'] = 'index'
        else:
            info['layout'] = 'page'
