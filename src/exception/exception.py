import sys 
from src.logger.logger import logging

def error_message_details(error,error_detail:sys):
    _,_,ex_tb = error_detail.exc_info()
    filename = ex_tb.tb_frame.f_code.co_filename
    line_number = ex_tb.tb_lineno
    error_message = "Error occurred in python script name [{0}] line number [{1}] and error message [{2}]".format(filename,line_number,str(error))
    return error_message

class MCP_AGENT_Exception(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message,error_detail)
        
    def __str__(self):
        return self.error_message



if __name__ == "__main__":
    try:
        1/0
    except Exception as e:
        logging.info("Error Occured during division")
        raise MCP_AGENT_Exception(e,sys)
        
        

        