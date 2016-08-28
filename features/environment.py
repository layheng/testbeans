import logging
LOG_FILENAME = 'testbeans.log'
logger = logging.getLogger(LOG_FILENAME)
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename=LOG_FILENAME,
                    filemode='w',
                    format='%(asctime)s: %(levelname)-8s: %(filename)-18s: %(message)s')


def before_all(context):
    # print("Executing before all")
    context.logger = logger


def before_feature(context, feature):
    # print("Before feature\n")
    pass

# Scenario level objects are popped off context when scenario exits
def before_scenario(context,scenario):
    # context.browser = webdriver.Chrome()
    # print("Before scenario\n")
    pass

def after_scenario(context,scenario):
    # context.browser.quit()
    # print("After scenario\n")
    pass

def after_feature(context,feature):
    print("")
    pass

def after_all(context):
    # print("Executing after all")
    pass

