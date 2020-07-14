import uuid
import os

def changeHTML(input):
    '''
    html转义字符问题
    :param input: 弃用
    :return:
    '''
    return input.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quto;','"').replace('&#39;','\'')




def starToNo(lis):
    '''
    去星星
    :return:
    '''
    return lis.replace('*','')


def objectStarToNo(dbDSMObject):
    '''
    对象中c.DNA和Pratein去星星
    :param dbDSMObject:
    :return:
    '''
    dbDSMObject.Protein = starToNo(dbDSMObject.Protein)
    dbDSMObject.cDNA = starToNo(dbDSMObject.cDNA)
    return  dbDSMObject







def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename










