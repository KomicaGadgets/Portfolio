class TFTP(object):
    def __init__(self):
        self.i = 1

    @skip_check
    def start_tftp(self, index, case_id, data={}):
        global tftp_temp_directory
        global tftpserver_logfile
        global tftpserver_logger

        tftpserver_logfile = tempfile.gettempdir()+"/tftp_server.log"
        if os.path.exists(tftpserver_logfile):
            os.remove(tftpserver_logfile)

        tftpserver_logger = None
        tftpserver_logger = logging.getLogger("tftpy.TftpServer")
        tftpserver_logger.setLevel(logging.INFO)
        format = "[%(asctime)s][%(levelname)s] %(message)s"
        formatter = logging.Formatter(format)
        filehandler = logging.FileHandler(tftpserver_logfile)
        filehandler.setFormatter(formatter)
        tftpserver_logger.addHandler(filehandler)
        tftpserver_logger.info("TFTP server ready")
        filename = ''

        tftp_temp_directory = tempfile.mkdtemp()
        if len(data['http']) != 0:
            if len(data['filename']) == 0:
                filename = data['http'].split('/')[-1]
            else:
                filename = data['filename']
            try:
                if "file_signed" in data:
                    urllib.urlretrieve(replace_sign_url(
                        data['file_signed']), filename=tftp_temp_directory + "/" + filename)
                else:
                    urllib.urlretrieve(
                        data['http'], filename=tftp_temp_directory + "/" + filename)
            except Exception as e:
                shutil.rmtree(tftp_temp_directory, ignore_errors=True)
                return {'index': index, 'case': case_id, 'return': False, 'reason': "SendTraffic-005: Return exception message: "+str(e)}
        thd = threading.Thread(target=self.tftp_server)
        thd.start()
        tftpserver_logger.info("%s ready for download" % filename)

        return {'index': index, 'case': case_id, 'return': True}

    @skip_check
    def is_new_file_added_in_tftp_server(self, index, case_id, data={}):
        report_b64 = ''
        if os.path.isfile(tftp_temp_directory+"/"+data['file']):
            lastModified_time = time.ctime(os.path.getmtime(
                tftp_temp_directory+"/"+data['file']))
            created_time = time.ctime(os.path.getctime(
                tftp_temp_directory+"/"+data['file']))
            file_size = os.path.getsize(tftp_temp_directory+"/"+data['file'])
            with open(tftp_temp_directory+"/"+data['file'], "rb") as fd:
                report_b64 = base64.b64encode(fd.read())

            return {'index': index, 'case': case_id, 'return': True, 'reason': 'File size: '+str(file_size)+' bytes, Created : '+str(created_time)+', Last Modified : '+str(lastModified_time), 'file': report_b64}
        else:
            return {'index': index, 'case': case_id, 'return': False, 'reason': 'file is not added'}

    @skip_check
    def stop_tftp(self, index, case_id, data={}):
        global tftpserver
        global tftpserver_logfile
        global tftpserver_logger

        logfile_b64 = ''
        if tftpserver != None:
            tftpserver.stop(now=True)
            shutil.rmtree(tftp_temp_directory)
            with open(tftpserver_logfile, "r") as fd:
                logfile_b64 = base64.b64encode(fd.read())
            tftpserver_logger.info("TFTP server stop")

            return {'index': index, 'case': case_id, 'return': True, 'reason': 'Tftp server has stopped, temporary directory: '+str(tftp_temp_directory)+' has also removed', 'file': logfile_b64}
        else:
            pass
