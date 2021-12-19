from modules import DevOps

# Deploys Handler functions
DevOps.deployHandlers()



### If this file needs to handle additional Deployment types/configs, use the below commented code to pass command line arguments

# import sys, getopt

# errorMessage = 'Please enter a value for target. Ex: "Deploy.py --target=handlers"'

# if len(sys.argv) == 1:
#     sys.exit(errorMessage)

# opts = getopt.getopt(
#     args = sys.argv[1:], 
#     shortopts="",
#     longopts= ["target="]
#     )[0]

# target = ""
# for o,a in opts:
#     if "target" in o:
#         target = a

# if target == "":
#     sys.exit(errorMessage)
# else:
#     if "handlers" in target:
#         DevOps.deployHandlers()
#     else:
#         sys.exit("Invalid target")