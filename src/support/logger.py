# =========================================================================
# 
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
# 
# Logging
# 
# =========================================================================
def get_logger():

    import logging

    log = logging.getLogger("app.py")
    log.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_handler.setFormatter(logging.Formatter('%(levelname)s:     %(asctime)s - %(message)s'))
    log.addHandler(c_handler) 
    
    return log