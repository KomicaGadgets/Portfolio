class TFTP(object):
    def __init__(self):
        self.i = 1

    def SetCaseInfo(self, index, case_id):
        self.index = index
        self.case_id = case_id

    def Response(self, bool_return=True, reason=None, file=None):
        BasicResponse = {
            'index': self.index,
            'case': self.case_id,
            'return': bool_return
        }

        if reason != None:
            BasicResponse.update({
                'reason': str(reason)
            })

        if file != None:
            report_b64 = ''

            with open(file, 'rb') as f:
                report_b64 = base64.b64encode(f.read()).decode('utf8')

            BasicResponse.update({
                'file': report_b64
            })

        return BasicResponse

    def Success(self, reason=None, file=None):
        return self.Response(True, reason=reason, file=file)

    def Error(self, reason=None, file=None):
        return self.Response(False, reason=reason, file=file)

    @skip_check
    def start_tftp(self, index, case_id, data={}):
        global tftp_temp_directory, tftpserver_logfile, tftpserver_logger

        self.SetCaseInfo(index, case_id)

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
            filename = data['http'].split(
                '/')[-1] if len(data['filename']) == 0 else data['filename']
            URLRetrieveFile = tftp_temp_directory + "/" + filename
            URLRetrieveParams = replace_sign_url(
                data['file_signed']) if "file_signed" in data else data['http']

            try:
                urllib.urlretrieve(URLRetrieveParams, filename=URLRetrieveFile)
            except Exception as e:
                shutil.rmtree(tftp_temp_directory, ignore_errors=True)
                return self.Error(reason='SendTraffic-005: Return exception message: {}'.format(e))
        thd = threading.Thread(target=self.tftp_server)
        thd.start()
        tftpserver_logger.info("{} ready for download".format(filename))

        return self.Success()

    @skip_check
    def is_new_file_added_in_tftp_server(self, index, case_id, data={}):
        self.SetCaseInfo(index, case_id)

        if os.path.isfile(tftp_temp_directory+"/"+data['file']):
            lastModified_time = time.ctime(os.path.getmtime(
                tftp_temp_directory+"/"+data['file']))
            created_time = time.ctime(os.path.getctime(
                tftp_temp_directory+"/"+data['file']))
            file_size = os.path.getsize(tftp_temp_directory+"/"+data['file'])

            return self.Success(
                'File size: {} bytes, Created : {}, Last Modified : {}'.format(
                    file_size, created_time, lastModified_time),
                tftp_temp_directory+"/"+data['file']
            )
        else:
            return self.Error('file is not added')

    @skip_check
    def stop_tftp(self, index, case_id, data={}):
        global tftpserver, tftpserver_logfile, tftpserver_logger

        self.SetCaseInfo(index, case_id)

        if tftpserver != None:
            tftpserver.stop(now=True)
            shutil.rmtree(tftp_temp_directory)
            tftpserver_logger.info("TFTP server stop")

            return self.Success(
                'Tftp server has stopped, temporary directory: {} has also removed'.format(
                    tftp_temp_directory),
                tftpserver_logfile
            )
        else:
            pass
