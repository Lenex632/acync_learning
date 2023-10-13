import threading


def task(function, *args, **kwargs):
    print(f'{"started_task":-^70}')
    print(f'{threading.current_thread().name=}, {threading.active_count()=}')
    function(*args, **kwargs)
    print(f'{"end_task":-^70}')


if __name__ == '__main__':
    # threading.Thread(target=print, args=('Simple', 'but useless'), kwargs={'sep': '\n'}).start()

    # print(threading.current_thread().name)

    task(print, 'Hellow World')

    threading.Thread(target=task, args=(print, 'Bay World')).start()

    thr_3 = threading.Thread(target=task, args=(print, 'Bay World'))
    thr_3.name = 'THR_3'
    thr_3.start()

