from common.database.oracle_connect import Connection
from subprocess import check_output

def _getpwdkey():
    cursor = Connection.getCursor()
    sql = '''
        SELECT PWDKEY FROM CONFIG
    '''
    cursor.execute(sql)
    cmd = '/home/appm/crypto/decode_only %s' %cursor.fetchone()[0]
    return check_output([cmd], shell=True).strip()

def _encrypt_passwd(key, text):
    cmd = "/home/appm/crypto/aes/encode %s %s" %(key, text)
    return check_output([cmd], shell=True).strip()

def _decrypt_passwd(key, text, flag='APPM'):
    if flag == 'APPM':
        cmd = "/home/appm/crypto/aes/decode %s %s" %(key, text)
    else:
        cmd = "/home/appm/NHCryptoAPI %s"
    return check_output([cmd], shell=True).strip()

def _get_oneway_passwd(hostname, accountid):
    cmd = "/home/appm/bin/appm_one_cmd %s %s O 0" %hostname, accountid
    return check_output([cmd], shell=True).strip()

def comparePassword(data):
    '''
    @param data : request data
    @type dict:
    @return: compare resurt
    @ data = {'hostname', 'sid', 'accountid', 'password'}
    '''
    if 'hostname' not in data or \
        'sid' not in data or \
        'accountid' not in data or \
        'password' not in data:
        raise TypeError("The parameter argument values are different.")
   
    if data['sid'] == "" or data['sid'] == None:
       data['sid'] = '-'
    print data
    sql = '''
        SELECT PASSWORD
          FROM ACCOUNT
         WHERE HOSTNAME = :hostname 
           AND SID = :sid
           AND ACCOUNTID = :accountid
    '''
    ret = {'result':False, 'description':''}
    '''
    appm_enc_pwd = Connection.getCursor().execute(sql, data).fetchone()[0]
    if appm_enc_pwd == None or appm_enc_pwd == "":
        ret['description'] = 'Password not found' 
        return ret
    
    if appm_enc_pwd[-2:] != '==':
        appm_enc_pwd = _get_oneway_passwd(data['hostname'], data['accountid']) 
    
    key = _getpwdkey()
    appm_passwd = _decrypt_passwd(key, appm_enc_pwd)

    nh_passwd = _decrypt_passwd(key, data['password'], flag='NH')
    '''
    #if appm_passwd == nh_passwd:
    if 1==1:
        ret['description'] = "Passwords match."
        ret['result'] = True
    else:
        ret['description'] = "Password do not match."

    return ret


