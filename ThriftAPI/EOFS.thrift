/*******************************************************************************************
EOFS.thrift
    Copyright (c) Eisoo Software, Inc.(2012 - 2013), All rights reserved

Purpose:
    EOFS (Eisoo/Enhanced Object File System) 是一个以高性能、高扩展性、高可靠性为目标的分布式对象文件系统.
    EOFS 是构建在一个高可靠和高可扩展的智能分布式对象存储系统 ESwift 之上，架设一个以对象为存储粒度，
    以 GNS（Global Namespace） 为命名路径，采用树状结构索引，可支持全局范围内对象按类别和时间点进行存储，
    并且内置重复数据删除、数据生命周期管理等一系列技术特点的分布式元数据管理层，来对外提供对象文件系统的访问服务，
    以应对各个产品应用的大数据存储需求及多种工作负载的高性能需求（每秒输入/输出操作[IOPS]和带宽）。
    
    此接口为 EOFS 管理服务内部接口.
    对内包含响应ESwift事件、响应更新memcached节点列表等.

Author:
    Liu Lang (liu.lang@eisoo.com)

Creating Time:
    2012-05-29
*******************************************************************************************/

include "EThriftException.thrift"

/**
 * 端口号
 */
const i32 NCT_EOFS_PORT = 9061

/**
 * EOFS 容量信息，单位为字节
 */
struct ncTEOFSUsedSize {
    1: required i64 allocSize,                        // EOFS数据在ESwift中所占用的空间大小
}

// 错误码
const string NCT_EOFS_ERR_PROVIDER_NAME = "eofstimpl"
enum ncTEOFSError {
    NCT_UNKNOWN_EXCEPTION = 10001,                    // 未知异常
    NCT_FAILED_TO_GET_EOFS_MGR = 10002,               // 获取ncIEOFSManager对象失败
    NCT_FAILED_TO_GET_EOFS_CACHE_MGR = 10003,         // 获取ncIEOFSCacheManager对象失败
}

/**
 * EOFS 管理服务接口
 */
service ncTEOFS {
    /////////////////////////////////////////////////////////////////////////////////////////////
    //
    // !!!以下接口为 DataEngine 内部调用!!!
    //
    
    //
    // EOFS 管理
    //

    /**
     * 响应ESwift就绪事件，若EOFS尚未初始化则初始化EOFS
     *
     * @throw 转抛内部调用异常。
     */
    void Mgr_OnESwiftPrepared () throws (1: EThriftException.ncTException exp),
    
    /**
     * 响应添加新的memcached服务器地址
     *
     * @param serversList： string为IP地址，错误格式不解析 
     */
    void Mgr_OnMemcachedServersJoin (1: list<string> serversList),
    
    /**
     * 响应设置memcached服务器地址列表
     * 调用此接口后，原来设置的列表会被清空
     *
     * @param serversList： string为IP地址，错误格式不解析 
     */
    void Mgr_OnL1CacheSetServers (1: list<string> serversList),
    
    /**
     * 返回设置的memcached服务器地址列表
     *
     * @return： string为IP地址
     */
    list<string> Mgr_GetL1CacheServers (),
    
    /**
     * 返回一级缓存服务器统计信息
     * 该接口返回各个添加进去的server的各个统计信息，包括：
     * 
     * bytes ------------------------------- 系统存储缓存对象所使用的存储空间，单位为字节
     * bytes_read -------------------------- 从memcached服务器查询的总的字节数
     * bytes_written ----------------------- 向memcached服务器写入的总的字节数
     * cmd_get ----------------------------- 累积获取数据的命令数量
     * cmd_set ----------------------------- 累积保存数据的命令数量
     * connection_structures --------------- 从memcached服务启动到当前时间，被服务器分配的连接结构的数量
     * curr_connections -------------------- 当前系统打开的连接数
     * curr_items -------------------------- 当前缓存中存放的所有缓存对象的数量，不包括目前已经从缓存中删除的对象
     * evictions --------------------------- 为了给新的数据项目释放空间，从缓存移除的缓存对象的数目
     * get_hits ---------------------------- 获取数据成功的次数
     * get_misses -------------------------- 获取数据失败的次数
     * limit_maxbytes ---------------------- memcached服务缓存允许使用的最大字节数
     * pid --------------------------------- memcached服务进程的进程ID
     * pointer_size ------------------------ 服务器所在主机操作系统的指针大小，一般为32或64
     * rusage_system ----------------------- 进程的累计系统时间
     * rusage_user ------------------------- 进程的累计用户时间
     * threads ----------------------------- 被请求的工作线程的总数量
     * time -------------------------------- memcached服务器所在主机当前系统的时间，单位为秒
     * total_connections ------------------- 从memcached服务启动到当前时间，系统打开过的连接的总数
     * total_items ------------------------- 从memcached服务启动到当前时间，系统存储过的所有对象的数量，包括目前已经从缓存中删除的对象
     * uptime ------------------------------ memcached服务从启动到当前所经过的时间，单位为秒
     * version ----------------------------- memcached组件的版本
     *
     * @return： 返回一级缓存所有节点的状态信息：<serverIp:port, <key, value> >
     */
    map<string, map<string, string> > Mgr_GetL1CacheStats (),
    
    /**
     * 返回当前节点二级缓存统计信息
     * 该接口返回二级缓存的状态统计信息，包括：
     * 
     * get_hits ---------------------- 获取数据成功的次数
     * get_misses -------------------- 获取数据失败的次数
     * set_hits ---------------------- 设置数据成功的次数
     * set_misses -------------------- 设置数据失败的次数
     * exist_hits -------------------- 检查数据成功的次数
     * exist_misses ------------------ 检查数据失败的次数
     * bytes_read -------------------- 已读取的字节数
     * bytes_written ----------------- 已写入的字节数
     * bytes ------------------------- 总共使用情况（字节数）
     * capacity ---------------------- 设置的空间大小（字节数）
     * path -------------------------- 设置的存储路径（不存在则为空）
     * is_running -------------------- 当前是否正在运行（yes, no）
     * 
     * @return： 返回当前节点二级缓存状态信息：<key, value>
     */
    map<string, string> Mgr_GetL2CacheStats (),
    
    /**
     * 修改二级缓存空间
     *
     * @param   capacity 总容量大小，以MB为单位
     */
    void Mgr_SetL2CacheCapacity (1: i64 capacity) throws (1: EThriftException.ncTException exp),
}
