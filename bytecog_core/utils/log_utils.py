def write_log_message(message, filename):
    log_file = open(filename, 'a')
    log_file.write(message + '\n')
    log_file.close()