import cpuinfo
import GPUtil

def cpuname():
    return cpuinfo.get_cpu_info()['brand_raw']

def gpuname():
    """Returns the model name of the first available GPU"""
    gpus = GPUtil.getGPUs()
    if len(gpus) == 0:
        print("No GPUs detected in the system")
    return gpus[0].name
