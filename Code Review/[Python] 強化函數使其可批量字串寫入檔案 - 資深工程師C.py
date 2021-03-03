def Insert_string_to_file(self, string):
    global report_dir, filename
    os.system("echo '" + string + "' >> " +
              report_dir + "/" + filename + ".tcl")


Insert_string_to_file('puts \"==== Stop to Send Packets ====\"')
Insert_string_to_file(
    'stc::perform CaptureStop -captureProxyId $captureRx')
Insert_string_to_file('stc::perform CaptureDataSave -captureProxyId $captureRx -FileName \"Rx_result_' +
                      filename + '.pcap\" -FileNamePath \"' + report_dir + '\"')
Insert_string_to_file('stc::perform SaveResult -DatabaseConnectionString \"' +
                      report_dir + '/Result_db_' + filename + '.db\"')
Insert_string_to_file('stc::perform ExportDbResultsCommand -TemplateUri \"/acts/modules/Spirent_TestCenter/results_reporter/templates/CustomDetailStats.rtp\" -ResultFileName \"Result_' +
                      filename + '.csv\" -Format \"CSV\" -ResultDbFile \"' + report_dir + '/Result_db_' + filename + '.db\"')
Insert_string_to_file('stc::perform analyzerStop -analyzerList $analyzer')
