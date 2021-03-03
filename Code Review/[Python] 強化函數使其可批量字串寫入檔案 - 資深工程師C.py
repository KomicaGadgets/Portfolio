def Insert_string_to_file(self, str_list=[]):
    global report_dir, filename

    if isinstance(str_list, str):
        str_list = [str_list]

    for string in str_list:
        os.system("echo '" + string + "' >> " +
                  report_dir + "/" + filename + ".tcl")


Insert_string_to_file([
    'puts \"==== Stop to Send Packets ====\"',
    'stc::perform CaptureStop -captureProxyId $captureRx',

    'stc::perform CaptureDataSave -captureProxyId $captureRx -FileName \"Rx_result_' +
    filename + '.pcap\" -FileNamePath \"' + report_dir + '\"',

    'stc::perform SaveResult -DatabaseConnectionString \"' +
    report_dir + '/Result_db_' + filename + '.db\"',

    'stc::perform ExportDbResultsCommand -TemplateUri \"/acts/modules/Spirent_TestCenter/results_reporter/templates/CustomDetailStats.rtp\" -ResultFileName \"Result_' +
    filename + '.csv\" -Format \"CSV\" -ResultDbFile \"' +
    report_dir + '/Result_db_' + filename + '.db\"',

    'stc::perform analyzerStop -analyzerList $analyzer'
])
