import math
import multiprocessing


## 多进程处理数据
def multipool_deal(func, data, cores = 5, slice_size =10000):
    data_length = len(data)
    slice = math.floor(data_length/slice_size)
    param = []
    for i in range(slice+1):
        param.append((i*slice_size, min(data_length,(i+1) * slice_size),data))
    pool = multiprocessing.Pool(processes=cores)
    pool_list = []
    for para in param:
        pool_list.append(pool.apply_async(func, (data, para[0],para[1])))  # 这里不能 get， 会阻塞进程
    result_list = [xx.get() for xx in pool_list]
    pool.close()
    pool.join()
    res =[]
    for i in range(len(result_list)):
        if i == 0 :
            res = result_list[i]
        else:
            res.extend(result_list[i])
    return res



## 多进程处理数据返回多个进程的结果的列表
def multipool_deal_list(func, data, cores = 5, slice_size =10000):
    data_length = len(data)
    slice = math.floor(data_length/slice_size)
    param = []
    for i in range(slice+1):
        param.append((i*slice_size, min(data_length,(i+1) * slice_size),data))
    pool = multiprocessing.Pool(processes=cores)
    pool_list = []
    for para in param:
        pool_list.append(pool.apply_async(func, (data, para[0],para[1])))  # 这里不能 get， 会阻塞进程
    result_list = [xx.get() for xx in pool_list]
    pool.close()
    pool.join()
    dic_list =[]
    for i in range(len(result_list)):
        if i == 0 :
            dic_list = [result_list[i]]
        else:
            dic_list.append(result_list[i])
    return dic_list


## 多进程处理数据返回字典列表,数据自行分片好了
def multipool_deal_partition_list(func, data_list, cores = 5,slice_size =None):

    param = data_list

    pool = multiprocessing.Pool(processes=cores)
    pool_list = []
    for para in param:
        pool_list.append(pool.apply_async(func, (para,)))  # 这里不能 get， 会阻塞进程
    result_list = [xx.get() for xx in pool_list]
    pool.close()
    pool.join()
    res =[]
    for i in range(len(result_list)):
        if i == 0 :
            res = result_list[i]
        else:
            res.extend(result_list[i])
    return res


## 多进程处理数据并返回所有数据集合
def multipool_deal_partition(func, datas, cores = 5, slice_size =None,args=None):
    data_length = len(datas)
    slice = math.floor(data_length / slice_size)
    param = []
    for i in range(slice + 1):
        param.append(datas[i * slice_size: min(data_length, (i + 1) * slice_size)])

    pool = multiprocessing.Pool(processes=cores)
    pool_list = []
    for para in param:
        pool_list.append(pool.apply_async(func, (para,args)))  # 这里不能 get， 会阻塞进程
    result_list = [xx.get() for xx in pool_list]
    pool.close()
    pool.join()
    res =[]
    for i in range(len(result_list)):
            res.append(result_list[i])
    return res

## 多进程处理数据并返回所有数据集合
def multipool_deal_partition_flatten(func, datas, cores = 5, slice_size =None,args=None):
    data_length = len(datas)
    slice = math.floor(data_length / slice_size)
    param = []
    for i in range(slice + 1):
        param.append(datas[i * slice_size: min(data_length, (i + 1) * slice_size)])

    pool = multiprocessing.Pool(processes=cores)
    pool_list = []
    for para in param:
        pool_list.append(pool.apply_async(func, (para,args)))  # 这里不能 get， 会阻塞进程
    result_list = [xx.get() for xx in pool_list]
    pool.close()
    pool.join()
    res =[]
    for i in range(len(result_list)):
        if i == 0 :
            res = result_list[i]
        else:
            res.extend(result_list[i])
    return res