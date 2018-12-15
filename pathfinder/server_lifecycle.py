
# import pathfinder_datastreamer
# from main import set_sound_stream
# 
# sound_stream = None

def on_server_loaded(server_context):
    ''' If present, this function is called when the server first starts. '''
    print('Server lifecycle: on_server_loaded...')
#     global sound_stream
#     sound_stream = pathfinder_datastreamer.PathfinderDataStreamer()
#     sound_stream.start_streaming()
#     print('--- STREAMING STARTED ---')
#     set_sound_stream(sound_stream)


def on_server_unloaded(server_context):
    ''' If present, this function is called when the server shuts down. '''
    print('Server lifecycle: on_server_unloaded...')

def on_session_created(session_context):
    ''' If present, this function is called when a session is created. '''
    print('Server lifecycle: on_session_created...')
#     set_sound_stream(sound_stream)

def on_session_destroyed(session_context):
    ''' If present, this function is called when a session is closed. '''
    print('Server lifecycle: on_session_destroyed...')
